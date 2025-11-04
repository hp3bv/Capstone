#!/usr/bin/env bash
set -e

# Get absolute path to project root (folder above scripts)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# App path
APP_PATH="$PROJECT_ROOT/src/App/main.py"

echo "=== Starting App ==="
echo "Project root: $PROJECT_ROOT"
echo ""

# Move to the project root so Python imports work correctly
cd "$PROJECT_ROOT"

# Specify server
SERVER_LINK=http://0.0.0.0:8000
export SERVER_LINK

# Start the app
python "$APP_PATH"