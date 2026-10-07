#!/usr/bin/env python3
"""Check helper control flow without touching the host desktop or power state."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / 'files/system/usr/bin'
for p in list(BIN.glob('bluecrest-*')) + list((ROOT / 'files/scripts').glob('*.sh')):
    subprocess.run(['bash', '-n', str(p)], check=True)
json.loads((ROOT / 'files/system/usr/share/bluecrest/waybar.json').read_text())
with tempfile.TemporaryDirectory() as tmp:
    temp = Path(tmp)
    mocks = temp / 'bin'
    mocks.mkdir()
    log = temp / 'calls'
    env = dict(os.environ, PATH=f'{mocks}:{os.environ["PATH"]}',
               XDG_CONFIG_HOME=str(temp / 'config'), CALL_LOG=str(log))
    rofi = mocks / 'rofi'
    rofi.write_text('#!/bin/sh\ncat >/dev/null\nprintf "%s\\n" "$CHOICE"\n')
    rofi.chmod(0o755)
    for name in ['waypaper', 'nwg-displays', 'nwg-look', 'pavucontrol',
                 'nm-connection-editor', 'pcmanfm-qt', 'loginctl',
                 'swaylock', 'systemctl', 'swaymsg', 'waybar']:
        p = mocks / name
        p.write_text('#!/bin/sh\nprintf "%s" "${0##*/}" >> "$CALL_LOG"\n'
                     'printf " <%s>" "$@" >> "$CALL_LOG"\nprintf "\\n" >> "$CALL_LOG"\n')
        p.chmod(0o755)
    def run(helper, choice=''):
        log.write_text('')
        subprocess.run([str(BIN / helper)], env=dict(env, CHOICE=choice), check=True)
        return log.read_text()
    assert run('bluecrest-settings', 'Wallpaper') == 'waypaper <--backend> <swaybg>\n'
    assert run('bluecrest-settings', 'Displays') == 'nwg-displays <>\n'
    assert run('bluecrest-settings', 'Lock') == 'loginctl <lock-session>\n'
    assert run('bluecrest-settings', '') == ''
    # Second prompt returns the initial choice, not Confirm: no power action.
    for choice in ['Restart', 'Shut down', 'Log out']:
        assert run('bluecrest-settings', choice) == ''
    assert run('bluecrest-settings', 'Suspend').splitlines() == ['swaylock <-f>', 'systemctl <suspend>']
    assert run('bluecrest-wallpaper') == ''
    cfg = temp / 'config/waypaper/config.ini'
    cfg.parent.mkdir(parents=True)
    cfg.touch()
    assert run('bluecrest-wallpaper') == 'waypaper <--restore> <--backend> <swaybg>\n'
    assert '/usr/share/bluecrest/waybar.json' in run('bluecrest-waybar')
    bar = temp / 'config/waybar/config.jsonc'
    bar.parent.mkdir(parents=True)
    bar.write_text('{}')
    assert run('bluecrest-waybar') == 'waybar <>\n'
print('PASS: shell syntax, bar JSON, settings actions, cancelled power actions, wallpaper restore and bar overrides')
