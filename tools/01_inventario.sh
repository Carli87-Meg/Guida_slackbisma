#!/usr/bin/env bash
# Inventario dei video sorgente. Non tocca i file, legge solo i metadati.
# Uso: bash tools/01_inventario.sh [cartella_video]

set -euo pipefail
DIR="${1:-video}"

command -v ffprobe >/dev/null || { echo "ffprobe non trovato: installa ffmpeg"; exit 1; }

printf "%-42s %9s %12s %7s %10s\n" "FILE" "DURATA" "RISOLUZIONE" "FPS" "DIMENSIONE"
printf '%.0s-' {1..85}; echo

total=0
find "$DIR" -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' \
     -o -iname '*.avi' -o -iname '*.mkv' -o -iname '*.insv' \) | sort | while read -r f; do
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null || echo 0)
  res=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
        -of csv=s=x:p=0 "$f" 2>/dev/null | head -1)
  fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate \
        -of csv=p=0 "$f" 2>/dev/null | head -1 | awk -F/ '{if($2)printf "%.0f",$1/$2; else print $1}')
  size=$(du -h "$f" | cut -f1)
  mmss=$(printf '%d:%02d' $(echo "$dur/60" | bc) $(echo "$dur%60" | bc))
  printf "%-42s %9s %12s %7s %10s\n" "$(basename "$f")" "$mmss" "$res" "$fps" "$size"
done

echo
echo "Durata totale:"
find "$DIR" -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.mkv' \) \
  -exec ffprobe -v error -show_entries format=duration -of csv=p=0 {} \; \
  | awk '{s+=$1} END {printf "  %d min %d s su %d file\n", s/60, s%60, NR}'
