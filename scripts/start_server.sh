#!/usr/bin/env bash
set -e

# Get absolute path to project root (folder above scripts)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== Starting FastAPI Server ==="
echo "Project root: $PROJECT_ROOT"
echo ""

# Move to the project root so Python imports work correctly
cd "$PROJECT_ROOT"

# Specify DB path
DB_PATH="$PROJECT_ROOT/bin/db/group_management.db"
export DB_PATH  # your main.py can use os.getenv("DB_PATH")

# Specify key
KEY="VpLUzRdlmTnWe54fEXanxUa9A33pQu3p"
export KEY

# Start the FastAPI Server
uvicorn src.Server.main:app --reload --host 0.0.0.0 --port 8000
