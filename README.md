# API de Gestion de Bibliothèque

## Description
API RESTful pour la gestion d'une bibliothèque (livres, emprunteurs, emprunts) avec FastAPI, SQLAlchemy et Pydantic. Base de données SQLite, validation d'email, prête à l'emploi.

## Prérequis
- Python 3.10+
- (Recommandé) UV installé pour la gestion rapide d'environnements et dépendances
- (Optionnel) Extension REST Client pour VS Code pour tester l'API

## 🚀 Quickstart (avec UV)
```bash
# 1) Créer l'environnement virtuel
uv venv

# 2) Installer les dépendances
uv pip install -r requirements.txt

# 3) Initialiser la base de données (tables + données de test)
uv run python init_db.py

# 4) Lancer l'API en mode reload
uv run uvicorn app.main:app --reload
```
API disponible sur: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Alternative (sans UV)
```bash
# 1) Créer un environnement virtuel
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 2) Installer les dépendances
pip install -r requirements.txt

# 3) Initialiser la base de données
python init_db.py

# 4) Lancer l'API
python -m uvicorn app.main:app --reload
```

## Structure du Projet
```
app/
├── main.py              # Point d'entrée FastAPI
├── database.py          # Configuration SQLAlchemy (SQLite)
├── models/              # Modèles SQLAlchemy
├── schemas/             # DTOs Pydantic
├── routers/             # Routes FastAPI
└── services/            # Logique métier
requests.http            # Tests d'API (34 tests complets)
```

## 🏗️ Architecture et Fonctionnement

### **📁 Fichiers de Configuration**

#### `requirements.txt`
- **Rôle** : Liste toutes les dépendances Python
- **Contenu** : FastAPI, Uvicorn, SQLAlchemy, Pydantic, email-validator
- **Utilisation** : `uv pip install -r requirements.txt`

#### `init_db.py`
- **Rôle** : Script d'initialisation de la base de données
- **Fonctionnalités** :
  - Crée les tables SQLAlchemy
  - Supprime tous les livres existants
  - Conserve les emprunteurs existants
  - Ajoute 10 nouveaux livres classiques
  - Affiche un rapport détaillé
- **Utilisation** : `uv run python init_db.py`

### **📁 Dossier `app/` - Application principale**

#### `app/main.py`
- **Rôle** : Point d'entrée de l'application FastAPI
- **Fonctionnalités** :
  - Configuration de l'app FastAPI
  - Inclusion des routers (livres, emprunteurs, emprunts)
  - Gestion des événements de démarrage (création des tables)
  - Configuration CORS et métadonnées
- **Endpoints** : `/docs`, `/redoc` (documentation automatique)

#### `app/database.py`
- **Rôle** : Configuration de la base de données SQLAlchemy
- **Fonctionnalités** :
  - Création du moteur SQLAlchemy (SQLite)
  - Factory de sessions de base de données
  - Déclaration de la base pour les modèles
  - Fonction `create_tables()` pour initialiser les tables
  - Import explicite de tous les modèles pour éviter les erreurs de mapping
- **Dépendances** : SQLAlchemy, import des modèles

### **📁 Dossier `app/models/` - Modèles SQLAlchemy**

#### `app/models/livre.py`
- **Rôle** : Modèle SQLAlchemy pour l'entité Livre
- **Champs** :
  - `id` : Clé primaire auto-incrémentée
  - `titre` : Titre du livre (255 caractères max)
  - `auteur` : Nom de l'auteur (255 caractères max)
  - `annee_publication` : Année de publication
  - `disponible` : Booléen (True par défaut)
  - `date_creation` : Timestamp automatique
- **Relations** : One-to-Many avec Emprunt

#### `app/models/emprunteur.py`
- **Rôle** : Modèle SQLAlchemy pour l'entité Emprunteur
- **Champs** :
  - `id` : Clé primaire auto-incrémentée
  - `nom` : Nom de l'emprunteur (255 caractères max)
  - `email` : Email unique (validation automatique)
  - `date_creation` : Timestamp automatique
- **Relations** : One-to-Many avec Emprunt

#### `app/models/emprunt.py`
- **Rôle** : Modèle SQLAlchemy pour l'entité Emprunt
- **Champs** :
  - `id` : Clé primaire auto-incrémentée
  - `livre_id` : Clé étrangère vers Livre
  - `emprunteur_id` : Clé étrangère vers Emprunteur
  - `date_emprunt` : Timestamp automatique
- **Relations** : Many-to-One avec Livre et Emprunteur

### **📁 Dossier `app/schemas/` - DTOs Pydantic**

#### `app/schemas/livre.py`
- **Rôle** : Validation et sérialisation des données Livre
- **DTOs** :
  - `LivreCreateDTO` : Validation des données de création
  - `LivreUpdateDTO` : Validation des données de mise à jour
  - `LivreResponseDTO` : Format de réponse avec tous les champs
- **Validation** : Contraintes sur les champs (longueur, types)

#### `app/schemas/emprunteur.py`
- **Rôle** : Validation et sérialisation des données Emprunteur
- **DTOs** :
  - `EmprunteurCreateDTO` : Validation avec EmailStr pour email
  - `EmprunteurResponseDTO` : Format de réponse complet
  - `EmprunteurDeleteResponseDTO` : Réponse de suppression
- **Validation** : Email automatique avec `email-validator`

#### `app/schemas/emprunt.py`
- **Rôle** : Validation et sérialisation des données Emprunt
- **DTOs** :
  - `EmpruntCreateDTO` : Validation des IDs livre et emprunteur
  - `EmpruntResponseDTO` : Réponse avec détails complets
- **Validation** : Vérification de l'existence des entités liées

### **📁 Dossier `app/services/` - Logique Métier**

#### `app/services/livre_service.py`
- **Rôle** : Logique métier pour les opérations sur les livres
- **Méthodes** :
  - `get_all_livres()` : Récupération de tous les livres
  - `get_livre_by_id()` : Récupération d'un livre par ID
  - `create_livre()` : Création d'un nouveau livre
  - `update_livre()` : Mise à jour d'un livre existant
  - `delete_livre()` : Suppression d'un livre
- **Gestion d'erreurs** : HTTPException pour ressources non trouvées

#### `app/services/emprunteur_service.py`
- **Rôle** : Logique métier pour les opérations sur les emprunteurs
- **Méthodes** :
  - `get_all_emprunteurs()` : Récupération de tous les emprunteurs
  - `get_emprunteur_by_id()` : Récupération d'un emprunteur par ID
  - `create_emprunteur()` : Création d'un nouvel emprunteur
  - `delete_emprunteur()` : Suppression avec vérification des emprunts actifs
- **Logique métier** : Empêche la suppression si emprunts actifs

#### `app/services/emprunt_service.py`
- **Rôle** : Logique métier pour les opérations sur les emprunts
- **Méthodes** :
  - `get_all_emprunts()` : Récupération de tous les emprunts avec détails
  - `create_emprunt()` : Création d'un emprunt avec vérifications
  - `return_livre()` : Retour d'un livre (marque comme disponible)
- **Logique métier** :
  - Vérifie disponibilité du livre avant emprunt
  - Marque automatiquement le livre comme indisponible
  - Marque automatiquement le livre comme disponible lors du retour

### **📁 Dossier `app/routers/` - Routes FastAPI**

#### `app/routers/livres.py`
- **Rôle** : Endpoints REST pour les livres
- **Endpoints** :
  - `GET /livres` : Liste tous les livres
  - `GET /livres/{id}` : Détail d'un livre
  - `POST /livres` : Création d'un livre
  - `PUT /livres/{id}` : Mise à jour d'un livre
  - `DELETE /livres/{id}` : Suppression d'un livre
- **Validation** : Utilise les DTOs Pydantic pour validation/sérialisation

#### `app/routers/emprunteurs.py`
- **Rôle** : Endpoints REST pour les emprunteurs
- **Endpoints** :
  - `GET /emprunteurs` : Liste tous les emprunteurs
  - `GET /emprunteurs/{id}` : Détail d'un emprunteur
  - `POST /emprunteurs` : Création d'un emprunteur
  - `DELETE /emprunteurs/{id}` : Suppression d'un emprunteur
- **Validation** : Email automatique avec EmailStr

#### `app/routers/emprunts.py`
- **Rôle** : Endpoints REST pour les emprunts et retours
- **Endpoints** :
  - `GET /emprunts` : Liste tous les emprunts avec détails
  - `POST /emprunts` : Création d'un emprunt
  - `POST /retours/{livre_id}` : Retour d'un livre
- **Logique métier** : Intégrée directement dans les endpoints

### **📄 Fichiers de Test**

#### `requests.http`
- **Rôle** : Suite de tests complète pour l'API
- **Contenu** : 34 tests organisés par fonctionnalité
- **Tests inclus** :
  - CRUD complet pour livres et emprunteurs
  - Gestion des emprunts et retours
  - Tests de validation (email, contraintes)
  - Tests d'erreurs et scénarios complets
- **Utilisation** : Extension REST Client dans VS Code

## 🧪 Tests d'API

### Tests avec REST Client (VS Code)
Le fichier `requests.http` contient **34 tests complets** pour tester tous les endpoints :

1. **Installer l'extension REST Client** dans VS Code
2. **Ouvrir le fichier** `requests.http`
3. **Cliquer sur "Send Request"** au-dessus de chaque requête
4. **Voir les réponses** directement dans VS Code

### Tests inclus :
- ✅ **CRUD Livres** : Créer, lire, modifier, supprimer
- ✅ **CRUD Emprunteurs** : Créer, lire, supprimer avec validation email
- ✅ **Gestion Emprunts** : Emprunter, retourner, lister
- ✅ **Tests d'erreurs** : Validation, contraintes métier
- ✅ **Scénarios complets** : Workflows end-to-end

### Tests avec curl (alternative)
Vous pouvez aussi utiliser les exemples curl ci-dessous ou dans le fichier `requests.http`.

## Endpoints Disponibles

### Livres (CRUD complet)
- `GET /livres` — Liste tous les livres
- `GET /livres/{id}` — Détail d'un livre
- `POST /livres` — Ajoute un livre
- `PUT /livres/{id}` — Met à jour un livre
- `DELETE /livres/{id}` — Supprime un livre

### Emprunteurs (CRUD complet)
- `GET /emprunteurs` — Liste tous les emprunteurs
- `GET /emprunteurs/{id}` — Détail d'un emprunteur
- `POST /emprunteurs` — Ajoute un emprunteur
- `DELETE /emprunteurs/{id}` — Supprime un emprunteur (si pas d'emprunts actifs)

### Emprunts
- `POST /emprunts` — Enregistre un emprunt (marque le livre indisponible)
- `GET /emprunts` — Liste tous les emprunts avec détails (bonus)
- `POST /retours/{livre_id}` — Retour d'un livre (le rend disponible) (bonus)

## Fonctionnalités Spéciales

### Validation d'Email
- Validation automatique du format email avec `email-validator`
- Erreur 422 si email invalide

### Logique Métier Intelligente
- **Emprunt** : Vérifie disponibilité du livre et existence de l'emprunteur
- **Retour** : Marque automatiquement le livre comme disponible
- **Suppression emprunteur** : Empêche la suppression si emprunts actifs

## Données de test
Le script `init_db.py` crée automatiquement:
- 10 livres classiques (Les Misérables, Don Quichotte, etc.)
- 5 emprunteurs (Jean Dupont, Marie Martin, etc.)

## Exemples rapides

### Ajouter un livre:
```bash
curl -X POST "http://localhost:8000/livres/" \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Le Petit Prince",
    "auteur": "Antoine de Saint-Exupéry",
    "annee_publication": 1943
  }'
```

### Ajouter un emprunteur:
```bash
curl -X POST "http://localhost:8000/emprunteurs/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Pierre Durand",
    "email": "pierre.durand@email.com"
  }'
```

### Emprunter un livre:
```bash
curl -X POST "http://localhost:8000/emprunts/" \
  -H "Content-Type: application/json" \
  -d '{
    "livre_id": 1,
    "emprunteur_id": 1
  }'
```

## Dépannage
- Si l'API ne se lance pas, vérifiez que l'init de la base a bien été exécuté: `uv run python init_db.py`
- Sous Windows, utilisez `Ctrl + C` pour arrêter le serveur Uvicorn.
- Si erreur de validation email, vérifiez le format: `utilisateur@domaine.com`
- Pour les tests, installez l'extension REST Client dans VS Code pour utiliser `requests.http`
