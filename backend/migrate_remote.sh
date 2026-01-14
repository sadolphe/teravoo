#!/bin/bash

echo "🚀 Starting Remote Migration..."

# Load .env variables if file exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Determine DB URL
if [ -n "$1" ]; then
    REMOTE_DB_URL="$1"
elif [ -n "$REMOTE_DATABASE_URL" ]; then
    echo "Using REMOTE_DATABASE_URL from .env"
    REMOTE_DB_URL="$REMOTE_DATABASE_URL"
else
    echo "Enter DATABASE_URL:"
    read REMOTE_DB_URL
fi

if [ -z "$REMOTE_DB_URL" ]; then
    echo "Error: No DATABASE_URL provided."
    exit 1
fi

export DATABASE_URL="$REMOTE_DB_URL"

# Run Migration Script
if [ -f "venv/bin/python" ]; then
    ./venv/bin/python scripts/mvp_migrate.py
else
    python3 scripts/mvp_migrate.py
fi
