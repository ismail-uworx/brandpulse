"""
Mock source for BrandPulse.

This module reads raw mock posts from a local JSON file.
It does NOT perform parsing, cleaning, or packet generation.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class MockSource:
    """
    Reads raw mock entries from a JSON file.
    """

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def fetch(self) -> list[dict[str, Any]]:
        """
        Read raw mock entries.

        Returns:
            List of raw mock entries.

        Raises:
            FileNotFoundError:
                If the JSON file does not exist.

            ValueError:
                If the JSON root is not a list.

            json.JSONDecodeError:
                If the JSON is invalid.
        """

        logger.info("Loading mock dataset: %s", self.file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Mock dataset not found: {self.file_path}"
            )

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Mock dataset must contain a JSON array."
            )

        logger.info("Loaded %d mock entries.", len(data))

        return data