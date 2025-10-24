"""
Utilitaires pour gérer les objets sqlite3.Row de manière compatible
"""

def safe_get(row, key, default=None):
    """
    Récupère une valeur d'un objet sqlite3.Row de manière sécurisée
    """
    if row is None:
        return default
    
    try:
        # Essayer d'accéder directement à la clé
        if hasattr(row, key):
            value = getattr(row, key)
            return value if value is not None else default
        elif hasattr(row, '__getitem__'):
            # Essayer l'indexation
            return row[key] if key in row.keys() else default
        else:
            return default
    except (KeyError, AttributeError, IndexError):
        return default

def row_to_dict(row):
    """
    Convertit un objet sqlite3.Row en dictionnaire
    """
    if row is None:
        return {}
    
    try:
        return dict(row)
    except:
        return {}

def safe_row_get(row, key, default=None):
    """
    Version sécurisée de .get() pour les objets sqlite3.Row
    """
    if row is None:
        return default
    
    # Essayer d'abord la conversion en dict
    try:
        row_dict = dict(row)
        return row_dict.get(key, default)
    except:
        # Fallback: essayer l'accès direct
        try:
            return getattr(row, key, default)
        except:
            return default
