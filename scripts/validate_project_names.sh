#!/usr/bin/env bash
set -uo pipefail

# Allow override via environment for testing
projects_dir="${PROJECTS_DIR:-vault/02-projects}"
ok=0
warn=0

shopt -s nullglob
for d in "$projects_dir"/*/ ; do
  name=$(basename "$d")
  if [[ "$name" =~ ^[0-9]{2}-[a-z0-9-]+$ ]]; then
    echo "✅ $name"
    ((ok++))
  else
    # Allow known legacy stub
    if [[ "$name" == "pkm-system" ]]; then
      echo "ℹ️  $name (legacy stub; merged into 01-pkm-system-meta)"
      ((ok++))
    else
      echo "⚠️  $name does not match NN-kebab-slug"
      ((warn++))
    fi
  fi
done

echo "\nSummary: $ok OK, $warn warnings"
if [[ $warn -gt 0 ]]; then exit 1; else exit 0; fi
