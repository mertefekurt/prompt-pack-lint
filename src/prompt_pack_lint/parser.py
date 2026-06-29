from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from prompt_pack_lint.models import PromptFile


def parse_prompt_file(path: Path) -> PromptFile:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, Any] = {}
    body = text

    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            metadata = _parse_frontmatter(text[4:end])
            body = text[end + 4 :].lstrip("\n")

    return PromptFile(path=path, metadata=metadata, body=body)


def metadata_list(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, list):
        return {str(item).strip() for item in value if str(item).strip()}
    if isinstance(value, str):
        raw = value.strip()
        if raw.startswith("[") and raw.endswith("]"):
            raw = raw[1:-1]
        return {part.strip().strip("\"'") for part in raw.split(",") if part.strip()}
    return {str(value).strip()} if str(value).strip() else set()


def extract_placeholders(body: str) -> set[str]:
    return set(re.findall(r"(?<!{){([a-zA-Z_][\w-]*)}(?!})", body))


def _parse_frontmatter(text: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    current_key = ""
    list_items: list[str] = []

    def flush_list() -> None:
        nonlocal list_items, current_key
        if current_key and list_items:
            metadata[current_key] = list_items
        list_items = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_key:
            list_items.append(stripped[2:].strip().strip("\"'"))
            continue
        flush_list()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        current_key = key.strip()
        clean_value = value.strip()
        if clean_value:
            metadata[current_key] = clean_value.strip("\"'")
            current_key = ""
        else:
            metadata[current_key] = []
    flush_list()
    return metadata

