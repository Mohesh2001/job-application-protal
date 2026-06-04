from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from pymongo.database import Database

from ..database import get_db
from ..models import to_oid, doc
from ..auth import require_role

router = APIRouter(prefix="/recruiter", tags=["recruiter"])
_recruiter = require_role("Recruiter")


def _job_dict(j: dict, db: Database) -> dict:
    return {
        "id":         str(j["_id"]),
        "title":      j.get("title"),
        "company":    j.get("company"),
        "type":       j.get("type"),
        "status":     j.get("status"),
        "applicants": db["applications"].count_documents({"job_id": j["_id"]}),
        "deadline":   str(j.get("deadline")) if j.get("deadline") else None,
    }


# ── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def dashboard(db: Database = Depends(get_db), me = Depends(_recruiter)):
    recruiter_oid = to_oid(me.id)
    jobs = list(db["jobs"].find({"recruiter_id": recruiter_oid}))
    job_ids = [j["_id"] for j in jobs]
    apps = list(db["applications"].find({"job_id": {"$in": job_ids}})) if job_ids else []
    return {
        "activeJobs":      sum(1 for j in jobs if j.get("status") == "Approved"),
        "totalApplicants": len(apps),
        "shortlisted":     sum(1 for a in apps if a.get("status") == "Shortlisted"),
        "pendingApproval": sum(1 for j in jobs if j.get("status") == "Pending"),
    }


# ── Jobs ──────────────────────────────────────────────────────────────────────

@router.get("/jobs")
def list_jobs(db: Database = Depends(get_db), me = Depends(_recruiter)):
    recruiter_oid = to_oid(me.id)
    jobs = list(db["jobs"].find({"recruiter_id": recruiter_oid}))
    return [_job_dict(j, db) for j in jobs]


@router.post("/jobs", status_code=201)
def post_job(payload: dict, db: Database = Depends(get_db), me = Depends(_recruiter)):
    recruiter_oid = to_oid(me.id)
    company_doc = db["companies"].find_one({"user_id": recruiter_oid})
    job_doc = {
        "recruiter_id": recruiter_oid,
        "title": payload.get("title", ""),
        "company": payload.get("company", company_doc.get("name") if company_doc else me.name),
        "type": payload.get("type", "Full-time"),
        "status": "Pending",
        "category": payload.get("category"),
        "skills": payload.get("skills", []),
        "description": payload.get("description", ""),
        "location": payload.get("location", ""),
        "deadline": payload.get("deadline") or None,
        "created_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc),
        "updated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc),
    }
    res = db["jobs"].insert_one(job_doc)
    job_doc["_id"] = res.inserted_id
    return _job_dict(job_doc, db)


@router.put("/jobs/{job_id}")
def update_job(job_id: str, payload: dict, db: Database = Depends(get_db), me = Depends(_recruiter)):
    job_oid = to_oid(job_id)
    recruiter_oid = to_oid(me.id)
    job = db["jobs"].find_one({"_id": job_oid, "recruiter_id": recruiter_oid})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    updates = {k: payload[k] for k in ["title", "company", "type", "status"] if k in payload}
    if updates:
        updates["updated_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        db["jobs"].update_one({"_id": job_oid}, {"$set": updates})
        job.update(updates)
    return _job_dict(job, db)


@router.delete("/jobs/{job_id}")
def delete_job(job_id: str, db: Database = Depends(get_db), me = Depends(_recruiter)):
    job_oid = to_oid(job_id)
    if job_oid is None:
        raise HTTPException(status_code=404, detail="Job not found")
    recruiter_oid = to_oid(me.id)
    result = db["jobs"].delete_one({"_id": job_oid, "recruiter_id": recruiter_oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"ok": True}


# ── Applicants ───────────────────────────────────────────────────────────────

@router.get("/applicants")
def list_applicants(db: Database = Depends(get_db), me = Depends(_recruiter)):
    recruiter_oid = to_oid(me.id)
    jobs = list(db["jobs"].find({"recruiter_id": recruiter_oid}))
    job_ids = [j["_id"] for j in jobs]
    if not job_ids:
        return []
    apps = list(db["applications"].find({"job_id": {"$in": job_ids}}))
    result = []
    for a in apps:
        student = db["users"].find_one({"_id": a["student_id"]})
        job = db["jobs"].find_one({"_id": a["job_id"]})
        result.append({
            "id": str(a["_id"]),
            "student": student["name"] if student else "",
            "job": job["title"] if job else "",
            "college": (db["student_profiles"].find_one({"user_id": a["student_id"]}) or {}).get("college"),
            "appliedDate": a["applied_date"].strftime("%Y-%m-%d") if a.get("applied_date") else None,
            "status": a.get("status"),
        })
    return result


@router.patch("/applicants/{app_id}/shortlist")
def shortlist(app_id: str, db: Database = Depends(get_db), me = Depends(_recruiter)):
    app_oid = to_oid(app_id)
    if app_oid is None:
        raise HTTPException(status_code=404, detail="Application not found")
    app = db["applications"].find_one({"_id": app_oid})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    job = db["jobs"].find_one({"_id": app["job_id"]})
    if not job or job.get("recruiter_id") != to_oid(me.id):
        raise HTTPException(status_code=404, detail="Application not found")
    db["applications"].update_one({"_id": app_oid}, {"$set": {"status": "Shortlisted"}})
    return {"id": str(app_oid), "status": "Shortlisted"}


@router.patch("/applicants/{app_id}/reject")
def reject(app_id: str, db: Database = Depends(get_db), me = Depends(_recruiter)):
    app_oid = to_oid(app_id)
    if app_oid is None:
        raise HTTPException(status_code=404, detail="Application not found")
    app = db["applications"].find_one({"_id": app_oid})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    job = db["jobs"].find_one({"_id": app["job_id"]})
    if not job or job.get("recruiter_id") != to_oid(me.id):
        raise HTTPException(status_code=404, detail="Application not found")
    db["applications"].update_one({"_id": app_oid}, {"$set": {"status": "Rejected"}})
    return {"id": str(app_oid), "status": "Rejected"}


# ── Company Profile ───────────────────────────────────────────────────────────

@router.get("/company")
def get_company(db: Database = Depends(get_db), me = Depends(_recruiter)):
    c = db["companies"].find_one({"user_id": to_oid(me.id)})
    if not c:
        return {"name": "", "industry": "", "website": "", "location": "", "about": ""}
    return {"name": c.get("name", ""), "industry": c.get("industry", ""), "website": c.get("website", ""),
            "location": c.get("location", ""), "about": c.get("about", "")}


@router.put("/company")
def update_company(payload: dict, db: Database = Depends(get_db), me = Depends(_recruiter)):
    user_oid = to_oid(me.id)
    c = db["companies"].find_one({"user_id": user_oid})
    updates = {k: payload[k] for k in ["name", "industry", "website", "location", "about"] if k in payload}
    if not c:
        updates["user_id"] = user_oid
        db["companies"].insert_one(updates)
    else:
        if updates:
            db["companies"].update_one({"_id": c["_id"]}, {"$set": updates})
    return {"ok": True}
