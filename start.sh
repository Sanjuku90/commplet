#!/bin/bash
# Script de démarrage pour Render
echo "🚀 Démarrage de l'application Investment Platform..."

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'application avec Gunicorn
echo "🌐 Lancement du serveur web..."
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 main:app
