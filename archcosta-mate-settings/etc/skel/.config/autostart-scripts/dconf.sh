#!/bin/sh
dconf load / < ~/.config/archcosta-dconf.ini
rm -rf ~/.config/archcosta-dconf.ini &
rm -rf ~/.config/autostart-scripts/dconf.sh &
 
 notify-send "MATE settings applied! 🔥"
 
