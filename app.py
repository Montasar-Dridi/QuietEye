from quieteye.core.camera import start_camera, show_camera_feed
from quieteye.core.pipeline import face_mesh_processor, gaze_estimation_processor, head_position_processor

frame_count = 0

def run():
    print("Running Quiet Eye...")
    cap = start_camera(0)

    def full_processor(frame, visualize=False):
        global frame_count
        frame_count += 1

        face_detected, landmarks_list = face_mesh_processor(frame, visualize=visualize)
        if face_detected:
            for landmarks in landmarks_list:
                gaze_estimation_processor(landmarks, frame_count)
                head_position_processor(frame, landmarks, frame_count)

        return frame

    show_camera_feed(cap, process_fn=full_processor, visualize=True)
    print("Exiting Quiet Eye")

if __name__ == "__main__":
    run()
