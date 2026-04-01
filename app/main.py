from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app.routers import user
from app import models, schemas
from app.routers import jobs, applications

# Create FastAPI app
app = FastAPI(title="Advanced Job Tracker API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)

# Include existing routers (auth)
app.include_router(user.router)

# Home route
@app.get("/")
def home():
    return {"message": "FastAPI Job Tracker Running Successfully"}

# Include routes
app.include_router(jobs.router)
app.include_router(applications.router)

@app.get("/")
def home():
    return {"message": "Job Portal Backend Running"}


# =========================
# ✅ POST: Upload Resume
# =========================
@app.post("/resume")
def upload_resume(resume: schemas.ResumeCreate, db: Session = Depends(get_db)):
    new_resume = models.Resume(
        user_id=resume.user_id,
        resume_link=resume.resume_link
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "message": "Resume uploaded successfully",
        "user_id": new_resume.user_id,
        "resume_link": new_resume.resume_link
    }


# =========================
# ✅ GET: Fetch Resume
# =========================
@app.get("/resume/{user_id}")
def get_resume(user_id: int, db: Session = Depends(get_db)):
    resume = db.query(models.Resume).filter(models.Resume.user_id == user_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return {
        "user_id": resume.user_id,
        "resume_link": resume.resume_link
    }
