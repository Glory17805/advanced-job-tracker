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

@router.post("/jobs")
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    new_job = models.Job(**job.dict())
    db.add(new_job)
    db.commit()
    return new_job

@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()