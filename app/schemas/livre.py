"""
Schémas Pydantic pour l'entité Livre
Définit les DTOs pour la validation et sérialisation des données
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LivreBase(BaseModel):
    """
    Schéma de base pour un livre
    Contient les champs communs à tous les schémas de livre
    """
    titre: str = Field(..., min_length=1, max_length=255, description="Titre du livre")
    auteur: str = Field(..., min_length=1, max_length=255, description="Nom de l'auteur")
    annee_publication: int = Field(..., ge=1000, le=2024, description="Année de publication")


class LivreCreateDTO(LivreBase):
    """
    DTO pour la création d'un livre
    Hérite de LivreBase et ajoute des validations spécifiques
    """
    pass


class LivreUpdateDTO(BaseModel):
    """
    DTO pour la mise à jour d'un livre
    Tous les champs sont optionnels pour permettre des mises à jour partielles
    """
    titre: Optional[str] = Field(None, min_length=1, max_length=255, description="Titre du livre")
    auteur: Optional[str] = Field(None, min_length=1, max_length=255, description="Nom de l'auteur")
    annee_publication: Optional[int] = Field(None, ge=1000, le=2024, description="Année de publication")
    disponible: Optional[bool] = Field(None, description="Disponibilité du livre")


class LivreResponseDTO(LivreBase):
    """
    DTO pour la réponse d'un livre
    Inclut tous les champs du livre avec l'ID et les métadonnées
    """
    id: int = Field(..., description="Identifiant unique du livre")
    disponible: bool = Field(..., description="Disponibilité du livre")
    date_creation: datetime = Field(..., description="Date de création de l'enregistrement")
    
    class Config:
        """Configuration Pydantic pour la sérialisation"""
        from_attributes = True  # Permet la sérialisation depuis les objets SQLAlchemy
