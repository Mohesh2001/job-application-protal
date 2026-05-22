"""Run once to create the admin user: ./venv/bin/python3 create_admin.py"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import bcrypt
from app.database import SessionLocal
from app.models import User

EMAIL    = "admin@jobportal.com"
PASSWORD = "Admin@123"
NAME     = "Admin"

db = SessionLocal()
try:
    existing = db.query(User).filter(User.email == EMAIL).first()
    if existing:
        # Update the hash in case it was inserted incorrectly
        existing.password_hash = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt()).decode()
        existing.role   = "Admin"
        existing.status = "Active"
        db.commit()
        print(f"✓ Admin user updated  →  {EMAIL}")
    else:
        user = User(
            name          = NAME,
            email         = EMAIL,
            password_hash = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt()).decode(),
            role          = "Admin",
            status        = "Active",
        )
        db.add(user)
        db.commit()
        print(f"✓ Admin user created  →  {EMAIL}")

    # Verify the hash works
    db.refresh(existing or user)
    stored = (existing or user).password_hash
    ok = bcrypt.checkpw(PASSWORD.encode(), stored.encode())
    print(f"✓ Password verify test: {'PASS' if ok else 'FAIL'}")
finally:
    db.close()
