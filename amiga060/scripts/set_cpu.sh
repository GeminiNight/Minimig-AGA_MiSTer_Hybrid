#!/bin/sh
set -eu
case "${1:-}" in
020|030|040|060) cpu=m68${1};;
*) echo 'Usage: set_cpu.sh 020|030|040|060' >&2; exit 1;;
esac
root=${AMIGA060_FAT_ROOT:-/media/fat}
test -d "$root/Minimig_Hybrid"
printf '%s\n' "$cpu" > "$root/Minimig_Hybrid/cpu_model.new"
mv "$root/Minimig_Hybrid/cpu_model.new" "$root/Minimig_Hybrid/cpu_model"
echo "Selected $cpu for the next launch. Return to the MiSTer menu, then reload the experimental core. Do not change CPU during a running session."
