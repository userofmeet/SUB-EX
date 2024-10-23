import cv2
from picamera2 import Picamera2
import time

# Initialize the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

cv2.namedWindow("Live Feed")

prev_time = 0

try:
    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()

        # Convert the frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Add FPS text to the frame
        fps_text = f"FPS: {fps:.2f}"
        cv2.putText(frame_rgb, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Live Feed", frame_rgb)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Cleanup
    cv2.destroyAllWindows()
    picam2.stop()

