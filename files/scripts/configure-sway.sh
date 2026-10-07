#!/usr/bin/env bash
set -euo pipefail
# Do not silently publish an image missing session integration.
test -f /usr/share/wayland-sessions/sway.desktop
test -f /usr/libexec/sway/layered-include
grep -q layered-include /etc/sway/config
for cmd in sway waybar rofi waypaper nwg-displays nwg-look cliphist grimshot herdr; do
    command -v "$cmd"
done
chmod 0755 /usr/bin/bluecrest-*
# SDDM remembers an existing user's previous session; select Sway at login.
systemctl set-default graphical.target
