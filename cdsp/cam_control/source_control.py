#!/usr/bin/env python3
import json
import time
from websocket import create_connection

CAMILLA_WS = "ws://127.0.0.1:1234"

# ALSA status for Raspotify
RASPO_STATUS = "/proc/asound/card1/pcm0p/sub0/status"

# Configs
CONFIG_SPOTIFY = "/home/top/cdsp/configs/raspotify.yml"
CONFIG_UAC2    = "/home/top/cdsp/configs/uac2.yml"

CHECK_INTERVAL = 1  # seconds


def raspotify_playing():
    """Check if Raspotify's ALSA device is RUNNING."""
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


def set_gain_0db(ws):
    """Set CamillaDSP gain to 0 dB (DSP volume = 0)."""
    ws.send(json.dumps({"SetVolume": 0}))
    resp = ws.recv()
    print("[CDSP] Set gain: 0 dB   → reply:", resp)


def load_config(ws, path):
    """Load and apply a new CamillaDSP config."""
    ws.send(json.dumps({"SetConfigFilePath": path}))
    ws.recv()  # ignore response

    ws.send(json.dumps("Reload"))
    ws.recv()  # ignore response

    print(f"[CDSP] Switched to: {path}")


def main():
    print("CamillaDSP auto-switcher started…")

    ws = create_connection(CAMILLA_WS)

    while True:
        # NEW logic: Spotify has priority
        spotify_active = raspotify_playing()
        should_be = CONFIG_SPOTIFY if spotify_active else CONFIG_UAC2

        current = get_current_config(ws)

        # Switch config if needed
        if current != should_be:
            load_config(ws, should_be)

            # Extra action: force gain to 0 dB only for Spotify
            if spotify_active:
                set_gain_0db(ws)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
