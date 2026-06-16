from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

# ============================================================
# Allowed Commands
# ============================================================

ALLOWED = [
    "adb shell input keyevent",
    "adb shell df -h",
    "adb shell dumpsys battery",
    "adb shell screencap",
    "adb pull",
    "adb push",
    "adb shell ls /sdcard/Download/",
    "adb connect",
    "adb disconnect",
    "adb devices",
    "adb shell pm list packages",
    "adb shell monkey -p",
    "adb shell am force-stop",
    "adb shell getprop ro.build.version.release",
]


def is_allowed(command: str):
    return any(command.startswith(prefix) for prefix in ALLOWED)


# ============================================================
# Web UI
# ============================================================

@app.route("/")
def index():
    return send_file("remote_control.html")


# ============================================================
# Device Discovery
# ============================================================

@app.route("/discover")
def discover():

    script = (
        "discover_projector.bat"
        if os.name == "nt"
        else "discover_projector.sh"
    )

    if not os.path.exists(script):
        return jsonify({
            "hosts": [],
            "error": f"{script} not found"
        })

    try:

        if os.name == "nt":

            result = subprocess.run(
                [script],
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )

        else:

            result = subprocess.run(
                ["bash", script],
                capture_output=True,
                text=True,
                timeout=60
            )

        hosts = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        return jsonify({
            "hosts": hosts
        })

    except Exception as e:

        return jsonify({
            "hosts": [],
            "error": str(e)
        }), 500


# ============================================================
# ADB Command Endpoint
# ============================================================

@app.route("/adb", methods=["POST"])
def run_adb():

    data = request.get_json(silent=True) or {}

    command = data.get("command", "").strip()

    if not command:

        return jsonify({
            "success": False,
            "output": "No command provided"
        }), 400

    if not is_allowed(command):

        return jsonify({
            "success": False,
            "output": f"Command not allowed: {command}"
        }), 403

    print(f"[ADB] {command}")

    try:

        timeout = 30

        if (
            command.startswith("adb push")
            or command.startswith("adb pull")
        ):
            timeout = 3600

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = (
            (result.stdout or "")
            + (result.stderr or "")
        ).strip()

        if not output:
            output = "(no output)"

        return jsonify({
            "success": True,
            "output": output
        })

    except subprocess.TimeoutExpired:

        return jsonify({
            "success": False,
            "output": "Command timed out"
        }), 504

    except Exception as e:

        return jsonify({
            "success": False,
            "output": str(e)
        }), 500


# ============================================================
# Startup
# ============================================================

if __name__ == "__main__":

    host = os.getenv("SCRD_HOST", "127.0.0.1")
    port = int(os.getenv("SCRD_PORT", "5000"))

    print("=" * 50)
    print(" Screendroid Server")
    print("=" * 50)
    print(f" Web UI : http://{host}:{port}")
    print(f" API    : http://{host}:{port}/adb")
    print(f" Scan   : http://{host}:{port}/discover")
    print("=" * 50)

    app.run(
        host=host,
        port=port,
        debug=False
    )
