"""
rules.py — decides how urgent a complaint is, based on what Basim's
AI stage figured out (sentiment + category + keywords).

Kept in its own file/folder (app/routing/) separate from the database
and API layers on purpose: priority policy changes often as the
business changes its mind about what's "urgent" — you don't want to
go hunting through database or API code to update a rule.
"""

from typing import Tuple

# Categories considered high-stakes regardless of sentiment.
CRITICAL_CATEGORIES = {"security", "payment", "billing", "outage"}

# Keywords that escalate priority even if sentiment is ambiguous.
URGENT_KEYWORDS = {"down", "hacked", "breach", "fraud", "500", "error", "unauthorized"}


def assign_priority(sentiment: str, category: str, keywords: list[str]) -> Tuple[str, str]:
    """
    Returns (priority, reason) — the reason is a human-readable
    explanation of the decision, so anyone reading a stored complaint
    later understands WHY it got that priority, not just that it did.
    """
    sentiment_l = sentiment.lower()
    category_l = category.lower()
    keywords_l = {k.lower() for k in keywords}

    if sentiment_l == "negative" and category_l in CRITICAL_CATEGORIES:
        return "Critical", f"Negative sentiment in a high-stakes category ({category})"

    matched = keywords_l & URGENT_KEYWORDS
    if matched:
        return "Critical", f"Urgent keyword(s) detected: {', '.join(matched)}"

    if sentiment_l == "negative":
        return "High", f"Negative sentiment in category '{category}'"

    if sentiment_l == "neutral":
        return "Medium", "Neutral sentiment — routine review"

    return "Low", "Positive sentiment — no action needed"