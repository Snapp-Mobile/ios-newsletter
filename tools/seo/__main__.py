"""Write the derived SEO front matter into the issue files.

    python3 -m tools.seo                 every issue that needs it
    python3 -m tools.seo --issue 110     just that one
    python3 -m tools.seo --check         exit 1 if anything would change

Adds exactly three keys - seo_title, description, sections - and leaves every
other byte of the file alone. Running it twice produces no diff.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List

from . import frontmatter as fm
from . import text
from .issue_parser import ISSUE_FILE_RE, parse_issue
from .taxonomy import is_known, normalize_section

ISSUES_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "_issues"


def issue_paths(issues_dir) -> List[Path]:
    paths = [p for p in Path(issues_dir).iterdir() if ISSUE_FILE_RE.match(p.name)]
    return sorted(paths, key=lambda p: int(ISSUE_FILE_RE.match(p.name).group(2)))


def updates_for(path) -> Dict[str, str]:
    issue = parse_issue(path)
    fm_lines, _ = fm.split(fm.read(path))
    tags = fm.tags(fm_lines) if fm_lines else []

    sections: List[str] = []
    for article in issue.articles:
        topic = normalize_section(article.section)
        if topic not in sections:
            sections.append(topic)

    return {
        "seo_title": fm.quote(text.seo_title(issue, tags)),
        "description": fm.quote(text.meta_description(issue, tags)),
        "sections": fm.flow_list(sections),
    }


def unmapped_sections(path) -> List[str]:
    """`## Section` headings nobody has mapped to a topic yet."""
    out = []
    for article in parse_issue(path).articles:
        raw = article.section
        if raw and not is_known(raw) and raw not in out:
            out.append(raw)
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="tools.seo", description=__doc__)
    parser.add_argument("--issue", type=int, help="only this issue number")
    parser.add_argument("--issues-dir", default=ISSUES_DIR)
    parser.add_argument("--check", action="store_true",
                        help="report what would change, write nothing, exit 1 if anything would")
    args = parser.parse_args(argv)

    changed, unmapped = [], {}
    for path in issue_paths(args.issues_dir):
        number = int(ISSUE_FILE_RE.match(path.name).group(2))
        if args.issue is not None and number != args.issue:
            continue
        for raw in unmapped_sections(path):
            unmapped.setdefault(raw, []).append(number)
        before = fm.read(path)
        after = fm.render(before, updates_for(path))
        if before == after:
            continue
        changed.append(path)
        if not args.check:
            path.write_text(after, encoding="utf-8")

    for raw, numbers in sorted(unmapped.items()):
        print(f"warning: section {raw!r} (issue(s) {numbers}) has no entry in "
              f"taxonomy.py SECTION_MAP, so it falls back to its own slug", file=sys.stderr)

    if not changed:
        print("seo front matter: up to date")
        return 0

    verb = "would update" if args.check else "updated"
    print(f"seo front matter: {verb} {len(changed)} file(s)")
    for path in changed:
        print(f"  {path.name}")
    return 1 if args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
