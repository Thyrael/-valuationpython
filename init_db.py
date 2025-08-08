"""
Script d'initialisation de la base de données
Crée les tables et ajoute des données de test
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, create_tables
from app.models.livre import Livre
from app.models.emprunteur import Emprunteur


def init_db():
    """
    Initialise la base de données avec des données de test
    """
    print("🔧 Initialisation de la base de données...")
    
    # Création des tables
    create_tables()
    print("✅ Tables créées avec succès")
    
    # Création d'une session de base de données
    db = SessionLocal()
    
    try:
        # Suppression de tous les livres existants
        existing_livres = db.query(Livre).count()
        if existing_livres > 0:
            print(f"🗑️  Suppression de {existing_livres} livres existants...")
            db.query(Livre).delete()
            db.commit()
            print("✅ Livres supprimés avec succès")
        
        # Vérification si des emprunteurs existent déjà
        existing_emprunteurs = db.query(Emprunteur).count()
        
        if existing_emprunteurs == 0:
            # Ajout d'emprunteurs de test seulement s'il n'y en a pas
            emprunteurs_test = [
                Emprunteur(
                    nom="Jean Dupont",
                    email="jean.dupont@email.com"
                ),
                Emprunteur(
                    nom="Marie Martin",
                    email="marie.martin@email.com"
                ),
                Emprunteur(
                    nom="Pierre Durand",
                    email="pierre.durand@email.com"
                ),
                Emprunteur(
                    nom="Sophie Bernard",
                    email="sophie.bernard@email.com"
                ),
                Emprunteur(
                    nom="Lucas Petit",
                    email="lucas.petit@email.com"
                )
            ]
            
            for emprunteur in emprunteurs_test:
                db.add(emprunteur)
            
            print("✅ Emprunteurs ajoutés avec succès")
        
        # Ajout de NOUVEAUX livres de test
        nouveaux_livres = [
            Livre(
                titre="Les Misérables",
                auteur="Victor Hugo",
                annee_publication=1862,
                disponible=True
            ),
            Livre(
                titre="Don Quichotte",
                auteur="Miguel de Cervantes",
                annee_publication=1605,
                disponible=True
            ),
            Livre(
                titre="Madame Bovary",
                auteur="Gustave Flaubert",
                annee_publication=1857,
                disponible=True
            ),
            Livre(
                titre="L'Étranger",
                auteur="Albert Camus",
                annee_publication=1942,
                disponible=True
            ),
            Livre(
                titre="Le Comte de Monte-Cristo",
                auteur="Alexandre Dumas",
                annee_publication=1844,
                disponible=True
            ),
            Livre(
                titre="Anna Karénine",
                auteur="Léon Tolstoï",
                annee_publication=1877,
                disponible=True
            ),
            Livre(
                titre="Les Fleurs du Mal",
                auteur="Charles Baudelaire",
                annee_publication=1857,
                disponible=True
            ),
            Livre(
                titre="Germinal",
                auteur="Émile Zola",
                annee_publication=1885,
                disponible=True
            ),
            Livre(
                titre="Le Rouge et le Noir",
                auteur="Stendhal",
                annee_publication=1830,
                disponible=True
            ),
            Livre(
                titre="Notre-Dame de Paris",
                auteur="Victor Hugo",
                annee_publication=1831,
                disponible=True
            )
        ]
        
        for livre in nouveaux_livres:
            db.add(livre)
        
        # Commit des données
        db.commit()
        
        print("✅ Nouveaux livres ajoutés avec succès")
        print(f"   - {len(nouveaux_livres)} nouveaux livres ajoutés")
        print(f"   - {existing_emprunteurs} emprunteurs conservés")
        print("\n🎉 Mise à jour terminée !")
        print("📚 Vous pouvez maintenant lancer l'API avec : uv run uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
