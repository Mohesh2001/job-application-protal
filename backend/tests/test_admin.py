import pytest
from app.models import Job, Category, Skill


# ── Auth guards ───────────────────────────────────────────────────────────────

def test_dashboard_requires_admin(client, student_headers):
    assert client.get("/admin/dashboard", headers=student_headers).status_code == 403


def test_dashboard_requires_auth(client):
    assert client.get("/admin/dashboard").status_code == 401


# ── Dashboard ─────────────────────────────────────────────────────────────────

def test_dashboard(client, admin_headers):
    res = client.get("/admin/dashboard", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "totalUsers" in data
    assert "students" in data
    assert "recruiters" in data
    assert "activeJobs" in data
    assert "applications" in data


def test_dashboard_counts(client, admin_headers, student_user, recruiter_user):
    res = client.get("/admin/dashboard", headers=admin_headers)
    data = res.json()
    assert data["students"] >= 1
    assert data["recruiters"] >= 1


# ── Users ─────────────────────────────────────────────────────────────────────

def test_list_users(client, admin_headers, student_user):
    res = client.get("/admin/users", headers=admin_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert any(u["email"] == "student@test.com" for u in res.json())


def test_create_user(client, admin_headers):
    res = client.post("/admin/users", json={
        "name": "New Student",
        "email": "newstudent@test.com",
        "role": "Student",
        "status": "Active",
    }, headers=admin_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "newstudent@test.com"
    assert data["role"] == "Student"


def test_create_duplicate_user(client, admin_headers, student_user):
    res = client.post("/admin/users", json={
        "name": "Dup",
        "email": "student@test.com",
        "role": "Student",
        "status": "Active",
    }, headers=admin_headers)
    assert res.status_code == 400


def test_update_user_name(client, admin_headers, student_user):
    res = client.put(f"/admin/users/{student_user.id}", json={"name": "Updated"}, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["name"] == "Updated"


def test_update_user_status(client, admin_headers, student_user):
    res = client.put(f"/admin/users/{student_user.id}", json={"status": "Inactive"}, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "Inactive"


def test_update_nonexistent_user(client, admin_headers):
    assert client.put("/admin/users/9999", json={"name": "X"}, headers=admin_headers).status_code == 404


def test_delete_user(client, admin_headers, student_user):
    res = client.delete(f"/admin/users/{student_user.id}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_delete_nonexistent_user(client, admin_headers):
    assert client.delete("/admin/users/9999", headers=admin_headers).status_code == 404


# ── Jobs ─────────────────────────────────────────────────────────────────────

def test_list_jobs(client, admin_headers, approved_job):
    res = client.get("/admin/jobs", headers=admin_headers)
    assert res.status_code == 200
    assert any(j["id"] == approved_job.id for j in res.json())


def test_approve_job(client, admin_headers, db, recruiter_user):
    job = Job(recruiter_id=recruiter_user.id, title="Job", company="Co", type="Full-time", status="Pending")
    db.add(job)
    db.commit()
    res = client.patch(f"/admin/jobs/{job.id}/approve", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "Approved"


def test_reject_job(client, admin_headers, db, recruiter_user):
    job = Job(recruiter_id=recruiter_user.id, title="Job", company="Co", type="Full-time", status="Pending")
    db.add(job)
    db.commit()
    res = client.patch(f"/admin/jobs/{job.id}/reject", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "Rejected"


def test_approve_nonexistent_job(client, admin_headers):
    assert client.patch("/admin/jobs/9999/approve", headers=admin_headers).status_code == 404


def test_update_job(client, admin_headers, approved_job):
    res = client.put(f"/admin/jobs/{approved_job.id}", json={"title": "New Title"}, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["title"] == "New Title"


def test_delete_job(client, admin_headers, approved_job):
    res = client.delete(f"/admin/jobs/{approved_job.id}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_delete_nonexistent_job(client, admin_headers):
    assert client.delete("/admin/jobs/9999", headers=admin_headers).status_code == 404


# ── Applications ─────────────────────────────────────────────────────────────

def test_list_applications(client, admin_headers):
    res = client.get("/admin/applications", headers=admin_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


# ── Content ───────────────────────────────────────────────────────────────────

def test_list_content_empty(client, admin_headers):
    res = client.get("/admin/content", headers=admin_headers)
    assert res.status_code == 200
    assert res.json() == []


def test_create_category(client, admin_headers):
    res = client.post("/admin/content", json={"type": "Category", "name": "Engineering"}, headers=admin_headers)
    assert res.status_code == 201
    assert res.json()["type"] == "Category"
    assert res.json()["name"] == "Engineering"


def test_create_skill(client, admin_headers):
    res = client.post("/admin/content", json={"type": "Skill", "name": "Python"}, headers=admin_headers)
    assert res.status_code == 201
    assert res.json()["type"] == "Skill"


def test_create_tag(client, admin_headers):
    res = client.post("/admin/content", json={"type": "Tag", "name": "Remote"}, headers=admin_headers)
    assert res.status_code == 201


def test_create_invalid_content_type(client, admin_headers):
    res = client.post("/admin/content", json={"type": "Invalid", "name": "X"}, headers=admin_headers)
    assert res.status_code == 400


def test_update_content(client, admin_headers, db):
    cat = Category(name="OldName")
    db.add(cat)
    db.commit()
    res = client.put(f"/admin/content/Category/{cat.id}", json={"name": "NewName"}, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["name"] == "NewName"


def test_update_nonexistent_content(client, admin_headers):
    assert client.put("/admin/content/Skill/9999", json={"name": "X"}, headers=admin_headers).status_code == 404


def test_delete_content(client, admin_headers, db):
    skill = Skill(name="DeleteMe")
    db.add(skill)
    db.commit()
    res = client.delete(f"/admin/content/Skill/{skill.id}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_list_content_shows_all_types(client, admin_headers, db):
    db.add(Category(name="Cat1"))
    db.add(Skill(name="Skill1"))
    db.commit()
    res = client.get("/admin/content", headers=admin_headers)
    types = [i["type"] for i in res.json()]
    assert "Category" in types
    assert "Skill" in types
