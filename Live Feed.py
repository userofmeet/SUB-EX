import cv2
from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.start()

cv2.namedWindow("Live Feed")

prev_time = 0

try:
    while True:
        frame = picam2.capture_array()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        fps_text = f"FPS: {fps:.2f}"
        cv2.putText(frame_rgb, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Live Feed", frame_rgb)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:=
    cv2.destroyAllWindows()
    picam2.stop()

