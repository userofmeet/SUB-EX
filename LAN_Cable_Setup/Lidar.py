import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Store last few readings to smooth out output
window_size = 5
buffer = []

def read_lidar():
    while True:
        if ser.in_waiting >= 9:
            data = ser.read(9)
            if data[0] == 0x59 and data[1] == 0x59:
                distance = data[2] + (data[3] << 8)  # In cm
                buffer.append(distance)

                if len(buffer) > window_size:
                    buffer.pop(0)

                average_distance = sum(buffer) / len(buffer)
                print(f"Distance: {average_distance:.1f} cm")

try:
    read_lidar()
except KeyboardInterrupt:
    ser.close()
    print("Stopped.")
