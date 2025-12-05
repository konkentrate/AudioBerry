#!/bin/bash
set -e

SERVICE_DIR="/home/top/AudioBerry/serv_files"
SYSTEMD_DIR="/etc/systemd/system"

echo "Copying service files..."
for svc in "$SERVICE_DIR"/*.service; do
    echo " → Installing $(basename "$svc")"
    sudo cp "$svc" "$SYSTEMD_DIR"/
done

echo "Reloading systemd..."
sudo systemctl daemon-reload

echo "Enabling services..."
for svc in "$SERVICE_DIR"/*.service; do
    svc_name=$(basename "$svc")
    echo " → Enabling $svc_name"
    sudo systemctl enable "$svc_name"
done

echo "Done!"
