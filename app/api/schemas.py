"""
schemas.py — defines what JSON is ALLOWED in and out of your API.

Different from models.py on purpose: models.py describes a database
ROW, this describes an API MESSAGE. E.g. when creating a complaint
you don't send an `id` (the database assigns that), but when reading
one back you DO get an `id`.

FastAPI uses these to auto-validate incoming requests — if a request
doesn't match the shape below, it's rejected with a clear error
before your code even runs.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AIPacketIn(BaseModel):
    """
    The shape you EXPECT to receive once Basim/Ismail's stages are
    wired in. This is your documented assumption — confirm it with
    them once they're ready, adjust here if their real output differs.
    """
    source: str
    author: str
    raw_text: str
    sentiment: str
    category: str
    confidence: Optional[float] = None
    original_timestamp: Optional[datetime] = None


class ComplaintOut(BaseModel):
    """What your API sends back out — includes fields YOU added."""
    id: int
    source: str
    author: str
    raw_text: str
    sentiment: str
    category: str
    priority: str
    reason: str
    created_at: datetime

    class Config:
        from_attributes = True  # lets Pydantic build this from a SQLAlchemy row directly