import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
# We enable refine_landmarks for more accurate iris detection
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,  # We are only interested in one main user
    refine_landmarks=True, # Crucial for getting iris landmarks
    min_detection_confidence=0.7, # Increased confidence for robust detection
    min_tracking_confidence=0.7   # Increased confidence for robust tracking
)

# Initialize MediaPipe Drawing utilities for visualization
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# --- Landmark Indices for Gaze Detection (MediaPipe Face Mesh) ---
# These are fixed indices provided by MediaPipe
# Left eye (when looking at the screen, it's the user's left eye)
LEFT_EYE_INDICES = [
    362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398
]
LEFT_IRIS_INDICES = [474, 475, 476, 477] # Center and 4 points around the iris

# Right eye (when looking at the screen, it's the user's right eye)
RIGHT_EYE_INDICES = [
    33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246
]
RIGHT_IRIS_INDICES = [469, 470, 471, 472] # Center and 4 points around the iris


def get_eye_landmarks(face_landmarks, image_shape, eye_indices, iris_indices):
    """
    Extracts eye and iris landmark coordinates from MediaPipe results.
    Returns pixel coordinates.
    """
    img_h, img_w, _ = image_shape
    eye_points = []
    iris_points = []

    for idx in eye_indices:
        pt = face_landmarks.landmark[idx]
        x, y = int(pt.x * img_w), int(pt.y * img_h)
        eye_points.append((x, y))

    for idx in iris_indices:
        pt = face_landmarks.landmark[idx]
        x, y = int(pt.x * img_w), int(pt.y * img_h)
        iris_points.append((x, y))
    
    return eye_points, iris_points

def calculate_gaze_direction(eye_points, iris_points, eye_side="left"):
    """
    Estimates gaze direction (horizontal and vertical) based on iris position
    relative to the eye.
    """
    if not eye_points or not iris_points:
        return "N/A", "N/A"

    # Calculate the bounding box of the eye
    eye_x_min = min([p[0] for p in eye_points])
    eye_x_max = max([p[0] for p in eye_points])
    eye_y_min = min([p[1] for p in eye_points])
    eye_y_max = max([p[1] for p in eye_points])

    eye_center_x = (eye_x_min + eye_x_max) / 2
    eye_center_y = (eye_y_min + eye_y_max) / 2
    eye_width = eye_x_max - eye_x_min
    eye_height = eye_y_max - eye_y_min

    # Calculate the center of the iris by averaging its points
    iris_center_x = sum([p[0] for p in iris_points]) / len(iris_points)
    iris_center_y = sum([p[1] for p in iris_points]) / len(iris_points)

    # --- Horizontal Gaze Estimation ---
    # Normalize iris position relative to eye width
    # A value of 0 means perfectly centered. Negative means left, positive means right.
    # We might need to flip the sign for left eye vs right eye for consistent "left" / "right"
    # This deviation is relative to the eye's center.
    horizontal_deviation = (iris_center_x - eye_center_x) / eye_width

    # Adjust for perspective if user moves head slightly.
    # For a general "left/right" gaze relative to the screen,
    # we need to consider which eye we are processing.
    # When looking at the screen, if the *user's* left iris is to the right of their eye center,
    # they are looking right (from their perspective).
    if eye_side == "left": # This is the user's left eye (right side of the image)
        # If horizontal_deviation is positive, iris is to the right (user looking right)
        gaze_h = "Right" if horizontal_deviation > 0.07 else ("Left" if horizontal_deviation < -0.07 else "Center")
    else: # This is the user's right eye (left side of the image)
        # If horizontal_deviation is negative, iris is to the left (user looking left)
        gaze_h = "Left" if horizontal_deviation < -0.07 else ("Right" if horizontal_deviation > 0.07 else "Center")
    
    # --- Vertical Gaze Estimation ---
    # Normalize iris position relative to eye height
    # Negative means up, positive means down
    vertical_deviation = (iris_center_y - eye_center_y) / eye_height

    gaze_v = "Down" if vertical_deviation > 0.1 else ("Up" if vertical_deviation < -0.1 else "Center")

    # These thresholds (0.07, 0.1) are approximate and will need fine-tuning
    # based on your webcam, lighting, and desired sensitivity.

    return gaze_h, gaze_v

def process_frame_for_gaze(frame):
    """
    Processes a single video frame to detect faces and estimate gaze.
    Returns the annotated frame, and gaze data.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    gaze_data = {
        "face_detected": False,
        "left_eye_gaze": {"horizontal": "N/A", "vertical": "N/A"},
        "right_eye_gaze": {"horizontal": "N/A", "vertical": "N/A"},
        "overall_gaze": "N/A"
    }

    if results.multi_face_landmarks:
        gaze_data["face_detected"] = True
        for face_landmarks in results.multi_face_landmarks:
            img_h, img_w, _ = frame.shape

            # Get left eye and iris points
            left_eye_points, left_iris_points = get_eye_landmarks(
                face_landmarks, (img_h, img_w, _), LEFT_EYE_INDICES, LEFT_IRIS_INDICES
            )
            # Get right eye and iris points
            right_eye_points, right_iris_points = get_eye_landmarks(
                face_landmarks, (img_h, img_w, _), RIGHT_EYE_INDICES, RIGHT_IRIS_INDICES
            )

            # Calculate gaze for each eye
            left_gaze_h, left_gaze_v = calculate_gaze_direction(left_eye_points, left_iris_points, eye_side="left")
            right_gaze_h, right_gaze_v = calculate_gaze_direction(right_eye_points, right_iris_points, eye_side="right")

            gaze_data["left_eye_gaze"]["horizontal"] = left_gaze_h
            gaze_data["left_eye_gaze"]["vertical"] = left_gaze_v
            gaze_data["right_eye_gaze"]["horizontal"] = right_gaze_h
            gaze_data["right_eye_gaze"]["vertical"] = right_gaze_v

            # Determine overall gaze for "QuietEye" purposes
            if left_gaze_h == "Center" and right_gaze_h == "Center" and \
               left_gaze_v == "Center" and right_gaze_v == "Center":
                gaze_data["overall_gaze"] = "Focused (Center)"
            elif (left_gaze_h != "Center" or right_gaze_h != "Center") or \
                 (left_gaze_v != "Center" or right_gaze_v != "Center"):
                gaze_data["overall_gaze"] = "Potentially Distracted (Looking Away)"
            else:
                gaze_data["overall_gaze"] = "Undetermined" # Should ideally not hit often

            # --- Optional: Drawing for Visualization ---
            # Draw Face Mesh landmarks
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS, # You can change this to FACEMESH_IRISES or TESSELATION
                drawing_spec,
                drawing_spec
            )
            # Draw iris centers for clear visualization
            if left_iris_points:
                left_iris_center = (
                    int(sum([p[0] for p in left_iris_points]) / len(left_iris_points)),
                    int(sum([p[1] for p in left_iris_points]) / len(left_iris_points))
                )
                cv2.circle(frame, left_iris_center, 2, (0, 255, 255), -1) # Yellow for left iris
            if right_iris_points:
                right_iris_center = (
                    int(sum([p[0] for p in right_iris_points]) / len(right_iris_points)),
                    int(sum([p[1] for p in right_iris_points]) / len(right_iris_points))
                )
                cv2.circle(frame, right_iris_center, 2, (0, 255, 255), -1) # Yellow for right iris

            # Display gaze status on the frame
            cv2.putText(frame, f"L Gaze: {left_gaze_h}, {left_gaze_v}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"R Gaze: {right_gaze_h}, {right_gaze_v}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Overall: {gaze_data['overall_gaze']}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


    return frame, gaze_data

# --- Main application loop ---
def main():
    cap = cv2.VideoCapture(0) # 0 for default webcam

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    print("Starting QuietEye Gaze Detection. Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        # Flip the frame horizontally for a more intuitive "selfie" view
        frame = cv2.flip(frame, 1)

        # Process the frame for gaze detection
        annotated_frame, gaze_info = process_frame_for_gaze(frame)

        # You can now use gaze_info for your QuietEye report generation
        # Example: print(gaze_info) or log it to a file

        cv2.imshow('QuietEye - Gaze Detection (Press Q to quit)', annotated_frame)

        if cv2.waitKey(5) & 0xFF == ord('q'): # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()
    print("QuietEye Gaze Detection stopped.")

if __name__ == "__main__":
    main()