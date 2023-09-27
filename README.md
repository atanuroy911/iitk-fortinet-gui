# IITK Fortinet Authenticator (WiFi & LAN)

![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

The **IITK Fortinet Authenticator** is a simple yet effective tool designed to streamline the process of logging in to the captive portal of the Indian Institute of Technology Kanpur (IITK). It provides a convenient way to remember your username and password and automatically log in to the Fortinet captive portal, ensuring uninterrupted internet access during your stay at IITK. The software is meant to be a GUI Interface over an existing Authenticator Script (which is used in the server at IITK) 

<p align="center">
  <img src="https://i.ibb.co/XtdH150/image.png">
</p>

**Note: This software is targetted for IITK WiFi (NOT IITK-Sec or IITK-Sec-5GHz) and LAN. Using on other networks will simply show that you are connected to internet. You can keep it running forever. Whenever it detects a network with no internet access it will attempt to connect to the Fortiguard Captive Portal and login**

## Features

- **Automated Login:** Forget the hassle of manually entering your credentials each time you connect to the IITK network. The IITK Fortinet Authenticator will handle it for you.

- **Password Encryption:** Your login credentials are securely stored in your local computer inside a local DB which uses SQLite.

- **Session Keep Alive:** The tool will periodically ping the captive portal to ensure your internet session remains active.

## Getting Started

### Installation

1. Go to the **[Releases Page](https://github.com/atanuroy911/iitk-fortinet-gui/releases)**

   ```bash
   https://github.com/atanuroy911/iitk-fortinet-gui/releases
   ```
3. Download the **appropriate installer** for your System
4. **Install** the software

### Usage

1. Open the App from your Applications menu
2. Enter Your Username Password
3. Click **Save Info**
4. Click on **Start Service**
5. Close or Minimize the Window

### State of Work
1. Start at startup only works on Windows (via Regedit)
2. Minimize to Taskbar do not work on Raspbian (Raspberry Pi) - Workaround Below
3. Update Section - work in progress
4. Rarely, It may give a variable error. Just Stop and Restart the script option

### BUGS & Fixes
#### 1. Auto Startup Option
Implementing this option on windows was fairly easy. For Mac and Linux, we have to work with Launch Agents and Service Daemons respectively. Making this work requires SUDO permission. Working to make this user friendly.

#### 2. Minimize to taskbar on Rasbperry Pi
The minimize to taskbar function is followed by Notification or Toast message i.e. the App has now gone to background. Furthermore there are several other notifications. Unfortunately the Raspbian OS does not give an interactive notification daemon or application. The library used in this project for notification is called plyer. This library calls the FreeDesktop Notification Handler that comes by default in every major Linux distributions whether it's running GTK Based desktop environment or not. The raspberry pi being lightweight, don't have this. Hence, we have to use a different notification daemon that can be spoofed as the FreeeDesktop Daemon which Plyer library uses. 
**Follow these steps:**
1. Run:
```shell
sudo apt install -y notification-daemon
```
2. Then, create a new file and paste the following script to it:
```shell
nano
```
```shell
#!/usr/bin/env bash

clear

if [ "${EUID}" -ne '0' ]; then
    printf "%s\n\n" 'You must run this script WITH root/sudo.'
fi

file=/usr/share/dbus-1/services/org.freedesktop.Notifications.service

cat > "${file}" <<'EOF'
[D-BUS Service]
Name=org.freedesktop.Notifications
Exec=/usr/lib/notification-daemon/notification-daemon
EOF
```
3. Press CTRL+O to save and CTRL+X to quit nano
4. Reboot the system

#### 3. Automatic Update Feature Pending
#### 4. Variable Error
This error is a peculiar one. It happens very rarely. I have seen it 1 time only. I am looking out for it. Need to replicate the error before solving it.

## Contribution

Contributions are welcome! If you have any ideas, suggestions, or improvements, please feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided as-is, without any warranties or guarantees. Use it responsibly and at your own risk.

---

Feel free to reach out if you have any questions or encounter any issues. Happy browsing at IITK! 🚀

Author: Atanu Shuvam Roy
