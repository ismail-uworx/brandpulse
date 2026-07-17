"""
Packet Builder for BrandPulse.

Converts a cleaned normalized record into the official
BrandPulse packet that is consumed by the AI layer.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import uuid4

logger = logging.getLogger(__name__)


class PacketBuilder:
    """
    Builds the BrandPulse packet.
    """

    @staticmethod
    def build(record: dict[str, str]) -> dict[str, str]:
        """
        Build the final BrandPulse packet.

        Args:
            record:
                A cleaned, normalized record.

        Returns:
            BrandPulse packet.
        """

        timestamp = record.get("timestamp", "").strip()

        # If timestamp is missing, use current UTC time.
        if not timestamp:
            timestamp = datetime.now(timezone.utc).isoformat()

        packet = {
            "packet_id": str(uuid4()),
            "source": record.get("source", ""),
            "author": record.get("author", "Unknown"),
            "raw_text": record.get("text", ""),
            "timestamp": timestamp,
        }

        logger.debug(
            "Packet created successfully. Packet ID: %s",
            packet["packet_id"],
        )

        return packet