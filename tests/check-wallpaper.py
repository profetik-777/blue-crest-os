#!/usr/bin/env python3
"""Check persisted wallpaper choices across changing monitor sets."""
import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader("picker", str(ROOT / "files/system/usr/bin/wallpaper-picker"))
spec = importlib.util.spec_from_loader(loader.name, loader)
picker = importlib.util.module_from_spec(spec)
loader.exec_module(picker)
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    picker.STATE = root / "state.json"
    picker.SWAY_CONFIG = root / "wallpapers.conf"
    laptop = root / 'laptop "wallpaper".png'
    external = root / "external.png"
    laptop.touch()
    external.touch()
    with patch.object(picker, "outputs", return_value=[{"name": "eDP-1"}, {"name": "DP-2"}]), patch.object(picker, "ipc"):
        picker.apply("DP-2", external, "fit")
        picker.apply("eDP-1", laptop, "fill")
    rules = picker.commands(picker.read_state())
    assert rules[0] == picker.wallpaper_command("*", laptop, "fill")
    assert rules[-1].startswith('output "eDP-1"')
    assert picker.read_state()["DP-2"]["path"] == str(external)
    # Replacing the laptop with a new DP connector retains the wildcard fallback.
    with patch.object(picker, "outputs", return_value=[{"name": "DP-2"}, {"name": "DP-4"}]), patch.object(picker, "ipc"):
        picker.apply("*", external, "center")
    assert all(setting == {"path": str(external), "mode": "center"} for setting in picker.read_state().values())
    before = picker.STATE.read_text()
    with patch.object(picker, "outputs", return_value=[{"name": "DP-2"}]), patch.object(picker, "ipc", side_effect=RuntimeError("rejected")):
        try:
            picker.apply("DP-2", laptop, "fill")
        except RuntimeError:
            pass
        else:
            raise AssertionError("Rejected apply did not fail")
    assert picker.STATE.read_text() == before
print("PASS: wallpaper fallback, per-monitor preservation, all monitors, failed apply")
