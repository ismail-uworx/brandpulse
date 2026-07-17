"""
main.py — starts the whole backend application.

Running `uvicorn app.main:app --reload` executes this file, which:
  1. Creates the `complaints` table if it doesn't exist yet
  2. Registers all routes from routes.py
  3. Starts listening for real HTTP requests
"""

from fastapi import FastAPI

from app.database.session import engine, Base
from app.database import models  # noqa: F401 — import needed so Base knows about the table
from app.api.routes import router

# Creates tables based on models.py if they don't already exist.
# Safe to call every time the app starts — does nothing if tables
# already exist (same create_all() behavior you already saw).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BrandPulse Backend",
    description="Applies priority rules to AI-analyzed complaints and stores them.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def health_check():
    """A simple endpoint just to confirm the server is alive."""
    return {"status": "BrandPulse backend is running"}