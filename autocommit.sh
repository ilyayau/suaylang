#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git rev-parse --is-inside-work-tree >/dev/null

while inotifywait -r -e modify,create,delete,move --exclude '\.git/' .; do
  if ! git diff --quiet || ! git diff --cached --quiet; then
    git add -A
    msg="auto: $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$msg" || true
    git push || true
  fi
done
