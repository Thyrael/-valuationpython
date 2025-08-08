"""
Router FastAPI pour la gestion des livres
Définit tous les endpoints CRUD pour les livres
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.livre import LivreCreateDTO, LivreUpdateDTO, LivreResponseDTO
from app.services.livre_service import LivreService

# Création du router
router = APIRouter(
    prefix="/livres",
    tags=["livres"],
    responses={404: {"description": "Livre non trouvé"}},
)


@router.get("/", response_model=List[LivreResponseDTO], summary="Liste tous les livres")
async def get_livres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les livres avec pagination
    
    Args:
        skip (int): Nombre d'enregistrements à ignorer (pour la pagination)
        limit (int): Nombre maximum d'enregistrements à retourner (max 100)
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        List[LivreResponseDTO]: Liste des livres avec leurs informations complètes
    """
    livres = LivreService.get_livres(db, skip=skip, limit=limit)
    return livres


@router.post("/", response_model=LivreResponseDTO, status_code=status.HTTP_201_CREATED, summary="Ajoute un livre")
async def create_livre(
    livre_data: LivreCreateDTO,
    db: Session = Depends(get_db)
):
    """
    Crée un nouveau livre dans la bibliothèque
    
    Args:
        livre_data (LivreCreateDTO): Données du livre à créer
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        LivreResponseDTO: Le livre créé avec toutes ses informations
        
    Raises:
        HTTPException: En cas d'erreur de validation ou de base de données
    """
    return LivreService.create_livre(db, livre_data)


@router.put("/{livre_id}", response_model=LivreResponseDTO, summary="Met à jour un livre")
async def update_livre(
    livre_id: int,
    livre_data: LivreUpdateDTO,
    db: Session = Depends(get_db)
):
    """
    Met à jour un livre existant
    
    Args:
        livre_id (int): ID du livre à mettre à jour
        livre_data (LivreUpdateDTO): Nouvelles données du livre
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        LivreResponseDTO: Le livre mis à jour
        
    Raises:
        HTTPException: En cas de livre non trouvé ou d'erreur de validation
    """
    return LivreService.update_livre(db, livre_id, livre_data)


@router.delete("/{livre_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprime un livre")
async def delete_livre(
    livre_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime un livre de la bibliothèque
    
    Args:
        livre_id (int): ID du livre à supprimer
        db (Session): Session de base de données injectée par FastAPI
        
    Returns:
        None: Aucun contenu retourné en cas de succès
        
    Raises:
        HTTPException: En cas de livre non trouvé ou d'erreur de suppression
    """
    LivreService.delete_livre(db, livre_id)
    return None
