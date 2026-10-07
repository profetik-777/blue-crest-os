#!/usr/bin/env python3
"""Check Blue Crest desktop helper syntax and static configuration."""
import ast
import configparser
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "files/system/usr/bin"
SCRIPTS = ROOT / "files/scripts"

for p in list(BIN.glob("bluecrest-*")) + list(SCRIPTS.glob("*.sh")):
    subprocess.run(["bash", "-n", str(p)], check=True)

json.loads((ROOT / "files/system/usr/share/bluecrest/waybar.json").read_text())

settings = (BIN / "bluecrest-settings").read_text()
sway = (ROOT / "files/system/etc/sway/config.d/99-bluecrest.conf").read_text()

assert "waypaper" not in settings.lower()
assert "herdr" not in settings.lower()
assert "waypaper" not in sway.lower()
assert "bluecrest-wallpaper" not in sway.lower()

picker = BIN / "wallpaper-picker"
ast.parse(picker.read_text())
desktop = configparser.ConfigParser(interpolation=None)
desktop.read(ROOT / "files/system/usr/share/applications/wallpaper-picker.desktop")
assert "/usr/bin/wallpaper-picker" in desktop["Desktop Entry"]["Exec"]
assert "/var/home/" not in desktop["Desktop Entry"]["Exec"]
subprocess.run(["python3", str(ROOT / "tests/check-wallpaper.py")], check=True)
print("PASS: shell syntax, bar JSON, wallpaper controls, and removed-tool references")
