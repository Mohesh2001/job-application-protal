from app.models import SavedJob, Application


# ── Auth guards ───────────────────────────────────────────────────────────────

def test_dashboard_requires_auth(client):
    assert client.get("/student/dashboard").status_code == 401


def test_student_cannot_access_admin(client, student_headers):
    assert client.get("/admin/dashboard", headers=student_headers).status_code == 403


def test_recruiter_cannot_access_student(client, recruiter_headers):
    assert client.get("/student/dashboard", headers=recruiter_headers).status_code == 403


# ── Dashboard ─────────────────────────────────────────────────────────────────

def test_dashboard(client, student_headers):
    res = client.get("/student/dashboard", headers=student_headers)
    assert res.status_code == 200
    data = res.json()
    assert "applicationsSent" in data
    assert "shortlisted" in data
    assert "savedJobs" in data
    assert "profileStrength" in data


def test_dashboard_initial_zeros(client, student_headers):
    res = client.get("/student/dashboard", headers=student_headers)
    data = res.json()
    assert data["applicationsSent"] == 0
    assert data["savedJobs"] == 0


# ── Profile ───────────────────────────────────────────────────────────────────

def test_get_profile(client, student_headers):
    res = client.get("/student/profile", headers=student_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "student@test.com"
    assert "skills" in data
    assert isinstance(data["skills"], list)


def test_update_profile(client, student_headers):
    res = client.put("/student/profile", json={
        "phone": "9876543210",
        "college": "MIT",
        "degree": "B.Tech CS",
        "graduationYear": "2025",
        "linkedin": "https://linkedin.com/in/test",
        "skills": ["Python", "FastAPI"],
    }, headers=student_headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_profile_reflects_updates(client, student_headers):
    client.put("/student/profile", json={"college": "Stanford"}, headers=student_headers)
    res = client.get("/student/profile", headers=student_headers)
    assert res.json()["college"] == "Stanford"


def test_update_profile_name(client, student_headers):
    res = client.put("/student/profile", json={"name": "New Name"}, headers=student_headers)
    assert res.status_code == 200


def test_update_profile_skills(client, student_headers):
    client.put("/student/profile", json={"skills": ["React", "Node.js"]}, headers=student_headers)
    res = client.get("/student/profile", headers=student_headers)
    assert set(res.json()["skills"]) == {"React", "Node.js"}


# ── Browse Jobs ───────────────────────────────────────────────────────────────

def test_browse_approved_jobs(client, student_headers, approved_job):
    res = client.get("/student/jobs", headers=student_headers)
    assert res.status_code == 200
    assert any(j["id"] == approved_job.id for j in res.json())


def test_pending_jobs_not_shown(client, student_headers, db, recruiter_user):
    from app.models import Job
    job = Job(recruiter_id=recruiter_user.id, title="Pending", company="Co", type="Full-time", status="Pending")
    db.add(job)
    db.commit()
    res = client.get("/student/jobs", headers=student_headers)
    assert not any(j["id"] == job.id for j in res.json())


def test_browse_jobs_has_is_applied_field(client, student_headers, approved_job):
    res = client.get("/student/jobs", headers=student_headers)
    job = next(j for j in res.json() if j["id"] == approved_job.id)
    assert "isApplied" in job
    assert job["isApplied"] is False


# ── Apply ─────────────────────────────────────────────────────────────────────

def test_apply_job(client, student_headers, approved_job):
    res = client.post(f"/student/apply/{approved_job.id}", headers=student_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "Applied"
    assert data["job"] == approved_job.title


def test_apply_marks_job_as_applied(client, student_headers, approved_job):
    client.post(f"/student/apply/{approved_job.id}", headers=student_headers)
    res = client.get("/student/jobs", headers=student_headers)
    job = next(j for j in res.json() if j["id"] == approved_job.id)
    assert job["isApplied"] is True


def test_apply_duplicate_blocked(client, student_headers, approved_job):
    client.post(f"/student/apply/{approved_job.id}", headers=student_headers)
    res = client.post(f"/student/apply/{approved_job.id}", headers=student_headers)
    assert res.status_code == 400


def test_apply_nonexistent_job(client, student_headers):
    assert client.post("/student/apply/9999", headers=student_headers).status_code == 404


def test_apply_pending_job_blocked(client, student_headers, db, recruiter_user):
    from app.models import Job
    job = Job(recruiter_id=recruiter_user.id, title="Pending", company="Co", type="Full-time", status="Pending")
    db.add(job)
    db.commit()
    assert client.post(f"/student/apply/{job.id}", headers=student_headers).status_code == 404


# ── My Applications ───────────────────────────────────────────────────────────

def test_my_applications_empty(client, student_headers):
    res = client.get("/student/applications", headers=student_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_my_applications_after_apply(client, student_headers, approved_job):
    client.post(f"/student/apply/{approved_job.id}", headers=student_headers)
    res = client.get("/student/applications", headers=student_headers)
    assert len(res.json()) == 1
    assert res.json()[0]["status"] == "Applied"


# ── Saved Jobs ────────────────────────────────────────────────────────────────

def test_save_job(client, student_headers, approved_job):
    res = client.post(f"/student/save/{approved_job.id}", headers=student_headers)
    assert res.status_code == 201
    assert res.json()["id"] == approved_job.id


def test_save_nonexistent_job(client, student_headers):
    assert client.post("/student/save/9999", headers=student_headers).status_code == 404


def test_saved_jobs_list(client, student_headers, approved_job):
    client.post(f"/student/save/{approved_job.id}", headers=student_headers)
    res = client.get("/student/saved-jobs", headers=student_headers)
    assert res.status_code == 200
    assert any(j["id"] == approved_job.id for j in res.json())


def test_remove_saved_job(client, student_headers, approved_job, db, student_user):
    client.post(f"/student/save/{approved_job.id}", headers=student_headers)
    res = client.delete(f"/student/saved/{approved_job.id}", headers=student_headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_remove_saved_updates_list(client, student_headers, approved_job):
    client.post(f"/student/save/{approved_job.id}", headers=student_headers)
    client.delete(f"/student/saved/{approved_job.id}", headers=student_headers)
    res = client.get("/student/saved-jobs", headers=student_headers)
    assert res.json() == []


def test_remove_nonexistent_saved(client, student_headers):
    assert client.delete("/student/saved/9999", headers=student_headers).status_code == 404
