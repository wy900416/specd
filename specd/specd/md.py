"""A deliberately small Markdown renderer.

The project does not depend on a Markdown package. Specs use a narrow subset:
headings, paragraphs, lists, fenced code, tables, blockquotes, links, emphasis
and checkboxes. That is enough for the viewer, and it keeps the tool portable.
"""

from __future__ import annotations

import html
import re

_SAFE_URL = re.compile(r"^(?:https?:|mailto:|#|/|\.{0,2}/|[A-Za-z0-9_./-]+$)")
_CODE_TOKEN = "\x00CODE{}\x00"


def inline(text: str) -> str:
    """Render inline Markdown. Input is escaped before formatting."""
    text = html.escape(text, quote=False)

    codes: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        codes.append(f"<code>{match.group(1)}</code>")
        return _CODE_TOKEN.format(len(codes) - 1)

    text = re.sub(r"`([^`]+)`", stash_code, text)

    def image(match: re.Match[str]) -> str:
        alt, url = match.group(1), match.group(2)
        if not _SAFE_URL.match(url):
            return alt
        return f'<img src="{url}" alt="{alt}" loading="lazy">'

    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", image, text)

    def link(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2)
        if not _SAFE_URL.match(url):
            return label
        return f'<a href="{url}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)

    for index, code in enumerate(codes):
        text = text.replace(_CODE_TOKEN.format(index), code)
    return text


def slugify(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", text).strip("-") or "section"


def _split_row(row: str) -> list[str]:
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def _is_table_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line


def _table(lines: list[str], start: int) -> tuple[str, int]:
    header = _split_row(lines[start])
    separators = _split_row(lines[start + 1])
    aligns: list[str] = []
    for cell in separators:
        left = cell.startswith(":")
        right = cell.endswith(":")
        aligns.append("center" if left and right else "right" if right else "left")

    rows: list[list[str]] = []
    index = start + 2
    while index < len(lines) and lines[index].strip() and "|" in lines[index]:
        rows.append(_split_row(lines[index]))
        index += 1

    parts = ["<div class=\"table-wrap\"><table><thead><tr>"]
    for cell_index, cell in enumerate(header):
        align = aligns[cell_index] if cell_index < len(aligns) else "left"
        parts.append(f'<th style="text-align:{align}">{inline(cell)}</th>')
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        for cell_index in range(len(header)):
            cell = row[cell_index] if cell_index < len(row) else ""
            align = aligns[cell_index] if cell_index < len(aligns) else "left"
            parts.append(f'<td style="text-align:{align}">{inline(cell)}</td>')
        parts.append("</tr>")
    parts.append("</tbody></table></div>")
    return "".join(parts), index


def _list(lines: list[str], start: int) -> tuple[str, int]:
    first = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", lines[start])
    assert first is not None
    ordered = first.group(2).endswith(".")
    items: list[list[str]] = []
    index = start
    while index < len(lines):
        match = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", lines[index])
        if match and (match.group(2).endswith(".") == ordered):
            items.append([match.group(3)])
            index += 1
            continue
        if match:
            break
        if not lines[index].strip():
            break
        if items and (lines[index].startswith(" ") or lines[index].startswith("\t")):
            items[-1].append(lines[index].strip())
            index += 1
            continue
        break

    has_tasks = any(re.match(r"^\[[ xX]\]\s+", item[0]) for item in items)
    tag = "ol" if ordered else "ul"
    css = " class=\"task-list\"" if has_tasks else ""
    parts = [f"<{tag}{css}>"]
    for item in items:
        text = " ".join(item)
        checkbox = ""
        match = re.match(r"^\[([ xX])\]\s+(.*)$", text)
        if match:
            checked = " checked" if match.group(1).lower() == "x" else ""
            checkbox = f'<input type="checkbox" disabled{checked}> '
            text = match.group(2)
        parts.append(f"<li>{checkbox}{inline(text)}</li>")
    parts.append(f"</{tag}>")
    return "".join(parts), index


def _paragraph(lines: list[str], start: int) -> tuple[str, int]:
    parts: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            break
        if re.match(r"^(#{1,6})\s+", line):
            break
        if re.match(r"^```", line):
            break
        if re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            break
        if line.lstrip().startswith(">"):
            break
        if re.match(r"^\s*(?:---+|\*\*\*+|___+)\s*$", line):
            break
        if "|" in line and index + 1 < len(lines) and _is_table_separator(lines[index + 1]):
            break
        parts.append(line.strip())
        index += 1
    return f"<p>{inline(' '.join(parts))}</p>", index


def render(markdown: str) -> str:
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    output: list[str] = []
    index = 0
    total = len(lines)

    while index < total:
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        fence = re.match(r"^```(\w*)\s*$", line)
        if fence:
            language = fence.group(1)
            index += 1
            code: list[str] = []
            while index < total and not re.match(r"^```\s*$", lines[index]):
                code.append(lines[index])
                index += 1
            index += 1
            css = f' class="language-{language}"' if language else ""
            output.append(f"<pre><code{css}>{html.escape(chr(10).join(code))}</code></pre>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            output.append(f'<h{level} id="{slugify(text)}">{inline(text)}</h{level}>')
            index += 1
            continue

        if re.match(r"^\s*(?:---+|\*\*\*+|___+)\s*$", line):
            output.append("<hr>")
            index += 1
            continue

        if "|" in line and index + 1 < total and _is_table_separator(lines[index + 1]):
            table, index = _table(lines, index)
            output.append(table)
            continue

        if line.lstrip().startswith(">"):
            quoted: list[str] = []
            while index < total and lines[index].lstrip().startswith(">"):
                quoted.append(re.sub(r"^\s*>\s?", "", lines[index]))
                index += 1
            output.append(f"<blockquote>{render(chr(10).join(quoted))}</blockquote>")
            continue

        if re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            rendered, index = _list(lines, index)
            output.append(rendered)
            continue

        paragraph, index = _paragraph(lines, index)
        output.append(paragraph)

    return "\n".join(output)
