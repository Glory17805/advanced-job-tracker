from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE JOB
@router.post("/jobs")
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    new_job = models.Job(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

# GET ALL JOBS
@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

# GET SINGLE JOB
@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# UPDATE JOB
@router.put("/jobs/{job_id}")
def update_job(job_id: int, job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")

    db_job.title = job.title
    db_job.description = job.description
    db_job.location = job.location
    db_job.skills = job.skills

    db.commit()
    return {"message": "Job updated"}

# DELETE JOB
@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}

# SEARCH JOB
@router.get("/jobs/search")
def search_jobs(skill: str, location: str, db: Session = Depends(get_db)):
    return db.query(models.Job).filter(
        models.Job.skills.contains(skill),
        models.Job.location.contains(location)
    ).all()