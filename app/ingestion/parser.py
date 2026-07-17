"""
Parser for BrandPulse ingestion.

Converts raw source-specific records into one common normalized structure.

Output schema:
{
    "author": "...",
    "text": "...",
    "timestamp": "...",
    "source": "reddit"
}
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class Parser:
    """
    Normalize records from different ingestion sources.
    """

    @staticmethod
    def parse_rss(entry: Any) -> dict[str, str]:
        """
        Normalize a feedparser RSS entry.

        Args:
            entry: feedparser entry.

        Returns:
            Normalized record.
        """

        author = getattr(entry, "author", "Unknown")

        title = getattr(entry, "title", "")

        summary = getattr(entry, "summary", "")

        timestamp = getattr(entry, "published", "")

        text = f"{title} {summary}".strip()

        logger.debug("Parsed RSS entry from author: %s", author)

        return {
            "author": author,
            "text": text,
            "timestamp": timestamp,
            "source": "reddit",
        }

    @staticmethod
    def parse_mock(entry: dict[str, Any]) -> dict[str, str]:
        author = entry.get("author", "Unknown")
        timestamp = entry.get("timestamp", "")
        
        # Check if a unified text key is provided directly
        if "text" in entry:
            text = entry["text"]
        else:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            text = f"{title} {summary}".strip()

        logger.debug("Parsed mock entry from author: %s", author)

        return {
            "author": author,
            "text": text,
            "timestamp": timestamp,
            "source": "mock",
        }