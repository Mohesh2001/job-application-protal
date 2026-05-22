import os
import shutil
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Job, Application, SavedJob, StudentProfile, Skill, StudentSkill
from ..auth import require_role

router = APIRouter(prefix="/student", tags=["student"])
_student = require_role("Student")


# ── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), me: User = Depends(_student)):
    apps    = db.query(Application).filter(Application.student_id == me.id).all()
    saved   = db.query(SavedJob).filter(SavedJob.student_id == me.id).count()
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == me.id).first()
    return {
        "applicationsSent": len(apps),
        "shortlisted":      sum(1 for a in apps if a.status == "Shortlisted"),
        "savedJobs":        saved,
        "profileStrength":  profile.profile_strength if profile else 0,
    }


# ── Profile ───────────────────────────────────────────────────────────────────

@router.get("/profile")
def get_profile(db: Session = Depends(get_db), me: User = Depends(_student)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == me.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    skills = [ss.skill.name for ss in profile.student_skills]
    return {
        "id":              me.id,
        "name":            me.name,
        "email":           me.email,
        "phone":           profile.phone,
        "college":         profile.college,
        "degree":          profile.degree,
        "graduationYear":  str(profile.graduation_year) if profile.graduation_year else "",
        "linkedin":        profile.linkedin_url or "",
        "resumeUrl":       profile.resume_url or "",
        "profileStrength": profile.profile_strength,
        "skills":          skills,
    }


@router.put("/profile")
def update_profile(payload: dict, db: Session = Depends(get_db), me: User = Depends(_student)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == me.id).first()
    if not profile:
        profile = StudentProfile(user_id=me.id)
        db.add(profile)
        db.flush()

    if "name" in payload:
        me.name = payload["name"]

    field_map = {
        "phone":          "phone",
        "college":        "college",
        "degree":         "degree",
        "graduationYear": "graduation_year",
        "linkedin":       "linkedin_url",
        "resumeUrl":      "resume_url",
    }
    for fk, dk in field_map.items():
        if fk in payload:
            setattr(profile, dk, payload[fk])

    if "skills" in payload and isinstance(payload["skills"], list):
        db.query(StudentSkill).filter(StudentSkill.student_profile_id == profile.id).delete()
        for skill_name in payload["skills"]:
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.add(skill)
                db.flush()
            db.add(StudentSkill(student_profile_id=profile.id, skill_id=skill.id))

    db.commit()
    return {"ok": True}


@router.post("/profile/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    me: User = Depends(_student),
):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in (".pdf", ".doc", ".docx"):
        raise HTTPException(status_code=400, detail="Only PDF and DOC/DOCX files are allowed")

    filename = f"{me.id}_{uuid.uuid4().hex[:8]}{ext}"
    save_path = os.path.join("uploads", "resumes", filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    resume_url = f"http://localhost:8000/uploads/resumes/{filename}"

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == me.id).first()
    if not profile:
        profile = StudentProfile(user_id=me.id)
        db.add(profile)
    profile.resume_url = resume_url
    db.commit()

    return {"resumeUrl": resume_url, "filename": file.filename}


# ── Jobs (browse approved) ────────────────────────────────────────────────────

@router.get("/jobs")
def browse_jobs(db: Session = Depends(get_db), me: User = Depends(_student)):
    jobs = db.query(Job).filter(Job.status == "Approved").all()
    applied_ids = {
        a.job_id
        for a in db.query(Application).filter(Application.student_id == me.id).all()
    }
    return [
        {
            "id":         j.id,
            "title":      j.title,
            "company":    j.company,
            "type":       j.type,
            "status":     j.status,
            "applicants": len(j.applications),
            "isApplied":  j.id in applied_ids,
        }
        for j in jobs
    ]


# ── Apply ─────────────────────────────────────────────────────────────────────

@router.post("/apply/{job_id}", status_code=201)
def apply(job_id: int, db: Session = Depends(get_db), me: User = Depends(_student)):
    job = db.query(Job).filter(Job.id == job_id, Job.status == "Approved").first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not open")
    if db.query(Application).filter(
        Application.student_id == me.id, Application.job_id == job_id
    ).first():
        raise HTTPException(status_code=400, detail="Already applied")

    app = Application(student_id=me.id, job_id=job_id)
    db.add(app)
    db.commit()
    db.refresh(app)
    return {
        "id":          app.id,
        "job":         job.title,
        "company":     job.company,
        "type":        job.type,
        "appliedDate": app.applied_date.strftime("%Y-%m-%d"),
        "status":      "Applied",
    }


# ── My Applications ───────────────────────────────────────────────────────────

@router.get("/applications")
def my_applications(db: Session = Depends(get_db), me: User = Depends(_student)):
    apps = db.query(Application).filter(Application.student_id == me.id).all()
    return [
        {
            "id":          a.id,
            "job":         a.job.title,
            "company":     a.job.company,
            "type":        a.job.type,
            "appliedDate": a.applied_date.strftime("%Y-%m-%d"),
            "status":      a.status,
        }
        for a in apps
    ]


# ── Saved Jobs ────────────────────────────────────────────────────────────────

@router.get("/saved-jobs")
def saved_jobs(db: Session = Depends(get_db), me: User = Depends(_student)):
    rows = db.query(SavedJob).filter(SavedJob.student_id == me.id).all()
    return [
        {
            "id":        s.job.id,
            "title":     s.job.title,
            "company":   s.job.company,
            "type":      s.job.type,
            "status":    s.job.status,
            "savedDate": s.saved_date.strftime("%Y-%m-%d"),
        }
        for s in rows
    ]


@router.post("/save/{job_id}", status_code=201)
def save_job(job_id: int, db: Session = Depends(get_db), me: User = Depends(_student)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if db.query(SavedJob).filter(
        SavedJob.student_id == me.id, SavedJob.job_id == job_id
    ).first():
        return {"ok": True}
    saved = SavedJob(student_id=me.id, job_id=job_id)
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return {
        "id":        job.id,
        "title":     job.title,
        "company":   job.company,
        "type":      job.type,
        "status":    job.status,
        "savedDate": saved.saved_date.strftime("%Y-%m-%d"),
    }


@router.delete("/saved/{job_id}")
def remove_saved(job_id: int, db: Session = Depends(get_db), me: User = Depends(_student)):
    row = db.query(SavedJob).filter(
        SavedJob.student_id == me.id, SavedJob.job_id == job_id
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(row)
    db.commit()
    return {"ok": True}
