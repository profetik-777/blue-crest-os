#!/usr/bin/env bash
set -euo pipefail
# Pinned official release; update version and checksum together.
version=v0.9.3
case "$(uname -m)" in
    x86_64) checksum=18a8dc65f1c2fa485884344356dea1cfd911c6f06cf46fa78e193f4087f4dba7 ;;
    aarch64) checksum=4de7aa3e25678812e92960de64f7c2aaa1bca1f0f80a3c5e559837e231e1f5c0 ;;
    *) echo 'Unsupported Herdr architecture' >&2; exit 1 ;;
esac
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
curl --fail --location --retry 3 "https://github.com/herdrdev/herdr/releases/download/${version}/herdr-linux-$(uname -m)" -o "$tmp/herdr"
printf '%s  %s\n' "$checksum" "$tmp/herdr" | sha256sum --check --strict
install -Dm755 "$tmp/herdr" /usr/bin/herdr
