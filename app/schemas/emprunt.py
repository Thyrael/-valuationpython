"""
Schémas Pydantic pour l'entité Emprunt
Définit les DTOs pour la validation et sérialisation des données
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EmpruntBase(BaseModel):
    """
    Schéma de base pour un emprunt
    Contient les champs communs à tous les schémas d'emprunt
    """
    livre_id: int = Field(..., gt=0, description="Identifiant du livre emprunté")
    emprunteur_id: int = Field(..., gt=0, description="Identifiant de l'emprunteur")


class EmpruntCreateDTO(EmpruntBase):
    """
    DTO pour la création d'un emprunt
    Hérite de EmpruntBase et ajoute des validations spécifiques
    """
    pass


class EmpruntResponseDTO(EmpruntBase):
    """
    DTO pour la réponse d'un emprunt
    Inclut tous les champs de l'emprunt avec l'ID et les métadonnées
    """
    id: int = Field(..., description="Identifiant unique de l'emprunt")
    date_emprunt: datetime = Field(..., description="Date et heure de l'emprunt")
    
    class Config:
        """Configuration Pydantic pour la sérialisation"""
        from_attributes = True  # Permet la sérialisation depuis les objets SQLAlchemy


class EmpruntDetailResponseDTO(EmpruntResponseDTO):
    """
    DTO pour la réponse détaillée d'un emprunt
    Inclut les informations du livre et de l'emprunteur
    """
    livre: dict = Field(..., description="Informations du livre emprunté")
    emprunteur: dict = Field(..., description="Informations de l'emprunteur")
    
    class Config:
        """Configuration Pydantic pour la sérialisation"""
        from_attributes = True
