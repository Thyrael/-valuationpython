"""
Service pour la gestion des emprunts
Contient toute la logique métier pour les opérations sur les emprunts
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.emprunt import Emprunt
from app.models.livre import Livre
from app.models.emprunteur import Emprunteur
from app.schemas.emprunt import EmpruntCreateDTO
from app.services.livre_service import LivreService
from app.services.emprunteur_service import EmprunteurService


class EmpruntService:
    """
    Service pour la gestion des emprunts
    Encapsule toute la logique métier pour les opérations sur les emprunts
    """
    
    @staticmethod
    def get_emprunts(db: Session, skip: int = 0, limit: int = 100) -> List[Emprunt]:
        """
        Récupère tous les emprunts avec pagination
        
        Args:
            db (Session): Session de base de données
            skip (int): Nombre d'enregistrements à ignorer (pour la pagination)
            limit (int): Nombre maximum d'enregistrements à retourner
            
        Returns:
            List[Emprunt]: Liste des emprunts
        """
        return db.query(Emprunt).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_emprunts_with_details(db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
        """
        Récupère tous les emprunts avec les détails du livre et de l'emprunteur
        
        Args:
            db (Session): Session de base de données
            skip (int): Nombre d'enregistrements à ignorer (pour la pagination)
            limit (int): Nombre maximum d'enregistrements à retourner
            
        Returns:
            List[dict]: Liste des emprunts avec détails
        """
        emprunts = db.query(Emprunt).offset(skip).limit(limit).all()
        
        result = []
        for emprunt in emprunts:
            emprunt_dict = {
                "id": emprunt.id,
                "date_emprunt": emprunt.date_emprunt,
                "livre": {
                    "id": emprunt.livre.id,
                    "titre": emprunt.livre.titre,
                    "auteur": emprunt.livre.auteur,
                    "annee_publication": emprunt.livre.annee_publication,
                    "disponible": emprunt.livre.disponible
                },
                "emprunteur": {
                    "id": emprunt.emprunteur.id,
                    "nom": emprunt.emprunteur.nom,
                    "email": emprunt.emprunteur.email
                }
            }
            result.append(emprunt_dict)
        
        return result
    
    @staticmethod
    def create_emprunt(db: Session, emprunt_data: EmpruntCreateDTO) -> Emprunt:
        """
        Crée un nouvel emprunt
        
        Args:
            db (Session): Session de base de données
            emprunt_data (EmpruntCreateDTO): Données de l'emprunt à créer
            
        Returns:
            Emprunt: L'emprunt créé
            
        Raises:
            HTTPException: En cas d'erreur de validation ou de base de données
        """
        try:
            # Vérification de l'existence du livre
            livre = LivreService.get_livre_by_id(db, emprunt_data.livre_id)
            if not livre:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Livre avec l'ID {emprunt_data.livre_id} non trouvé"
                )
            
            # Vérification de l'existence de l'emprunteur
            emprunteur = EmprunteurService.get_emprunteur_by_id(db, emprunt_data.emprunteur_id)
            if not emprunteur:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Emprunteur avec l'ID {emprunt_data.emprunteur_id} non trouvé"
                )
            
            # Vérification de la disponibilité du livre
            if not livre.disponible:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Le livre '{livre.titre}' n'est pas disponible à l'emprunt"
                )
            
            # Création du nouvel emprunt
            db_emprunt = Emprunt(
                livre_id=emprunt_data.livre_id,
                emprunteur_id=emprunt_data.emprunteur_id
            )
            
            # Sauvegarde de l'emprunt
            db.add(db_emprunt)
            
            # Mise à jour de la disponibilité du livre
            livre.disponible = False
            
            # Commit de toutes les modifications
            db.commit()
            db.refresh(db_emprunt)
            
            return db_emprunt
            
        except HTTPException:
            # Re-raise les HTTPException
            raise
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création de l'emprunt"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur interne du serveur"
            )
    
    @staticmethod
    def retourner_livre(db: Session, livre_id: int) -> Optional[Livre]:
        """
        Remet un livre à disposition (fonctionnalité bonus)
        
        Args:
            db (Session): Session de base de données
            livre_id (int): ID du livre à remettre à disposition
            
        Returns:
            Optional[Livre]: Le livre mis à jour ou None si non trouvé
            
        Raises:
            HTTPException: En cas d'erreur de validation
        """
        # Vérification de l'existence du livre
        livre = LivreService.get_livre_by_id(db, livre_id)
        if not livre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Livre avec l'ID {livre_id} non trouvé"
            )
        
        # Vérification si le livre est déjà disponible
        if livre.disponible:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le livre '{livre.titre}' est déjà disponible"
            )
        
        try:
            # Mise à jour de la disponibilité du livre
            livre.disponible = True
            db.commit()
            db.refresh(livre)
            
            return livre
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur interne du serveur"
            )
