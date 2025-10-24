#!/usr/bin/env python3
"""
Script de démarrage optimisé pour Render
Évite tous les problèmes de base de données et de connexion
"""

import os
import sys
import sqlite3
from datetime import datetime

def create_directories():
    """Créer les répertoires nécessaires"""
    os.makedirs('static', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    print("✅ Répertoires créés")

def init_database_safe():
    """Initialiser la base de données de manière sécurisée"""
    try:
        conn = sqlite3.connect('investment_platform.db', timeout=30)
        conn.row_factory = sqlite3.Row
        
        # Créer les tables essentielles
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                two_factor_secret TEXT,
                two_factor_enabled BOOLEAN DEFAULT 0
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                transaction_hash TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_name TEXT NOT NULL,
                amount REAL NOT NULL,
                daily_profit REAL NOT NULL,
                total_earned REAL DEFAULT 0.0,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_trading_bots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                strategy_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                total_profit REAL DEFAULT 0.0,
                daily_profit REAL DEFAULT 0.0,
                last_profit_date TIMESTAMP,
                transaction_hash TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_copy_trading (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                trader_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                total_profit REAL DEFAULT 0.0,
                copy_ratio REAL DEFAULT 1.0,
                transaction_hash TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS trading_strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                daily_return REAL DEFAULT 0.0,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS top_traders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                monthly_return REAL DEFAULT 0.0,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS support_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                priority TEXT DEFAULT 'normal',
                status TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS ticket_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES support_tickets (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Créer les comptes administrateur par défaut
        from werkzeug.security import generate_password_hash
        
        admin_accounts = [
            ('admin@ttrust.com', 'AdminSecure2024!', 'Admin', 'Principal'),
            ('support@ttrust.com', 'SupportSecure2024!', 'Support', 'Team'),
            ('security@ttrust.com', 'SecuritySecure2024!', 'Security', 'Team'),
            ('a@gmail.com', 'aaaaaa', 'Admin', 'User')
        ]
        
        for email, password, first_name, last_name in admin_accounts:
            try:
                # Vérifier si l'utilisateur existe déjà
                existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
                if not existing:
                    conn.execute('''
                        INSERT INTO users (email, password_hash, first_name, last_name, is_admin, balance)
                        VALUES (?, ?, ?, ?, 1, 10000.0)
                    ''', (email, generate_password_hash(password), first_name, last_name))
                    print(f"✅ Compte admin créé: {email}")
                else:
                    print(f"⚠️ Compte admin existe déjà: {email}")
            except Exception as e:
                print(f"❌ Erreur création compte {email}: {e}")
        
        conn.commit()
        conn.close()
        
        print("✅ Base de données initialisée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur initialisation base de données: {e}")
        return False

def main():
    """Point d'entrée principal pour Render"""
    print("🚀 Démarrage de l'application Investment Platform sur Render...")
    
    # Créer les répertoires
    create_directories()
    
    # Initialiser la base de données
    if not init_database_safe():
        print("❌ Impossible d'initialiser la base de données")
        sys.exit(1)
    
    # Importer et démarrer l'application Flask
    try:
        # Désactiver le scheduler pour éviter les erreurs
        import os
        os.environ['DISABLE_SCHEDULER'] = 'true'
        
        from main import app
        
        # Configuration pour Render
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') != 'production'
        
        print(f"🌐 Démarrage sur le port {port}")
        print(f"🔧 Mode debug: {debug}")
        
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except Exception as e:
        print(f"❌ Erreur démarrage application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
