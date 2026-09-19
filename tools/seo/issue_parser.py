"""Issue discovery and parsing over ios-newsletter/docs/_issues/."""

import re
from pathlib import Path
from typing import Optional

from .models import Article, Issue

ISSUE_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-issue-(\d+)\.md$")

_TITLE_RE = re.compile(r"^###\s+\[(?P<title>.+?)\]\((?P<url>[^)\s]+)\)\s*$")
# one author-link token, e.g. [Name](url){: .author} — used both to pull names
# out of a line and (anchored, repeated) to confirm the whole line is nothing else
_AUTHOR_LINK_RE = re.compile(r"\[(?P<author>[^\]]+)\]\((?P<url>[^)]*)\)\{:\s*\.author\s*\}")
# optional leading dash/em-dash/en-dash ("— [Name](url){: .author}") — issue 106
# switched to that style; earlier issues start straight at the author link
_AUTHOR_LINE_RE = re.compile(r"^(?:[—–-]\s*)?(?:\[[^\]]+\]\([^)]*\)\{:\s*\.author\s*\}(?:,\s*)?)+$")
_SECTION_RE = re.compile(r"^##\s+(?P<section>.+?)\s*$")
_FRONTMATTER_DATE_RE = re.compile(r"^date:\s*(\d{4}-\d{2}-\d{2})\s*$")

_GREETING_RE = re.compile(r"^(hi|hello|hey)\b.{0,40}[,!]$", re.IGNORECASE)
_SIGNOFF_RE = re.compile(r"^enjoy\W{0,3}$", re.IGNORECASE)
_BUTTON_RE = re.compile(r"^\[[^\]]+\]\([^)]*\)\{:\s*\.btn\s*\}")


def _frontmatter_date(lines) -> Optional[str]:
    """The `date:` value from the YAML front matter block, or None if absent."""
    if not (lines and lines[0].strip() == "---"):
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = _FRONTMATTER_DATE_RE.match(line.strip())
        if m:
            return m.group(1)
    return None


def _parse_welcome(lines) -> str:
    """Editorial intro: prose between YAML front matter and the first heading,
    minus the greeting, sign-off, and subscribe button."""
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    kept = []
    while i < len(lines) and not lines[i].startswith("#"):
        text = lines[i].strip()
        i += 1
        if not text or _GREETING_RE.match(text) or _SIGNOFF_RE.match(text) or _BUTTON_RE.match(text):
            continue
        kept.append(text)
    return " ".join(kept)


def find_latest_issue_path(issues_dir) -> Optional[Path]:
    """Highest issue number wins (numeric, not lexicographic)."""
    best, best_n = None, -1
    for path in Path(issues_dir).iterdir():
        m = ISSUE_FILE_RE.match(path.name)
        if m and int(m.group(2)) > best_n:
            best_n = int(m.group(2))
            best = path
    return best


def parse_issue(path) -> Issue:
    path = Path(path)
    m = ISSUE_FILE_RE.match(path.name)
    if not m:
        raise ValueError(f"not an issue file: {path.name}")
    date, number = m.group(1), int(m.group(2))

    lines = path.read_text(encoding="utf-8").splitlines()
    articles = []
    section = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        sec = _SECTION_RE.match(line)
        if sec:
            section = sec.group("section")
            i += 1
            continue
        title = _TITLE_RE.match(line)
        if title:
            author = ""
            author_urls = {}
            description = ""
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                author_line = lines[j].strip()
                if _AUTHOR_LINE_RE.match(author_line):
                    matches = list(_AUTHOR_LINK_RE.finditer(author_line))
                    author = " & ".join(m.group("author") for m in matches)
                    author_urls = {m.group("author"): m.group("url") for m in matches}
                    j += 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            desc_lines = []
            while j < len(lines) and lines[j].strip() and not lines[j].startswith("#"):
                desc_lines.append(lines[j].strip())
                j += 1
            description = " ".join(desc_lines)
            articles.append(Article(
                title=title.group("title"),
                url=title.group("url"),
                author=author,
                section=section,
                description=description,
                author_urls=author_urls,
            ))
            i = j
            continue
        i += 1

    return Issue(number=number, date=date, path=str(path), articles=articles,
                 welcome=_parse_welcome(lines), frontmatter_date=_frontmatter_date(lines))


def load_latest_issue(issues_dir) -> Issue:
    path = find_latest_issue_path(issues_dir)
    if path is None:
        raise FileNotFoundError(f"no issue files in {issues_dir}")
    return parse_issue(path)
