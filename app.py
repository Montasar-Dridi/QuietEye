from quieteye.core.camera import start_camera, show_camera_feed
from quieteye.core.pipeline import face_mesh_processor, gaze_estimation_processor
from quieteye.core.detector import detect_face_mesh

frame_count = 0

def run():
    print("Running Quiet Eye...")
    cap = start_camera(0)

    def full_processor(frame, visualize=False):
        global frame_count
        frame_count += 1

        face_detected, landmarks_list = detect_face_mesh(frame)
        if face_detected:
            gaze_estimation_processor(landmarks_list[0], frame_count)
        return face_mesh_processor(frame, visualize=visualize)

    show_camera_feed(cap, process_fn=full_processor, visualize=True)
    print("Exiting Quiet Eye")

if __name__ == "__main__":
    run()
