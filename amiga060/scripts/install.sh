#!/bin/sh
set -eu
root=${AMIGA060_FAT_ROOT:-/media/fat}
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
for path in Minimig_Hybrid Amiga060_Testing _Computer/Amiga_060_Testing.rbf; do
 if [ -e "$root/$path" ] || [ -L "$root/$path" ]; then echo "Refusing to overwrite $root/$path" >&2; exit 1; fi
done
test -f "$root/MiSTer"
mkdir -p "$root/_Computer"
cp -R payload/Minimig_Hybrid "$root/Minimig_Hybrid"
cp -R payload/Amiga060_Testing "$root/Amiga060_Testing"
cp payload/_Computer/Amiga_060_Testing.rbf "$root/_Computer/Amiga_060_Testing.rbf"
sync
echo 'Installed separate experimental core. Normal Main has not been changed. Read README before activation.'
