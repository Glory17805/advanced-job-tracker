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

# APPLY JOB
@router.post("/jobs/{job_id}/apply")
def apply_job(job_id: int, data: schemas.ApplyJob, db: Session = Depends(get_db)):
    application = models.Application(
        job_id=job_id,
        resume_link=data.resume_link
    )
    db.add(application)
    db.commit()
    return {"message": "Applied successfully"}

# VIEW APPLICATIONS
@router.get("/applications")
def get_applications(db: Session = Depends(get_db)):
    return db.query(models.Application).all()