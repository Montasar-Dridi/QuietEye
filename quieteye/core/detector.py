import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.8)

def detect_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    detections = []
    face_detected = False

    if results.detections:
        face_detected = True
        h, w, _ = frame.shape
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            bbox = (
                int(bboxC.xmin * w),
                int(bboxC.ymin * h),
                int(bboxC.width * w),
                int(bboxC.height * h)
            )
            confidence = detection.score[0]
            detections.append({"bbox": bbox, "confidence": confidence})

    return face_detected, detections
