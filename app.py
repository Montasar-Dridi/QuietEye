from quieteye.core.camera import start_camera, show_camera_feed
from quieteye.core.pipeline import face_mesh_processor

def run():
    print("Running Quiet Eye...")
    cap = start_camera(0)
    print("Camera Started")
    show_camera_feed(cap, process_fn=face_mesh_processor, visualize=False)
    print("Exiting Quiet Eye")

if __name__ == "__main__":
    run()