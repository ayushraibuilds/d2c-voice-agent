"""
Sentiment Analysis for D2C Voice-First Agent.

Uses keyword-based + LLM-backed sentiment detection to identify
frustrated customers and auto-escalate when needed.

Sentiment levels:
  - POSITIVE: Happy, grateful, satisfied
  - NEUTRAL: Default, informational queries
  - NEGATIVE: Mild frustration, complaint
  - CRITICAL: Angry, threatening, abusive — auto-escalate
"""

import re
from enum import Enum
from logger import get_logger

log = get_logger()


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    CRITICAL = "critical"


# ── Keyword patterns ──
_CRITICAL_PATTERNS = [
    r"consumer\s*(court|forum|complaint)",
    r"legal\s*(action|notice)",
    r"police\s*(complaint|report)",
    r"worst\s*(service|experience|company|app)",
    r"scam|fraud|cheat|loot|dhoka",
    r"report\s*(you|this|company)",
    r"never\s*(buy|order|use)\s*(again|from)",
    r"disgusting|pathetic|horrible|terrible|useless",
    r"social\s*media|twitter|tweet|viral",
    r"refund\s*(abhi|now|immediately|turant)",
]

_NEGATIVE_PATTERNS = [
    r"angry|frustrated|irritated|upset|annoyed",
    r"problem|issue|complaint",
    r"not\s*(happy|satisfied|working|received)",
    r"bad|poor|slow|late|wrong|broken|damaged",
    r"kaise|kyun|kab\s*(aayega|milega)",
    r"bahut\s*(bura|kharab|slow)|bohot\s*(bura|kharab)",
    r"waiting|still\s*(waiting|pending)",
    r"no\s*(response|reply|update)",
    r"disappointed|unacceptable",
]

_POSITIVE_PATTERNS = [
    r"thank|thanks|dhanyavad|shukriya",
    r"great|awesome|excellent|amazing|perfect",
    r"happy|satisfied|pleased",
    r"love|loved|good\s*(service|job|work)",
    r"helpful|resolved|fixed|sorted",
    r"bahut\s*(accha|acha|badhiya)|very\s*(good|nice)",
]

_CRITICAL_RE = re.compile("|".join(_CRITICAL_PATTERNS), re.IGNORECASE)
_NEGATIVE_RE = re.compile("|".join(_NEGATIVE_PATTERNS), re.IGNORECASE)
_POSITIVE_RE = re.compile("|".join(_POSITIVE_PATTERNS), re.IGNORECASE)

# Auto-escalation threshold: if negative sentiment repeats this many times
# in the conversation, escalate even without CRITICAL keywords.
ESCALATION_THRESHOLD = 3


def analyze_sentiment(message: str) -> Sentiment:
    """
    Analyze sentiment using keyword matching.

    Returns the detected sentiment level.
    """
    if not message:
        return Sentiment.NEUTRAL

    text = message.lower()

    # Check critical first
    if _CRITICAL_RE.search(text):
        log.info("Sentiment: CRITICAL detected")
        return Sentiment.CRITICAL

    positive_matches = len(_POSITIVE_RE.findall(text))
    negative_matches = len(_NEGATIVE_RE.findall(text))

    if negative_matches > 0 and negative_matches > positive_matches:
        log.info(f"Sentiment: NEGATIVE ({negative_matches} signals)")
        return Sentiment.NEGATIVE

    if positive_matches > 0:
        return Sentiment.POSITIVE

    return Sentiment.NEUTRAL


def should_auto_escalate(
    current_sentiment: Sentiment,
    conversation_sentiments: list[Sentiment],
) -> bool:
    """
    Decide if we should auto-escalate to a human agent.

    Escalate if:
    1. Current message is CRITICAL, OR
    2. There have been ESCALATION_THRESHOLD or more NEGATIVE messages
       in the recent conversation.
    """
    if current_sentiment == Sentiment.CRITICAL:
        return True

    # Count recent negative sentiments (including current)
    recent = conversation_sentiments[-10:]  # last 10 messages
    negative_count = sum(
        1 for s in recent
        if s in (Sentiment.NEGATIVE, Sentiment.CRITICAL)
    )

    if current_sentiment == Sentiment.NEGATIVE:
        negative_count += 1

    return negative_count >= ESCALATION_THRESHOLD
