import cv2
import time
import mediapipe as mp
from quieteye.core.detector import detect_face_mesh

mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles


def face_mesh_processor(frame, visualize=False):
    face_detected, landmarks_list = detect_face_mesh(frame)

    if visualize:
        for landmarks in landmarks_list:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=landmarks,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_style.get_default_face_mesh_tesselation_style()
            )

    return frame