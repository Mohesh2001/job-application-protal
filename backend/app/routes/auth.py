from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database

from ..database import get_db
from ..schemas import LoginRequest, RegisterRequest, TokenResponse, UserInfo
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Database = Depends(get_db)):
    user = db["users"].find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})
    return TokenResponse(
        access_token=token,
        user=UserInfo(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            role=user["role"],
        ),
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Database = Depends(get_db)):
    if payload.role not in ("Student", "Recruiter"):
        raise HTTPException(status_code=400, detail="Role must be Student or Recruiter")
    if db["users"].find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    now = datetime.now(timezone.utc)
    user_doc = {
        "name": payload.name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "role": payload.role,
        "status": "Active",
        "created_at": now,
        "updated_at": now,
    }
    result = db["users"].insert_one(user_doc)
    user_id = result.inserted_id

    if payload.role == "Student":
        db["student_profiles"].insert_one({
            "user_id": user_id,
            "phone": None,
            "college": None,
            "degree": None,
            "graduation_year": None,
            "linkedin_url": None,
            "resume_url": None,
            "profile_strength": 0,
            "skills": [],
        })
    else:
        db["companies"].insert_one({
            "user_id": user_id,
            "name": f"{payload.name}'s Company",
            "industry": None,
            "website": None,
            "location": None,
            "about": None,
        })

    return {"id": str(user_id), "name": payload.name, "email": payload.email, "role": payload.role}
