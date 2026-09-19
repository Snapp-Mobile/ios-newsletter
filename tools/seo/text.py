"""Per-issue `<title>` and `<meta name="description">` text.

Both are derived, never authored: the title comes from what the issue actually
covers, the description from the editorial intro that already gets written every
week. Deterministic, so a rerun produces the same bytes.
"""

import re
from typing import List, Optional

from . import DESCRIPTION_MAX, TITLE_MAX

BRAND = "Snapp iOS Weekly"

# Where a headline stops being the topic and starts being the pitch.
_CLAUSE_SPLIT_RE = re.compile(r"\s+[—–-]\s+|:\s+|\s+\(|,\s+|\s+\|\s+")
# Lead-ins that carry no topic: "How to animate a view" -> "animate a view".
_LEAD_IN_RE = re.compile(
    r"^(how to|how i|why you should|why i|what's new in|whats new in|a guide to|"
    r"an introduction to|introduction to|getting started with|understanding|"
    r"exploring|using|building|the complete guide to)\s+",
    re.IGNORECASE,
)
_TRAILING_PUNCT_RE = re.compile(r"[\s,.;:!?—–-]+$")

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_SIGNOFF_RE = re.compile(
    r"^(we hope|hope you|enjoy|happy reading|have a (great|good|nice)|"
    r"see you|let us know|as always,? (enjoy|thanks)|thanks for reading)",
    re.IGNORECASE,
)
_GREETING_RE = re.compile(r"^(hi|hello|hey)\b[^.!?]{0,40}[,!]\s*", re.IGNORECASE)
# A whole opening sentence that is only a greeting: "Hello again.", "Hey folks!"
_GREETING_SENTENCE_RE = re.compile(
    r"^(hi|hello|hey|welcome back|good morning|happy \w+)\b[^.!?]{0,40}[.!?]?$", re.IGNORECASE
)


def _topic_phrase(title: str, max_words: int) -> str:
    """The head noun phrase of an article title, at most `max_words` long."""
    head = _CLAUSE_SPLIT_RE.split(title.strip(), maxsplit=1)[0]
    head = _LEAD_IN_RE.sub("", head)
    words = head.split()
    if len(words) > max_words:
        words = words[:max_words]
    return _TRAILING_PUNCT_RE.sub("", " ".join(words))


def _candidates(issue, tags: Optional[List[str]] = None) -> List[str]:
    """Lead topics, best source first.

    `tags:` wins: they are hand-written short topic labels ("Swift Documentation",
    "iPhone Duo"), present on all 109 issues, and already the thing a human would
    put in a title. Article titles are the fallback, reduced to a head phrase —
    clipping a real headline to N words produces rubbish like "An Even Closer".
    """
    out = []
    for tag in (tags or []):
        tag = tag.strip()
        if tag and tag not in out:
            out.append(tag)
    if out:
        return out
    for article in issue.articles:
        phrase = _topic_phrase(article.title, 4)
        if phrase and phrase not in out:
            out.append(phrase)
    return out


def seo_title(issue, tags=None, limit: int = TITLE_MAX) -> str:
    """`Snapp iOS Weekly Issue 109`.

    Deliberately plain: the issue number identifies it, the brand names it. An
    earlier version led with the lead topics, which reads as keyword stuffing in
    a 109-row archive listing. The topics still reach search through the meta
    description and the topic hubs.
    """
    return f"{BRAND} Issue {issue.number}"


_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_MD_NOISE_RE = re.compile(r"^[>\s]+|[*_`]")


_DASH_RE = re.compile(r"\s*[\u2014\u2013\u2015]+\s*")


def _undash(text: str) -> str:
    """No em/en dashes in anything a reader sees.

    The intros are written with them; a comma carries the same clause break and
    keeps search snippets, social cards and feed summaries free of the dash.
    """
    return _DASH_RE.sub(", ", text)


def _demarkdown(text: str) -> str:
    """Plain prose out of the intro: link text without the target, no emphasis
    markers, no leading blockquote arrow."""
    text = _MD_LINK_RE.sub(r"\1", text)
    return _MD_NOISE_RE.sub("", text).strip()


def _clean_welcome(welcome: str) -> List[str]:
    text = _undash(_GREETING_RE.sub("", _demarkdown(welcome or "")))
    sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(text) if s.strip()]
    while sentences and _GREETING_SENTENCE_RE.match(sentences[0]):
        sentences.pop(0)
    while sentences and _SIGNOFF_RE.match(sentences[-1]):
        sentences.pop()
    return sentences


def meta_description(issue, tags: Optional[List[str]] = None, limit: int = DESCRIPTION_MAX) -> str:
    """The editorial intro, trimmed to a sentence boundary under `limit`.

    Falls back to a synthesized line for the early issues that have no intro.
    """
    sentences = _clean_welcome(issue.welcome)

    out = ""
    for sentence in sentences:
        candidate = f"{out} {sentence}".strip()
        if len(candidate) > limit:
            break
        out = candidate

    if not out and sentences:
        # A single opening sentence longer than the limit: clip on a word.
        clipped = sentences[0][:limit - 1].rsplit(" ", 1)[0]
        return _TRAILING_PUNCT_RE.sub("", clipped) + "…"

    # Nothing usable, or an intro so thin ("Exciting week ahead!") that it says
    # nothing a searcher could match on — top up with what the issue covers.
    if len(out) < _MIN_USEFUL:
        topics = _topic_summary(issue, tags, limit - len(out) - 1 if out else limit)
        if topics:
            return f"{out} {topics}".strip() if out else topics
    return out


_MIN_USEFUL = 80


def _topic_summary(issue, tags: Optional[List[str]], budget: int) -> str:
    """`Inside: Swift Documentation, CoreAI Quickstart, and 6 more links.`"""
    topics = _candidates(issue, tags)[:3]
    count = len(issue.articles)
    if not topics:
        if budget < 40:
            return ""
        return f"Issue {issue.number}: {count} curated iOS and Swift links with commentary."

    for take in (3, 2, 1):
        picked = topics[:take]
        rest = max(count - len(picked), 0)
        tail = f", and {rest} more links." if rest else " and more."
        text = "Inside: " + ", ".join(picked) + tail
        if len(text) <= budget:
            return text
    return ""
