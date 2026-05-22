from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, StudentProfile, Company
from ..schemas import LoginRequest, RegisterRequest, TokenResponse, UserInfo
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_access_token({"sub": user.id, "role": user.role})
    return TokenResponse(
        access_token=token,
        user=UserInfo(id=user.id, name=user.name, email=user.email, role=user.role),
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.role not in ("Student", "Recruiter"):
        raise HTTPException(status_code=400, detail="Role must be Student or Recruiter")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        status="Active",
    )
    db.add(user)
    db.flush()

    if payload.role == "Student":
        db.add(StudentProfile(user_id=user.id))
    else:
        db.add(Company(user_id=user.id, name=f"{payload.name}'s Company"))

    db.commit()
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
