import cv2
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
