"""Minimal YAML front-matter handling for issue files.

Hand-rolled on purpose, like the rest of socialgen/sitegen: a real YAML
round-trip would reflow `tags: [a, b, c]` into block style and rewrite quoting
across all 109 files, turning a 3-line-per-file diff into an unreviewable one.
Here every untouched line is preserved byte for byte.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_KEY_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):\s?(?P<value>.*)$")

# Keys sitegen owns. Order is the order they are written in.
MANAGED_KEYS = ("seo_title", "description", "sections")


def split(text: str) -> Tuple[Optional[List[str]], str]:
    """(front matter lines without the --- fences, body including its leading
    newline). Returns (None, text) when the file has no front matter."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            # The body keeps the newline that follows the closing fence, so
            # `"---" + body` reconstructs the file exactly.
            return lines[1:i], "\n" + "\n".join(lines[i + 1:])
    return None, text


def values(fm_lines: List[str]) -> Dict[str, str]:
    """Top-level `key: value` pairs as raw (unparsed) strings."""
    out = {}
    for line in fm_lines:
        if line[:1] in (" ", "\t", "#") or not line.strip():
            continue
        m = _KEY_RE.match(line)
        if m:
            out[m.group("key")] = m.group("value").strip()
    return out


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def tags(fm_lines: List[str]) -> List[str]:
    """The `tags:` flow sequence. Block sequences are supported too, since a few
    early issues use them."""
    raw = values(fm_lines).get("tags", "")
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [unquote(t.strip()) for t in inner.split(",") if t.strip()] if inner else []
    if raw:
        return [unquote(raw)]
    # block style: `tags:` then `  - item`
    out = []
    seen_tags = False
    for line in fm_lines:
        if line.strip() == "tags:":
            seen_tags = True
            continue
        if seen_tags:
            if line.startswith(("-", " ", "\t")) and line.strip().startswith("- "):
                out.append(unquote(line.strip()[2:].strip()))
            elif line.strip():
                break
    return out


def quote(value: str) -> str:
    """Double-quoted YAML scalar. Issue titles carry apostrophes, colons and
    em-dashes, so quoting is not optional."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def flow_list(items) -> str:
    return "[" + ", ".join(items) + "]"


def render(text: str, updates: Dict[str, str]) -> str:
    """Return `text` with `updates` applied to its front matter.

    An existing managed key is replaced in place; a new one is appended at the
    end of the block. Every other line — key order, comments, quoting, the body —
    is untouched, so re-running on an already-backfilled file is a no-op.
    """
    fm_lines, body = split(text)
    if fm_lines is None:
        raise ValueError("file has no YAML front matter")

    out = list(fm_lines)
    for key, value in updates.items():
        line = f"{key}: {value}"
        for i, existing in enumerate(out):
            m = _KEY_RE.match(existing)
            if m and m.group("key") == key:
                out[i] = line
                break
        else:
            out.append(line)

    return "---\n" + "\n".join(out) + "\n---" + body


def read(path) -> str:
    return Path(path).read_text(encoding="utf-8")
