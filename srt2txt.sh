#!/usr/bin/env bash
# Convert every *.en-orig.srt in this directory into a plain-text article:
# no sequence numbers, no timestamps, consecutive duplicate lines removed,
# text joined into one continuous paragraph.
set -euo pipefail

shopt -s nullglob
files=( *.en-orig.srt )
if (( ${#files[@]} == 0 )); then
  echo "No *.en-orig.srt files found in $(pwd)" >&2
  exit 1
fi

for in in "${files[@]}"; do
  out="${in%.srt}.txt"
  awk '
    /^[0-9]+$/  { next }            # sequence-number lines
    /--> /      { next }            # timestamp lines
    {
      gsub(/^[[:space:]]+/, ""); gsub(/[[:space:]]+$/, "")
      if ($0 == "") next
      if ($0 == prev) next          # drop consecutive duplicate lines
      prev = $0
      print
    }
  ' "$in" | tr '\n' ' ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//' > "$out"
  printf 'Wrote: %s\n' "$out"
done
