import cv2
import time
import mediapipe as mp
from quieteye.core.detector import detect_face_mesh, estimate_gaze_direction, estimate_head_position

mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles


def face_mesh_processor(frame, visualize=False):
    face_detected, landmarks_list = detect_face_mesh(frame)

    if visualize and face_detected:
        for landmarks in landmarks_list:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=landmarks,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_style.get_default_face_mesh_tesselation_style()
            )

    return face_detected, landmarks_list


def gaze_estimation_processor(landmarks, frame_count):
    if frame_count % 5 == 0:
        gaze_direction = estimate_gaze_direction(landmarks)
        print(f"[Frame {frame_count}] | Gaze Direction {gaze_direction}")

def head_position_processor(frame, landmarks, frame_count):
    if frame_count % 5 == 0:
        head_pose = estimate_head_position(frame, landmarks)
        print(f"[Frame {frame_count}] | Yaw: {head_pose['yaw']:.2f}, Pitch: {head_pose['pitch']:.2f}, Roll: {head_pose['roll']:.2f} → {head_pose['status']}")