import socket
import json
from pymavlink import mavutil
import time

# MAVLink connection (adjust port if needed)
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)

# Wait for a heartbeat to confirm connection
print("Waiting for Pixhawk...")
master.wait_heartbeat()
print("Connected to Pixhawk")

# UDP setup
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Listening for joystick data on port {UDP_PORT}...")

# Track arming state to avoid repeated sends
armed = False

while True:
    data, addr = sock.recvfrom(1024)
    try:
        controller = json.loads(data.decode())
        print(f"\nFrom {addr}:")
        print("  Axes:", controller['axes'])
        print("  Buttons:", controller['buttons'])

        # If button 0 is pressed and Pixhawk is not yet armed
        if controller['buttons'][0] == 1 and not armed:
            print("🟢Arming Pixhawk...")
            master.arducopter_arm()
            master.motors_armed_wait()
            print("✅Pixhawk armed!")
            armed = True

        # Optional: Disarm on button 1
        if controller['buttons'][1] == 1 and armed:
            print("🔴Disarming Pixhawk...")
            master.arducopter_disarm()
            master.motors_disarmed_wait()
            print("🔴Pixhawk disarmed!")
            armed = False

    except Exception as e:
        print("Error decoding or sending to Pixhawk:", e)
