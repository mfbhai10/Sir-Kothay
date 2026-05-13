#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/server"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created server/.env from .env.example — edit SECRET_KEY for non-local use."
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
echo ""
echo "Starting Django at http://127.0.0.1:8000/ — serve client/ over http (e.g. live-server) for the UI."
python manage.py runserver 127.0.0.1:8000
