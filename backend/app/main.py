import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import db
from .routes import auth, admin, student, recruiter

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


@app.on_event("startup")
def create_indexes():
    db["users"].create_index("email", unique=True)
    db["applications"].create_index([("student_id", 1), ("job_id", 1)], unique=True)
    db["jobs"].create_index("status")
    db["saved_jobs"].create_index([("student_id", 1), ("job_id", 1)])


@app.get("/health")
def health():
    return {"status": "ok", "message": "Job Portal API is running"}


@app.get("/")
def home():
    return {"message": "Job Portal API is running"}
