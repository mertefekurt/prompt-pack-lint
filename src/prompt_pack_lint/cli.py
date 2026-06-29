from __future__ import annotations

import argparse
import sys
from pathlib import Path

from prompt_pack_lint import __version__
from prompt_pack_lint.linter import (
    has_failure,
    issues_to_json,
    issues_to_markdown,
    scan_prompt_path,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt-pack-lint",
        description="Lint prompt packs for metadata, placeholder, and instruction risks.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    scan = subparsers.add_parser("scan", help="scan a prompt file or directory")
    scan.add_argument("path", type=Path)
    scan.add_argument("--format", choices=("markdown", "json"), default="markdown")
    scan.add_argument("--fail-on", choices=("low", "medium", "high"), default="high")
    scan.set_defaults(func=_scan)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except (OSError, ValueError) as exc:
        print(f"prompt-pack-lint: error: {exc}", file=sys.stderr)
        return 1


def _scan(args: argparse.Namespace) -> int:
    issues = scan_prompt_path(args.path)
    if args.format == "json":
        print(issues_to_json(issues), end="")
    else:
        print(issues_to_markdown(issues), end="")
    return 2 if has_failure(issues, args.fail_on) else 0
