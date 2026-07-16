#!/bin/bash
# ------------------------------------------------------------
# Renames every photo in this folder to photo1.jpg, photo2.jpg, ...
# in the order your camera numbered them (DSCF0022, DSCF0023, ...).
# This is the exact naming the gallery page looks for.
#
# HOW TO USE:
# 1. Save this file as rename_photos.sh inside the SAME folder as
#    your DSCF____.JPG photos, that's campsite/images/gallery/.
# 2. Open Terminal and run:
#      cd path/to/images/gallery
#      bash rename_photos.sh
# 3. Check the output, it prints every rename it makes.
#
# Safe to run more than once, it only touches .jpg/.jpeg/.png files
# and never overwrites anything mid-rename (two-pass, via temp names).
# ------------------------------------------------------------

cd "$(dirname "$0")"

shopt -s nullglob nocaseglob
files=(*.jpg *.jpeg *.png)
shopt -u nocaseglob

# sort in the same order your camera numbered them
IFS=$'\n' files=($(printf '%s\n' "${files[@]}" | sort -V))
unset IFS

if [ ${#files[@]} -eq 0 ]; then
  echo "No .jpg, .jpeg, or .png files found in this folder."
  echo "Make sure this script is sitting in the same folder as your photos."
  exit 0
fi

echo "Found ${#files[@]} photos. Renaming..."
echo ""

# Pass 1: move everything to safe temporary names first,
# so nothing ever gets overwritten partway through.
i=1
tempnames=()
for f in "${files[@]}"; do
  tmp="__tmp_photo_${i}.tmp"
  mv "$f" "$tmp"
  tempnames+=("$tmp")
  i=$((i+1))
done

# Pass 2: rename temp files to their final photoN.jpg names.
i=1
for tmp in "${tempnames[@]}"; do
  orig="${files[$((i-1))]}"
  ext="${orig##*.}"
  ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  if [ "$ext_lower" = "jpeg" ]; then ext_lower="jpg"; fi
  final="photo${i}.${ext_lower}"
  mv "$tmp" "$final"
  echo "  $orig  ->  $final"
  i=$((i+1))
done

echo ""
echo "Done! Renamed $((i-1)) photos."
