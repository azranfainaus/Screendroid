# Screendroid

**Remote‑control Android TVs, projectors, and other Android devices from any web browser**

## Overview
Screendroid is a lightweight web UI that talks to a Flask proxy which, in turn, runs ADB commands on the host machine.  It lets you:
* Navigate (DPAD, Home, Back, Menu, OK)
* Control volume and media playback
* Upload / download files to `/sdcard/Download/`
* Capture screenshots
* Launch and force‑close apps
* View storage, battery and OS version information

All actions are sent over HTTP to `http://<host>:<port>/adb` and the proxy validates the command against an **allow‑list** before executing it.

## Quick‑Start (Linux/macOS)
```bash
# 1️⃣ Clone the repo
git clone https://github.com/azranfainaus/Screendroid.git
cd Screendroid

# 2️⃣ Create a virtual environment and install Flask
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3️⃣ Run the starter script (it launches the Flask proxy and a static HTTP server)
chmod +x run.sh
./run.sh
```
The UI will be available at **`http://localhost:8000/`**.  Open it in a browser and:
* Click **Detect Projector** – the backend scans the local network for devices listening on ADB port 5555 and automatically fills the address.
* Press **Connect** – the UI stores the address in `localStorage` and runs `adb connect <IP>:5555`.
* Use the navigation and media buttons to control the device.

## Quick‑Start (Windows) – using `run.bat`
```bat
rem 1️⃣ Clone the repo (Git Bash or PowerShell)
git clone https://github.com/azranfainaus/Screendroid.git
cd Screendroid

rem 2️⃣ Create a virtual environment and install Flask
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

rem 3️⃣ Run the starter batch file
run.bat
```
The UI opens at **`http://localhost:8000/`**.

## How it works
* **Flask proxy (`adb_proxy.py`)** – receives JSON `{"command": "adb …"}`, checks it against `ALLOWED`, runs it via `subprocess.run`, and returns a JSON response `{success: bool, output: str}`.
* **Discovery endpoint (`/discover`)** – runs `discover_projector.sh` (Linux/macOS) or `discover_projector.bat` (Windows) to scan the local /24 subnet for hosts with TCP port 5555 open.  Returns `{"hosts": ["192.168.1.15", …]}`.
* **Web UI (`remote_control.html`)** – a single HTML file with CSS, JavaScript and a textarea log.  It stores the projector IP in `localStorage` so you only need to detect it once.
* **Starter scripts** – `run.sh` (POSIX) and `run.bat` (Windows) launch the Flask proxy in the background and serve the UI via Python's built‑in HTTP server on port 8000.

## Configuration
You can change the host and port the Flask server binds to by setting environment variables before running the scripts:
```bash
export SCRD_HOST=0.0.0.0   # listen on all interfaces
export SCRD_PORT=5000
./run.sh
```
On Windows set them in the command prompt:
```bat
set SCRD_HOST=0.0.0.0
set SCRD_PORT=5000
run.bat
```

## License
This project is licensed under the MIT License – see the `LICENSE` file.
