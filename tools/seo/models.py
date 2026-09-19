"""The two records the parser produces."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Article:
    title: str
    url: str
    author: str
    section: str = ""
    description: str = ""
    author_urls: Dict[str, str] = field(default_factory=dict)


@dataclass
class Issue:
    number: int
    date: str            # YYYY-MM-DD, from the filename
    path: str
    articles: List[Article] = field(default_factory=list)
    welcome: str = ""    # the editorial intro between the front matter and "# Articles"
    frontmatter_date: Optional[str] = None
