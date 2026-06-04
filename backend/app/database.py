import os
from typing import Optional, Any
import importlib
import importlib.util


def _try_load_dotenv() -> None:
    """Load dotenv if available, silently do nothing otherwise."""
    if importlib.util.find_spec("dotenv") is None:
        return None
    mod = importlib.import_module("dotenv")
    fn = getattr(mod, "load_dotenv", None)
    if callable(fn):
        fn()
    return None

# expose load_dotenv name like the original module did
load_dotenv = _try_load_dotenv

# Try to import pymongo dynamically to avoid static import errors in editors/CI
_MongoClient = None
if importlib.util.find_spec("pymongo") is not None:
    pymongo = importlib.import_module("pymongo")
    _MongoClient = getattr(pymongo, "MongoClient", None)
    try:
        db_mod = importlib.import_module("pymongo.database")
        _Database = getattr(db_mod, "Database", Any)
    except Exception:
        _Database = Any
else:
    _MongoClient = None
    _Database = Any

# Public names expected by the rest of the codebase
MongoClient = _MongoClient  # type: ignore
Database = _Database  # type: ignore

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "job_portal_db")

# If MongoClient isn't available at import time, db will be None. Code that
# actually needs the database should handle a None return from get_db().
if MongoClient is None:
    db = None  # type: ignore
else:
    _client = MongoClient(MONGO_URL)
    db = _client[DB_NAME]


def get_db() -> Optional["Database"]:
    return db
