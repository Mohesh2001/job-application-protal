import os
import shutil
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from bson import ObjectId
from pymongo.database import Database

from ..database import get_db
from ..models import to_oid, doc
from ..auth import require_role

router = APIRouter(prefix="/student", tags=["student"])
_student = require_role("Student")


# ── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def dashboard(db: Database = Depends(get_db), me = Depends(_student)):
    student_oid = to_oid(me.id)
    apps = list(db["applications"].find({"student_id": student_oid}))
    saved = db["saved_jobs"].count_documents({"student_id": student_oid})
    profile = db["student_profiles"].find_one({"user_id": student_oid})
    return {
        "applicationsSent": len(apps),
        "shortlisted":      sum(1 for a in apps if a.get("status") == "Shortlisted"),
        "savedJobs":        saved,
        "profileStrength":  profile.get("profile_strength", 0) if profile else 0,
    }


# ── Profile ───────────────────────────────────────────────────────────────────

@router.get("/profile")
def get_profile(db: Database = Depends(get_db), me = Depends(_student)):
    profile = db["student_profiles"].find_one({"user_id": to_oid(me.id)})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    user = db["users"].find_one({"_id": to_oid(me.id)})
    skills = profile.get("skills", [])
    return {
        "id":              str(user["_id"]),
        "name":            user["name"],
        "email":           user["email"],
        "phone":           profile.get("phone"),
        "college":         profile.get("college"),
        "degree":          profile.get("degree"),
        "graduationYear":  str(profile.get("graduation_year")) if profile.get("graduation_year") else "",
        "linkedin":        profile.get("linkedin_url") or "",
        "resumeUrl":       profile.get("resume_url") or "",
        "profileStrength": profile.get("profile_strength", 0),
        "skills":          skills,
    }


@router.put("/profile")
def update_profile(payload: dict, db: Database = Depends(get_db), me = Depends(_student)):
    user_oid = to_oid(me.id)
    if "name" in payload:
        db["users"].update_one({"_id": user_oid}, {"$set": {"name": payload["name"]}})

    # map incoming fields to profile document keys
    field_map = {
        "phone":          "phone",
        "college":        "college",
        "degree":         "degree",
        "graduationYear": "graduation_year",
        "linkedin":       "linkedin_url",
        "resumeUrl":      "resume_url",
    }
    updates = {}
    for fk, dk in field_map.items():
        if fk in payload:
            updates[dk] = payload[fk]

    if "skills" in payload and isinstance(payload["skills"], list):
        updates["skills"] = payload["skills"]

    if updates:
        updates["updated_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        db["student_profiles"].update_one({"user_id": user_oid}, {"$set": updates}, upsert=True)

    return {"ok": True}


@router.post("/profile/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Database = Depends(get_db),
    me = Depends(_student),
):
    ext = file.filename and file.filename.rsplit(".", 1)[-1].lower() or ""
    if ext not in ("pdf", "doc", "docx"):
        raise HTTPException(status_code=400, detail="Only PDF and DOC/DOCX files are allowed")

    import os, uuid
    filename = f"{me.id}_{uuid.uuid4().hex[:8]}.{ext}"
    save_path = os.path.join("uploads", "resumes", filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as f:
        f.write(await file.read())

    resume_url = f"http://localhost:8000/uploads/resumes/{filename}"

    user_oid = to_oid(me.id)
    db["student_profiles"].update_one({"user_id": user_oid}, {"$set": {"resume_url": resume_url}}, upsert=True)
    return {"resumeUrl": resume_url, "filename": file.filename}


# ── Jobs (browse approved) ────────────────────────────────────────────────────

@router.get("/jobs")
def browse_jobs(db: Database = Depends(get_db), me = Depends(_student)):
    jobs = list(db["jobs"].find({"status": "Approved"}))
    applied = db["applications"].find({"student_id": to_oid(me.id)})
    applied_ids = {a["job_id"] for a in applied}

    def j_out(j):
        return {
            "id":         str(j["_id"]),
            "title":      j.get("title"),
            "company":    j.get("company"),
            "type":       j.get("type"),
            "status":     j.get("status"),
            "applicants": db["applications"].count_documents({"job_id": j["_id"]}),
            "isApplied":  j["_id"] in applied_ids,
        }

    return [j_out(j) for j in jobs]


# ── Apply ─────────────────────────────────────────────────────────────────────

@router.post("/apply/{job_id}", status_code=201)
def apply(job_id: str, db: Database = Depends(get_db), me = Depends(_student)):
    job_oid = to_oid(job_id)
    if job_oid is None:
        raise HTTPException(status_code=404, detail="Job not found or not open")
    job = db["jobs"].find_one({"_id": job_oid, "status": "Approved"})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not open")
    if db["applications"].find_one({"student_id": to_oid(me.id), "job_id": job_oid}):
        raise HTTPException(status_code=400, detail="Already applied")

    app_doc = {"student_id": to_oid(me.id), "job_id": job_oid, "status": "Applied", "applied_date": __import__("datetime").datetime.now(__import__("datetime").timezone.utc)}
    res = db["applications"].insert_one(app_doc)
    app_doc["_id"] = res.inserted_id
    return {
        "id":          str(app_doc["_id"]),
        "job":         job.get("title"),
        "company":     job.get("company"),
        "type":        job.get("type"),
        "appliedDate": app_doc["applied_date"].strftime("%Y-%m-%d"),
        "status":      app_doc["status"],
    }


# ── My Applications ───────────────────────────────────────────────────────────

@router.get("/applications")
def my_applications(db: Database = Depends(get_db), me = Depends(_student)):
    apps = list(db["applications"].find({"student_id": to_oid(me.id)}))
    result = []
    for a in apps:
        job = db["jobs"].find_one({"_id": a["job_id"]})
        result.append({
            "id":          str(a["_id"]),
            "job":         job.get("title") if job else "",
            "company":     job.get("company") if job else "",
            "type":        job.get("type") if job else "",
            "appliedDate": a["applied_date"].strftime("%Y-%m-%d"),
            "status":      a.get("status"),
        })
    return result


# ── Saved Jobs ────────────────────────────────────────────────────────────────

@router.get("/saved-jobs")
def saved_jobs(db: Database = Depends(get_db), me = Depends(_student)):
    rows = list(db["saved_jobs"].find({"student_id": to_oid(me.id)}))
    result = []
    for s in rows:
        job = db["jobs"].find_one({"_id": s["job_id"]})
        result.append({
            "id":        str(job["_id"]) if job else "",
            "title":     job.get("title") if job else "",
            "company":   job.get("company") if job else "",
            "type":      job.get("type") if job else "",
            "status":    job.get("status") if job else "",
            "savedDate": s["saved_date"].strftime("%Y-%m-%d"),
        })
    return result


@router.post("/save/{job_id}", status_code=201)
def save_job(job_id: str, db: Database = Depends(get_db), me = Depends(_student)):
    job_oid = to_oid(job_id)
    if job_oid is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job = db["jobs"].find_one({"_id": job_oid})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if db["saved_jobs"].find_one({"student_id": to_oid(me.id), "job_id": job["_id"]}):
        return {"ok": True}
    saved = {"student_id": to_oid(me.id), "job_id": job["_id"], "saved_date": __import__("datetime").datetime.now(__import__("datetime").timezone.utc)}
    res = db["saved_jobs"].insert_one(saved)
    saved["_id"] = res.inserted_id
    return {
        "id":        str(job["_id"]),
        "title":     job.get("title"),
        "company":   job.get("company"),
        "type":      job.get("type"),
        "status":    job.get("status"),
        "savedDate": saved["saved_date"].strftime("%Y-%m-%d"),
    }


@router.delete("/saved/{job_id}")
def remove_saved(job_id: str, db: Database = Depends(get_db), me = Depends(_student)):
    job_oid = to_oid(job_id)
    if job_oid is None:
        raise HTTPException(status_code=404, detail="Not found")
    result = db["saved_jobs"].delete_one({"student_id": to_oid(me.id), "job_id": job_oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"ok": True}
