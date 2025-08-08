"""
Point d'entrée principal de l'API de gestion de bibliothèque
Configuration FastAPI et inclusion de tous les routers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables
from app.routers import livres, emprunteurs, emprunts

# Création de l'application FastAPI
app = FastAPI(
    title="API de Gestion de Bibliothèque",
    description="API RESTful pour la gestion d'une bibliothèque avec FastAPI et SQLAlchemy",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Événement de démarrage de l'application
    Crée les tables de la base de données si elles n'existent pas
    """
    create_tables()


@app.get("/", summary="Page d'accueil")
async def root():
    """
    Endpoint racine de l'API
    
    Returns:
        dict: Informations sur l'API
    """
    return {
        "message": "Bienvenue dans l'API de Gestion de Bibliothèque",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "livres": "/livres",
            "emprunteurs": "/emprunteurs",
            "emprunts": "/emprunts"
        }
    }


@app.get("/health", summary="Vérification de l'état de l'API")
async def health_check():
    """
    Endpoint de vérification de l'état de l'API
    
    Returns:
        dict: État de l'API
    """
    return {
        "status": "healthy",
        "message": "L'API fonctionne correctement"
    }


# Inclusion des routers
app.include_router(livres.router)
app.include_router(emprunteurs.router)
app.include_router(emprunts.router)


if __name__ == "__main__":
    """
    Point d'entrée pour l'exécution directe du script
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
