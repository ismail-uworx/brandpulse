"""
crud.py — Create, Read, Update, Delete. The only file allowed to
run actual queries against the database.

Why separate this from routes.py? routes.py should only worry about
HTTP concerns (status codes, request/response shapes). Database logic
lives here so it can be reused or tested independently of the API.
"""

from sqlalchemy.orm import Session
from app.database import models


def create_complaint(db: Session, *, source: str, author: str, raw_text: str,
                      sentiment: str, category: str, confidence: float | None,
                      original_timestamp, priority: str, reason: str) -> models.Complaint:
    """Takes the finished decision (from rules.py) and writes ONE row."""
    db_complaint = models.Complaint(
        source=source,
        author=author,
        raw_text=raw_text,
        original_timestamp=original_timestamp,
        sentiment=sentiment,
        category=category,
        confidence=confidence,
        priority=priority,
        reason=reason,
    )
    db.add(db_complaint)      # stage the row (not written yet)
    db.commit()                # actually write it to Postgres
    db.refresh(db_complaint)   # pull back the auto-generated id + created_at
    return db_complaint


def get_complaints(db: Session, priority: str | None = None, limit: int = 100):
    """Read complaints, optionally filtered by priority."""
    query = db.query(models.Complaint)
    if priority:
        query = query.filter(models.Complaint.priority == priority)
    return query.order_by(models.Complaint.created_at.desc()).limit(limit).all()