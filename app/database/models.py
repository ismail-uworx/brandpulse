"""
models.py — defines the `complaints` table.

Each class here = one table. Each class attribute = one column.
SQLAlchemy translates this Python class into real SQL behind the
scenes — you'll never hand-write CREATE TABLE yourself.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.database.session import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    packet_id = Column(String, nullable=True, index=True)

    source = Column(String, index=True)
    author = Column(String)
    raw_text = Column(String)
    timestamp = Column(String, nullable=True)   # renamed from original_timestamp

    sentiment = Column(String, index=True)
    category = Column(String, index=True)
    confidence = Column(Float, nullable=True)

    priority = Column(String, index=True)
    reason = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())