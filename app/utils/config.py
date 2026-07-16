"""
config.py — the ONLY file that reads raw environment variables.

Everything else in the app imports `settings` from here instead of
calling os.getenv() directly. If a variable name ever changes, you
fix it in exactly one place.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Reads your .env file and loads its values into the process's
# environment variables. Safe to call even with no .env file present
# (it just does nothing in that case) — so this works the same
# whether you're running locally or inside Docker.
# Prefer .env.local (for running Python directly on your machine).
# Falls back to .env if .env.local doesn't exist (e.g. inside Docker).
env_file = ".env.local" if Path(".env.local").exists() else ".env"
load_dotenv(env_file)


class Settings:
    postgres_user: str = os.getenv("POSTGRES_USER", "brandpulse")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "brandpulse123")
    postgres_db: str = os.getenv("POSTGRES_DB", "brandpulse")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")

    @property
    def database_url(self) -> str:
        """
        Builds the full connection string SQLAlchemy needs, e.g.:
        postgresql://brandpulse:brandpulse123@localhost:5432/brandpulse
        """
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


# One shared instance the whole app imports.
settings = Settings()