"""Heuristic content scan for specs.

Specs are inputs to agents, so they are also an attack surface: prompt
injection, embedded scripts, leaked credentials and internal endpoints. This is
not a security product; it is a cheap gate that makes the risk visible.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .model import iter_proposals, iter_specs, relpath


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str
    line: int
    excerpt: str


PATTERNS: list[tuple[str, str, re.Pattern[str], str]] = [
    (
        "critical",
        "SEC001",
        re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions", re.I),
        "prompt-injection phrase",
    ),
    (
        "critical",
        "SEC002",
        re.compile(r"<(?:script|iframe|object|embed)\b", re.I),
        "embedded active HTML",
    ),
    (
        "high",
        "SEC003",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
        "possible AWS access key",
    ),
    (
        "high",
        "SEC004",
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        "private key material",
    ),
    (
        "high",
        "SEC005",
        re.compile(r"\b(?:password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[^\s'\"`]{6,}", re.I),
        "possible hard-coded credential",
    ),
    (
        "medium",
        "SEC006",
        re.compile(r"javascript:\s*", re.I),
        "javascript: URL",
    ),
    (
        "medium",
        "SEC007",
        re.compile(r"\bcurl\s+[^\n|]+\|\s*(?:ba)?sh\b", re.I),
        "pipe-to-shell command",
    ),
    (
        "medium",
        "SEC008",
        re.compile(r"\b(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|\.internal\b|\.local\b)", re.I),
        "internal endpoint or private address",
    ),
    (
        "low",
        "SEC009",
        re.compile(r"\b(?:you are now|act as|system prompt|developer message)\b", re.I),
        "role-manipulation phrase",
    ),
    (
        "low",
        "SEC010",
        re.compile(r"\b(?:TODO|TBD|FIXME)\b"),
        "unresolved placeholder",
    ),
]


def scan_text(text: str, path: str = "") -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for severity, code, pattern, message in PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding(
                        severity=severity,
                        code=code,
                        message=message,
                        path=path,
                        line=line_number,
                        excerpt=line.strip()[:160],
                    )
                )
    return findings


def scan(root: Path) -> list[Finding]:
    root = Path(root).resolve()
    paths = list(iter_specs(root)) + list(iter_proposals(root)) + list((root / "standards").rglob("*.md"))
    findings: list[Finding] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        findings.extend(scan_text(text, relpath(path, root)))
    findings.sort(key=lambda item: ({"critical": 0, "high": 1, "medium": 2, "low": 3}[item.severity], item.path, item.line))
    return findings
