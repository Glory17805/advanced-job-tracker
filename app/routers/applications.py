from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs/{job_id}/apply")
def apply_job(job_id: int, data: schemas.ApplyJob, db: Session = Depends(get_db)):
    app = models.Application(
        job_id=job_id,
        resume_link=data.resume_link
    )
    db.add(app)
    db.commit()
    return {"message": "Applied"}