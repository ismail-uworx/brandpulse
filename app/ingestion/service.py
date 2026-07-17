"""
Service layer for BrandPulse ingestion.

This module orchestrates the complete ingestion pipeline.

Pipeline:
Source
    ↓
Parser
    ↓
Cleaner
    ↓
Packet Builder
"""

from __future__ import annotations

import logging
from itertools import cycle
from pathlib import Path

from app.ingestion.cleaner import Cleaner
from app.ingestion.packet import PacketBuilder
from app.ingestion.parser import Parser
from app.ingestion.sources.mock import MockSource
from app.ingestion.sources.rss import RSSSource

logger = logging.getLogger(__name__)


class IngestionService:
    """
    Orchestrates the complete ingestion pipeline.
    """

    def __init__(
        self,
        rss_url: str,
        mock_file: str | Path,
        default_source: str = "rss",
    ) -> None:

        self.rss = RSSSource(rss_url)
        self.mock = MockSource(mock_file)

        self.default_source = default_source.lower()

        # Used to iterate through entries one-by-one
        self._rss_entries = None
        self._mock_entries = None

    def _next_rss(self) -> dict:
        """
        Return the next RSS packet.
        """

        if self._rss_entries is None:
            entries = self.rss.fetch()

            if not entries:
                raise RuntimeError("RSS feed returned no entries.")

            self._rss_entries = cycle(entries)

        entry = next(self._rss_entries)

        record = Parser.parse_rss(entry)

        record["text"] = Cleaner.clean(record["text"])

        return PacketBuilder.build(record)

    def _next_mock(self) -> dict:
        """
        Return the next mock packet.
        """

        if self._mock_entries is None:
            entries = self.mock.fetch()

            if not entries:
                raise RuntimeError("Mock dataset is empty.")

            self._mock_entries = cycle(entries)

        entry = next(self._mock_entries)

        record = Parser.parse_mock(entry)

        record["text"] = Cleaner.clean(record["text"])

        return PacketBuilder.build(record)

    def next_packet(self) -> dict:
        """
        Return the next BrandPulse packet.

        Returns:
            BrandPulse packet.
        """

        logger.info("Generating next packet.")

        if self.default_source == "rss":
            return self._next_rss()

        if self.default_source == "mock":
            return self._next_mock()

        raise ValueError(
            f"Unknown source '{self.default_source}'. "
            "Expected 'rss' or 'mock'."
        )