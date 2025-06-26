from quieteye.camera import start_camera, show_camera_feed

def run():
    print("Running Quiet Eye...")
    cap = start_camera(0)
    print("Camera Started")
    show_camera_feed(cap)
    print("Exiting Quiet Eye")

if __name__ == "__main__":
    run()