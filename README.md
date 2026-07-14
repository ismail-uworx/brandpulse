# BrandPulse

BrandPulse is a real-time AI-powered sentiment monitoring pipeline that ingests customer feedback, classifies sentiment and issue categories using local Hugging Face models, applies business routing rules, stores processed results in PostgreSQL, and exposes REST APIs through FastAPI.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Hugging Face Transformers
- Docker & Docker Compose
- Postman (API Testing)

## Project Structure

- `app/ingestion/` — Stream simulation and packet generation
- `app/ai/` — Sentiment and category inference
- `app/routing/` — Business rules and priority assignment
- `app/database/` — Database models and CRUD operations
- `app/api/` — REST API endpoints
- `data/` — Mock streaming dataset
- `tests/` — Test suite

## Team Responsibilities

- **Ismail:** Ingestion Pipeline
- **Basim:** AI Inference Pipeline
- **Momina:** Backend API, Database & Routing

## Development Workflow

- `main` → Stable releases
- `develop` → Integration branch
- `feature/ismail-ingestion`
- `feature/basim-ai`
- `feature/momina-backend`