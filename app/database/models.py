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

    # Primary key — uniquely identifies each row. The database
    # assigns 1, 2, 3... automatically; you never set this yourself.
    id = Column(Integer, primary_key=True, index=True)

    # --- From Ismail's ingestion stage ---
    source = Column(String, index=True)       # e.g. "reddit", "twitter"
    author = Column(String)
    raw_text = Column(String)
    # When the complaint actually happened, per Ismail's packet —
    # nullable=True because you don't control whether every source
    # reliably includes a timestamp.
    original_timestamp = Column(DateTime(timezone=True), nullable=True)

    # --- From Basim's AI stage ---
    sentiment = Column(String, index=True)     # "Positive" / "Negative" / "Neutral"
    category = Column(String, index=True)      # "Billing" / "Security" / etc.
    confidence = Column(Float, nullable=True)  # how sure the AI was, 0-1
    # keywords removed — Basim isn't doing keyword extraction

    # --- Your decision ---
    priority = Column(String, index=True)      # "Low" / "Medium" / "High" / "Critical"
    reason = Column(String)                    # why — from rules.py

    # When YOUR system processed/stored it (separate from when the
    # complaint originally happened — see original_timestamp above)
    created_at = Column(DateTime(timezone=True), server_default=func.now())