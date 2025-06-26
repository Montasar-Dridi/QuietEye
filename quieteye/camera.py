import cv2


def start_camera(index = 0):
    cap = cv2.VideoCapture(index)
    
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")
        exit()
    
    return cap


def show_camera_feed(cap, window_name="Quiet Eye"):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    while True:
        ret, frame = cap.read()

        if not ret:
            raise RuntimeError("Cannot recieve frame")
            break

        cv2.imshow(window_name, frame)

        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()





    