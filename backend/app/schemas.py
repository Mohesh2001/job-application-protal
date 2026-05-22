from typing import List, Optional
from pydantic import BaseModel


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserInfo(BaseModel):
    id: int
    name: str
    email: str
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo


# ── Users ─────────────────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    status: str
    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    name: str
    email: str
    password: Optional[str] = "Welcome@123"
    role: str
    status: str = "Active"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None


# ── Jobs ──────────────────────────────────────────────────────────────────────

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    type: str
    status: str
    applicants: int = 0
    deadline: Optional[str] = None
    model_config = {"from_attributes": True}

class JobCreate(BaseModel):
    title: str
    company: str
    type: str = "Full-time"
    status: str = "Pending"
    skills: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    deadline: Optional[str] = None
    category: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    applicants: Optional[int] = None


# ── Content ───────────────────────────────────────────────────────────────────

class ContentItem(BaseModel):
    id: int
    type: str
    name: str

class ContentCreate(BaseModel):
    type: str
    name: str

class ContentUpdate(BaseModel):
    name: str
