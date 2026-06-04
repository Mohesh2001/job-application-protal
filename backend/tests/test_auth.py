def test_register_student(client):
    res = client.post("/auth/register", json={
        "name": "Test Student",
        "email": "new_student@test.com",
        "password": "pass123",
        "role": "Student",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["role"] == "Student"
    assert data["email"] == "new_student@test.com"


def test_register_recruiter(client):
    res = client.post("/auth/register", json={
        "name": "Test Recruiter",
        "email": "new_recruiter@test.com",
        "password": "pass123",
        "role": "Recruiter",
    })
    assert res.status_code == 201
    assert res.json()["role"] == "Recruiter"


def test_register_invalid_role(client):
    res = client.post("/auth/register", json={
        "name": "Bad Actor",
        "email": "bad@test.com",
        "password": "pass123",
        "role": "Admin",
    })
    assert res.status_code == 400


def test_register_duplicate_email(client):
    payload = {"name": "Dup", "email": "dup@test.com", "password": "pass123", "role": "Student"}
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 400


def test_login_success(client, student_user):
    res = client.post("/auth/login", json={"email": "student@test.com", "password": "student123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["role"] == "Student"
    assert data["user"]["email"] == "student@test.com"


def test_login_wrong_password(client, student_user):
    res = client.post("/auth/login", json={"email": "student@test.com", "password": "wrongpass"})
    assert res.status_code == 401


def test_login_nonexistent_user(client):
    res = client.post("/auth/login", json={"email": "nobody@test.com", "password": "pass"})
    assert res.status_code == 401


def test_login_returns_token_type(client, student_user):
    res = client.post("/auth/login", json={"email": "student@test.com", "password": "student123"})
    assert res.json()["token_type"] == "bearer"


def test_login_admin(client, admin_user):
    res = client.post("/auth/login", json={"email": "admin@test.com", "password": "admin123"})
    assert res.status_code == 200
    assert res.json()["user"]["role"] == "Admin"
