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