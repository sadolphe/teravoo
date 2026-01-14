#!/bin/bash

# Warning
echo "⚠️  ATTENTION : Ce script va EFFACER et REINITALISER la base de données cible."
echo "Assurez-vous de viser la bonne base de données (celle en ligne par exemple)."
echo ""

# Load .env variables if file exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 1. Check argument
# 2. Check REMOTE_DATABASE_URL from .env
# 3. Prompt user
if [ -n "$1" ]; then
    REMOTE_DB_URL="$1"
elif [ -n "$REMOTE_DATABASE_URL" ]; then
    echo "URL trouvée dans .env (REMOTE_DATABASE_URL)..."
    REMOTE_DB_URL="$REMOTE_DATABASE_URL"
else
    echo "Entrez votre DATABASE_URL (ex: postgres://user:pass@host/db) :"
    read REMOTE_DB_URL
fi

if [ -z "$REMOTE_DB_URL" ]; then
    echo "Erreur: DATABASE_URL ne peut pas être vide."
    exit 1
fi

# Export variable
export DATABASE_URL="$REMOTE_DB_URL"

echo ""
echo "Configuration de DATABASE_URL pour cette session..."
echo "Lancement du seed..."

# Run seed using venv python if available, else system python
if [ -f "venv/bin/python" ]; then
    echo "Utilisation de l'environnement virtuel (venv)..."
    ./venv/bin/python seed_db.py
else
    echo "Attention: venv non trouvé, utilisation de python3 système..."
    python3 seed_db.py
fi

echo "Terminé."
