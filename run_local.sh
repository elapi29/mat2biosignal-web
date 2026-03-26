#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo "[1/3] Starting backend..."
cd "$BACKEND_DIR"
source .venv/bin/activate
export DYLD_LIBRARY_PATH="$(brew --prefix libmatio)/lib:$DYLD_LIBRARY_PATH"

uvicorn app.main:app --reload > "$PROJECT_ROOT/backend.log" 2>&1 &
BACKEND_PID=$!

echo "[2/3] Starting frontend..."
cd "$FRONTEND_DIR"
python3 -m http.server 8080 > "$PROJECT_ROOT/frontend.log" 2>&1 &
FRONTEND_PID=$!

echo "[3/3] App started"
echo ""
echo "Frontend: http://127.0.0.1:8080"
echo "Backend health: http://127.0.0.1:8000/health"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  $PROJECT_ROOT/backend.log"
echo "  $PROJECT_ROOT/frontend.log"
echo ""
echo "Press Ctrl+C to stop both."

cleanup() {
  echo ""
  echo "Stopping services..."
  kill $BACKEND_PID 2>/dev/null || true
  kill $FRONTEND_PID 2>/dev/null || true
  exit 0
}

trap cleanup INT TERM

wait