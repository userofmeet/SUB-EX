# Raspberry Pi Ethernet Tethering and SSH Access via Laptop

This guide explains how to share your laptop's internet connection with a Raspberry Pi using an Ethernet cable and access it via SSH.

---

## 🧩 Step 1: Connect Ethernet Cable
- First, **connect the tether cable** (Ethernet) from your **laptop to the Raspberry Pi**.

---

## ⚙️ Step 2: Enable Internet Sharing on Windows

1. Go to **Control Panel** → **Network and Internet** → **Network and Sharing Center** → **Change adapter settings**.
2. Right-click on your **Wi-Fi connection** → click **Properties**.
3. Under the **Sharing** tab:
   - Check **"Allow other network users to connect through this computer’s internet connection"**.
   - Check **"Allow other network users to control or disable the shared Internet connection"**.
4. In the **Home networking connection**, choose **Ethernet**.
5. Click **OK**.

---

## 🌐 Step 3: Set Static IP for Ethernet

1. Go to **Ethernet** → **Properties**.
2. Select **Internet Protocol Version 4 (TCP/IPv4)** → click **Properties**.
3. Select **Use the following IP address**:
   - **IP address**: `192.168.137.1`
   - **Subnet mask**: `255.255.255.0`
   - Leave other fields blank and click **OK**.

---
If your RPi is freshly booted then run this command in the CMD or PowerShell to remove the old key 
```bash
ssh-keygen -R raspberry.local
```
or
```bash
ssh-keygen -R 192.168.137.2
```
Update your Raspberry Pi and use the following commands to update your RPi to use the codes in this repository:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y v4l-utils
sudo apt install -y python3-picamera2
sudo apt install -y python3-numpy
sudo apt install -y python3-opencv
sudo apt install -y python3-scipy
sudo apt install python3-pip
pip3 install flask --break-system-packages
sudo apt install fswebcam -y
pip3 install pymavlink --break-system-packages
sudo apt install python3-serial python3-matplotlib
sudo apt-get install x11-apps
```

## 🧰 Step 4: Enable and Configure dhcpcd on Raspberry Pi

Check the status of `dhcpcd`:

```bash
sudo systemctl status dhcpcd
```
If it’s inactive or not found, run the following commands:
```bash
sudo apt update
sudo apt install dhcpcd5
sudo systemctl enable dhcpcd
sudo systemctl start dhcpcd
```
---

## 🛠️ Step 5: Configure Static IP on Raspberry Pi
Edit the **dhcpcd.conf** file

```bash
sudo nano /etc/dhcpcd.conf
```
Add the following lines at the end
```bash
interface eth0
static ip_address=192.168.137.2/24
static routers=192.168.137.1
static domain_name_servers=8.8.8.8

```
---
## 📁 Step 6: Modify config.txt
Edit the boot firmware configuration: 
```bash
sudo nano /boot/firmware/config.txt
```
Add the following lines at the end:
```bash
dtoverlay=disable-wifi
```
---
## 🖧 Step 7: Enable SSH Access
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

## 🔄 Step 8: Reboot Raspberry Pi
```bash
sudo reboot
```
Now you can connect to your Raspbery Pi using SSH:
```bash
ssh pi@192.168.137.2
```

✅ You’re now connected to your Raspberry Pi via Ethernet with SSH access and shared internet.





