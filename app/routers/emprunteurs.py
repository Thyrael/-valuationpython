"""
Router FastAPI pour la gestion des emprunteurs
Définit tous les endpoints pour les emprunteurs
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.emprunteur import EmprunteurCreateDTO, EmprunteurResponseDTO, EmprunteurDeleteResponseDTO
from app.services.emprunteur_service import EmprunteurService

# Création du router
router = APIRouter(
    prefix="/emprunteurs",
    tags=["emprunteurs"],
    responses={404: {"description": "Emprunteur non trouvé"}},
)


@router.get("/", response_model=List[EmprunteurResponseDTO], summary="Liste tous les emprunteurs")
async def get_emprunteurs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les emprunteurs avec pagination
    
    Args:
        skip (int): Nombre d'enregistrements à ignorer (pour la pagination)
        limit (int): Nombre maximum d'enregistrements à retourner (max 100)
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        List[EmprunteurResponseDTO]: Liste des emprunteurs avec leurs informations complètes
    """
    emprunteurs = EmprunteurService.get_emprunteurs(db, skip=skip, limit=limit)
    return emprunteurs


@router.post("/", response_model=EmprunteurResponseDTO, status_code=status.HTTP_201_CREATED, summary="Ajoute un emprunteur")
async def create_emprunteur(
    emprunteur_data: EmprunteurCreateDTO,
    db: Session = Depends(get_db)
):
    """
    Crée un nouvel emprunteur dans la bibliothèque
    
    Args:
        emprunteur_data (EmprunteurCreateDTO): Données de l'emprunteur à créer
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        EmprunteurResponseDTO: L'emprunteur créé avec toutes ses informations
        
    Raises:
        HTTPException: En cas d'erreur de validation ou d'email déjà existant
    """
    return EmprunteurService.create_emprunteur(db, emprunteur_data)


@router.delete("/{emprunteur_id}", response_model=EmprunteurDeleteResponseDTO, summary="Supprime un emprunteur")
async def delete_emprunteur(
    emprunteur_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime un emprunteur de la bibliothèque
    
    Args:
        emprunteur_id (int): Identifiant de l'emprunteur à supprimer
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        EmprunteurDeleteResponseDTO: Message de confirmation avec l'ID supprimé
        
    Raises:
        HTTPException: Si l'emprunteur n'existe pas ou a des emprunts actifs
    """
    return EmprunteurService.delete_emprunteur(db, emprunteur_id)
