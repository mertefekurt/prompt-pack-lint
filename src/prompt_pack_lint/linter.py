from __future__ import annotations

import json
import re
from pathlib import Path

from prompt_pack_lint.models import Issue, PromptFile
from prompt_pack_lint.parser import extract_placeholders, metadata_list, parse_prompt_file

REQUIRED_METADATA = ("owner", "version", "purpose")
RISK_PATTERNS = {
    "override-instructions": re.compile(r"\b(ignore|override).{0,30}(previous|system)", re.I),
    "unbounded-compliance": re.compile(r"\b(always comply|do anything|no restrictions)\b", re.I),
    "secret-exposure": re.compile(r"\b(print|reveal|show).{0,30}(secret|api key|token)\b", re.I),
}
SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3}


def scan_prompt_path(path: Path) -> list[Issue]:
    files = _prompt_files(path)
    issues: list[Issue] = []
    for file_path in files:
        issues.extend(lint_prompt_file(file_path))
    return issues


def lint_prompt_file(path: Path) -> list[Issue]:
    prompt = parse_prompt_file(path)
    issues: list[Issue] = []
    issues.extend(_metadata_issues(prompt))
    issues.extend(_variable_issues(prompt))
    issues.extend(_risk_issues(prompt))
    return issues


def issues_to_json(issues: list[Issue]) -> str:
    return json.dumps([issue.to_dict() for issue in issues], indent=2) + "\n"


def issues_to_markdown(issues: list[Issue]) -> str:
    if not issues:
        return "# prompt-pack-lint report\n\nNo issues found.\n"
    lines = ["# prompt-pack-lint report", ""]
    for issue in issues:
        lines.append(f"- **{issue.severity}** `{issue.code}` in `{issue.path}`: {issue.message}")
    return "\n".join(lines) + "\n"


def has_failure(issues: list[Issue], fail_on: str) -> bool:
    threshold = SEVERITY_ORDER[fail_on]
    return any(SEVERITY_ORDER[issue.severity] >= threshold for issue in issues)


def _metadata_issues(prompt: PromptFile) -> list[Issue]:
    issues: list[Issue] = []
    for key in REQUIRED_METADATA:
        if not str(prompt.metadata.get(key, "")).strip():
            issues.append(
                Issue(
                    path=str(prompt.path),
                    code="missing-metadata",
                    severity="medium",
                    message=f"frontmatter is missing required key '{key}'",
                )
            )
    return issues


def _variable_issues(prompt: PromptFile) -> list[Issue]:
    declared = metadata_list(prompt.metadata.get("variables"))
    used = extract_placeholders(prompt.body)
    issues: list[Issue] = []

    for name in sorted(used - declared):
        issues.append(
            Issue(
                path=str(prompt.path),
                code="undeclared-placeholder",
                severity="high",
                message=f"placeholder '{name}' is used but not declared in variables",
            )
        )

    for name in sorted(declared - used):
        issues.append(
            Issue(
                path=str(prompt.path),
                code="unused-variable",
                severity="low",
                message=f"variable '{name}' is declared but never used",
            )
        )
    return issues


def _risk_issues(prompt: PromptFile) -> list[Issue]:
    issues: list[Issue] = []
    for code, pattern in RISK_PATTERNS.items():
        if pattern.search(prompt.body):
            issues.append(
                Issue(
                    path=str(prompt.path),
                    code=code,
                    severity="high",
                    message="body contains wording commonly used in unsafe prompt instructions",
                )
            )
    if "refuse" not in prompt.body.casefold() and "policy" not in prompt.body.casefold():
        issues.append(
            Issue(
                path=str(prompt.path),
                code="missing-guardrail-language",
                severity="low",
                message="prompt has no obvious refusal or policy handling language",
            )
        )
    return issues


def _prompt_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.exists():
        raise ValueError(f"path does not exist: {path}")
    return sorted(
        file_path
        for file_path in path.rglob("*")
        if file_path.suffix.lower() in {".md", ".txt", ".prompt"}
    )

