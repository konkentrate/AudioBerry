#!/usr/bin/env python3
import json
import time
from websocket import create_connection

# --- CONFIG ---
CAMILLA_WS = "ws://127.0.0.1:1234"

RASPOTIFY_STATUS = "/proc/asound/card2/pcm0p/sub0/status"  # Replace if needed
CONFIG_SPOTIFY = "/home/top/AudioBerry/cdsp/configs/raspotify.yml"
CONFIG_UAC2 = "/home/top/AudioBerry/cdsp/configs/uac2.yml"

CHECK_INTERVAL = 1  # seconds


def raspotify_active():
    """Return True if Raspotify (or whatever is using this PCM) is streaming audio."""
    try:
        with open(RASPOTIFY_STATUS, "r") as f:
            return "RUNNING" in f.read()
    except FileNotFoundError:
        return False


def load_config(path):
    """Set config file path, then reload CamillaDSP."""
    ws = create_connection(CAMILLA_WS)

    ws.send(json.dumps({"SetConfigFilePath": path}))
    reply1 = ws.recv()

    ws.send(json.dumps({"Reload": None}))
    reply2 = ws.recv()

    ws.close()

    print(f"[CDSP] Loaded config: {path}")
    print("Reply1:", reply1)
    print("Reply2:", reply2)


def get_current_path():
    """Read which config file is currently active."""
    ws = create_connection(CAMILLA_WS)
    ws.send(json.dumps("GetConfigFilePath"))
    reply = json.loads(ws.recv())
    ws.close()
    return reply["GetConfigFilePath"]


def main():
    print("CamillaDSP simple auto-switch started…")

    while True:
        # NEW LOGIC: Spotify first, UAC2 fallback
        if raspotify_active():
            target = CONFIG_SPOTIFY
        else:
            target = CONFIG_UAC2

        current = get_current_path()

        if current != target:
            load_config(target)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
