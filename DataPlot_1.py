import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

#Enter your COM port from device manager
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)

distances = []
timestamps = []
threshold = 1.5
sampling_interval = 200 / 1000

def read_distance():
    ser.write(b'\n')
    line = ser.readline().decode().strip()
    try:
        distance = float(line)
    except ValueError:
        distance = None
    return distance

def update(frame):
    distance = read_distance()
    if distance is not None:
        distances.append(distance)
        timestamps.append(len(distances) * sampling_interval)
        if len(distances) > 100:
            distances.pop(0)
            timestamps.pop(0)
        plt.cla()
        plt.plot(timestamps, distances, label="Distance (cm)", color='blue')
        for i in range(1, len(distances)):
            if abs(distances[i] - distances[i - 1]) >= threshold:
                plt.scatter(timestamps[i], distances[i], color='red', label="Crack Detected" if i == 1 else "")
        if distances:
            plt.scatter(timestamps[-1], distances[-1], color='green', label=f"Current: {distances[-1]:.1f} cm")
        plt.xlabel("Time (s)")
        plt.ylabel("Distance (cm)")
        plt.title("Crack Detection Using Ultrasonic Sensor")
        plt.legend(loc="upper left")
        plt.grid()

fig, ax = plt.subplots()
ani = FuncAnimation(fig, update, interval=sampling_interval * 1000)

plt.show()
ser.close()
