#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

cd "$APP_DIR"

echo "[1/5] Pulling latest code"
git pull --ff-only

echo "[2/5] Activating virtual environment"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
. .venv/bin/activate

echo "[3/5] Updating dependencies"
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "[4/5] Running tests"
python -m pytest -q

echo "[5/5] Restarting service when systemd unit exists"
if command -v systemctl >/dev/null 2>&1 && systemctl list-unit-files | grep -q '^mcp-server.service'; then
  sudo systemctl restart mcp-server
  sudo systemctl status mcp-server --no-pager -l
else
  echo "No systemd service found. Start manually with ./scripts/run_web.sh or ./scripts/run_mcp.sh"
fi
