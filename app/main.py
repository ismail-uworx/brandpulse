"""
main.py — starts the whole backend application.

Running `uvicorn app.main:app --reload` executes this file, which:
  1. Creates the `complaints` table if it doesn't exist yet
  2. Registers all routes from routes.py
  3. Starts listening for real HTTP requests
"""

from fastapi import FastAPI

from app.database.session import engine, Base
from app.database import models  # noqa: F401
from app.api.routes import router

# Create database tables if they don't already exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BrandPulse Backend",
    description="Applies priority rules to AI-analyzed complaints and stores them.",
    version="1.0.0",
)

# Register API routes
app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "BrandPulse backend is running"}