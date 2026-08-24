#!/usr/bin/env python3
"""Validate a CSS-backed zhouxing-paiban-wx theme JSON file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_SELECTORS = (
    ".note-to-mp", ".note-to-mp h1", ".note-to-mp h2", ".note-to-mp h3",
    ".note-to-mp p", ".note-to-mp blockquote", ".note-to-mp code",
    ".note-to-mp .code-section", ".note-to-mp img",
)
FORBIDDEN_PATTERNS = {
    "@import": r"@import\b",
    "@font-face": r"@font-face\b",
    "javascript URL": r"javascript\s*:",
    "CSS expression": r"expression\s*\(",
    "remote background URL": r"url\s*\(\s*['\"]?https?://",
    "animation": r"(?:^|[;{])\s*animation(?:-[\w-]+)?\s*:",
    "@keyframes": r"@(?:-webkit-)?keyframes\b",
    "CSS counter": r"counter-(?:reset|increment)\s*:",
    "hover selector": r":hover\b",
}
ALLOWED_FONT_FAMILIES = {
    "-apple-system", "blinkmacsystemfont", "pingfang sc", "hiragino sans gb",
    "microsoft yahei", "songti sc", "stsong", "simsun", "kaiti sc", "stkaiti",
    "kaiti", "sf pro display", "arial", "arial black", "georgia", "menlo",
    "monaco", "consolas", "serif", "sans-serif", "monospace", "inherit",
    "system-ui",
}


def validate_css_compatibility(css: str, *, allow_media: bool = False) -> list[str]:
    """Return paste-safety errors for theme or component CSS."""
    errors: list[str] = []
    lowered = css.lower()
    for label, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, lowered, flags=re.M):
            errors.append(f"css uses forbidden feature: {label}")
    if not allow_media and re.search(r"@media\b", lowered):
        errors.append("css uses forbidden feature: media query")
    for declaration in re.findall(r"font-family\s*:\s*([^;}]+)", css, flags=re.I):
        families = [re.sub(r"\s*!important\s*$", "", item, flags=re.I).strip().strip("'\"").lower() for item in declaration.split(",")]
        unsupported = [item for item in families if item and item not in ALLOWED_FONT_FAMILIES]
        if unsupported:
            errors.append(f"css uses unsupported font family: {', '.join(unsupported)}")
    return errors


def validate_theme(data: object, source: Path, *, learned: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"]
    theme_id = data.get("id")
    if not isinstance(theme_id, str) or not ID.fullmatch(theme_id):
        errors.append("id must use lowercase kebab-case")
    if source.stem != theme_id:
        errors.append(f"filename must match id ({theme_id}.json)")
    for key in ("name", "description"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key} must be a non-empty string")
    if not isinstance(data.get("order"), int) or data["order"] < 1:
        errors.append("order must be a positive integer")
    if not isinstance(data.get("default"), bool):
        errors.append("default must be a boolean")
    if not isinstance(data.get("accent"), str) or not HEX.fullmatch(data["accent"]):
        errors.append("accent must be #RRGGBB")
    if not isinstance(data.get("hue_range"), (int, float)) or not 0 <= data["hue_range"] <= 180:
        errors.append("hue_range must be 0-180")
    if data.get("heading_label") is not None and not isinstance(data.get("heading_label"), str):
        errors.append("heading_label must be a string or null")

    css = data.get("css")
    if not isinstance(css, str) or not css.strip():
        errors.append("css must be a non-empty string")
    else:
        allow_media = source.parent.name == "style-library"
        errors.extend(validate_css_compatibility(css, allow_media=allow_media))
        for selector in REQUIRED_SELECTORS:
            if selector not in css:
                errors.append(f"css is missing selector: {selector}")
        if css.count("{") != css.count("}"):
            errors.append("css brace count is unbalanced")

    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence must be an object")
    else:
        confidence = evidence.get("confidence")
        if confidence not in {"high", "medium", "low"}:
            errors.append("evidence.confidence must be high, medium, or low")
        if evidence.get("source_type") not in {"screenshot", "url", "mixed", "original"}:
            errors.append("evidence.source_type must be screenshot, url, mixed, or original")
        evidence_items: dict[str, list[str]] = {}
        for key in ("observed", "inferred", "unobserved"):
            value = evidence.get(key)
            if not isinstance(value, list):
                errors.append(f"evidence.{key} must be a list")
            elif any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"evidence.{key} items must be non-empty strings")
            else:
                evidence_items[key] = value
        if not isinstance(evidence.get("source"), str) or not evidence["source"].strip():
            errors.append("evidence.source must be a non-empty string")
        if evidence_items and not any(evidence_items.values()):
            errors.append("evidence must contain at least one observed, inferred, or unobserved item")
        if confidence == "high" and not evidence_items.get("observed"):
            errors.append("high-confidence evidence requires at least one observed item")

    if learned or source.parent.name == "learned-style-library":
        if data.get("default") is not False:
            errors.append("learned theme must not be the default")
        if not isinstance(data.get("order"), int) or data["order"] < 100:
            errors.append("learned theme order must start at 100")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--learned", action="store_true", help="enforce learned-theme order, default, and compatibility rules")
    parser.add_argument("themes", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False
    defaults = 0
    orders: set[int] = set()
    ids: set[str] = set()
    for path in args.themes:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"FAIL {path}: {exc}", file=sys.stderr)
            failed = True
            continue
        errors = validate_theme(data, path, learned=args.learned)
        if data.get("default") is True:
            defaults += 1
        if isinstance(data.get("order"), int):
            if data["order"] in orders:
                errors.append(f"duplicate order: {data['order']}")
            orders.add(data["order"])
        if isinstance(data.get("id"), str):
            if data["id"] in ids:
                errors.append(f"duplicate id: {data['id']}")
            ids.add(data["id"])
        if errors:
            failed = True
            print(f"FAIL {path}", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"OK {path}: {data['name']}")
    if len(args.themes) > 1 and defaults != 1:
        failed = True
        print(f"FAIL theme library must contain exactly one default theme; found {defaults}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
