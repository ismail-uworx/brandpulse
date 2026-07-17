"""
routes.py — every URL your API responds to.

Kept "thin" on purpose: each route mostly just calls rules.py and
crud.py, then shapes the HTTP response. Business logic doesn't
belong here — it belongs in the files that already own it.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import crud
from app.api import schemas
from app.api.dependencies import get_db
from app.routing.rules import assign_priority

router = APIRouter()

@router.post("/complaints", response_model=schemas.ComplaintOut)
def ingest_complaint(packet: schemas.AIPacketIn, db: Session = Depends(get_db)):
    """
    The endpoint Basim's AI stage (eventually) calls once it's done
    analyzing a complaint. FastAPI checks the incoming JSON against
    AIPacketIn automatically — bad data gets rejected before this
    function even runs.
    """
    priority, reason = assign_priority(packet.sentiment, packet.category, [])

    saved = crud.create_complaint(
        db,
        packet_id=packet.packet_id,
        source=packet.source,
        author=packet.author,
        raw_text=packet.raw_text,
        sentiment=packet.sentiment,
        category=packet.category,
        confidence=packet.confidence,
        timestamp=packet.timestamp,
        priority=priority,
        reason=reason,
    )
    return saved

@router.get("/complaints", response_model=list[schemas.ComplaintOut])
def list_complaints(priority: str | None = None, db: Session = Depends(get_db)):
    """GET /complaints or GET /complaints?priority=Critical"""
    return crud.get_complaints(db, priority=priority)


@router.get("/critical", response_model=list[schemas.ComplaintOut])
def list_critical(db: Session = Depends(get_db)):
    """Shortcut for GET /complaints?priority=Critical, matching the original spec."""
    return crud.get_complaints(db, priority="Critical")