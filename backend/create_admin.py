"""Create or update the admin user in MongoDB.
Run: .venv/bin/python create_admin.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import bcrypt
from bson import ObjectId

# Import app.database to reuse MONGO_URL/DB_NAME configuration
from app import database as _db_module

EMAIL    = os.getenv("ADMIN_EMAIL", "admin@jobportal.com")
PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")
NAME     = os.getenv("ADMIN_NAME", "Admin")

# Ensure we have a pymongo Database instance
db = _db_module.db
if db is None:
    try:
        from pymongo import MongoClient
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("pymongo is required to run this script") from exc
    client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
    db = client[os.getenv("DB_NAME", "job_portal_db")]

users = db["users"]

try:
    existing = users.find_one({"email": EMAIL})
    hashed = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt()).decode()

    if existing:
        users.update_one({"_id": existing["_id"]}, {"$set": {"password_hash": hashed, "role": "Admin", "status": "Active"}})
        print(f"✓ Admin user updated  →  {EMAIL}")
        user_doc = users.find_one({"_id": existing["_id"]})
    else:
        now = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        user_doc = {
            "name": NAME,
            "email": EMAIL,
            "password_hash": hashed,
            "role": "Admin",
            "status": "Active",
            "created_at": now,
            "updated_at": now,
        }
        res = users.insert_one(user_doc)
        user_doc["_id"] = res.inserted_id
        print(f"✓ Admin user created  →  {EMAIL}")

    # Verify the hash works
    stored = user_doc["password_hash"]
    ok = bcrypt.checkpw(PASSWORD.encode(), stored.encode())
    print(f"✓ Password verify test: {'PASS' if ok else 'FAIL'}")

finally:
    # nothing to close for mongomock/pymongo client here
    pass
