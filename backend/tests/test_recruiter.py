from app.models import Job, Application, User, Company
from app.auth import hash_password


# ── Auth guards ───────────────────────────────────────────────────────────────

def test_dashboard_requires_auth(client):
    assert client.get("/recruiter/dashboard").status_code == 401


def test_student_cannot_access_recruiter(client, student_headers):
    assert client.get("/recruiter/dashboard", headers=student_headers).status_code == 403


# ── Dashboard ─────────────────────────────────────────────────────────────────

def test_dashboard(client, recruiter_headers):
    res = client.get("/recruiter/dashboard", headers=recruiter_headers)
    assert res.status_code == 200
    data = res.json()
    assert "activeJobs" in data
    assert "totalApplicants" in data
    assert "shortlisted" in data
    assert "pendingApproval" in data


def test_dashboard_initial_zeros(client, recruiter_headers):
    res = client.get("/recruiter/dashboard", headers=recruiter_headers)
    data = res.json()
    assert data["activeJobs"] == 0
    assert data["totalApplicants"] == 0


# ── Jobs ──────────────────────────────────────────────────────────────────────

def test_post_job(client, recruiter_headers):
    res = client.post("/recruiter/jobs", json={
        "title": "Backend Developer",
        "company": "Tech Corp",
        "type": "Full-time",
        "description": "Build APIs",
        "location": "Remote",
    }, headers=recruiter_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Backend Developer"
    assert data["status"] == "Pending"


def test_post_job_internship(client, recruiter_headers):
    res = client.post("/recruiter/jobs", json={
        "title": "Intern",
        "type": "Internship",
    }, headers=recruiter_headers)
    assert res.status_code == 201
    assert res.json()["type"] == "Internship"


def test_list_jobs(client, recruiter_headers, approved_job):
    res = client.get("/recruiter/jobs", headers=recruiter_headers)
    assert res.status_code == 200
    assert any(j["id"] == approved_job.id for j in res.json())


def test_list_jobs_only_own(client, recruiter_headers, db):
    other = User(name="Other", email="other@test.com", password_hash=hash_password("x"), role="Recruiter", status="Active")
    db.add(other)
    db.flush()
    job = Job(recruiter_id=other.id, title="Other Job", company="Other Co", type="Full-time", status="Pending")
    db.add(job)
    db.commit()
    res = client.get("/recruiter/jobs", headers=recruiter_headers)
    assert not any(j["id"] == job.id for j in res.json())


def test_update_job(client, recruiter_headers, approved_job):
    res = client.put(f"/recruiter/jobs/{approved_job.id}", json={"title": "Senior Engineer"}, headers=recruiter_headers)
    assert res.status_code == 200
    assert res.json()["title"] == "Senior Engineer"


def test_update_other_recruiter_job_blocked(client, recruiter_headers, db):
    other = User(name="Other", email="other2@test.com", password_hash=hash_password("x"), role="Recruiter", status="Active")
    db.add(other)
    db.flush()
    job = Job(recruiter_id=other.id, title="Job", company="Co", type="Full-time", status="Pending")
    db.add(job)
    db.commit()
    assert client.put(f"/recruiter/jobs/{job.id}", json={"title": "Hacked"}, headers=recruiter_headers).status_code == 404


def test_delete_job(client, recruiter_headers, db, recruiter_user):
    job = Job(recruiter_id=recruiter_user.id, title="To Delete", company="Co", type="Full-time", status="Pending")
    db.add(job)
    db.commit()
    res = client.delete(f"/recruiter/jobs/{job.id}", headers=recruiter_headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_delete_nonexistent_job(client, recruiter_headers):
    assert client.delete("/recruiter/jobs/9999", headers=recruiter_headers).status_code == 404


# ── Applicants ────────────────────────────────────────────────────────────────

def test_list_applicants_empty(client, recruiter_headers):
    res = client.get("/recruiter/applicants", headers=recruiter_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_list_applicants_after_application(client, recruiter_headers, approved_job, student_headers):
    client.post(f"/student/apply/{approved_job.id}", headers=student_headers)
    res = client.get("/recruiter/applicants", headers=recruiter_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["status"] == "Applied"


def test_shortlist_applicant(client, recruiter_headers, approved_job, student_headers, db):
    client.post(f"/student/apply/{approved_job.id}", headers=student_headers)
    app_obj = db.query(Application).first()
    res = client.patch(f"/recruiter/applicants/{app_obj.id}/shortlist", headers=recruiter_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "Shortlisted"


def test_reject_applicant(client, recruiter_headers, approved_job, student_headers, db):
    client.post(f"/student/apply/{approved_job.id}", headers=student_headers)
    app_obj = db.query(Application).first()
    res = client.patch(f"/recruiter/applicants/{app_obj.id}/reject", headers=recruiter_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "Rejected"


def test_shortlist_nonexistent_application(client, recruiter_headers):
    assert client.patch("/recruiter/applicants/9999/shortlist", headers=recruiter_headers).status_code == 404


# ── Company Profile ───────────────────────────────────────────────────────────

def test_get_company(client, recruiter_headers):
    res = client.get("/recruiter/company", headers=recruiter_headers)
    assert res.status_code == 200
    data = res.json()
    assert "name" in data
    assert data["name"] == "Test Company"


def test_update_company(client, recruiter_headers):
    res = client.put("/recruiter/company", json={
        "name": "Updated Corp",
        "industry": "Technology",
        "website": "https://updated.com",
        "location": "New York",
        "about": "A great company",
    }, headers=recruiter_headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_company_update_reflects(client, recruiter_headers):
    client.put("/recruiter/company", json={"name": "New Name Corp"}, headers=recruiter_headers)
    res = client.get("/recruiter/company", headers=recruiter_headers)
    assert res.json()["name"] == "New Name Corp"
