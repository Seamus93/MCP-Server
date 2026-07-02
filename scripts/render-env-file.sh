#!/usr/bin/env bash
set -euo pipefail

TEMPLATE_FILE="${1:-.env.example}"
OUTPUT_FILE="${2:-.env}"

if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "Template file not found: $TEMPLATE_FILE"
  exit 1
fi

: > "$OUTPUT_FILE"

while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in
    ''|'#'*)
      printf '%s\n' "$line" >> "$OUTPUT_FILE"
      continue
      ;;
  esac

  key="${line%%=*}"
  default_value="${line#*=}"

  if [ -n "${!key+x}" ]; then
    value="${!key}"
  else
    value="$default_value"
  fi

  escaped_value="$(printf '%s' "$value" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  printf '%s="%s"\n' "$key" "$escaped_value" >> "$OUTPUT_FILE"
done < "$TEMPLATE_FILE"

chmod 600 "$OUTPUT_FILE"
