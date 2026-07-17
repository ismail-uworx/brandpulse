"""
Cleaner for BrandPulse ingestion.

Responsible for sanitizing normalized text before it is sent
to the AI pipeline.

The cleaner removes formatting artifacts while preserving
the original meaning of the text.
"""

from __future__ import annotations

import html
import logging
import re

logger = logging.getLogger(__name__)


class Cleaner:
    """
    Cleans normalized text for NLP processing.
    """

    # Matches HTML tags such as <p>, <div>, <b>, etc.
    HTML_TAG_PATTERN = re.compile(r"<[^>]+>")

    # Matches multiple whitespace characters
    WHITESPACE_PATTERN = re.compile(r"\s+")

    @classmethod
    def clean(cls, text: str) -> str:
        """
        Clean text while preserving punctuation and casing.

        Args:
            text:
                Raw normalized text.

        Returns:
            Cleaned text.
        """

        if not text:
            return ""

        logger.debug("Cleaning text.")

        # Convert HTML entities
        # Example:
        # "&amp;" -> "&"
        # "&lt;"  -> "<"
        text = html.unescape(text)

        # Remove HTML tags
        text = cls.HTML_TAG_PATTERN.sub(" ", text)

        # Replace tabs/newlines/multiple spaces with a single space
        text = cls.WHITESPACE_PATTERN.sub(" ", text)

        # Remove leading/trailing whitespace
        text = text.strip()

        logger.debug("Finished cleaning text.")

        return text