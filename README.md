# Screendroid

**A free, network-based remote control for Android TVs, projectors, and Android devices — powered by ADB and accessible from any web browser.**

---

## Features

### Remote Control

* DPAD Navigation (Up, Down, Left, Right)
* OK / Select
* Home
* Back
* Menu
* Power Toggle

### Keyboard Controls

Use your keyboard directly:

| Key       | Action      |
| --------- | ----------- |
| ↑ ↓ ← →   | Navigation  |
| Enter     | OK          |
| Backspace | Back        |
| +         | Volume Up   |
| -         | Volume Down |
| *         | Mute        |

Basic text input is also supported.

---

### Media Controls

* Play / Pause
* Stop
* Next Track
* Previous Track

---

### Device Information

* Storage Information
* Battery Information
* Android OS Version
* Connected Device List

---

### File Management

Transfer files over your local network without installing any third-party applications.

Supported actions:

* Upload files to `/sdcard/Download/`
* Download files from `/sdcard/Download/`
* Browse downloaded files
* Capture screenshots

---

### Application Management

* Launch installed apps
* Force-close apps
* Search installed packages

---

### Smart Connection Features

* Automatic projector/TV discovery
* Stored device address using browser localStorage
* One-click reconnect
* Wireless ADB support

---

## Requirements

Before using Screendroid, install:

* Python 3.10+
* ADB (Android Debug Bridge)
* Android TV, projector, or Android device
* USB Debugging or Wireless Debugging enabled
* Device connected to the same network as your computer

---

## Installation

### Clone Repository

```bash
git clone https://github.com/azranfainaus/Screendroid.git

cd Screendroid
```

---

### Create Virtual Environment

#### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

#### Windows

```bat
python -m venv venv

venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask
```

---

## Install ADB

### macOS

```bash
brew install android-platform-tools
```

### Ubuntu / Debian

```bash
sudo apt update

sudo apt install android-tools-adb
```

### Windows

```bat
choco install adb
```

Or install Google Platform Tools manually:

https://developer.android.com/tools/releases/platform-tools

---

## Connect Your Device

### Wireless ADB

```bash
adb connect DEVICE_IP:5555
```

Example:

```bash
adb connect 192.168.1.10:5555
```

Verify:

```bash
adb devices
```

Expected:

```text
List of devices attached
192.168.1.10:5555 device
```

---

## Running Screendroid

### macOS / Linux

```bash
chmod +x run.sh

./run.sh
```

### Windows

```bat
run.bat
```

Or directly:

```bash
python3 adb_proxy.py
```

---

## Open Screendroid

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

Do not open:

```text
remote_control.html
```

directly from disk.

The UI is served by the Flask application and relies on its API endpoints.

---

## How It Works

### Flask Backend

`adb_proxy.py`

Responsible for:

* Serving the web interface
* Device discovery
* Executing approved ADB commands
* Returning JSON responses

---

### Web Interface

`remote_control.html`

Provides:

* Remote control UI
* File transfer tools
* Keyboard shortcuts
* Device management tools
* Activity log

---

### Device Discovery

`/discover`

Scans the local network for Android devices exposing ADB on port 5555 and returns available hosts.

---

## Configuration

You can override the default host and port.

### macOS / Linux

```bash
export SCRD_HOST=0.0.0.0

export SCRD_PORT=5000
```

### Windows

```bat
set SCRD_HOST=0.0.0.0

set SCRD_PORT=5000
```

---

## Troubleshooting

### ADB Not Found

Verify installation:

```bash
adb version
```

---

### Device Not Detected

Verify:

```bash
adb devices
```

Ensure:

* USB Debugging is enabled
* Wireless Debugging is enabled
* Device and computer are on the same network

---

### Connection Refused

Restart ADB:

```bash
adb kill-server

adb start-server
```

Reconnect:

```bash
adb connect DEVICE_IP:5555
```

---

## License

Released under the MIT License.

---

## Disclaimer

Screendroid is intended for controlling devices that you own or are authorized to manage. The project simply provides a browser-based interface for ADB and does not bypass Android security mechanisms.
