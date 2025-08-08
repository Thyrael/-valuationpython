"""
Service pour la gestion des emprunteurs
Contient toute la logique métier pour les opérations sur les emprunteurs
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.emprunteur import Emprunteur
from app.models.emprunt import Emprunt
from app.schemas.emprunteur import EmprunteurCreateDTO


class EmprunteurService:
    """
    Service pour la gestion des emprunteurs
    Encapsule toute la logique métier pour les opérations sur les emprunteurs
    """
    
    @staticmethod
    def get_emprunteurs(db: Session, skip: int = 0, limit: int = 100) -> List[Emprunteur]:
        """
        Récupère tous les emprunteurs avec pagination
        
        Args:
            db (Session): Session de base de données
            skip (int): Nombre d'enregistrements à ignorer (pour la pagination)
            limit (int): Nombre maximum d'enregistrements à retourner
            
        Returns:
            List[Emprunteur]: Liste des emprunteurs
        """
        return db.query(Emprunteur).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_emprunteur_by_id(db: Session, emprunteur_id: int) -> Optional[Emprunteur]:
        """
        Récupère un emprunteur par son ID
        
        Args:
            db (Session): Session de base de données
            emprunteur_id (int): ID de l'emprunteur à récupérer
            
        Returns:
            Optional[Emprunteur]: L'emprunteur trouvé ou None
        """
        return db.query(Emprunteur).filter(Emprunteur.id == emprunteur_id).first()
    
    @staticmethod
    def get_emprunteur_by_email(db: Session, email: str) -> Optional[Emprunteur]:
        """
        Récupère un emprunteur par son email
        
        Args:
            db (Session): Session de base de données
            email (str): Email de l'emprunteur à récupérer
            
        Returns:
            Optional[Emprunteur]: L'emprunteur trouvé ou None
        """
        return db.query(Emprunteur).filter(Emprunteur.email == email).first()
    
    @staticmethod
    def create_emprunteur(db: Session, emprunteur_data: EmprunteurCreateDTO) -> Emprunteur:
        """
        Crée un nouvel emprunteur
        
        Args:
            db (Session): Session de base de données
            emprunteur_data (EmprunteurCreateDTO): Données de l'emprunteur à créer
            
        Returns:
            Emprunteur: L'emprunteur créé
            
        Raises:
            HTTPException: En cas d'erreur de validation ou de base de données
        """
        try:
            # Vérification si l'email existe déjà
            existing_emprunteur = EmprunteurService.get_emprunteur_by_email(db, emprunteur_data.email)
            if existing_emprunteur:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Un emprunteur avec l'email {emprunteur_data.email} existe déjà"
                )
            
            # Création du nouvel emprunteur
            db_emprunteur = Emprunteur(
                nom=emprunteur_data.nom,
                email=emprunteur_data.email
            )
            
            # Sauvegarde en base
            db.add(db_emprunteur)
            db.commit()
            db.refresh(db_emprunteur)
            
            return db_emprunteur
            
        except HTTPException:
            # Re-raise les HTTPException
            raise
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création de l'emprunteur"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur interne du serveur"
            )

    @staticmethod
    def delete_emprunteur(db: Session, emprunteur_id: int):
        """
        Supprime un emprunteur de la bibliothèque
        
        Args:
            db (Session): Session de base de données
            emprunteur_id (int): Identifiant de l'emprunteur à supprimer
            
        Returns:
            dict: Message de confirmation avec l'ID de l'emprunteur supprimé
            
        Raises:
            HTTPException: Si l'emprunteur n'existe pas ou a des emprunts actifs
        """
        # Vérifier que l'emprunteur existe
        emprunteur = db.query(Emprunteur).filter(Emprunteur.id == emprunteur_id).first()
        if not emprunteur:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Emprunteur avec l'ID {emprunteur_id} non trouvé"
            )
        
        # Vérifier s'il a des emprunts actifs
        emprunts_actifs = db.query(Emprunt).filter(Emprunt.emprunteur_id == emprunteur_id).count()
        if emprunts_actifs > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Impossible de supprimer l'emprunteur {emprunteur_id} : il a {emprunts_actifs} emprunt(s) actif(s)"
            )
        
        # Supprimer l'emprunteur
        db.delete(emprunteur)
        db.commit()
        
        return {
            "message": "Emprunteur supprimé avec succès",
            "emprunteur_id": emprunteur_id
        }
