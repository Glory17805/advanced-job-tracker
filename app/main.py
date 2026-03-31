from job_portal_project.app.database import Base, engine
from app import models

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advanced Job Tracker API")

# Include routers
app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "FastAPI Job Tracker Running Successfully"}
app.include_router(jobs.router)
app.include_router(applications.router)
