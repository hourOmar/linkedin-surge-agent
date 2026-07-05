from pathlib import Path
from typing import Any

import yaml

from app.services.content_calendar_loader import (
    CONTENT_CALENDAR_FILENAME,
    ContentCalendarLoadError,
    load_content_calendar,
)

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
CONTENT_CALENDAR_DIRNAME = "content_calendar"

MARKDOWN_SUFFIXES = {".md"}
YAML_SUFFIXES = {".yaml", ".yml"}


class KnowledgeLoadError(Exception):
    """Raised when the knowledge base cannot be loaded."""


def _load_files_in_dir(dir_path: Path) -> dict[str, Any]:
    """Load Markdown and YAML files directly inside `dir_path` into a dict keyed by filename stem."""
    files: dict[str, Any] = {}

    for file_path in sorted(dir_path.iterdir()):
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()
        key = file_path.stem

        if suffix in MARKDOWN_SUFFIXES:
            files[key] = file_path.read_text(encoding="utf-8")
        elif suffix in YAML_SUFFIXES:
            try:
                files[key] = yaml.safe_load(file_path.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                raise KnowledgeLoadError(f"Invalid YAML in {file_path.name}: {exc}") from exc
        else:
            continue

    return files


def load_knowledge(knowledge_dir: Path | str = KNOWLEDGE_DIR) -> dict[str, Any]:
    """Load all Markdown and YAML files from `knowledge_dir` into a single dict.

    Files directly inside `knowledge_dir` are loaded as top-level keys. The dict
    key is the filename without its extension, e.g. `company_profile.md` ->
    kb["company_profile"].

    The LinkedIn content calendar is loaded from
    `content_calendar/linkedin_content_calendar.xlsx` and nested under
    kb["content_calendar"] as {"Week 1": {"Post 1": {...}, ...}, ...}. See
    `app.services.content_calendar_loader` for the schema and helpers
    (`get_week`, `get_post`, `iter_posts`). If that file does not exist,
    kb["content_calendar"] is an empty dict.
    """
    knowledge_dir = Path(knowledge_dir)

    if not knowledge_dir.is_dir():
        raise KnowledgeLoadError(f"Knowledge folder not found: {knowledge_dir}")

    kb = _load_files_in_dir(knowledge_dir)

    calendar_path = knowledge_dir / CONTENT_CALENDAR_DIRNAME / CONTENT_CALENDAR_FILENAME
    try:
        kb[CONTENT_CALENDAR_DIRNAME] = load_content_calendar(calendar_path)
    except ContentCalendarLoadError as exc:
        raise KnowledgeLoadError(str(exc)) from exc

    return kb
