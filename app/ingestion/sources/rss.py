"""
RSS source for BrandPulse.

This module is responsible for fetching raw Reddit RSS entries.
It does NOT perform parsing, cleaning, or packet generation.
"""

from __future__ import annotations

import logging
from typing import List

import feedparser

logger = logging.getLogger(__name__)


class RSSSource:
    """
    Fetches raw entries from a Reddit RSS feed.
    """

    def __init__(self, feed_url: str) -> None:
        self.feed_url = feed_url

    def fetch(self) -> List[feedparser.FeedParserDict]:
        """
        Fetch raw RSS entries.

        Returns:
            List of feedparser entries.

        Raises:
            RuntimeError:
                If the RSS feed cannot be parsed.
        """

        logger.info("Fetching RSS feed: %s", self.feed_url)

        feed = feedparser.parse(self.feed_url)

        if feed.bozo:
            logger.warning("RSS parsing warning: %s", feed.bozo_exception)

        entries = feed.entries

        logger.info("Fetched %d RSS entries.", len(entries))

        return entries