from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Job, Application, Category, Skill, Tag
from ..schemas import UserOut, UserCreate, UserUpdate, ContentItem, ContentCreate, ContentUpdate
from ..auth import require_role, hash_password

router = APIRouter(prefix="/admin", tags=["admin"])
_admin = require_role("Admin")


def _job_dict(j: Job) -> dict:
    return {
        "id": j.id,
        "title": j.title,
        "company": j.company,
        "type": j.type,
        "status": j.status,
        "applicants": len(j.applications),
        "deadline": str(j.deadline) if j.deadline else None,
    }


# ── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(_admin)):
    return {
        "totalUsers":   db.query(User).filter(User.role != "Admin").count(),
        "students":     db.query(User).filter(User.role == "Student").count(),
        "recruiters":   db.query(User).filter(User.role == "Recruiter").count(),
        "activeJobs":   db.query(Job).filter(Job.status.in_(["Approved", "Pending"])).count(),
        "applications": db.query(Application).count(),
    }


# ── Users ────────────────────────────────────────────────────────────────────

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), _=Depends(_admin)):
    return db.query(User).all()


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _=Depends(_admin)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password or "Welcome@123"),
        role=payload.role,
        status=payload.status,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), _=Depends(_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}


# ── Jobs ─────────────────────────────────────────────────────────────────────

@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db), _=Depends(_admin)):
    return [_job_dict(j) for j in db.query(Job).all()]


@router.put("/jobs/{job_id}")
def update_job(job_id: int, payload: dict, db: Session = Depends(get_db), _=Depends(_admin)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field in ["title", "company", "type", "status"]:
        if field in payload:
            setattr(job, field, payload[field])
    db.commit()
    return _job_dict(job)


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), _=Depends(_admin)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"ok": True}


@router.patch("/jobs/{job_id}/approve")
def approve_job(job_id: int, db: Session = Depends(get_db), _=Depends(_admin)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Not found")
    job.status = "Approved"
    db.commit()
    return _job_dict(job)


@router.patch("/jobs/{job_id}/reject")
def reject_job(job_id: int, db: Session = Depends(get_db), _=Depends(_admin)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Not found")
    job.status = "Rejected"
    db.commit()
    return _job_dict(job)


# ── Applications ─────────────────────────────────────────────────────────────

@router.get("/applications")
def list_applications(db: Session = Depends(get_db), _=Depends(_admin)):
    return [
        {
            "id": a.id,
            "student": a.student.name,
            "job": a.job.title,
            "company": a.job.company,
            "status": a.status,
        }
        for a in db.query(Application).all()
    ]


# ── Content (categories + skills + tags) ─────────────────────────────────────

@router.get("/content", response_model=List[ContentItem])
def list_content(db: Session = Depends(get_db), _=Depends(_admin)):
    items = []
    for c in db.query(Category).all():
        items.append({"id": c.id, "type": "Category", "name": c.name})
    for s in db.query(Skill).all():
        items.append({"id": s.id, "type": "Skill", "name": s.name})
    for t in db.query(Tag).all():
        items.append({"id": t.id, "type": "Tag", "name": t.name})
    return items


@router.post("/content", response_model=ContentItem, status_code=201)
def create_content(payload: ContentCreate, db: Session = Depends(get_db), _=Depends(_admin)):
    model_map = {"Category": Category, "Skill": Skill, "Tag": Tag}
    model = model_map.get(payload.type)
    if not model:
        raise HTTPException(status_code=400, detail="Invalid type")
    item = model(name=payload.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "type": payload.type, "name": item.name}


@router.put("/content/{content_type}/{item_id}", response_model=ContentItem)
def update_content(
    content_type: str, item_id: int, payload: ContentUpdate,
    db: Session = Depends(get_db), _=Depends(_admin),
):
    model_map = {"Category": Category, "Skill": Skill, "Tag": Tag}
    model = model_map.get(content_type)
    if not model:
        raise HTTPException(status_code=400, detail="Invalid content type")
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    item.name = payload.name
    db.commit()
    return {"id": item.id, "type": content_type, "name": item.name}


@router.delete("/content/{content_type}/{item_id}")
def delete_content(
    content_type: str, item_id: int,
    db: Session = Depends(get_db), _=Depends(_admin),
):
    model_map = {"Category": Category, "Skill": Skill, "Tag": Tag}
    model = model_map.get(content_type)
    if not model:
        raise HTTPException(status_code=400, detail="Invalid content type")
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
