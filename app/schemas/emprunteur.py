"""
Schémas Pydantic pour l'entité Emprunteur
"""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class EmprunteurCreateDTO(BaseModel):
    """DTO pour la création d'un emprunteur"""
    nom: str = Field(..., min_length=1, max_length=255)
    email: EmailStr = Field(..., description="Adresse email valide")


class EmprunteurResponseDTO(EmprunteurCreateDTO):
    """DTO pour la réponse d'un emprunteur"""
    id: int
    date_creation: datetime
    
    class Config:
        from_attributes = True


class EmprunteurDeleteResponseDTO(BaseModel):
    """DTO pour la réponse de suppression d'un emprunteur"""
    message: str = "Emprunteur supprimé avec succès"
    emprunteur_id: int
