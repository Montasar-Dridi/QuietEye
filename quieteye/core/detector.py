import cv2
import numpy as np
import mediapipe as mp

face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


def detect_face_mesh(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        return True, results.multi_face_landmarks
    else:
        return False, []

# TODO: make the return as dictionary that has right, left, center, and the avg_ratio for Machine Learning ratio attention scoring later.
def estimate_gaze_direction(landmarks):
    # Left eye
    left_eye_left = landmarks.landmark[33].x
    left_eye_right = landmarks.landmark[133].x
    left_iris = landmarks.landmark[468].x

    # Right eye
    right_eye_left = landmarks.landmark[362].x
    right_eye_right = landmarks.landmark[263].x
    right_iris = landmarks.landmark[473].x

    left_ratio = (left_iris - left_eye_left) / (left_eye_right - left_eye_left)
    right_ratio = (right_iris - right_eye_left) / (right_eye_right - right_eye_left)

    avg_ratio = (left_ratio + right_ratio) / 2.0

    if avg_ratio < 0.35:
        return "RIGHT"
    elif avg_ratio > 0.65:
        return "LEFT"
    else:
        return "CENTER"

#TODO: fix inverse output looking down --> looking up etc...
def estimate_head_position(frame, landmarks):
    image_height, image_width = frame.shape[:2]

    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (0.0, -63.6, -12.5),         # Chin
        (-43.3, 32.7, -26.0),        # Left eye outer corner
        (43.3, 32.7, -26.0),         # Right eye outer corner
        (-28.9, -28.9, -24.1),       # Left mouth corner
        (28.9, -28.9, -24.1)         # Right mouth corner
    ])

    landmark_ids = [1, 152, 33, 263, 61, 291]
    image_points = np.array([
        (landmarks.landmark[i].x * image_width,
         landmarks.landmark[i].y * image_height)
        for i in landmark_ids
    ], dtype="double")

    focal_length = image_width
    center = (image_width / 2, image_height / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))

    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs
    )

    if not success:
        return None

    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

    _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(
        np.hstack((rotation_matrix, translation_vector))
    )
    pitch, yaw, roll = euler_angles.flatten()

    # Debug print
    print(f"[DEBUG] Pitch: {pitch:.2f}, Yaw: {yaw:.2f}, Roll: {roll:.2f}")

    if abs(yaw) > 25:
        status = "Looking Away"
    elif pitch < -10:
        status = "Looking Up"
    elif pitch > 10:
        status = "Looking Down"
    else:
        status = "Looking Straight"

    return {
        "yaw": yaw,
        "pitch": pitch,
        "roll": roll,
        "status": status
    }
