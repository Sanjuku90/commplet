"""
Configuration de base de données optimisée pour Render
Gère les problèmes de connexion et de verrouillage
"""

import sqlite3
import os
import time
from functools import wraps

def get_db_connection():
    """Obtenir une connexion à la base de données avec retry automatique"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            conn = sqlite3.connect('investment_platform.db', timeout=30)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                print(f"⚠️ Base de données verrouillée, tentative {attempt + 1}/{max_retries}")
                time.sleep(retry_delay)
                retry_delay *= 2  # Augmenter le délai à chaque tentative
                continue
            else:
                print(f"❌ Erreur connexion base de données: {e}")
                raise
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            raise

def db_retry(max_retries=3):
    """Décorateur pour retry automatique des opérations de base de données"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    if "database is locked" in str(e) and attempt < max_retries - 1:
                        print(f"⚠️ Retry opération DB, tentative {attempt + 1}/{max_retries}")
                        time.sleep(1)
                        continue
                    else:
                        raise
            return None
        return wrapper
    return decorator

def init_tables():
    """Initialiser les tables de base de données"""
    conn = get_db_connection()
    
    try:
        # Table users
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
        
        # Table transactions
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
        
        # Table notifications
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
        
        # Table user_investments
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
        
        conn.commit()
        print("✅ Tables de base de données initialisées")
        
    except Exception as e:
        print(f"❌ Erreur initialisation tables: {e}")
        raise
    finally:
        conn.close()
