#!/usr/bin/env bash
set -e

# Get the absolute path to the project root (the folder above scripts/)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Define paths using the project root
DB_PATH="$PROJECT_ROOT/bin/db/group_management.db"
DB_SCRIPT="$PROJECT_ROOT/src/Database/db.py"
INSERT_SCRIPT="$PROJECT_ROOT/src/Database/insert_data.py"

echo "=== Capstone Initialization ==="
echo "Project root: $PROJECT_ROOT"
echo "Database target: $DB_PATH"
echo ""

# 1. Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 2. Ensure database directory exists
mkdir -p "$(dirname "$DB_PATH")"

# 3. Create the database schema
echo ""
echo "Creating database schema..."
python "$DB_SCRIPT" -o "$DB_PATH"

# 4. Insert initial data
echo ""
echo "Inserting initial data..."
python "$INSERT_SCRIPT" -d "$DB_PATH"

echo ""
echo "✅ Initialization complete!"
echo "Database successfully created at: $DB_PATH"
