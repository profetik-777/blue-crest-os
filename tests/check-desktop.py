#!/usr/bin/env python3
"""Check Blue Crest desktop helper syntax and static configuration."""
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

print("PASS: shell syntax, bar JSON, and removed-tool references")
