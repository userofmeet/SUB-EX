import pygame
import serial
import time
import json

arduino = serial.Serial('COM5', 115200)
time.sleep(2)  # Wait for the serial connection to initialize
pygame.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()

def pwm_forward(val):
    # val 0..1 → 1000..2000us
    return int(1000 + val * 1000)

def pwm_down(val):
    # vertical thruster: 0..1 → 1000..2000
    return int(1000 + val * 1000)

print("Sending joystick values...")

while True:
    pygame.event.pump()

    # forward
    forward = -joy.get_axis(1)     # up = -1

    if forward < 0:
        forward = 0   # no reverse

    # steering
    turn = joy.get_axis(0)         # -1 left, +1 right

    # motor mixing (but only forward)
    left = forward - (turn * 0.5)
    right = forward + (turn * 0.5)

    # clamp 0..1
    left = max(0, min(1, left))
    right = max(0, min(1, right))

    # vertical thruster 
    rt = (joy.get_axis(5) + 1) / 2    # 0..1
    vertical = rt                     # only downward thrust

    data = {
        "L": pwm_forward(left),
        "R": pwm_forward(right),
        "V": pwm_down(vertical)
    }

    arduino.write((json.dumps(data) + "\n").encode())
    time.sleep(0.02)
