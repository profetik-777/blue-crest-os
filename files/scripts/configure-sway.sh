#!/usr/bin/env bash
set -euo pipefail
# Do not silently publish an image missing session integration.
test -f /usr/share/wayland-sessions/sway.desktop
test -f /usr/libexec/sway/layered-include
grep -q layered-include /etc/sway/config
for cmd in sway waybar rofi nwg-displays nwg-look cliphist grimshot grim slurp flatpak xdg-user-dir; do
    command -v "$cmd"
done
chmod 0755 /usr/bin/bluecrest-* /usr/bin/wallpaper-picker
python3 -c 'import curses'
foot --check-config --config /etc/xdg/foot/foot.ini
# SDDM remembers an existing user's previous session; select Sway at login.
systemctl set-default graphical.target

bash -n /etc/profile.d/90-bluecrest-yazi.sh

bash -n /usr/bin/bluecrest-screenshot
