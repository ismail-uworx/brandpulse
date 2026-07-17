"""
test_crud.py — a throwaway script to manually verify the pipeline:
rules engine -> crud.py -> Postgres, end to end.

Not part of the actual app - just for you to run and check things work.
"""

from app.database.session import SessionLocal
from app.database import crud
from app.routing.rules import assign_priority

db = SessionLocal()

priority, reason = assign_priority("Negative", "Billing", [])

row = crud.create_complaint(
    db,
    source="reddit",
    author="user123",
    raw_text="I cannot make payments, getting a 500 error.",
    sentiment="Negative",
    category="Billing",
    confidence=0.9,
    original_timestamp=None,
    priority=priority,
    reason=reason,
)

print("Inserted:", row.id, row.priority, row.reason)

db.close()