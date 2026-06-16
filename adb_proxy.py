from flask import Flask, request, jsonify, send_file
import os, subprocess

app = Flask(__name__)

# Allowed commands
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


@app.route("/")
def index():
    return send_file("remote_control.html")


@app.route("/discover")
def discover():
    """Scan the local network for devices with ADB port 5555 open.
    Returns JSON: {"hosts": ["192.168.1.15", ...]}
    The helper script is OS‑specific and placed in the repo.
    """
    script = "discover_projector.sh" if os.name != "nt" else "discover_projector.bat"
    if not os.path.exists(script):
        return jsonify({"hosts": []})
    try:
        result = subprocess.run(
            ["bash", "-c", f"./{script}"],
            shell=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        hosts = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return jsonify({"hosts": hosts})
    except Exception as e:
        return jsonify({"hosts": [], "error": str(e)}), 500


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
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600
        )

        output = (
            (result.stdout or "") +
            (result.stderr or "")
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


if __name__ == "__main__":
    # Bind to configurable host/port via environment variables (default localhost:5000)
    host = os.getenv('SCRD_HOST', '127.0.0.1')
    port = int(os.getenv('SCRD_PORT', '5000'))
    print("=" * 50)
    print("Screendroid Server")
    print("=" * 50)
    print(f"Web UI : http://{host}:{port}")
    print(f"API    : http://{host}:{port}/adb")
    print("=" * 50)
    app.run(host=host, port=port, debug=False)
