"""MkDocs hook: refresh capy's figures on the Explore page at build time.

The docs workflow clones capy (bare, blob-less) and exports CAPY_STATS_REPO with
the clone's path. This hook then counts capy's commits, ADRs and finished feature
records and writes them, with today's date, into the Explore page's
`explore.closing.stats` front matter before the template renders it.

Without CAPY_STATS_REPO (local builds, or a failed clone) the page keeps the
snapshot figures and as-of date written in docs/explore/index.md. If counting
fails or gives an implausible result, the snapshot is kept too and the reason is
reported as a GitHub Actions warning: dated figures are better than blocking a
docs deploy over three numbers. The report is logged at INFO, not WARNING,
because `mkdocs build --strict` aborts on warnings.

Try it locally with: CAPY_STATS_REPO=../capy/.git make docs-build
"""

from __future__ import annotations

import datetime
import logging
import os
import re
import subprocess

log = logging.getLogger("mkdocs.hooks.capy_stats")

PAGE = "explore/index.md"
ADR_FILE = re.compile(r"^docs/adr/\d+-[^/]+\.md$")

_figures: dict[str, int] | None = None


def _git(repo: str, *args: str) -> str:
    return subprocess.run(
        ["git", "--git-dir", repo, *args], check=True, capture_output=True, text=True
    ).stdout


def _count(repo: str) -> dict[str, int]:
    commits = int(_git(repo, "rev-list", "--count", "HEAD").strip())
    adrs = sum(
        1 for path in _git(repo, "ls-tree", "--name-only", "HEAD", "docs/adr/").splitlines()
        if ADR_FILE.match(path)
    )
    features = len(_git(repo, "ls-tree", "-d", "--name-only", "HEAD", "docs/feat/done/").splitlines())
    figures = {"commits": commits, "adrs": adrs, "features": features}
    # A zero means capy's layout changed (or the clone is broken), not that the work vanished.
    empty = [key for key, value in figures.items() if value <= 0]
    if empty:
        raise ValueError(f"no {', '.join(empty)} found; has capy's docs layout changed?")
    return figures


def _report(message: str) -> None:
    log.info(message)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::warning title=Explore page figures::{message}")


def on_config(config):
    global _figures
    _figures = None
    repo = os.environ.get("CAPY_STATS_REPO")
    if not repo:
        return config
    try:
        _figures = _count(repo)
    except (OSError, subprocess.CalledProcessError, ValueError) as err:
        detail = err.stderr.strip() if isinstance(err, subprocess.CalledProcessError) else err
        _report(f"Kept the snapshot capy figures: counting {repo} failed: {detail}")
    else:
        log.info("capy figures from %s: %s", repo, _figures)
    return config


def on_page_markdown(markdown, page, config, files):
    if _figures is None or page.file.src_uri != PAGE:
        return markdown
    stats = page.meta.get("explore", {}).get("closing", {}).get("stats")
    if not stats:
        _report(f"Kept the snapshot capy figures: {PAGE} has no explore.closing.stats")
        return markdown
    for item in stats["items"]:
        if item.get("key") in _figures:
            item["value"] = str(_figures[item["key"]])
    stats["as_of"] = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    return markdown
