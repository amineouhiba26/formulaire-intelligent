# Formulaire Intelligent - Backend API

Backend FastAPI pour le formulaire dynamique "Le Nexus Connecté" de la Nuit de l'Info 2025.

## 🚀 Fonctionnalités

- **Classification intelligente** : Détecte automatiquement la mission à partir d'un prompt utilisateur
- **Génération de formulaires dynamiques** : Crée des champs de formulaire adaptés à chaque mission
- **Soumission et persistance** : Sauvegarde les soumissions dans MongoDB avec métadonnées
- **Messages de confirmation personnalisés** : Génère des réponses contextuelles via IA

## 📋 Prérequis

- Python 3.8+
- MongoDB (local ou distant)
- Clé API Groq (pour l'IA)

## 🛠️ Installation

### 1. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate  # Sur Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

Copier le fichier `.env.example` vers `.env` :

```bash
cp .env.example .env
```

Puis éditer `.env` avec vos valeurs :

```env
GROQ_API_KEY=votre_clé_api_groq
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=formMagique
FRONTEND_ORIGIN=http://localhost:5173
```

### 4. Démarrer MongoDB

Assurez-vous que MongoDB est en cours d'exécution :

```bash
# Sur macOS avec Homebrew
brew services start mongodb-community

# Ou directement
mongod
```

### 5. Lancer le serveur

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Le serveur sera accessible sur `http://localhost:8000`

## 📚 Documentation API

Une fois le serveur lancé, accédez à :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔌 Endpoints principaux

### 1. Health Check
```
GET /health
```
Vérifie que le serveur est en ligne.

### 2. Classification de mission
```
POST /api/classify
```
Détecte la mission à partir d'un prompt utilisateur.

**Body:**
```json
{
  "prompt": "Je voudrais faire un don",
  "language": "fr"
}
```

### 3. Génération de formulaire
```
POST /api/generate
```
Génère les champs de formulaire pour une mission.

### 4. Soumission de formulaire
```
POST /api/submit
```
Soumet un formulaire et sauvegarde dans MongoDB.

**Body:**
```json
{
  "mission": "donation",
  "values": {
    "nom": "Jean Dupont",
    "email": "jean@example.com",
    "montant": 50
  },
  "username": "Jean Dupont",
  "language": "fr"
}
```

## 🗄️ Structure MongoDB

### Collection: `submissions`

Chaque soumission contient :
- `mission` : Type de mission (contact, donation, volunteer, information)
- `values` : Valeurs du formulaire
- `username` : Nom de l'utilisateur
- `language` : Langue de soumission
- `confirmation_message` : Message de confirmation généré
- `submitted_at` : Timestamp de soumission
- `ip_address` : Adresse IP de l'utilisateur
- `user_agent` : User agent du navigateur

## 🔧 Configuration

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `GROQ_API_KEY` | Clé API Groq pour l'IA | - |
| `MODEL_NAME` | Modèle IA à utiliser | `llama-3.1-70b-versatile` |
| `APP_ENV` | Environnement (dev/prod) | `dev` |
| `FRONTEND_ORIGIN` | URL du frontend | `http://localhost:5173` |
| `MONGODB_URL` | URL de connexion MongoDB | `mongodb://localhost:27017` |
| `MONGODB_DB_NAME` | Nom de la base de données | `formMagique` |

## 🧪 Tests

Pour tester l'API, vous pouvez utiliser :

1. **Swagger UI** : http://localhost:8000/docs
2. **cURL** :
```bash
curl -X POST "http://localhost:8000/api/classify" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Je veux faire un don", "language": "fr"}'
```

## 📦 Structure du projet

```
formulaire-intelligent/
├── app/
│   ├── constants/       # Constantes (missions, champs de base)
│   ├── routers/         # Routes API
│   ├── schemas/         # Schémas Pydantic
│   ├── services/        # Logique métier et services IA
│   ├── config.py        # Configuration
│   ├── database.py      # Connexion MongoDB
│   ├── models.py        # Modèles de données
│   └── main.py          # Point d'entrée FastAPI
├── requirements.txt     # Dépendances Python
├── .env.example         # Template de configuration
└── README.md           # Ce fichier
```

## 🚨 Dépannage

### MongoDB ne démarre pas
```bash
# Vérifier le statut
brew services list

# Redémarrer MongoDB
brew services restart mongodb-community
```

### Erreur de connexion MongoDB
Vérifiez que :
1. MongoDB est en cours d'exécution
2. L'URL dans `.env` est correcte
3. Le port 27017 n'est pas bloqué

### Erreur API Groq
Vérifiez que :
1. Votre clé API est valide dans `.env`
2. Vous avez une connexion Internet
3. Votre quota API n'est pas dépassé

## 📝 Licence

Projet développé pour la Nuit de l'Info 2025.
