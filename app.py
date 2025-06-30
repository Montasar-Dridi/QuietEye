from quieteye.core.camera import start_camera, show_camera_feed
from quieteye.core.pipeline import face_mesh_processor, gaze_estimation_processor, head_position_processor
from quieteye.core.metrics import compute_attention_score
from quieteye.utils.tracker import start_session, log_attention, get_session_data
from quieteye.utils.reporting import generate_terminal_report
from quieteye.utils.terminal import update_terminal_data, start_terminal_display, stop_terminal_display


import threading
import time

frame_count = 0

threading.Thread(target=start_terminal_display, daemon=True).start()


start_session()

def run():
    print("Running QuietEye...")
    cap = start_camera(0)

    def full_processor(frame, visualize=False):
        global frame_count
        frame_count += 1

        face_detected, landmarks_list = face_mesh_processor(frame, visualize=visualize)
        if face_detected:
            for landmarks in landmarks_list:
                gaze_direction = gaze_estimation_processor(landmarks, frame_count)
                head_pose = head_position_processor(frame, landmarks, frame_count)

                if gaze_direction and head_pose:
                    score = compute_attention_score(
                        gaze_direction=gaze_direction.lower(),
                        pitch=head_pose['pitch'],
                        yaw=head_pose['yaw']
                    )

                    update_terminal_data(
                        frame=frame_count,
                        gaze=gaze_direction.lower(),
                        pitch=head_pose['pitch'],
                        yaw=head_pose['yaw'],
                        head_status=head_pose['status'],
                        score=score
                    )
                    log_attention(score)

        return frame

    show_camera_feed(cap, process_fn=full_processor, visualize=True)
    
    stop_terminal_display()  # ✅ tell the thread to stop
    time.sleep(0.2)           # ⏱ allow thread to exit gracefully

    report_session_summary()  # ✅ finally print the report


def report_session_summary():
    start_time, end_time, attention_log = get_session_data()
    generate_terminal_report(start_time, end_time, attention_log)

if __name__ == "__main__":
    run()
