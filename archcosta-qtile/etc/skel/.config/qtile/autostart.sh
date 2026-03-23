#!/bin/bash
# Autostart script for Qtile

# Set wallpaper
nitrogen --restore &

# Start compositor
picom -f &

# Network manager
nm-applet &

# Power manager
xfce4-power-manager &

# Volume
volumeicon &

# Polkit agent
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# Notification daemon
dunst &

# Desktop entry autostart
dex --autostart --environment qtile &
