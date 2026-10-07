#!/usr/bin/env python3
"""Exercise first-login Yazi setup without downloads or a real Homebrew prefix."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "files/system"
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    home = root / "home"
    home.mkdir()
    prefix = root / "brew"
    (prefix / "bin").mkdir(parents=True)
    brew = prefix / "bin/brew"
    brew.write_text('#!/bin/sh\nexit "${TEST_BREW_STATUS:-0}"\n')
    brew.chmod(0o755)
    yazi = prefix / "bin/yazi"
    yazi.write_text('#!/bin/bash\nfor arg; do case "$arg" in --cwd-file=*) printf "%s\\0" "$TEST_CWD" > "${arg#--cwd-file=}";; esac; done\n')
    yazi.chmod(0o755)
    setup = root / "setup.sh"
    text = (SOURCE / "usr/bin/bluecrest-yazi-setup").read_text()
    text = text.replace("brew_prefix=/home/linuxbrew/.linuxbrew", f'brew_prefix="{prefix}"')
    text = text.replace("defaults=/usr/share/bluecrest", f'defaults="{SOURCE / "usr/share/bluecrest"}"')
    setup.write_text(text)
    env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(home / ".config"),
               XDG_STATE_HOME=str(home / ".local/state"), TEST_BREW_STATUS="1")
    assert subprocess.run(["bash", str(setup)], env=env, capture_output=True).returncode != 0
    marker = home / ".local/state/bluecrest/yazi-v1.complete"
    assert not marker.exists()
    env["TEST_BREW_STATUS"] = "0"
    subprocess.run(["bash", str(setup)], env=env, check=True, capture_output=True)
    assert marker.exists()
    keymap = home / ".config/yazi/keymap.toml"
    assert 'on = "t"' in keymap.read_text()
    keymap.write_text("# personal bindings\n")
    marker.unlink()
    subprocess.run(["bash", str(setup)], env=env, check=True, capture_output=True)
    assert keymap.read_text() == "# personal bindings\n"
    # A retry after completion must not invoke a now-failing installer.
    env["TEST_BREW_STATUS"] = "1"
    subprocess.run(["bash", str(setup)], env=env, check=True, capture_output=True)
    destination = home / 'folder with spaces'
    destination.mkdir()
    env.update(PATH=str(prefix / "bin") + ":" + os.environ["PATH"], TEST_CWD=str(destination))
    profile = SOURCE / "etc/profile.d/90-bluecrest-yazi.sh"
    result = subprocess.run(["bash", "--noprofile", "--norc", "-ic",
        'source "$1"; y; pwd', "test", str(profile)], env=env, capture_output=True, text=True, check=True)
    assert result.stdout.strip() == str(destination), result.stdout
print("PASS: setup retries, existing-keymap preservation, completion marker, shell directory handoff")
