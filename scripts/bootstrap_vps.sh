#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/mcp-server}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$APP_DIR"

echo "[1/6] Updating repository"
git fetch --all --prune
git pull --ff-only

echo "[2/6] Installing system packages when apt is available"
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y git curl python3 python3-venv python3-pip nodejs npm
fi

echo "[3/6] Creating Python virtual environment"
if [ ! -d .venv ]; then
  "$PYTHON_BIN" -m venv .venv
fi

. .venv/bin/activate

echo "[4/6] Installing Python dependencies"
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "[5/6] Preparing local folders"
mkdir -p .mcp_outbox .mcp_outbox/responses logs config

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

echo "[6/6] Done"
echo "Run web UI: ./scripts/run_web.sh"
echo "Run MCP stdio server: ./scripts/run_mcp.sh"
