#!/bin/sh
set -eu
root=${AMIGA060_FAT_ROOT:-/media/fat}
backup="$root/Amiga060_Testing/original-main"
(cd "$backup" && sha256sum -c SHA256SUMS)
cp "$backup/MiSTer" "$root/MiSTer.amiga060.restore"
cmp "$backup/MiSTer" "$root/MiSTer.amiga060.restore"
chmod +x "$root/MiSTer.amiga060.restore"
mv "$root/MiSTer.amiga060.restore" "$root/MiSTer"
sync
echo 'Original Main restored; backup retained. Reboot MiSTer.'
