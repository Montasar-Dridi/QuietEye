import cv2
import time
from quieteye.core.detector import detect_faces

last_print_time = 0

def face_detection_processor(frame, visualize=False):
    global last_print_time
    face_detected, detections = detect_faces(frame)

    if face_detected:
        current_time = time.time()
        if current_time - last_print_time >= 10:
            formatted_time = time.strftime("%H:%M:%S", time.localtime(current_time))
            print(f"Face detected at {formatted_time}")
            last_print_time = current_time

        if visualize:
            for det in detections:
                x, y, w, h = det['bbox']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{det['confidence']:.2f}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return frame