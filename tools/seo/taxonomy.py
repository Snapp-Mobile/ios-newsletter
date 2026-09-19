"""Section normalization.

The real taxonomy of the newsletter lives in `## Section` headings inside issue
bodies, written by hand over two years — so it drifted: `AI/ML` vs `AI / ML` vs
`AI`, `Talk` vs `Talks`, `Xcode` vs `XCode` vs `Xcode tips`. 70 distinct strings
collapse to the topics below.

An unknown string is NOT silently dropped: it falls through to a slugified
passthrough and `sitegen check` reports it, which is the signal to add a mapping
here before the next issue ships.
"""

import re
import unicodedata

# canonical slug -> display label
TOPIC_LABELS = {
    "swift": "Swift",
    "swiftui": "SwiftUI",
    "ui-ux": "UI & UX",
    "ai-ml": "AI & ML",
    "tools": "Tools",
    "talks-videos": "Talks & Videos",
    "utils": "Utils & Tips",
    "data": "Data & Persistence",
    "development": "Development & Architecture",
    "testing": "Testing",
    "frameworks": "Frameworks",
    "concurrency": "Concurrency",
    "visionos": "visionOS",
    "platforms": "Other Apple Platforms",
    "news": "News & Opinion",
    "server-web": "Server & Web",
    "app-store": "App Store & Monetization",
    "security": "Security & Privacy",
    "open-source": "Open Source",
    "misc": "Miscellaneous",
}

# Raw heading text (lowercased, whitespace-collapsed) -> canonical slug.
SECTION_MAP = {
    # swift
    "swift": "swift",
    "swift 6": "swift",
    "swift6": "swift",
    "programming": "swift",
    "api": "swift",
    # swiftui
    "swiftui": "swiftui",
    # ui / ux
    "ui/ux": "ui-ux",
    "ui": "ui-ux",
    "ux": "ui-ux",
    "design": "ui-ux",
    "accessibility": "ui-ux",
    "3d": "ui-ux",
    # ai
    "ai/ml": "ai-ml",
    "ai": "ai-ml",
    "ml": "ai-ml",
    "agents": "ai-ml",
    # tooling
    "tools": "tools",
    "xcode": "tools",
    "xcode tips": "tools",
    "automation": "tools",
    "instruments": "tools",
    "profiling": "tools",
    "spm": "tools",
    "swift package manager": "tools",
    # talks + video
    "talk": "talks-videos",
    "talks": "talks-videos",
    "video": "talks-videos",
    "videos": "talks-videos",
    "wwdc": "talks-videos",
    "wwdc26": "talks-videos",
    # data
    "data": "data",
    "swiftdata": "data",
    "persistence": "data",
    # utils
    "utils": "utils",
    "tips": "utils",
    "productivity": "utils",
    # testing
    "testing": "testing",
    # frameworks
    "framework": "frameworks",
    "frameworks": "frameworks",
    "maps": "frameworks",
    # concurrency
    "concurrency": "concurrency",
    "swift concurrency": "concurrency",
    # visionOS
    "visionos": "visionos",
    # development
    "development": "development",
    "architecture": "development",
    "software architecture": "development",
    "ci": "development",
    "deployment": "development",
    # other Apple platforms
    "macos": "platforms",
    "watchos": "platforms",
    "ipados": "platforms",
    "ios": "platforms",
    "multiplatform": "platforms",
    # news
    "news": "news",
    "apple": "news",
    "opinion": "news",
    # server / web
    "swift on server": "server-web",
    "server-side swift": "server-web",
    "website": "server-web",
    "vm": "server-web",
    "virtualization": "server-web",
    # store
    "appstore": "app-store",
    "app store": "app-store",
    "storekit": "app-store",
    "payments": "app-store",
    "sales": "app-store",
    "app": "app-store",
    # security
    "security": "security",
    "privacy": "security",
    "hacking": "security",
    # open source
    "repository": "open-source",
    "repositories": "open-source",
    # genuinely unclassifiable headings
    "other": "misc",
    "interesting": "misc",
    "fun": "misc",
    "book": "misc",
}

# Topics that never get a hub page no matter how many items they collect.
NEVER_HUB = {"misc"}

_WS_RE = re.compile(r"\s+")
_SLUG_STRIP_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Lowercase ASCII slug: 'Swift on Server' -> 'swift-on-server'."""
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return _SLUG_STRIP_RE.sub("-", norm.lower()).strip("-")


def canonical_key(raw: str) -> str:
    """Lookup key: lowercased, whitespace collapsed, and spaces removed around
    a slash so 'AI / ML' and 'AI/ML' land on the same entry."""
    key = _WS_RE.sub(" ", raw.strip().lower())
    return re.sub(r"\s*/\s*", "/", key)


def normalize_section(raw: str) -> str:
    """Canonical topic slug for a raw `## Section` heading.

    Unknown headings return their own slug — visible, not lost — and are
    reported by `sitegen check`.
    """
    if not raw or not raw.strip():
        return "misc"
    return SECTION_MAP.get(canonical_key(raw), slugify(raw))


def is_known(raw: str) -> bool:
    return canonical_key(raw) in SECTION_MAP


def label_for(slug: str) -> str:
    return TOPIC_LABELS.get(slug, slug.replace("-", " ").title())
