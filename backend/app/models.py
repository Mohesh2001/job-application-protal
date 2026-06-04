from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from typing import Optional


# ── Lightweight models for tests (plain objects) ──────────────────────────────
class _BaseObj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if not hasattr(self, "id"):
            self.id = None


class User(_BaseObj):
    pass


class StudentProfile(_BaseObj):
    pass


class Company(_BaseObj):
    pass


class Job(_BaseObj):
    pass


class Application(_BaseObj):
    pass


class SavedJob(_BaseObj):
    pass


class Category(_BaseObj):
    pass


class Skill(_BaseObj):
    pass


class StudentSkill(_BaseObj):
    pass


# ── Collection names ──────────────────────────────────────────────────────────

USERS            = "users"
STUDENT_PROFILES = "student_profiles"
COMPANIES        = "companies"
JOBS             = "jobs"
APPLICATIONS     = "applications"
SAVED_JOBS       = "saved_jobs"
NOTIFICATIONS    = "notifications"
CATEGORIES       = "categories"
SKILLS           = "skills"
TAGS             = "tags"


# ── Helpers ───────────────────────────────────────────────────────────────────

def to_oid(id_str: str) -> Optional[ObjectId]:
    """Convert a string to ObjectId.

    Returns an ObjectId or None when the provided id is not a valid ObjectId.
    Routes should treat a None as a 'not found' case and return 404 instead
    of a 400 bad request to match the original SQL-based behavior in tests.
    """
    try:
        return ObjectId(id_str)
    except (InvalidId, Exception):
        return None


def doc(d: dict) -> dict | None:
    """Convert a MongoDB document: replace _id with id as string."""
    if d is None:
        return None
    d = dict(d)
    d["id"] = str(d.pop("_id"))
    return d


def docs(cursor) -> list[dict]:
    return [doc(d) for d in cursor]
