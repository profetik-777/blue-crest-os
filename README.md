# Blue Crest OS

**Blue Crest OS** is an opinionated Sway experience with user-friendly keybindings, practical desktop tools, and sensible defaults. Built on Universal Blue with BlueBuild, it pairs a lightweight Wayland tiling desktop with approachable keyboard shortcuts and touchpad gestures.

**Where we're headed:** Future releases will focus on making tiling window managers easier to approach, especially for people trying one for the first time. The goal is to keep Sway's speed and flexibility while improving onboarding, discoverability, sensible defaults, and everyday desktop conveniences. It is a work in progress rather than a finished beginner-friendly distribution.

All work is done w/ the help of AI tools. 

The base remains `ghcr.io/ublue-os/base-main`. Fedora's `sway-config-fedora`
and `sway-systemd` provide the session integration used by Fedora Sway.
This is a custom uBlue image, not a rebase to Fedora's Sway Atomic registry image.
Fedora is pinned to **44** so desktop packages and the selected COPR builds agree.

## Included software

- Sway, SDDM with its Sway greeter, Waybar, Rofi, Foot, Mako, Swaylock and Swayidle.
- nwg-displays and nwg-look for display and appearance controls.
- Audio/network controls, clipboard history, screenshots, media and brightness keys.
- PCManFM-Qt, LXQt Archiver, FileZilla, tmux, Kitty and Terminator retained.
- Yazi via Homebrew after first Sway login, with Bash integration and terminal-oriented keys.
- Podman, Distrobox, Homebrew, Geany (themes/addons), virt-manager and GNOME Boxes.
- Tailscale with `tailscaled.service` enabled. Authenticate with `sudo tailscale up`.
- System Flatpaks: Firefox, Bazaar, DistroShelf, Flatseal, Impression, Remmina,
  ksnip, and Android Studio. These are provisioned after boot by BlueBuild's
  default-flatpaks service and need internet access on first installation.

LXQt's desktop session/panel and KWin are replaced. Its small PolicyKit agent
remains because Fedora's Sway configuration uses it for authentication dialogs.
The existing wallpaper and icon/theme packages are retained.

## First login

Select **Sway** in SDDM after updating from the old LXQt image. SDDM may remember
an old session. Existing user files are not overwritten.

- **Super + comma** or the **Settings** button: desktop settings menu.
- **Super + F1**: searchable shortcut guide.
- **Ctrl + Space**: app launcher; **Super + Enter**: native Foot terminal.
- **Super + Shift + Enter**: file manager.
- **Super + Q**: close the focused window.
- **Four-finger swipe left/right**: previous/next workspace on the current monitor.
- Workspaces **1, 2, 3** stay visible in the bar; Foot defaults to **12-point** text.
- The bar clock uses **12-hour time with AM/PM**.
- **Super + Shift + V**: clipboard history (text and images).
- **Super + Shift + X**: lock. Idle lock occurs after five minutes by default.
- **Print** or **Ctrl + Print**: select an area and open it in ksnip to annotate.
- **Shift + Print**: current monitor screenshot; **Alt + Print**: active window.
- Area captures are saved in `~/Pictures/Screenshots`; **Escape** cancels selection.

Clipboard history persists locally. Clear it with `cliphist wipe`; disable the
`wl-paste` lines in your override if you do not want clipboard history.
Kanshi is installed but not started automatically, to avoid competing with
nwg-displays. Choose one monitor management approach if adding docking profiles.

Search **wallpaper** or **backgrounds** in the app launcher to open the terminal
wallpaper picker. Choose **All monitors** or a specific monitor, then an image.
It starts in `~/Pictures/Wallpapers`; `/` filters names, `p` accepts a path, and
`m` cycles scaling modes. Selections persist in user-owned Sway snippets.
Selecting a laptop wallpaper also supplies a fallback to newly connected screens;
explicit monitor choices take precedence. No personal images, monitor positions,
or sleep/graphics workarounds are shipped.
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

## Yazi first-login setup

Thirty seconds after Sway login, a user service installs the bundled Brewfile.
Internet access and the primary user's Homebrew prefix are required. Failed setup
retries every five minutes while the session is running; the completion marker is
written only after installation succeeds. The Brew module owns its prefix for UID
1000, so this provisioning is intended for that primary user.

Open a new Foot terminal and run `y`. Browse with arrow keys and press **t** or
**q** to return to the same shell in that folder. **Shift+Q** keeps the original
folder. **Ctrl+T** creates a new Yazi tab, replacing the default `t t` sequence.

Setup copies the keymap only if `~/.config/yazi/keymap.toml` does not exist.
Existing keymaps and Bash functions are preserved. To adopt the keys manually,
merge the entries from `/usr/share/bluecrest/yazi/keymap.toml` into your keymap.
The Bash wrapper is supplied by `/etc/profile.d/90-bluecrest-yazi.sh`.

Check or retry setup:
```sh
systemctl --user status bluecrest-yazi-setup.service
journalctl --user -u bluecrest-yazi-setup.service
systemctl --user start bluecrest-yazi-setup.service
```

The service runs provisioning only; Brew's update timers manage subsequent app
updates independently of OS image updates. This is a small login service, not a
new graphical onboarding portal.
