"""
dependencies.py — small reusable pieces that FastAPI "injects" into
routes automatically. Right now just one: a database session per request.
"""

from app.database.session import get_db

# Just re-exporting get_db here so routes.py imports from `api.dependencies`
# instead of reaching into `database.session` directly — keeps the API
# layer's imports pointing at API-layer files.