#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

cd "$APP_DIR"
. .venv/bin/activate
exec uvicorn backend.web.app:app --host "$HOST" --port "$PORT"
