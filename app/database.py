"""
Configuration de la base de données SQLAlchemy
Gère la connexion à SQLite et la création des tables
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./bibliotheque.db"

# Création du moteur SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
)

# Création de la session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles déclaratifs
Base = declarative_base()

def get_db():
    """
    Fonction pour obtenir une session de base de données
    Utilisée comme dépendance dans FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Crée toutes les tables dans la base de données.
    IMPORTANT: importer les modèles avant pour enregistrer toutes les mappes.
    """
    # Import paresseux des modèles pour s'assurer qu'ils sont enregistrés auprès de Base
    # et que les relations par nom (e.g. "Emprunt") peuvent être résolues.
    from app.models import livre as _livre  # noqa: F401
    from app.models import emprunteur as _emprunteur  # noqa: F401
    from app.models import emprunt as _emprunt  # noqa: F401

    Base.metadata.create_all(bind=engine)
