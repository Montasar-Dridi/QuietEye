import cv2


def start_camera(index = 0):
    cap = cv2.VideoCapture(index)
    
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")
        exit()
    
    return cap


def show_camera_feed(cap, process_fn=None, visualize=False):
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if process_fn:
            frame = process_fn(frame, visualize=visualize)

        cv2.imshow("QuietEye Camera Feed", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return




    