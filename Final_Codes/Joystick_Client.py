import pygame
import socket
import time
import json

RPi_IP = '192.168.104.138'; # Enter the IP Address 
RPi_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pygame.init()
pygame.joystick.init()

while pygame.joystick.get_count() == 0:
    print("Waiting for controller...")
    time.sleep(1)
    pygame.joystick.quit()
    pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Connected to: {joystick.get_name()}")

try:
    while True:
        pygame.event.pump()
        data = {
            'axes': [joystick.get_axis(i) for i in range(joystick.get_numaxes())],
            'buttons': [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
        }
        message = json.dumps(data).encode()
        sock.sendto(message, (RPi_IP, RPi_PORT))
        time.sleep(0.05)  # 20 Hz

except KeyboardInterrupt:
    print("Stopped")
