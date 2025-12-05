#!/usr/bin/env python3
import json
import time
from websocket import create_connection

CAMILLA_WS = "ws://127.0.0.1:1234"

# Path to ALSA status file for Raspotify output
RASPO_STATUS = "/proc/asound/card2/pcm0p/sub0/status"

# Config files
CONFIG_SPOTIFY = "/home/top/cdsp/configs/raspotify.yml"
CONFIG_UAC2    = "/home/top/cdsp/configs/uac2.yml"

CHECK_INTERVAL = 1  # seconds


def raspotify_playing():
    """Check if Raspotify's ALSA device is in RUNNING state."""
    try:
        with open(RASPO_STATUS, "r") as f:
            return "RUNNING" in f.read()
    except:
        return False


def get_current_config(ws):
    """Ask CamillaDSP which config is currently loaded."""
    ws.send(json.dumps("GetConfigFilePath"))
    reply = json.loads(ws.recv())
    return reply["GetConfigFilePath"]["value"]


def load_config(ws, path):
    """Load a new config and apply it."""
    ws.send(json.dumps({"SetConfigFilePath": path}))
    ws.recv()  # ignore response

    ws.send(json.dumps("Reload"))
    ws.recv()  # ignore response

    print(f"[CDSP] Switched to: {path}")


def main():
    print("CamillaDSP auto-switcher started…")

    ws = create_connection(CAMILLA_WS)

    while True:
        # Decide which config should be active
        should_be = CONFIG_SPOTIFY if raspotify_playing() else CONFIG_UAC2

        current = get_current_config(ws)

        if current != should_be:
            load_config(ws, should_be)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
