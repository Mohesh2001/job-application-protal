from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from ..database import get_db
from ..models import to_oid
from ..schemas import UserCreate, UserUpdate, ContentCreate, ContentUpdate
from ..auth import require_role, hash_password

router = APIRouter(prefix="/admin", tags=["admin"])
_admin = require_role("Admin")


def _user_out(u: dict) -> dict:
    return {
        "id": str(u["_id"]),
        "name": u["name"],
        "email": u["email"],
        "role": u["role"],
        "status": u["status"],
    }


def _job_out(j: dict, db: Database) -> dict:
    return {
        "id": str(j["_id"]),
        "title": j["title"],
        "company": j["company"],
        "type": j["type"],
        "status": j["status"],
        "applicants": db["applications"].count_documents({"job_id": j["_id"]}),
        "deadline": str(j["deadline"]) if j.get("deadline") else None,
    }


# ── Dashboard ─────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def dashboard(db: Database = Depends(get_db), _=Depends(_admin)):
    return {
        "totalUsers":   db["users"].count_documents({"role": {"$ne": "Admin"}}),
        "students":     db["users"].count_documents({"role": "Student"}),
        "recruiters":   db["users"].count_documents({"role": "Recruiter"}),
        "activeJobs":   db["jobs"].count_documents({"status": {"$in": ["Approved", "Pending"]}}),
        "applications": db["applications"].count_documents({}),
    }


# ── Users ─────────────────────────────────────────────────────────────────────

@router.get("/users")
def list_users(db: Database = Depends(get_db), _=Depends(_admin)):
    return [_user_out(u) for u in db["users"].find()]


@router.post("/users", status_code=201)
def create_user(payload: UserCreate, db: Database = Depends(get_db), _=Depends(_admin)):
    if db["users"].find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    now = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    user_doc = {
        "name": payload.name,
        "email": payload.email,
        "password_hash": hash_password(payload.password or "Welcome@123"),
        "role": payload.role,
        "status": payload.status,
        "created_at": now,
        "updated_at": now,
    }
    result = db["users"].insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return _user_out(user_doc)


@router.put("/users/{user_id}")
def update_user(user_id: str, payload: UserUpdate, db: Database = Depends(get_db), _=Depends(_admin)):
    oid = to_oid(user_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="User not found")
    updates = {k: v for k, v in payload.model_dump(exclude_none=True).items()}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    updates["updated_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    result = db["users"].find_one_and_update(
        {"_id": oid},
        {"$set": updates},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_out(result)


@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Database = Depends(get_db), _=Depends(_admin)):
    oid = to_oid(user_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="User not found")
    result = db["users"].delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}


# ── Jobs ─────────────────────────────────────────────────────────────────────

@router.get("/jobs")
def list_jobs(db: Database = Depends(get_db), _=Depends(_admin)):
    return [_job_out(j, db) for j in db["jobs"].find()]


@router.put("/jobs/{job_id}")
def update_job(job_id: str, payload: dict, db: Database = Depends(get_db), _=Depends(_admin)):
    oid = to_oid(job_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="Job not found")
    updates = {k: payload[k] for k in ["title", "company", "type", "status"] if k in payload}
    result = db["jobs"].find_one_and_update(
        {"_id": oid},
        {"$set": updates},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return _job_out(result, db)


@router.delete("/jobs/{job_id}")
def delete_job(job_id: str, db: Database = Depends(get_db), _=Depends(_admin)):
    oid = to_oid(job_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="Job not found")
    result = db["jobs"].delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"ok": True}


@router.patch("/jobs/{job_id}/approve")
def approve_job(job_id: str, db: Database = Depends(get_db), _=Depends(_admin)):
    oid = to_oid(job_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="Not found")
    result = db["jobs"].find_one_and_update(
        {"_id": oid},
        {"$set": {"status": "Approved"}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return _job_out(result, db)


@router.patch("/jobs/{job_id}/reject")
def reject_job(job_id: str, db: Database = Depends(get_db), _=Depends(_admin)):
    oid = to_oid(job_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="Not found")
    result = db["jobs"].find_one_and_update(
        {"_id": oid},
        {"$set": {"status": "Rejected"}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return _job_out(result, db)


# ── Applications ─────────────────────────────────────────────────────────────

@router.get("/applications")
def list_applications(db: Database = Depends(get_db), _=Depends(_admin)):
    result = []
    for a in db["applications"].find():
        student = db["users"].find_one({"_id": a["student_id"]})
        job     = db["jobs"].find_one({"_id": a["job_id"]})
        result.append({
            "id":      str(a["_id"]),
            "student": student["name"] if student else "",
            "job":     job["title"]    if job else "",
            "company": job["company"]  if job else "",
            "status":  a["status"],
        })
    return result


# ── Content (categories + skills + tags) ─────────────────────────────────────

_COLL_MAP = {"Category": "categories", "Skill": "skills", "Tag": "tags"}


@router.get("/content")
def list_content(db: Database = Depends(get_db), _=Depends(_admin)):
    items = []
    for type_name, coll in _COLL_MAP.items():
        for item in db[coll].find():
            items.append({"id": str(item["_id"]), "type": type_name, "name": item["name"]})
    return items


@router.post("/content", status_code=201)
def create_content(payload: ContentCreate, db: Database = Depends(get_db), _=Depends(_admin)):
    coll = _COLL_MAP.get(payload.type)
    if not coll:
        raise HTTPException(status_code=400, detail="Invalid type")
    result = db[coll].insert_one({"name": payload.name})
    return {"id": str(result.inserted_id), "type": payload.type, "name": payload.name}


@router.put("/content/{content_type}/{item_id}")
def update_content(
    content_type: str, item_id: str, payload: ContentUpdate,
    db: Database = Depends(get_db), _=Depends(_admin),
):
    coll = _COLL_MAP.get(content_type)
    if not coll:
        raise HTTPException(status_code=400, detail="Invalid content type")
    oid = to_oid(item_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="Not found")
    result = db[coll].find_one_and_update(
        {"_id": oid},
        {"$set": {"name": payload.name}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": str(result["_id"]), "type": content_type, "name": result["name"]}


@router.delete("/content/{content_type}/{item_id}")
def delete_content(
    content_type: str, item_id: str,
    db: Database = Depends(get_db), _=Depends(_admin),
):
    coll = _COLL_MAP.get(content_type)
    if not coll:
        raise HTTPException(status_code=400, detail="Invalid content type")
    oid = to_oid(item_id)
    if oid is None:
        raise HTTPException(status_code=404, detail="Not found")
    result = db[coll].delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"ok": True}
