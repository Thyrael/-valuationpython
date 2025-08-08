"""
Router FastAPI pour la gestion des emprunts
Définit tous les endpoints pour les emprunts et les retours
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.emprunt import EmpruntCreateDTO, EmpruntResponseDTO
from app.schemas.livre import LivreResponseDTO
from app.services.emprunt_service import EmpruntService

# Création du router
router = APIRouter(
    prefix="/emprunts",
    tags=["emprunts"],
    responses={404: {"description": "Emprunt non trouvé"}},
)


@router.post("/", response_model=EmpruntResponseDTO, status_code=status.HTTP_201_CREATED, summary="Enregistre un emprunt")
async def create_emprunt(
    emprunt_data: EmpruntCreateDTO,
    db: Session = Depends(get_db)
):
    """
    Enregistre un nouvel emprunt de livre
    
    Args:
        emprunt_data (EmpruntCreateDTO): Données de l'emprunt à créer
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        EmpruntResponseDTO: L'emprunt créé avec toutes ses informations
        
    Raises:
        HTTPException: En cas d'erreur de validation, livre non trouvé, emprunteur non trouvé ou livre non disponible
    """
    return EmpruntService.create_emprunt(db, emprunt_data)


@router.get("/", summary="Liste tous les emprunts avec détails")
async def get_emprunts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les emprunts avec les détails du livre et de l'emprunteur (BONUS)
    
    Args:
        skip (int): Nombre d'enregistrements à ignorer (pour la pagination)
        limit (int): Nombre maximum d'enregistrements à retourner (max 100)
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        List[dict]: Liste des emprunts avec détails du livre et de l'emprunteur
    """
    return EmpruntService.get_emprunts_with_details(db, skip=skip, limit=limit)


@router.post("/retours/{livre_id}", response_model=LivreResponseDTO, summary="Remet un livre à disposition")
async def retourner_livre(
    livre_id: int,
    db: Session = Depends(get_db)
):
    """
    Remet un livre à disposition (BONUS)
    
    Args:
        livre_id (int): ID du livre à remettre à disposition
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        LivreResponseDTO: Le livre mis à jour avec disponibilité = True
        
    Raises:
        HTTPException: En cas de livre non trouvé ou déjà disponible
    """
    return EmpruntService.retourner_livre(db, livre_id)
