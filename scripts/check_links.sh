#!/bin/sh
set -e
# Check all internal markdown links (README, docs/, results/, paper/)
find . -type f \( -name '*.md' -o -name '*.MD' \) | while read f; do
  grep -oE '\[[^\]]+\]\(([^)]+)\)' "$f" | while read link; do
    target=$(echo "$link" | sed -E 's/.*\(([^)]+)\).*/\1/')
    # Only check local (non-http) links
    case "$target" in
      http*) continue;;
      *)
        # Remove anchors/fragments
        file="${target%%#*}"
        # If relative, resolve from $f's dir
        if [ -n "$file" ] && [ ! -f "$(dirname "$f")/$file" ] && [ ! -f "$file" ]; then
          echo "Broken link: $f -> $target"
          exit 1
        fi
      ;;
    esac
  done
done
