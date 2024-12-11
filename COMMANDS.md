This repository contains all the commands and steps to connect Raspberry Pi to VS Code via SSH protocol. You can write all the commands in the terminal section of the VS Code and execute your programs in RPi

# STEPS 
ssh -> connect to host -> add new host -> pi@raspberrypi.local -> select ssh file to config -> continue -> ENTER YOUR PASSWORD -> let it connect -> Explorer -> open folder -> /home/pi -> ENTER PASSWORD -> 

# COMMANDS
## Enable VNC / Camera
```
sudo raspi-config
```

## Update the RPi to the latest version
```
sudo apt update && sudo apt upgrade -y
```

## Reboot the RPi
```
sudo reboot
```

## Install python and pip
```
sudo apt install -y python3 python3-pip
```

## Install opencv for image processing
```
sudo apt install -y python3-opencv
```

## Install packages (Recommended for System-Wide Use)
```
sudo apt install python3-numpy python3-picamera2
```

## Verify the Camera Module Installation: Test with:
## If the camera is working, you'll see a live preview.
```
libcamera-hello
```

## Capture an image
```
libcamera-jpeg -o test.jpg
```

## Install matplotlib
```
sudo apt install python3-matplotlib
```

