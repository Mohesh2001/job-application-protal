import pytest
import mongomock
from fastapi.testclient import TestClient
from bson import ObjectId

from app import database as _db_module
from app.main import app  # noqa: E402 — app must be imported after DB patching
from app.models import User, Job, StudentProfile, Company, Category, Skill
from app.auth import hash_password, create_access_token

# Create a mongomock client and database for tests
_mongoclient = mongomock.MongoClient()
_test_db = _mongoclient["job_portal_test"]

# Patch the app.database.db so get_db() returns our test db
_db_module.db = _test_db


class TestDB:
    """A tiny compatibility layer used by tests.

    Methods supported: add(obj), commit(), flush(), close(), query(Model).
    """

    TYPE_MAP = {
        "User": "users",
        "StudentProfile": "student_profiles",
        "Company": "companies",
        "Job": "jobs",
        "Application": "applications",
        "SavedJob": "saved_jobs",
        "Category": "categories",
        "Skill": "skills",
        "StudentSkill": "student_skills",
    }

    def __init__(self, db):
        self._db = db
        self._added = {v: [] for v in self.TYPE_MAP.values()}

    def add(self, obj):
        name = obj.__class__.__name__
        coll = self.TYPE_MAP.get(name)
        if not coll:
            raise RuntimeError(f"Unknown test object type: {name}")
        doc = {}
        for k, v in obj.__dict__.items():
            if k == "id":
                continue
            if k.endswith("_id") and isinstance(v, str):
                try:
                    doc[k] = ObjectId(v)
                    continue
                except Exception:
                    pass
            doc[k] = v
        res = self._db[coll].insert_one(doc)
        obj.id = str(res.inserted_id)
        self._added[coll].append(obj)
        return obj

    def flush(self):
        return None

    def commit(self):
        return None

    def close(self):
        return None

    def query(self, model):
        """Return a simple query shim for Model classes used in tests."""
        coll = self.TYPE_MAP.get(model.__name__)
        db = self._db

        class QueryShim:
            def __init__(self, coll_name, db):
                self.coll_name = coll_name
                self.db = db
                self._filter = None

            def filter(self, *args, **kwargs):
                # tests do not rely on SQL expressions here; store filter for potential use
                self._filter = (args, kwargs)
                return self

            def first(self):
                # prefer documents inserted by API (stored in mongomock) then inserted via TestDB
                doc = self.db[self.coll_name].find_one()
                if doc:
                    return self._doc_to_obj(doc)
                # fallback to TestDB tracked objects
                lst = self.db.list_collection_names()
                added = []
                # reconstruct from inserted documents
                cursor = self.db[self.coll_name].find()
                for d in cursor:
                    added.append(d)
                if not added:
                    return None
                return self._doc_to_obj(added[0])

            def all(self):
                docs = list(self.db[self.coll_name].find())
                return [self._doc_to_obj(d) for d in docs]

            def _doc_to_obj(self, d):
                # build a lightweight object matching the model
                cls_name = model.__name__
                from app import models as m
                cls = getattr(m, cls_name)
                kwargs = {}
                for k, v in d.items():
                    if k == "_id":
                        kwargs["id"] = str(v)
                    else:
                        # convert ObjectId references to string ids
                        if isinstance(v, ObjectId):
                            kwargs[k] = str(v)
                        else:
                            kwargs[k] = v
                return cls(**kwargs)

        return QueryShim(coll, db)


@pytest.fixture(autouse=True)
def setup_collections():
    # Ensure a clean database for each test
    for name in list(_test_db.list_collection_names()):
        _test_db.drop_collection(name)
    yield


@pytest.fixture
def db():
    return TestDB(_test_db)


@pytest.fixture
def client(db):
    def _override():
        yield _test_db

    app.dependency_overrides[_db_module.get_db] = _override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Seed users ────────────────────────────────────────────────────────────────

@pytest.fixture
def admin_user(db):
    user = User(
        name="Admin User",
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        role="Admin",
        status="Active",
    )
    db.add(user)
    return user


@pytest.fixture
def student_user(db):
    user = User(
        name="Student User",
        email="student@test.com",
        password_hash=hash_password("student123"),
        role="Student",
        status="Active",
    )
    db.add(user)
    db.add(StudentProfile(user_id=user.id))
    return user


@pytest.fixture
def recruiter_user(db):
    user = User(
        name="Recruiter User",
        email="recruiter@test.com",
        password_hash=hash_password("recruiter123"),
        role="Recruiter",
        status="Active",
    )
    db.add(user)
    db.add(Company(user_id=user.id, name="Test Company"))
    return user


# ── Auth headers ──────────────────────────────────────────────────────────────

@pytest.fixture
def admin_headers(admin_user):
    token = create_access_token({"sub": admin_user.id, "role": "Admin"})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def student_headers(student_user):
    token = create_access_token({"sub": student_user.id, "role": "Student"})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def recruiter_headers(recruiter_user):
    token = create_access_token({"sub": recruiter_user.id, "role": "Recruiter"})
    return {"Authorization": f"Bearer {token}"}


# ── Shared data ───────────────────────────────────────────────────────────────

@pytest.fixture
def approved_job(db, recruiter_user):
    job = Job(
        recruiter_id=recruiter_user.id,
        title="Software Engineer",
        company="Test Company",
        type="Full-time",
        status="Approved",
    )
    db.add(job)
    return job
