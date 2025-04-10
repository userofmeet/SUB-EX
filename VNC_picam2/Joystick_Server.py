# Python code for receiving the controller inputs which it further sends to the Pixhawk flight controller
import socket
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for controller data on port {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    try:
        controller = json.loads(data.decode())
        print(f"\nFrom {addr}:")
        print("  Axes:", controller['axes'])
        print("  Buttons:", controller['buttons'])
    except Exception as e:
        print("Error decoding data:", e)
