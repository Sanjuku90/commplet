#!/usr/bin/env python3
"""
Script de démarrage optimisé pour Render
Gère l'initialisation de la base de données et les erreurs courantes
"""

import os
import sys
import sqlite3
from datetime import datetime

def init_database():
    """Initialiser la base de données avec gestion d'erreurs"""
    try:
        # Créer les répertoires nécessaires
        os.makedirs('static', exist_ok=True)
        os.makedirs('uploads', exist_ok=True)
        
        # Importer et utiliser la configuration de base de données
        from database_config import init_tables
        init_tables()
        
        print("✅ Base de données initialisée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur initialisation base de données: {e}")
        return False

def main():
    """Point d'entrée principal pour Render"""
    print("🚀 Démarrage de l'application Investment Platform sur Render...")
    
    # Initialiser la base de données
    if not init_database():
        print("❌ Impossible d'initialiser la base de données")
        sys.exit(1)
    
    # Importer et démarrer l'application Flask
    try:
        from main import app
        
        # Configuration pour Render
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') != 'production'
        
        print(f"🌐 Démarrage sur le port {port}")
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except Exception as e:
        print(f"❌ Erreur démarrage application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
