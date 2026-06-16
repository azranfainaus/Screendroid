#!/usr/bin/env bash
# Screendroid starter script – runs the Flask proxy (which also serves the UI).
# Works on Linux/macOS. For Windows, use run.bat.

set -e

# Activate virtual environment if it exists
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
fi

# Run the Flask app (host/port can be overridden with SCRD_HOST/ SCRD_PORT env vars)
python3 adb_proxy.py
