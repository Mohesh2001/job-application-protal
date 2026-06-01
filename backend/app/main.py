import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import engine
from . import models
from .routes import auth, admin, student, recruiter

models.Base.metadata.create_all(bind=engine)
os.makedirs("uploads/resumes", exist_ok=True)

app = FastAPI(title="Job Portal API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(student.router)
app.include_router(recruiter.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/health")
def health():
    return {"status": "ok", "message": "Job Portal API is running"}
