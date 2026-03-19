from fastapi import APIRouter, UploadFile, BackgroundTasks
from app.services.pipeline_service import process_dataset

router = APIRouter()

@router.post("/upload")
async def upload_dataset(file: UploadFile, background_tasks: BackgroundTasks):
    result = await process_dataset(file, background_tasks)
    return result

@router.get("/history")
async def get_processing_history():
    from app.db.session import SessionLocal
    from app.models.database_models import ProcessingHistory
    db = SessionLocal()
    try:
        history = db.query(ProcessingHistory).order_by(ProcessingHistory.processed_at.desc()).all()
        return history
    finally:
        db.close()
