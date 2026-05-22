from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Job, Application, Company, Category
from ..auth import require_role

router = APIRouter(prefix="/recruiter", tags=["recruiter"])
_recruiter = require_role("Recruiter")


def _job_dict(j: Job) -> dict:
    return {
        "id":         j.id,
        "title":      j.title,
        "company":    j.company,
        "type":       j.type,
        "status":     j.status,
        "applicants": len(j.applications),
        "deadline":   str(j.deadline) if j.deadline else None,
    }


# ── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    jobs     = db.query(Job).filter(Job.recruiter_id == me.id).all()
    job_ids  = [j.id for j in jobs]
    apps     = (
        db.query(Application).filter(Application.job_id.in_(job_ids)).all()
        if job_ids else []
    )
    return {
        "activeJobs":      sum(1 for j in jobs if j.status == "Approved"),
        "totalApplicants": len(apps),
        "shortlisted":     sum(1 for a in apps if a.status == "Shortlisted"),
        "pendingApproval": sum(1 for j in jobs if j.status == "Pending"),
    }


# ── Jobs ──────────────────────────────────────────────────────────────────────

@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    return [_job_dict(j) for j in db.query(Job).filter(Job.recruiter_id == me.id).all()]


@router.post("/jobs", status_code=201)
def post_job(payload: dict, db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    company     = db.query(Company).filter(Company.user_id == me.id).first()
    category_id = None
    if payload.get("category"):
        cat = db.query(Category).filter(Category.name == payload["category"]).first()
        if cat:
            category_id = cat.id

    job = Job(
        recruiter_id    = me.id,
        title           = payload.get("title", ""),
        company         = payload.get("company", company.name if company else me.name),
        type            = payload.get("type", "Full-time"),
        status          = "Pending",
        category_id     = category_id,
        skills_required = payload.get("skills", ""),
        description     = payload.get("description", ""),
        location        = payload.get("location", ""),
        deadline        = payload.get("deadline") or None,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return _job_dict(job)


@router.put("/jobs/{job_id}")
def update_job(job_id: int, payload: dict, db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    job = db.query(Job).filter(Job.id == job_id, Job.recruiter_id == me.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field in ["title", "company", "type", "status"]:
        if field in payload:
            setattr(job, field, payload[field])
    db.commit()
    return _job_dict(job)


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    job = db.query(Job).filter(Job.id == job_id, Job.recruiter_id == me.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"ok": True}


# ── Applicants ────────────────────────────────────────────────────────────────

@router.get("/applicants")
def list_applicants(db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    job_ids = [j.id for j in db.query(Job).filter(Job.recruiter_id == me.id).all()]
    if not job_ids:
        return []
    apps = db.query(Application).filter(Application.job_id.in_(job_ids)).all()
    return [
        {
            "id":          a.id,
            "student":     a.student.name,
            "job":         a.job.title,
            "college":     a.student.student_profile.college if a.student.student_profile else None,
            "appliedDate": a.applied_date.strftime("%Y-%m-%d"),
            "status":      a.status,
        }
        for a in apps
    ]


@router.patch("/applicants/{app_id}/shortlist")
def shortlist(app_id: int, db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app or app.job.recruiter_id != me.id:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = "Shortlisted"
    db.commit()
    return {"id": app.id, "status": "Shortlisted"}


@router.patch("/applicants/{app_id}/reject")
def reject(app_id: int, db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app or app.job.recruiter_id != me.id:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = "Rejected"
    db.commit()
    return {"id": app.id, "status": "Rejected"}


# ── Company Profile ───────────────────────────────────────────────────────────

@router.get("/company")
def get_company(db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    c = db.query(Company).filter(Company.user_id == me.id).first()
    if not c:
        return {"name": "", "industry": "", "website": "", "location": "", "about": ""}
    return {"name": c.name, "industry": c.industry or "", "website": c.website or "",
            "location": c.location or "", "about": c.about or ""}


@router.put("/company")
def update_company(payload: dict, db: Session = Depends(get_db), me: User = Depends(_recruiter)):
    c = db.query(Company).filter(Company.user_id == me.id).first()
    if not c:
        c = Company(user_id=me.id, name=payload.get("name", ""))
        db.add(c)
    for field in ["name", "industry", "website", "location", "about"]:
        if field in payload:
            setattr(c, field, payload[field])
    db.commit()
    return {"ok": True}
