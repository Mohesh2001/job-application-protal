from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Enum, Boolean,
    Date, DateTime, ForeignKey, SmallInteger,
)
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(100), nullable=False)
    email         = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role          = Column(Enum("Admin", "Student", "Recruiter"), nullable=False)
    status        = Column(Enum("Active", "Inactive", "Pending"), default="Active")
    created_at    = Column(DateTime, default=datetime.utcnow)
    updated_at    = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student_profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    company         = relationship("Company",        back_populates="user", uselist=False, cascade="all, delete-orphan")
    jobs            = relationship("Job",            back_populates="recruiter", cascade="all, delete-orphan")
    applications    = relationship("Application",    back_populates="student",  cascade="all, delete-orphan")
    saved_jobs      = relationship("SavedJob",       back_populates="student",  cascade="all, delete-orphan")
    notifications   = relationship("Notification",   back_populates="user",     cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    phone            = Column(String(20))
    college          = Column(String(200))
    degree           = Column(String(150))
    graduation_year  = Column(SmallInteger)
    linkedin_url     = Column(String(255))
    resume_url       = Column(String(255))
    profile_strength = Column(SmallInteger, default=0)

    user           = relationship("User", back_populates="student_profile")
    student_skills = relationship("StudentSkill", back_populates="student_profile", cascade="all, delete-orphan")


class Company(Base):
    __tablename__ = "companies"

    id       = Column(Integer, primary_key=True, index=True)
    user_id  = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name     = Column(String(150), nullable=False)
    industry = Column(String(100))
    website  = Column(String(255))
    location = Column(String(150))
    about    = Column(Text)

    user = relationship("User", back_populates="company")


class Category(Base):
    __tablename__ = "categories"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)


class Skill(Base):
    __tablename__ = "skills"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    student_skills = relationship("StudentSkill", back_populates="skill")


class Tag(Base):
    __tablename__ = "tags"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)


class StudentSkill(Base):
    __tablename__ = "student_skills"

    student_profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), primary_key=True)
    skill_id           = Column(Integer, ForeignKey("skills.id",           ondelete="CASCADE"), primary_key=True)

    student_profile = relationship("StudentProfile", back_populates="student_skills")
    skill           = relationship("Skill",          back_populates="student_skills")


class Job(Base):
    __tablename__ = "jobs"

    id               = Column(Integer, primary_key=True, index=True)
    recruiter_id     = Column(Integer, ForeignKey("users.id",       ondelete="CASCADE"),   nullable=False)
    title            = Column(String(150), nullable=False)
    company          = Column(String(150), nullable=False)
    category_id      = Column(Integer, ForeignKey("categories.id",  ondelete="SET NULL"),  nullable=True)
    type             = Column(Enum("Full-time", "Internship"),       nullable=False)
    status           = Column(Enum("Pending", "Approved", "Rejected"), default="Pending")
    skills_required  = Column(String(500))
    description      = Column(Text)
    location         = Column(String(150))
    deadline         = Column(Date)
    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recruiter    = relationship("User",        back_populates="jobs")
    category     = relationship("Category")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    saved_by     = relationship("SavedJob",    back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id           = Column(Integer, primary_key=True, index=True)
    student_id   = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id       = Column(Integer, ForeignKey("jobs.id",  ondelete="CASCADE"), nullable=False)
    status       = Column(Enum("Applied", "Shortlisted", "Rejected"), default="Applied")
    applied_date = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", back_populates="applications")
    job     = relationship("Job",  back_populates="applications")


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id     = Column(Integer, ForeignKey("jobs.id",  ondelete="CASCADE"), nullable=False)
    saved_date = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", back_populates="saved_jobs")
    job     = relationship("Job",  back_populates="saved_by")


class Notification(Base):
    __tablename__ = "notifications"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message    = Column(String(500), nullable=False)
    is_read    = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
