"""
Modèle SQLAlchemy pour l'entité Emprunteur
Représente un emprunteur de la bibliothèque
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Emprunteur(Base):
    """
    Modèle Emprunteur - Représente un emprunteur de la bibliothèque
    
    Attributs:
        id (int): Identifiant unique de l'emprunteur (clé primaire)
        nom (str): Nom complet de l'emprunteur
        email (str): Adresse email de l'emprunteur
        date_creation (datetime): Date de création de l'enregistrement
        emprunts (relationship): Relation vers les emprunts de cet emprunteur
    """
    
    __tablename__ = "emprunteurs"
    
    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations de l'emprunteur
    nom = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    
    # Métadonnées
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    emprunts = relationship("Emprunt", back_populates="emprunteur", cascade="all, delete-orphan")
    
    def __repr__(self):
        """Représentation string de l'emprunteur"""
        return f"<Emprunteur(id={self.id}, nom='{self.nom}', email='{self.email}')>"
