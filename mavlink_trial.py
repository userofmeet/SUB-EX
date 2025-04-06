import socket
import json
import cv2
from picamera2 import Picamera2
import numpy as np
import math
import scipy.ndimage
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from pymavlink import mavutil

# ------------- Globals -------------
output_frame = None
frame_lock = threading.Lock()
controller_data = {"axes": [], "buttons": []}
master = None  # Pixhawk connection

# --------- Pixhawk Connection ---------
def connect_pixhawk():
    global master
    try:
        master = mavutil.mavlink_connection('/dev/ttyACM0', baud=115200)
        master.wait_heartbeat()
        print(f"[Pixhawk] Connected to system {master.target_system}")
    except Exception as e:
        print(f"[Pixhawk] Connection failed: {e}")

# --------- Joystick UDP Receiver ---------
def joystick_listener():
    global controller_data, master
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"[Joystick] Listening on UDP {UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            controller_data = json.loads(data.decode())
            print(f"\n[Joystick] From {addr}:")
            print("  Axes:", controller_data['axes'])
            print("  Buttons:", controller_data['buttons'])

            if master:
                axes = controller_data['axes']
                buttons_list = controller_data['buttons']

                # Scale axes values
                x = int(axes[0] * 1000) if len(axes) > 0 else 0
                y = int(axes[1] * 1000) if len(axes) > 1 else 0
                z = int((1 - axes[2]) * 500) if len(axes) > 2 else 500
                r = int(axes[3] * 1000) if len(axes) > 3 else 0

                # Buttons to bitmask
                buttons = 0
                for i, b in enumerate(buttons_list):
                    if b:
                        buttons |= 1 << i

                master.mav.manual_control_send(
                    target=master.target_system,
                    x=x, y=y, z=z, r=r,
                    buttons=buttons
                )
        except Exception as e:
            print("Error decoding joystick data:", e)

# --------- Crack Detection Function ---------
def non_max_suppression(data, win):
    data_max = scipy.ndimage.maximum_filter(data, footprint=win, mode='constant')
    data_max[data != data_max] = 0
    return data_max

def orientated_non_max_suppression(mag, ang):
    ang_quant = np.round(ang / (np.pi / 4)) % 4
    winE = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
    winSE = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    winS = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    winSW = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])

    magE = non_max_suppression(mag, winE)
    magSE = non_max_suppression(mag, winSE)
    magS = non_max_suppression(mag, winS)
    magSW = non_max_suppression(mag, winSW)

    mag[ang_quant == 0] = magE[ang_quant == 0]
    mag[ang_quant == 1] = magSE[ang_quant == 1]
    mag[ang_quant == 2] = magS[ang_quant == 2]
    mag[ang_quant == 3] = magSW[ang_quant == 3]
    return mag

# --------- Video Capture & Processing ---------
def camera_worker():
    global output_frame, frame_lock

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    prev_time = time.time()

    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255.0
        blur = cv2.GaussianBlur(gray, (43, 43), 21)
        subtracted = cv2.subtract(gray, blur)

        sobelx = cv2.Sobel(subtracted, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(subtracted, cv2.CV_64F, 0, 1, ksize=3)
        mag = np.hypot(sobelx, sobely)
        ang = np.arctan2(sobely, sobelx)

        threshold = 4 * 1.3 * np.mean(mag)
        mag[mag < threshold] = 0
        mag = orientated_non_max_suppression(mag, ang)
        mag[mag > 0] = 255
        mag = mag.astype(np.uint8)

        contours, _ = cv2.findContours(mag, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        fps = 1 / (time.time() - prev_time)
        prev_time = time.time()
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        with frame_lock:
            output_frame = frame.copy()

# --------- MJPEG Stream Server ---------
class MJPEGHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header('Content-type',
                         'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

        while True:
            with frame_lock:
                if output_frame is None:
                    continue
                success, jpeg = cv2.imencode('.jpg', output_frame)
                if not success:
                    continue
                frame_bytes = jpeg.tobytes()

            try:
                self.wfile.write(b'--frame\r\n')
                self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n' +
                                 frame_bytes + b'\r\n')
                time.sleep(0.05)
            except BrokenPipeError:
                break

def start_http_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MJPEGHandler)
    print(f"[MJPEG] Streaming started on http://<your_pi_ip>:8080")
    httpd.serve_forever()

# --------- Main Start ---------
if __name__ == "__main__":
    connect_pixhawk()
    threading.Thread(target=joystick_listener, daemon=True).start()
    threading.Thread(target=camera_worker, daemon=True).start()
    start_http_server()
