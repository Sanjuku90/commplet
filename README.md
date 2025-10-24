# Investment Platform

Une plateforme d'investissement complète développée avec Flask, incluant des fonctionnalités PWA, des bots de trading automatique, et un tableau de bord administrateur.

## 🚀 Fonctionnalités

- **Interface Utilisateur Moderne** : Design responsive avec support PWA
- **Système d'Authentification** : Connexion/inscription sécurisée avec 2FA
- **Plans d'Investissement** : Ultra, Staking, et Frozen plans
- **Trading Automatique** : Bots de trading avec calcul de profits
- **Copy Trading** : Suivez les traders experts
- **Tableau de Bord Admin** : Gestion complète des utilisateurs et transactions
- **Système de Support** : Tickets de support intégrés
- **Sécurité Avancée** : Chiffrement des mots de passe, sessions sécurisées

## 🛠️ Technologies Utilisées

- **Backend** : Flask (Python)
- **Base de données** : SQLite
- **Frontend** : HTML5, CSS3, JavaScript
- **PWA** : Service Worker, Manifest
- **Sécurité** : Werkzeug, 2FA avec pyotp
- **Scheduling** : APScheduler pour les tâches automatiques
- **Trading** : Intégration Telegram Bot

## 📦 Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-username/investment-platform.git
   cd investment-platform
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python main.py
   ```

4. **Accéder à l'application**
   - Ouvrez votre navigateur sur `http://localhost:5000`

## 🔐 Comptes Administrateur

L'application crée automatiquement des comptes administrateur :
- `admin@ttrust.com` / `AdminSecure2024!`
- `support@ttrust.com` / `SupportSecure2024!`
- `security@ttrust.com` / `SecuritySecure2024!`
- `a@gmail.com` / `aaaaaa`

## 📱 Fonctionnalités PWA

- Installation sur mobile/desktop
- Mode hors ligne
- Notifications push
- Interface native

## 🤖 Trading Automatique

- Bots de trading configurés
- Calcul automatique des profits
- Copy trading entre utilisateurs
- Historique des transactions

## 🔧 Configuration

- **Base de données** : SQLite (fichier `investment_platform.db`)
- **Port** : 5000 (configurable dans `main.py`)
- **Debug** : Activé par défaut

## 📊 Structure du Projet

```
investment-platform/
├── main.py                 # Application Flask principale
├── templates/              # Templates HTML
├── static/                 # Fichiers statiques (CSS, JS, images)
├── uploads/                # Fichiers uploadés
├── investment_platform.db # Base de données SQLite
├── pyproject.toml         # Dépendances Python
└── README.md              # Documentation
```

## 🚀 Déploiement

Pour déployer en production :

1. **Variables d'environnement**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

2. **Base de données**
   - Configurez une base de données PostgreSQL/MySQL pour la production
   - Mettez à jour la configuration dans `main.py`

3. **Serveur Web**
   - Utilisez Gunicorn ou uWSGI
   - Configurez un reverse proxy (Nginx)

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📞 Support

Pour toute question ou support, contactez-nous via le système de tickets intégré dans l'application.
