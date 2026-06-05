"""
Seed MongoDB with all data from the MySQL dump.

Usage:
    python seed_mongodb.py           # skips records that already exist
    python seed_mongodb.py --clear   # drops all collections first, then seeds fresh
"""

import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

try:
    import bcrypt
    from pymongo import MongoClient
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install pymongo bcrypt python-dotenv")
    sys.exit(1)

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "job_portal_db")

client = MongoClient(MONGO_URL)
db     = client[DB_NAME]

CLEAR = "--clear" in sys.argv


def ts(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


def hash_pw(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()


def main():
    if CLEAR:
        print("Clearing all collections...")
        for coll in [
            "users", "student_profiles", "companies", "categories",
            "skills", "tags", "jobs", "applications", "saved_jobs", "notifications",
        ]:
            db[coll].drop()
        print("Done.\n")

    # ── 1. Users ──────────────────────────────────────────────────────────────
    # Users 1-7 had plain-text passwords in MySQL — hash them here.
    # Users 8-12 already have bcrypt hashes — keep them as-is.
    user_rows = [
        (1,  "Admin",        "pmohesh2001@gmail.com",   hash_pw("Mohesh2001@"),                                              "Admin",     "Active",   "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (2,  "Raj Kumar",    "raj@student.com",          hash_pw("Mohesh2001@"),                                              "Student",   "Active",   "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (3,  "David Lee",    "david@student.com",        hash_pw("Mohesh2001@"),                                              "Student",   "Inactive", "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (4,  "John Paul",    "john@student.com",         hash_pw("Mohesh2001@"),                                              "Student",   "Active",   "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (5,  "Anita Sharma", "anita@hireflow.com",       hash_pw("Mohesh2001@"),                                              "Recruiter", "Active",   "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (6,  "Maya Singh",   "maya@talenthub.com",       hash_pw("Mohesh2001@"),                                              "Recruiter", "Active",   "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (7,  "Sara Khan",    "sara@careerbridge.com",    hash_pw("Mohesh2001@"),                                              "Recruiter", "Pending",  "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (8,  "Gowtham",      "gowtham@gmail.com",        "$2b$12$57jS0.Q844ngAsqVqW/wWu0q525MyGaGf8XUhQN2BAM2RgBA5Z7Ua",    "Student",   "Active",   "2026-05-17 02:12:05", "2026-05-17 02:12:05"),
        (9,  "Rec",          "rec@gmail.com",            "$2b$12$vu6kjN/9yfrXZUHaO63tMOA8HoF0Jv.5H.8srPD6E94hMmuwrCv/6",    "Recruiter", "Active",   "2026-05-17 02:34:55", "2026-05-17 02:34:55"),
        (10, "Admin",        "admin@jobportal.com",      "$2b$12$nDgPMl15Qlw22uSlej0A7uC0iL77Y6WY3eV8CE6Q9pVQlAWwzHF/a",    "Admin",     "Active",   "2026-05-17 02:47:44", "2026-05-17 02:47:44"),
        (11, "Mohesh",       "pmohesh402@gmail.com",     "$2b$12$QBg9WlXf7jl3HOK4XjhxWuPWjpWhJa13cfwuisTdI5KLhI.ct/DMi",    "Student",   "Active",   "2026-05-17 12:14:12", "2026-05-17 12:14:12"),
        (12, "Rahul",        "rahul2002@gmail.com",      "$2b$12$y7bp68Qm/2LKkVKrwuhQUuYEUFtZK5nsWBJHwaq2FR9tlOy43NwY.",    "Recruiter", "Active",   "2026-06-01 12:29:18", "2026-06-01 12:29:18"),
    ]

    user_id_map = {}   # mysql int id → MongoDB ObjectId
    inserted = skipped = 0
    for mid, name, email, pw_hash, role, status, created, updated in user_rows:
        existing = db["users"].find_one({"email": email})
        if existing:
            user_id_map[mid] = existing["_id"]
            skipped += 1
        else:
            doc = {
                "name": name, "email": email, "password_hash": pw_hash,
                "role": role, "status": status,
                "created_at": ts(created), "updated_at": ts(updated),
            }
            result = db["users"].insert_one(doc)
            user_id_map[mid] = result.inserted_id
            inserted += 1
    print(f"Users          : {inserted} inserted, {skipped} skipped")

    # ── 2. Skills ─────────────────────────────────────────────────────────────
    skill_rows = [
        (1, "ReactJS"), (2, "FastAPI"), (3, "Python"), (4, "SQL"),
        (5, "Node.js"), (6, "Machine Learning"), (7, "UI/UX Design"),
        (8, "Java"), (9, "DevOps"), (10, "AWS"),
    ]

    skill_id_map = {}  # mysql int id → MongoDB ObjectId
    inserted = skipped = 0
    for mid, name in skill_rows:
        existing = db["skills"].find_one({"name": name})
        if existing:
            skill_id_map[mid] = existing["_id"]
            skipped += 1
        else:
            result = db["skills"].insert_one({"name": name})
            skill_id_map[mid] = result.inserted_id
            inserted += 1
    print(f"Skills         : {inserted} inserted, {skipped} skipped")

    # ── 3. Categories ─────────────────────────────────────────────────────────
    category_rows = [
        (1, "Software Engineering"), (2, "Data Science"),
        (3, "Marketing"), (4, "Finance"), (5, "Design"),
    ]

    category_id_map = {}  # mysql int id → MongoDB ObjectId
    inserted = skipped = 0
    for mid, name in category_rows:
        existing = db["categories"].find_one({"name": name})
        if existing:
            category_id_map[mid] = existing["_id"]
            skipped += 1
        else:
            result = db["categories"].insert_one({"name": name})
            category_id_map[mid] = result.inserted_id
            inserted += 1
    print(f"Categories     : {inserted} inserted, {skipped} skipped")

    # ── 4. Tags ───────────────────────────────────────────────────────────────
    tag_names = ["Remote", "Internship", "Full-time", "Hybrid", "On-site"]
    inserted = skipped = 0
    for name in tag_names:
        if db["tags"].find_one({"name": name}):
            skipped += 1
        else:
            db["tags"].insert_one({"name": name})
            inserted += 1
    print(f"Tags           : {inserted} inserted, {skipped} skipped")

    # ── 5. Student Profiles ───────────────────────────────────────────────────
    # student_skills in MySQL: profile_id → list of skill mysql ids
    profile_skills_map = {
        1: [1, 3, 4, 5],   # Raj Kumar  → ReactJS, Python, SQL, Node.js
        4: [3, 8],          # Gowtham    → Python, Java
    }

    profile_rows = [
        # (mysql_profile_id, user_mysql_id, phone, college, degree, grad_year, linkedin, resume, strength)
        (1, 2,  "+91 9876543210", "National Institute of Technology", "B.Tech Computer Science", 2025, "linkedin.com/in/rajkumar",  None,                                                    72),
        (2, 3,  None,             "IIT Delhi",                        "B.Tech Electronics",       2025, None,                        None,                                                    40),
        (3, 4,  None,             "VIT University",                   "B.Tech IT",                2026, None,                        None,                                                    35),
        (4, 8,  "6382526592",     "Maran college",                    "phd",                      2022, "gowtham.linkedin.com",      "http://localhost:8000/uploads/resumes/8_021a3dd7.pdf",  0),
        (5, 11, None,             None,                               None,                       None, None,                        None,                                                    0),
    ]

    inserted = skipped = 0
    for mid, user_mid, phone, college, degree, grad_year, linkedin, resume, strength in profile_rows:
        user_oid = user_id_map[user_mid]
        existing = db["student_profiles"].find_one({"user_id": user_oid})
        if existing:
            skipped += 1
        else:
            skill_names = [
                db["skills"].find_one({"_id": skill_id_map[sid]})["name"]
                for sid in profile_skills_map.get(mid, [])
            ]
            doc = {
                "user_id": user_oid,
                "phone": phone, "college": college, "degree": degree,
                "graduation_year": grad_year, "linkedin_url": linkedin,
                "resume_url": resume, "profile_strength": strength,
                "skills": skill_names,
            }
            db["student_profiles"].insert_one(doc)
            inserted += 1
    print(f"Student profiles: {inserted} inserted, {skipped} skipped")

    # ── 6. Companies ──────────────────────────────────────────────────────────
    company_rows = [
        # (user_mysql_id, name, industry, website, location, about)
        (5,  "HireFlow",        "HR Technology",   "hireflow.com",     "Mumbai, India",    "HireFlow specializes in connecting talent with opportunity."),
        (6,  "TalentHub",       "Recruitment",     "talenthub.com",    "Delhi, India",     "TalentHub is India's leading talent acquisition platform."),
        (7,  "CareerBridge",    "Career Services", "careerbridge.com", "Bangalore, India", "CareerBridge helps professionals find their dream careers."),
        (9,  "EY",              "MNC",             "ey.com",           "Newzaland",        "worst company in the universe"),
        (12, "Rahul's Company", None,              None,               None,               None),
    ]

    inserted = skipped = 0
    for user_mid, name, industry, website, location, about in company_rows:
        user_oid = user_id_map[user_mid]
        if db["companies"].find_one({"user_id": user_oid}):
            skipped += 1
        else:
            db["companies"].insert_one({
                "user_id": user_oid, "name": name,
                "industry": industry, "website": website,
                "location": location, "about": about,
            })
            inserted += 1
    print(f"Companies      : {inserted} inserted, {skipped} skipped")

    # ── 7. Jobs ───────────────────────────────────────────────────────────────
    job_rows = [
        # (mysql_id, recruiter_mysql_id, category_mysql_id, title, company, type, status, skills, description, location, deadline, created, updated)
        (1, 5,  1, "Frontend Developer",  "TechNova",  "Full-time",  "Pending",  [],         None,                              None,      "2025-06-30", "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (2, 6,  2, "Data Analyst Intern", "InsightIQ", "Internship", "Approved", [],         None,                              None,      "2025-07-15", "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (3, 5,  5, "UI/UX Designer",      "DesignPro", "Full-time",  "Rejected", [],         None,                              None,      "2025-06-15", "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (4, 6,  1, "Backend Engineer",    "CloudStack","Full-time",  "Pending",  [],         None,                              None,      "2025-07-30", "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (5, 7,  1, "QA Tester",           "AppWorks",  "Internship", "Approved", [],         None,                              None,      "2025-06-20", "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (6, 9,  1, "Data Scientist",      "EY",        "Full-time",  "Approved", ["Python"], "Able to create fastapi application","Germany","2026-05-19", "2026-05-17 02:36:58", "2026-05-17 02:37:41"),
        (7, 12, 1, "data analyst",        "TechNova",  "Full-time",  "Pending",  ["reatjs"], "",                                "",        "2026-06-02", "2026-06-01 12:31:40", "2026-06-01 12:31:40"),
    ]

    job_id_map = {}  # mysql int id → MongoDB ObjectId
    inserted = skipped = 0
    for mid, rec_mid, cat_mid, title, company, jtype, status, skills, desc, loc, deadline, created, updated in job_rows:
        rec_oid = user_id_map[rec_mid]
        existing = db["jobs"].find_one({"title": title, "recruiter_id": rec_oid})
        if existing:
            job_id_map[mid] = existing["_id"]
            skipped += 1
        else:
            doc = {
                "recruiter_id": rec_oid,
                "category_id":  category_id_map.get(cat_mid),
                "title": title, "company": company,
                "type": jtype, "status": status,
                "skills": skills, "description": desc,
                "location": loc, "deadline": deadline,
                "created_at": ts(created), "updated_at": ts(updated),
            }
            result = db["jobs"].insert_one(doc)
            job_id_map[mid] = result.inserted_id
            inserted += 1
    print(f"Jobs           : {inserted} inserted, {skipped} skipped")

    # ── 8. Applications ───────────────────────────────────────────────────────
    application_rows = [
        # (student_mysql_id, job_mysql_id, status, applied_date, updated_at)
        (2,  1, "Applied",     "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (3,  2, "Shortlisted", "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (4,  4, "Rejected",    "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (2,  5, "Applied",     "2026-05-17 13:26:17", "2026-05-17 13:26:17"),
        (8,  2, "Applied",     "2026-05-17 02:27:06", "2026-05-17 02:27:06"),
    ]

    inserted = skipped = 0
    for student_mid, job_mid, status, applied, updated in application_rows:
        student_oid = user_id_map[student_mid]
        job_oid     = job_id_map[job_mid]
        if db["applications"].find_one({"student_id": student_oid, "job_id": job_oid}):
            skipped += 1
        else:
            db["applications"].insert_one({
                "student_id": student_oid, "job_id": job_oid,
                "status": status,
                "applied_date": ts(applied), "updated_at": ts(updated),
            })
            inserted += 1
    print(f"Applications   : {inserted} inserted, {skipped} skipped")

    # ── 9. Saved Jobs ─────────────────────────────────────────────────────────
    saved_rows = [
        # (student_mysql_id, job_mysql_id, saved_date)
        (2,  2, "2026-05-17 13:26:17"),
        (2,  4, "2026-05-17 13:26:17"),
        (2,  5, "2026-05-17 13:26:17"),
        (8,  2, "2026-05-17 02:27:11"),
        (8,  5, "2026-05-17 02:28:00"),
        (11, 2, "2026-05-17 12:15:09"),
    ]

    inserted = skipped = 0
    for student_mid, job_mid, saved in saved_rows:
        student_oid = user_id_map[student_mid]
        job_oid     = job_id_map[job_mid]
        if db["saved_jobs"].find_one({"student_id": student_oid, "job_id": job_oid}):
            skipped += 1
        else:
            db["saved_jobs"].insert_one({
                "student_id": student_oid, "job_id": job_oid,
                "saved_date": ts(saved),
            })
            inserted += 1
    print(f"Saved jobs     : {inserted} inserted, {skipped} skipped")

    # ── 10. Notifications ─────────────────────────────────────────────────────
    notification_rows = [
        # (user_mysql_id, message, is_read, created_at)
        (2, "Your application for Frontend Developer has been received.",      False, "2026-05-17 13:26:17"),
        (2, "You have been shortlisted for Data Analyst Intern at InsightIQ.", False, "2026-05-17 13:26:17"),
        (3, "Your application for Data Analyst Intern has been shortlisted.",  False, "2026-05-17 13:26:17"),
    ]

    inserted = skipped = 0
    for user_mid, message, is_read, created in notification_rows:
        user_oid = user_id_map[user_mid]
        if db["notifications"].find_one({"user_id": user_oid, "message": message}):
            skipped += 1
        else:
            db["notifications"].insert_one({
                "user_id": user_oid, "message": message,
                "is_read": is_read, "created_at": ts(created),
            })
            inserted += 1
    print(f"Notifications  : {inserted} inserted, {skipped} skipped")

    # ── 11. Indexes ───────────────────────────────────────────────────────────
    db["users"].create_index("email", unique=True)
    db["applications"].create_index([("student_id", 1), ("job_id", 1)], unique=True)
    db["jobs"].create_index("status")
    db["saved_jobs"].create_index([("student_id", 1), ("job_id", 1)])
    print("\nIndexes ensured.")
    print("Seeding complete!")


if __name__ == "__main__":
    main()
