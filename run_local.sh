#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

echo "[1/1] Starting mat2biosignal-web..."
cd "$BACKEND_DIR"
source .venv/bin/activate
export DYLD_LIBRARY_PATH="$(brew --prefix libmatio)/lib:$DYLD_LIBRARY_PATH"

echo ""
echo "App: http://127.0.0.1:8000"
echo "Health: http://127.0.0.1:8000/health"
echo ""

uvicorn app.main:app --reload