"""Build a derived graph index from the specs on disk.

The index is not a source of truth. It is a cache for search, graph queries,
the viewer and drift checks. Delete it at any time and rebuild.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .model import SpecError, iter_proposals, iter_specs, load_spec, now_iso, relpath


def build_index(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    specs: dict[str, Any] = {}
    duplicates: list[str] = []
    errors: list[str] = []

    for path in iter_specs(root):
        try:
            spec = load_spec(path)
        except SpecError as exc:
            errors.append(str(exc))
            continue
        if spec.id in specs:
            duplicates.append(spec.id)
            continue
        specs[spec.id] = spec

    edges: list[dict[str, str]] = []
    incoming: dict[str, list[dict[str, str]]] = {spec_id: [] for spec_id in specs}
    broken: list[dict[str, str]] = []

    for spec in specs.values():
        for link in spec.links:
            target = link["target"]
            edge = {"from": spec.id, "rel": link["rel"], "to": target}
            if target.startswith(("http://", "https://")):
                continue
            edges.append(edge)
            if target in incoming:
                incoming[target].append({"from": spec.id, "rel": link["rel"]})
            else:
                broken.append(edge)

    summaries = {spec_id: spec.to_summary(root) for spec_id, spec in specs.items()}
    kind_counts = Counter(summary["kind"] for summary in summaries.values())
    status_counts = Counter(summary["status"] for summary in summaries.values())
    requirement_count = sum(summary["requirement_count"] for summary in summaries.values())
    open_questions = sum(summary["open_questions"] for summary in summaries.values())

    proposals = []
    for path in iter_proposals(root):
        try:
            proposal = load_spec(path)
        except SpecError:
            continue
        proposals.append(
            {
                "id": proposal.id,
                "title": proposal.title,
                "target": str(proposal.meta.get("target", "")),
                "base_version": str(proposal.meta.get("base_version", "")),
                "bump": str(proposal.meta.get("bump", "")),
                "status": proposal.status,
                "author": str(proposal.meta.get("author", "")),
                "summary": str(proposal.meta.get("summary", "")),
                "path": relpath(path, root),
            }
        )

    index: dict[str, Any] = {
        "generated_at": now_iso(),
        "root": str(root),
        "specs": summaries,
        "edges": edges,
        "incoming": incoming,
        "broken_links": broken,
        "duplicates": duplicates,
        "errors": errors,
        "proposals": proposals,
        "stats": {
            "specs": len(summaries),
            "requirements": requirement_count,
            "open_questions": open_questions,
            "proposals": len(proposals),
            "by_kind": dict(sorted(kind_counts.items())),
            "by_status": dict(sorted(status_counts.items())),
            "orphans": [
                spec_id
                for spec_id, summary in summaries.items()
                if not incoming.get(spec_id) and summary["kind"] not in ("system", "standard")
            ],
            "broken_links": len(broken),
        },
    }

    (root / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return index


def load_index(root: Path) -> dict[str, Any] | None:
    path = Path(root) / "index.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
