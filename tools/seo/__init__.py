"""Derive an issue's SEO front matter from the issue itself.

Standard library only, so a GitHub Actions runner needs nothing installed.
"""

# Google truncates around these.
TITLE_MAX = 60
DESCRIPTION_MAX = 155
