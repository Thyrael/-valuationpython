"""
Modèle SQLAlchemy pour l'entité Emprunt
Représente un emprunt de livre par un emprunteur
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Emprunt(Base):
    """
    Modèle Emprunt - Représente un emprunt de livre par un emprunteur
    
    Attributs:
        id (int): Identifiant unique de l'emprunt (clé primaire)
        livre_id (int): Clé étrangère vers le livre emprunté
        emprunteur_id (int): Clé étrangère vers l'emprunteur
        date_emprunt (datetime): Date et heure de l'emprunt
        livre (relationship): Relation vers le livre emprunté
        emprunteur (relationship): Relation vers l'emprunteur
    """
    
    __tablename__ = "emprunts"
    
    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)
    
    # Clés étrangères
    livre_id = Column(Integer, ForeignKey("livres.id"), nullable=False, index=True)
    emprunteur_id = Column(Integer, ForeignKey("emprunteurs.id"), nullable=False, index=True)
    
    # Date de l'emprunt
    date_emprunt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relations
    livre = relationship("Livre", back_populates="emprunts")
    emprunteur = relationship("Emprunteur", back_populates="emprunts")
    
    def __repr__(self):
        """Représentation string de l'emprunt"""
        return f"<Emprunt(id={self.id}, livre_id={self.livre_id}, emprunteur_id={self.emprunteur_id})>"
