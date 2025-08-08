"""
Service pour la gestion des livres
Contient toute la logique métier pour les opérations CRUD sur les livres
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.livre import Livre
from app.schemas.livre import LivreCreateDTO, LivreUpdateDTO


class LivreService:
    """
    Service pour la gestion des livres
    Encapsule toute la logique métier pour les opérations sur les livres
    """
    
    @staticmethod
    def get_livres(db: Session, skip: int = 0, limit: int = 100) -> List[Livre]:
        """
        Récupère tous les livres avec pagination
        
        Args:
            db (Session): Session de base de données
            skip (int): Nombre d'enregistrements à ignorer (pour la pagination)
            limit (int): Nombre maximum d'enregistrements à retourner
            
        Returns:
            List[Livre]: Liste des livres
        """
        return db.query(Livre).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_livre_by_id(db: Session, livre_id: int) -> Optional[Livre]:
        """
        Récupère un livre par son ID
        
        Args:
            db (Session): Session de base de données
            livre_id (int): ID du livre à récupérer
            
        Returns:
            Optional[Livre]: Le livre trouvé ou None
        """
        return db.query(Livre).filter(Livre.id == livre_id).first()
    
    @staticmethod
    def create_livre(db: Session, livre_data: LivreCreateDTO) -> Livre:
        """
        Crée un nouveau livre
        
        Args:
            db (Session): Session de base de données
            livre_data (LivreCreateDTO): Données du livre à créer
            
        Returns:
            Livre: Le livre créé
            
        Raises:
            HTTPException: En cas d'erreur de validation ou de base de données
        """
        try:
            # Création du nouveau livre
            db_livre = Livre(
                titre=livre_data.titre,
                auteur=livre_data.auteur,
                annee_publication=livre_data.annee_publication,
                disponible=True  # Par défaut, un nouveau livre est disponible
            )
            
            # Sauvegarde en base
            db.add(db_livre)
            db.commit()
            db.refresh(db_livre)
            
            return db_livre
            
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création du livre"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur interne du serveur"
            )
    
    @staticmethod
    def update_livre(db: Session, livre_id: int, livre_data: LivreUpdateDTO) -> Optional[Livre]:
        """
        Met à jour un livre existant
        
        Args:
            db (Session): Session de base de données
            livre_id (int): ID du livre à mettre à jour
            livre_data (LivreUpdateDTO): Nouvelles données du livre
            
        Returns:
            Optional[Livre]: Le livre mis à jour ou None si non trouvé
            
        Raises:
            HTTPException: En cas d'erreur de validation ou de base de données
        """
        # Récupération du livre
        db_livre = LivreService.get_livre_by_id(db, livre_id)
        if not db_livre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Livre avec l'ID {livre_id} non trouvé"
            )
        
        try:
            # Mise à jour des champs fournis
            update_data = livre_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_livre, field, value)
            
            # Sauvegarde en base
            db.commit()
            db.refresh(db_livre)
            
            return db_livre
            
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la mise à jour du livre"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur interne du serveur"
            )
    
    @staticmethod
    def delete_livre(db: Session, livre_id: int) -> bool:
        """
        Supprime un livre
        
        Args:
            db (Session): Session de base de données
            livre_id (int): ID du livre à supprimer
            
        Returns:
            bool: True si le livre a été supprimé, False sinon
            
        Raises:
            HTTPException: En cas d'erreur de base de données
        """
        # Récupération du livre
        db_livre = LivreService.get_livre_by_id(db, livre_id)
        if not db_livre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Livre avec l'ID {livre_id} non trouvé"
            )
        
        try:
            # Suppression du livre
            db.delete(db_livre)
            db.commit()
            
            return True
            
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de supprimer ce livre (probablement emprunté)"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur interne du serveur"
            )
    
    @staticmethod
    def set_livre_disponibilite(db: Session, livre_id: int, disponible: bool) -> Optional[Livre]:
        """
        Met à jour la disponibilité d'un livre
        
        Args:
            db (Session): Session de base de données
            livre_id (int): ID du livre
            disponible (bool): Nouvelle disponibilité
            
        Returns:
            Optional[Livre]: Le livre mis à jour ou None si non trouvé
        """
        db_livre = LivreService.get_livre_by_id(db, livre_id)
        if not db_livre:
            return None
        
        db_livre.disponible = disponible
        db.commit()
        db.refresh(db_livre)
        
        return db_livre
