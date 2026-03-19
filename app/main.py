from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.blockchain_routes import router as blockchain_router
from app.api.auth_routes import router as auth_router
from app.api.investigation_routes import router as investigation_router

from app.db.session import engine, Base
import app.models.database_models # Ensure models are loaded

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Money Muling Detection API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; refine for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register API routes
app.include_router(router, tags=["Dataset"])
app.include_router(blockchain_router, prefix="/blockchain", tags=["Blockchain"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(investigation_router, prefix="/investigation", tags=["Investigation"])


@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/reset")
def reset_system():
    from app.db.session import engine, Base
    import app.models.database_models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "system reset complete"}

@app.get("/stats")
def get_stats():
    from app.db.session import SessionLocal
    from app.models.database_models import Transaction, SuspiciousAccount, AccountMapping
    db = SessionLocal()
    try:
        analyzed = db.query(Transaction).count()
        suspicious = db.query(SuspiciousAccount).count()
        # For simplicity, we'll use a fixed uptime for now or a calculation
        return {
            "analyzed": analyzed,
            "suspicious": suspicious,
            "onChain": suspicious, # In this prototype, each detection is logged
            "uptime": "99.9%"
        }
    finally:
        db.close()