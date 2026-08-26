#!/usr/bin/env python3
"""Build an offline, single-file WeChat article formatting preview."""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
import tempfile
from pathlib import Path

from validate_theme import validate_css_compatibility, validate_theme

SKILL_DIR = Path(__file__).resolve().parent.parent
THEMES_DIR = SKILL_DIR / "assets" / "style-library"
LEARNED_THEMES_DIR = SKILL_DIR / "assets" / "learned-style-library"
TEMPLATE = SKILL_DIR / "assets" / "preview-template.html"
COMPONENTS = SKILL_DIR / "assets" / "component-library.json"
REQUIRED_MODULES = {"h1", "h2", "h3", "quote", "code", "inline-code", "strong", "em", "ordered-list", "unordered-list", "table", "divider", "link"}
THEME_SAMPLE_IMAGE = (SKILL_DIR / "assets" / "sample-image.svg").resolve()


def strip_frontmatter(text: str) -> str:
    return re.sub(r"^---\s*\n.*?\n---\s*\n?", "", text, count=1, flags=re.S)


def embed_image(url: str, base_dir: Path, warnings: list[str]) -> str:
    if re.match(r"^(https?:|data:)", url, flags=re.I):
        return url
    candidate = Path(url).expanduser()
    if not candidate.is_absolute():
        candidate = (base_dir / candidate).resolve()
    if not candidate.is_file():
        warnings.append(f"missing image: {url}")
        return url
    mime = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(candidate.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def sample_image_attribute(url: str, base_dir: Path) -> str:
    if re.match(r"^(https?:|data:)", url, flags=re.I):
        return ""
    candidate = Path(url).expanduser()
    if not candidate.is_absolute():
        candidate = (base_dir / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return ' data-theme-sample="true"' if candidate == THEME_SAMPLE_IMAGE else ""


def inline_markup(text: str, base_dir: Path, warnings: list[str]) -> str:
    placeholders: dict[str, str] = {}

    def hold(fragment: str) -> str:
        key = f"ZXPH{len(placeholders)}TOKEN"
        placeholders[key] = fragment
        return key

    def wiki_image(match: re.Match[str]) -> str:
        raw = match.group(1).split("|", 1)[0].strip()
        src = html.escape(embed_image(raw, base_dir, warnings), quote=True)
        sample_attr = sample_image_attribute(raw, base_dir)
        return hold(f'<img src="{src}" alt="{html.escape(Path(raw).name)}"{sample_attr}>')

    def md_image(match: re.Match[str]) -> str:
        alt, raw = match.group(1), match.group(2).strip()
        src = html.escape(embed_image(raw, base_dir, warnings), quote=True)
        sample_attr = sample_image_attribute(raw, base_dir)
        return hold(f'<img src="{src}" alt="{html.escape(alt, quote=True)}"{sample_attr}>')

    def md_link(match: re.Match[str]) -> str:
        label, href = match.group(1), match.group(2)
        safe_href = html.escape(href, quote=True)
        return hold(f'<a href="{safe_href}">{html.escape(label)}</a>')

    text = re.sub(r"!\[\[([^\]]+)\]\]", wiki_image, text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", md_image, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", md_link, text)
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", lambda m: hold(f"<code>{html.escape(html.unescape(m.group(1)))}</code>"), text)
    text = re.sub(r"\*\*(.+?)\*\*|__(.+?)__", lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)|(?<!_)_([^_\n]+)_(?!_)", lambda m: f"<em>{m.group(1) or m.group(2)}</em>", text)
    for key, fragment in placeholders.items():
        text = text.replace(key, fragment)
    return text


def is_table_separator(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return len(cells) > 0 and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def unsupported_syntax_warnings(lines: list[str]) -> list[str]:
    """Report constructs the intentionally small Markdown parser would flatten."""
    warnings: list[str] = []
    for number, line in enumerate(lines, start=1):
        if re.match(r"^\s{2,}(?:[-+*]|\d+\.)\s+", line):
            warnings.append(f"line {number}: nested list is flattened")
        if re.search(r"\[\^[^\]]+\]", line):
            warnings.append(f"line {number}: footnote syntax is not supported")
        if re.match(r"^\s*</?[A-Za-z][^>]*>\s*$", line):
            warnings.append(f"line {number}: raw HTML is escaped as text")
    return warnings


def markdown_to_html(markdown: str, base_dir: Path) -> tuple[str, list[str]]:
    lines = strip_frontmatter(markdown).replace("\r\n", "\n").split("\n")
    output: list[str] = []
    warnings = unsupported_syntax_warnings(lines)
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        fence = re.match(r"^```\s*([\w+-]*)\s*$", line)
        if fence:
            language = fence.group(1)
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not re.match(r"^```\s*$", lines[i]):
                code_lines.append(lines[i])
                i += 1
            if i == len(lines):
                warnings.append("unclosed code fence")
            else:
                i += 1
            lang_attr = f' data-language="{html.escape(language)}"' if language else ""
            output.append(f'<section class="code-section"{lang_attr}><pre><code>{html.escape(chr(10).join(code_lines))}</code></pre></section>')
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markup(heading.group(2), base_dir, warnings)}</h{level}>")
            i += 1
            continue
        if re.fullmatch(r"\s*(?:---+|\*\*\*+|___+)\s*", line):
            output.append("<hr>")
            i += 1
            continue
        if i + 1 < len(lines) and "|" in line and is_table_separator(lines[i + 1]):
            table_line = i + 1
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            column_count = max([len(headers), *(len(row) for row in rows)])
            counts = {len(headers), *(len(row) for row in rows)}
            if len(counts) > 1:
                warnings.append(f"line {table_line}: table rows have inconsistent column counts; padded to {column_count} columns")
            headers += [""] * (column_count - len(headers))
            rows = [row + [""] * (column_count - len(row)) for row in rows]
            head = "".join(f"<th>{inline_markup(c, base_dir, warnings)}</th>" for c in headers)
            body = "".join("<tr>" + "".join(f"<td>{inline_markup(c, base_dir, warnings)}</td>" for c in row) + "</tr>" for row in rows)
            output.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
            continue
        if line.lstrip().startswith(">"):
            quote: list[str] = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            output.append(f"<blockquote><p>{inline_markup(' '.join(quote), base_dir, warnings)}</p></blockquote>")
            continue
        list_match = re.match(r"^\s*(?:([-+*])|(\d+)\.)\s+(.+)$", line)
        if list_match:
            ordered = bool(list_match.group(2))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while i < len(lines):
                match = re.match(r"^\s*(?:([-+*])|(\d+)\.)\s+(.+)$", lines[i])
                if not match or bool(match.group(2)) != ordered:
                    break
                items.append(f"<li>{inline_markup(match.group(3), base_dir, warnings)}</li>")
                i += 1
            output.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        paragraph = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip():
            nxt = lines[i]
            if re.match(r"^(#{1,6})\s+|^```|^\s*>|^\s*(?:[-+*]|\d+\.)\s+", nxt):
                break
            if re.fullmatch(r"\s*(?:---+|\*\*\*+|___+)\s*", nxt):
                break
            if i + 1 < len(lines) and "|" in nxt and is_table_separator(lines[i + 1]):
                break
            paragraph.append(nxt.strip())
            i += 1
        output.append(f"<p>{inline_markup('<br>'.join(paragraph), base_dir, warnings).replace('&lt;br&gt;', '<br>')}</p>")
    return "\n".join(output), warnings


def load_themes() -> list[dict]:
    themes: list[dict] = []
    ids: set[str] = set()
    paths = sorted(THEMES_DIR.glob("*.json"))
    if LEARNED_THEMES_DIR.is_dir():
        paths += sorted(LEARNED_THEMES_DIR.glob("*.json"))
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_theme(data, path, learned=path.parent == LEARNED_THEMES_DIR)
        if errors:
            raise ValueError(f"invalid theme {path.name}: {'; '.join(errors)}")
        if data["id"] in ids:
            raise ValueError(f"duplicate theme id: {data['id']}")
        ids.add(data["id"])
        themes.append(data)
    if not themes:
        raise ValueError("style library is empty")
    defaults = [theme["id"] for theme in themes if theme.get("default")]
    if len(defaults) != 1:
        raise ValueError(f"combined style library must contain exactly one default theme; found {len(defaults)}")
    return sorted(themes, key=lambda theme: theme["order"])


def load_components() -> dict:
    data = json.loads(COMPONENTS.read_text(encoding="utf-8"))
    modules = data.get("modules")
    if not isinstance(modules, dict) or set(modules) != REQUIRED_MODULES:
        raise ValueError(f"component library must define exactly: {', '.join(sorted(REQUIRED_MODULES))}")
    for module_id, module in modules.items():
        if not isinstance(module.get("label"), str) or not isinstance(module.get("options"), list):
            raise ValueError(f"invalid component module: {module_id}")
        option_ids: set[str] = set()
        for option in module["options"]:
            option_id, css = option.get("id"), option.get("css")
            if not isinstance(option_id, str) or option_id in option_ids or not isinstance(option.get("label"), str):
                raise ValueError(f"invalid or duplicate option in component module: {module_id}")
            if not isinstance(css, str):
                raise ValueError(f"component CSS must be a string: {module_id}/{option_id}")
            compatibility_errors = validate_css_compatibility(css)
            if compatibility_errors:
                raise ValueError(f"unsafe CSS in component module {module_id}/{option_id}: {'; '.join(compatibility_errors)}")
            if css.count("{") != css.count("}"):
                raise ValueError(f"unbalanced CSS in component module: {module_id}/{option_id}")
            if option_id != "theme" and ".note-to-mp" not in css:
                raise ValueError(f"component CSS must be scoped to .note-to-mp: {module_id}/{option_id}")
            if module_id in {"h1", "h2", "h3"} and option_id != "theme":
                css_without_tokens = re.sub(r"\{\{[^}]+\}\}", "TOKEN", css)
                first_rule = css_without_tokens.split("}", 1)[0].split("{", 1)
                declarations = first_rule[1] if len(first_rule) == 2 else ""
                if not re.search(r"(?:^|;)\s*color\s*:", declarations):
                    raise ValueError(f"heading component must set a readable foreground color: {module_id}/{option_id}")
            unknown_tokens = set(re.findall(r"\{\{([^}]+)\}\}", css)) - {"accent", "soft", "pale", "dark", "shadow"}
            if unknown_tokens:
                raise ValueError(f"unknown color token in component module {module_id}/{option_id}: {sorted(unknown_tokens)}")
            option_ids.add(option_id)
        if not module["options"] or module["options"][0].get("id") != "theme":
            raise ValueError(f"component module must start with theme default: {module_id}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--article", required=True, type=Path)
    parser.add_argument("--theme")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    article = args.article.expanduser().resolve()
    if not article.is_file():
        parser.error(f"article not found: {article}")
    themes = load_themes()
    components = load_components()
    theme_ids = {theme["id"] for theme in themes}
    default_theme = next((theme for theme in themes if theme.get("default")), themes[0])
    selected = args.theme or default_theme["id"]
    if selected not in theme_ids:
        parser.error(f"unknown theme: {selected}; choose from {', '.join(sorted(theme_ids))}")
    content = article.read_text(encoding="utf-8")
    article_html, warnings = markdown_to_html(content, article.parent)
    if not re.sub(r"<[^>]+>", "", article_html).strip():
        parser.error("article is empty after parsing")
    output = args.output.expanduser().resolve() if args.output else Path(tempfile.gettempdir()) / "zhouxing-paiban-wx-preview" / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    template = TEMPLATE.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", strip_frontmatter(content), flags=re.M)
    title = title_match.group(1).strip() if title_match else article.stem
    themes_json = json.dumps(themes, ensure_ascii=False).replace("</", "<\\/")
    components_json = json.dumps(components, ensure_ascii=False).replace("</", "<\\/")
    page = (template.replace("__PAGE_TITLE__", html.escape(title))
            .replace("__ARTICLE_HTML__", article_html)
            .replace("__THEMES_JSON__", themes_json)
            .replace("__COMPONENTS_JSON__", components_json)
            .replace("__INITIAL_THEME__", json.dumps(selected)))
    output.write_text(page, encoding="utf-8")
    summary = {"output": str(output), "themes": len(themes), "components": len(components["modules"]), "selected_theme": selected,
               "article_bytes": len(content.encode("utf-8")), "warnings": warnings}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
