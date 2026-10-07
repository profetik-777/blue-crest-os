# Blue Crest OS

A lightweight Sway desktop on **Universal Blue**, built with BlueBuild.

The base remains `ghcr.io/ublue-os/base-main`. Fedora's `sway-config-fedora`
and `sway-systemd` provide the session integration used by Fedora Sway.
This is a custom uBlue image, not a rebase to Fedora's Sway Atomic registry image.
Fedora is pinned to **44** so desktop packages and the selected COPR builds agree.

## Included software

- Sway, SDDM with its Sway greeter, Waybar, Rofi, Foot, Mako, Swaylock and Swayidle.
- nwg-displays and nwg-look for display and appearance controls.
- Audio/network controls, clipboard history, screenshots, media and brightness keys.
- PCManFM-Qt, LXQt Archiver, FileZilla, tmux, Kitty and Terminator retained.
- Podman, Distrobox, Homebrew, Geany (themes/addons), virt-manager and GNOME Boxes.
- Tailscale with `tailscaled.service` enabled. Authenticate with `sudo tailscale up`.
- System Flatpaks: Firefox, Bazaar, DistroShelf, Flatseal, Impression, Remmina,
  and Android Studio. These are provisioned after boot by BlueBuild's
  default-flatpaks service and need internet access on first installation.

LXQt's desktop session/panel and KWin are replaced. Its small PolicyKit agent
remains because Fedora's Sway configuration uses it for authentication dialogs.
The existing wallpaper and icon/theme packages are retained.

## First login

Select **Sway** in SDDM after updating from the old LXQt image. SDDM may remember
an old session. Existing user files are not overwritten.

- **Super + comma** or the **Settings** button: desktop settings menu.
- **Super + F1**: searchable shortcut guide.
- **Super + D**: app launcher; **Super + Enter**: native Foot terminal.
- **Super + Shift + Enter**: file manager.
- **Super + Shift + V**: clipboard history (text and images).
- **Super + Shift + X**: lock. Idle lock occurs after five minutes by default.
- **Print**, **Ctrl + Print**, **Alt + Print**: output, region, or window screenshot.

Clipboard history persists locally. Clear it with `cliphist wipe`; disable the
`wl-paste` lines in your override if you do not want clipboard history.
Kanshi is installed but not started automatically, to avoid competing with
nwg-displays. Choose one monitor management approach if adding docking profiles.

The Fedora background packages remain installed, but Blue Crest does not currently ship a dedicated wallpaper picker.
The theme editor changes GTK settings; retained Qt applications may require
separate Qt/Kvantum settings.

## Configuration

System conveniences live in `/etc/sway/config.d/99-bluecrest.conf`.
Fedora's layered-include mechanism lets you override a file by creating one with
the same name under `~/.config/sway/config.d/`.
The bar override is `90-bar.conf`. Supply `~/.config/waybar/config` or
`config.jsonc` to use your own bar; otherwise the image uses the small Blue Crest
bar in `/usr/share/bluecrest/`.

A pre-existing `~/.config/sway/config` takes precedence over Fedora's main config.
It must use Fedora's layered-include mechanism to pick up these snippets.
Back up custom configs before adapting them. No migration deletes user settings.

## Package sources

The desktop and original RPM apps use the base image/Fedora repositories.
Only `nwg-look` and `nwg-displays` come from `tofik/nwg-shell` COPR. The local repo definition uses
`includepkgs`, verifies RPM signatures, and is removed after the build.
That community repository cannot supply replacement Sway or wlroots packages.
Homebrew uses BlueBuild's brew module. Flatpaks use Flathub.

## Install or update

Wait for the image build to succeed before rebasing.
From an existing Fedora Atomic system, first install the image's trust policy:

```sh
sudo rpm-ostree rebase ostree-unverified-registry:ghcr.io/profetik-777/blue-crest-os:latest
systemctl reboot
```

Then select the signed image and reboot:

```sh
sudo rpm-ostree rebase ostree-image-signed:docker://ghcr.io/profetik-777/blue-crest-os:latest
systemctl reboot
```

Existing Blue Crest installations can use `sudo rpm-ostree upgrade` followed by
a reboot. The published `latest` image tag follows this recipe, currently Fedora
44; it does not imply tracking the base image's unpinned `latest` tag.

## Validation and recovery

The GitHub Actions build installs the packages and checks required desktop commands/session integration. Local helper checks:

```sh
python3 tests/check-desktop.py
```

A successful container build does not replace a hardware boot test. Verify login,
Wi-Fi, audio, suspend/lock, display scaling and browser screen sharing on the
actual laptop. The additional software increases disk usage; virtualization apps
do not start automatically.

If the desktop fails, select the previous deployment from the boot menu, or run
`sudo rpm-ostree rollback` from a working terminal and reboot.
