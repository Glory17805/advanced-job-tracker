from pydantic import BaseModel, EmailStr,  HttpUrl

class ResumeCreate(BaseModel):
    user_id: int
    resume_link: HttpUrl   # ✅ ensures valid URL

class ResumeCreate(BaseModel):
    user_id: int
    resume_link: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    skills: str

class ApplyJob(BaseModel):
    resume_link: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
