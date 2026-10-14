#!/bin/sh
set -eu
root=${AMIGA060_FAT_ROOT:-/media/fat}
backup="$root/Amiga060_Testing/original-main"
test -f "$root/MiSTer"
test -f "$root/Amiga060_Testing/Hybrid_Main"
# Refuse repeat activation: never replace an existing backup, even after restoration.
mkdir "$backup"
cp "$root/MiSTer" "$backup/MiSTer"
cmp "$root/MiSTer" "$backup/MiSTer"
(cd "$backup" && sha256sum MiSTer > SHA256SUMS)
sync
cp "$root/Amiga060_Testing/Hybrid_Main" "$root/MiSTer.amiga060.new"
cmp "$root/Amiga060_Testing/Hybrid_Main" "$root/MiSTer.amiga060.new"
chmod +x "$root/MiSTer.amiga060.new"
mv "$root/MiSTer.amiga060.new" "$root/MiSTer"
sync
echo 'Hybrid Main activated. Reboot MiSTer. Backup retained permanently in Amiga060_Testing/original-main.'
