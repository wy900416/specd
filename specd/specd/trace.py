"""Requirement-to-artifact tracing.

Scans source, test and config files for `REQ-...` markers and combines them
with the `Traces:` declarations in specs. The result is the raw material for
the verification loop: which requirements are actually referenced, and which
ones exist only on paper.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from .model import SpecError, iter_specs, load_spec, relpath

REQ_ID = re.compile(r"\bREQ-[A-Z][A-Z0-9]*-\d{3,}\b")
EXTENSIONS = {
    ".py",
    ".pyi",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".kts",
    ".rb",
    ".cs",
    ".php",
    ".swift",
    ".scala",
    ".sql",
    ".feature",
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
}
SKIP_DIRS = {".git", "__pycache__", "node_modules", "dist", ".venv", ".specd"}


def _iter_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        path = Path(path)
        if path.is_file():
            if path.suffix in EXTENSIONS:
                yield path
            continue
        if not path.exists():
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file():
                continue
            if candidate.suffix not in EXTENSIONS:
                continue
            if any(part in SKIP_DIRS for part in candidate.parts):
                continue
            yield candidate


def trace(root: Path, paths: Iterable[str | Path]) -> dict[str, Any]:
    root = Path(root).resolve()
    specs: dict[str, Any] = {}
    for path in iter_specs(root):
        try:
            spec = load_spec(path)
        except SpecError:
            continue
        specs[spec.id] = spec

    references: dict[str, set[str]] = {}
    files: dict[str, set[str]] = {}
    unknown: dict[str, set[str]] = {}

    all_req_ids: set[str] = set()
    declared: dict[str, set[str]] = {}
    for spec in specs.values():
        for requirement in spec.requirements:
            all_req_ids.add(requirement.id)
            if requirement.traces:
                declared.setdefault(requirement.id, set()).update(requirement.traces)

    for path in _iter_files(Path(p) if Path(p).is_absolute() else root / p for p in paths):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rel = relpath(path, root)
        for match in REQ_ID.finditer(text):
            req_id = match.group(0)
            references.setdefault(req_id, set()).add(rel)
            files.setdefault(rel, set()).add(req_id)
            if req_id not in all_req_ids:
                unknown.setdefault(req_id, set()).add(rel)

    for req_id, declared_paths in declared.items():
        for declared_path in declared_paths:
            references.setdefault(req_id, set()).add(declared_path)
            files.setdefault(declared_path, set()).add(req_id)

    covered = sorted(req_id for req_id in all_req_ids if references.get(req_id))
    uncovered = sorted(req_id for req_id in all_req_ids if not references.get(req_id))

    result = {
        "requirements": len(all_req_ids),
        "covered": len(covered),
        "uncovered": len(uncovered),
        "coverage": round(len(covered) / len(all_req_ids), 3) if all_req_ids else 0.0,
        "references": {req_id: sorted(paths_set) for req_id, paths_set in sorted(references.items())},
        "uncovered_ids": uncovered,
        "unknown_ids": {req_id: sorted(paths_set) for req_id, paths_set in sorted(unknown.items())},
        "files": {rel: sorted(req_ids) for rel, req_ids in sorted(files.items())},
    }

    directory = root / ".specd"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "trace.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result
