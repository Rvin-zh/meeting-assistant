#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -f .env ]; then
  echo "Error: .env not found. Copy .env.example and add your API keys."
  exit 1
fi

PYTHON="${PYTHON:-/home/arvinzaheri/miniconda3/bin/python3}"
if [ ! -x "$PYTHON" ]; then
  PYTHON="$(command -v python3)"
fi

export PYTHONPATH="$ROOT"
echo "Running LIVE integration tests (real Google + Jira API calls)..."
exec "$PYTHON" -m pytest backend/tests/test_live_integration.py --run-live -v -s "$@"
