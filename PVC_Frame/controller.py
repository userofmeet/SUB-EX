import pygame
import serial
import time

SERIAL_PORT = 'COM8'
BAUD_RATE = 115200

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected! Please connect your Logitech F310.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Controller detected: {joystick.get_name()}")
print(f"Number of axes: {joystick.get_numaxes()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to initialize
    print(f"Connected to Arduino on {SERIAL_PORT}")
except:
    print(f"Failed to connect to Arduino on {SERIAL_PORT}")
    print("Available ports:")
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"  {port.device}")
    exit()

def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def apply_deadzone(value, deadzone=0.1):
    if abs(value) < deadzone:
        return 0.0
    return value

# Test all axes to find the correct mapping
print("\n=== Testing Controller Axes ===")
print("Move all sticks and triggers to see their axis numbers")
print("Press any button to continue...")
print("=" * 50)

waiting = True
while waiting:
    pygame.event.pump()
    
    # Display all axis values
    print("\rAxes: ", end='')
    for i in range(joystick.get_numaxes()):
        value = joystick.get_axis(i)
        print(f"[{i}]:{value:+.2f} ", end='')
    
    # Check if any button is pressed
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            waiting = False
            break
    
    time.sleep(0.05)

print("\n\n=== ROV Control Started ===")
print("Controls (F310 in DirectInput mode):")
print("  Left Stick Y-axis (Axis 1): Forward/Backward")
print("  Left Stick X-axis (Axis 0): Left/Right turning")
print("  Right Stick Y-axis (Axis 3): Vertical Up/Down")
print("  Press START button (button 7) to exit and STOP all motors")
print("=" * 50 + "\n")

try:
    clock = pygame.time.Clock()
    running = True
    
    while running:
        pygame.event.pump()
        
        # Read controller inputs with safety checks
        num_axes = joystick.get_numaxes()
        
        # Left stick for forward/backward and turning
        forward_backward = apply_deadzone(-joystick.get_axis(1)) if num_axes > 1 else 0.0  # Inverted
        left_right = apply_deadzone(joystick.get_axis(0)) if num_axes > 0 else 0.0
        
        # Right stick Y-axis for vertical (axis 3 on F310)
        if num_axes > 3:
            vertical = apply_deadzone(-joystick.get_axis(3))  # Right stick Y
        else:
            vertical = 0.0
        
        # Calculate thruster speeds
        # Left and Right thrusters for forward/backward and turning
        left_speed = forward_backward - left_right
        right_speed = forward_backward + left_right
        
        # Constrain to -1.0 to 1.0
        left_speed = max(-1.0, min(1.0, left_speed))
        right_speed = max(-1.0, min(1.0, right_speed))
        
        # Map to ESC range (0-180, 0 is stop)
        left_pwm = map_value(left_speed, -1.0, 1.0, 0, 180)
        right_pwm = map_value(right_speed, -1.0, 1.0, 0, 180)
        vertical_pwm = map_value(vertical, -1.0, 1.0, 0, 180)
        
        # Send data to Arduino
        command = f"{left_pwm},{right_pwm},{vertical_pwm}\n"
        arduino.write(command.encode())
        
        # Read any feedback from Arduino
        while arduino.in_waiting > 0:
            arduino_msg = arduino.readline().decode('utf-8').strip()
            if arduino_msg:
                print(f"\n[Arduino]: {arduino_msg}")
        
        # Print debug info
        print(f"\rController -> L:{left_pwm:3d} R:{right_pwm:3d} V:{vertical_pwm:3d}  ", end='')
        
        # Check for START button to exit
        num_buttons = joystick.get_numbuttons()
        if num_buttons > 7 and joystick.get_button(7):
            print("\n\nExit button pressed. Stopping all motors...")
            running = False
        
        # Run at 50Hz
        clock.tick(50)
        
except KeyboardInterrupt:
    print("\n\nProgram interrupted by user")

except Exception as e:
    print(f"\n\nError occurred: {e}")

finally:
    # STOP all thrusters completely before exiting
    print("Sending STOP command to all motors...")
    
    # Send 0,0,0 multiple times to ensure motors STOP
    for i in range(10):
        arduino.write(b"0,0,0\n")
        time.sleep(0.1)
    
    print("All motors STOPPED!")
    time.sleep(0.5)
    
    arduino.close()
    pygame.quit()
    print("Program ended safely. Motors are OFF.")
