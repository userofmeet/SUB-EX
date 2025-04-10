from flask import Flask, Response
import cv2
import time

app = Flask(__name__)

# Open the USB webcam (index 0)
camera = cv2.VideoCapture(0)

# Set resolution (optional)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize time for FPS calculation
prev_time = 0

def generate_frames():
    global prev_time
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time else 0
            prev_time = curr_time

            # Add FPS text to the frame
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "<h1>USB Webcam Stream with FPS</h1><img src='/video_feed'>"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
