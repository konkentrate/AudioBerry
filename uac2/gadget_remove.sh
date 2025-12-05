#!/bin/sh
# remove_gadget.sh
# Safely removes the UAC2 gadget named uac2_audio

G=/sys/kernel/config/usb_gadget/uac2_audio

# Check if gadget exists
if [ ! -d "$G" ]; then
    echo "Gadget uac2_audio not found. Nothing to remove."
    exit 0
fi

echo "Disabling gadget..."
# Unbind the gadget
echo "" > $G/UDC 2>/dev/null

echo "Removing function links..."
# Remove symlinks to functions
rm -f $G/configs/c.1/uac2.usb0 2>/dev/null

echo "Removing functions..."
# Remove UAC2 function
rmdir $G/functions/uac2.usb0 2>/dev/null

echo "Removing configuration strings..."
# Remove config strings
rmdir $G/configs/c.1/strings/0x409 2>/dev/null

echo "Removing configuration..."
rmdir $G/configs/c.1 2>/dev/null

echo "Removing gadget strings..."
# Remove device strings
rmdir $G/strings/0x409 2>/dev/null

echo "Removing gadget directory..."
rmdir $G 2>/dev/null

echo "Gadget uac2_audio removed successfully."
