#!/bin/bash
XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
# Allow users to override command-line flags
if [[ -f "$XDG_CONFIG_HOME/brave-flags.conf" ]]; then
   mapfile -t BRAVE_FLAGS < "$XDG_CONFIG_HOME/brave-flags.conf"
fi
exec /opt/brave-bin/brave "${BRAVE_FLAGS[@]}" "$@"
