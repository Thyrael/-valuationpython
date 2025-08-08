"""
Modèle SQLAlchemy pour l'entité Livre
Représente un livre dans la bibliothèque
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Livre(Base):
    """
    Modèle Livre - Représente un livre dans la bibliothèque
    
    Attributs:
        id (int): Identifiant unique du livre (clé primaire)
        titre (str): Titre du livre
        auteur (str): Nom de l'auteur
        annee_publication (int): Année de publication
        disponible (bool): Indique si le livre est disponible à l'emprunt
        date_creation (datetime): Date de création de l'enregistrement
        emprunts (relationship): Relation vers les emprunts de ce livre
    """
    
    __tablename__ = "livres"
    
    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations du livre
    titre = Column(String(255), nullable=False, index=True)
    auteur = Column(String(255), nullable=False, index=True)
    annee_publication = Column(Integer, nullable=False)
    
    # État de disponibilité
    disponible = Column(Boolean, default=True, nullable=False)
    
    # Métadonnées
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    emprunts = relationship("Emprunt", back_populates="livre", cascade="all, delete-orphan")
    
    def __repr__(self):
        """Représentation string du livre"""
        return f"<Livre(id={self.id}, titre='{self.titre}', auteur='{self.auteur}')>"
