# Reproduction

1. Preparation
Add `dtoverlay=dwc2` inside /boot/firmware/config.txt and ``
Create /etc/modules-load.d/aloop.conf with `snd-aloop` to create mix-sink for Raspotify and UAC2
    - Install Raspotify `sudo apt-get -y install curl && curl -sL https://dtcooper.github.io/raspotify/install.sh | sh`
    - Edit /etc/raspotify/conf `LIBRESPOT_BACKEND=alsa` and `LIBRESPOT_DEVICE=hw:Loopback,0,0` or mix-sink name
    - nano /etc/modprobe.d/aloop.conf `options snd-aloop pcm_devs=1 pcm_substreams=1 enable=1 index=2`

### How to handle the sudden pops on pauses

```
amixer -c 0 set 'Auto Mute' off
amixer -c 0 set 'Auto Mute Mono' off
```

```
# example 2
pcm.mixer {
    type dmix
    ipc_key 1939 # must be unique
    slave { pcm "hw:2" }
}

pcm.!default mixer
```




pcm.loopback {
    type hw
    card 2
    device 0
    subdevice 0
}

pcm.dmixer {
    type dmix
    ipc_key 2048
    ipc_perm 0666
    slave {
        pcm "loopback"     # loopback playback device
        rate 44100
        format S32_LE
        channels 2
        period_time 0
        period_size 1024
        buffer_size 4096
    }
}

ctl.dmixer {
    type hw
    card 2
}

pcm.!default {
    type plug
    slave.pcm "dmixer"
}

/etc/modprobe.d/loopback.conf
options snd-aloop enable=1 pcm_substreams=1

pcm.!default {
    type hw
    card Loopback
    device 0
    subdevice 0
}

ctl.!default {
    type hw
    card Loopback
}