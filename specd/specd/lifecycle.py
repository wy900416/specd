"""Proposal / diff / release lifecycle.

Published specs are read-only for agents. An agent edits a copy in `changes/`;
a human (or a release job) merges it, bumps the version and archives the
proposal. The version number is a release decision, never an edit side effect.
"""

from __future__ import annotations

import difflib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .events import append_event
from .model import (
    BUMPS,
    Spec,
    bump_version,
    iter_proposals,
    load_spec,
    now_iso,
    relpath,
    write_spec,
)

TEMPLATE_DIR = "templates"
ARCHIVE_DIR = "changes/archive"


def _load_specs(root: Path) -> dict[str, Spec]:
    specs: dict[str, Spec] = {}
    for path in (root / "specs").rglob("*.md"):
        if "changes" in path.parts:
            continue
        spec = load_spec(path)
        if spec.id not in specs:
            specs[spec.id] = spec
    return specs


def _proposal_id(target_id: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"CHG-{stamp}-{target_id}"


def propose(
    root: Path,
    target_id: str,
    bump: str,
    summary: str,
    author: str = "agent",
    title: str | None = None,
) -> tuple[Path, Spec]:
    root = Path(root).resolve()
    if bump not in BUMPS:
        raise ValueError(f"bump must be one of {BUMPS}")
    specs = _load_specs(root)
    if target_id not in specs:
        raise KeyError(f"unknown spec: {target_id}")
    target = specs[target_id]
    if target.status != "approved":
        raise ValueError(f"{target_id} is {target.status}; only approved specs get change proposals")

    proposal_id = _proposal_id(target_id)
    path = root / "changes" / f"{proposal_id}.md"
    counter = 2
    while path.exists():
        proposal_id = _proposal_id(target_id) + f"-{counter}"
        path = root / "changes" / f"{proposal_id}.md"
        counter += 1

    meta: dict[str, Any] = {
        "id": proposal_id,
        "kind": "change",
        "title": title or f"Change to {target.title}",
        "target": target_id,
        "base_version": target.version,
        "bump": bump,
        "status": "proposed",
        "author": author,
        "created": now_iso(),
        "summary": summary,
        "spec": {},
    }
    write_spec(path, meta, target.body)
    append_event(root, "propose", spec=target_id, proposal=proposal_id, bump=bump, author=author)
    return path, load_spec(path)


def diff_proposal(root: Path, proposal_path: Path) -> str:
    root = Path(root).resolve()
    proposal = load_spec(Path(proposal_path))
    target_id = str(proposal.meta.get("target", ""))
    specs = _load_specs(root)
    if target_id not in specs:
        raise KeyError(f"proposal target not found: {target_id}")
    target = specs[target_id]

    lines: list[str] = []
    overrides = proposal.meta.get("spec") or {}
    if isinstance(overrides, dict) and overrides:
        lines.append("Front-matter overrides:")
        for key in sorted(overrides):
            old = target.meta.get(key)
            new = overrides[key]
            if old != new:
                lines.append(f"  {key}: {json.dumps(old, ensure_ascii=False)} -> {json.dumps(new, ensure_ascii=False)}")
        lines.append("")

    diff = difflib.unified_diff(
        target.body.splitlines(),
        proposal.body.splitlines(),
        fromfile=f"{target.id}@{target.version} (published)",
        tofile=f"{proposal.id} (proposed, bump={proposal.meta.get('bump')})",
        lineterm="",
    )
    body = "\n".join(diff)
    if not body and not lines:
        return "No changes: proposal body and front-matter are identical to the target."
    if body:
        lines.append(body)
    return "\n".join(lines)


def release(root: Path, proposal_path: Path, approved_by: str) -> dict[str, Any]:
    root = Path(root).resolve()
    proposal_path = Path(proposal_path)
    proposal = load_spec(proposal_path)
    if proposal.kind != "change":
        raise ValueError("not a change proposal")
    target_id = str(proposal.meta.get("target", ""))
    specs = _load_specs(root)
    if target_id not in specs:
        raise KeyError(f"proposal target not found: {target_id}")
    target = specs[target_id]

    base_version = str(proposal.meta.get("base_version", ""))
    if base_version != target.version:
        raise ValueError(
            f"stale proposal: base_version {base_version} != current {target.version}; rebase the proposal"
        )
    bump = str(proposal.meta.get("bump", ""))
    if bump not in BUMPS:
        raise ValueError(f"invalid bump: {bump}")

    new_version = bump_version(target.version, bump)
    overrides = proposal.meta.get("spec") or {}
    if overrides and not isinstance(overrides, dict):
        raise ValueError("proposal 'spec' must be a mapping")

    merged = dict(target.meta)
    for key, value in overrides.items():
        merged[key] = value
    merged["id"] = target.id
    merged["kind"] = target.kind
    merged["version"] = new_version
    merged["status"] = "approved"
    merged["approved_by"] = approved_by
    merged["approved_at"] = now_iso()
    merged["updated"] = now_iso()[:10]

    write_spec(target.path, merged, proposal.body)

    archive = root / ARCHIVE_DIR
    archive.mkdir(parents=True, exist_ok=True)
    archived_meta = dict(proposal.meta)
    archived_meta["status"] = "released"
    archived_meta["released_as"] = new_version
    archived_meta["released_by"] = approved_by
    archived_meta["released_at"] = now_iso()
    write_spec(archive / proposal_path.name, archived_meta, proposal.body)
    proposal_path.unlink()

    append_event(
        root,
        "release",
        spec=target.id,
        version=new_version,
        proposal=proposal.id,
        by=approved_by,
    )
    return {
        "spec": target.id,
        "version": new_version,
        "proposal": proposal.id,
        "path": relpath(target.path, root),
    }


def list_proposals(root: Path) -> list[dict[str, Any]]:
    root = Path(root).resolve()
    result = []
    for path in iter_proposals(root):
        proposal = load_spec(path)
        result.append(
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
    return result


def _render_template(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def new_spec(
    root: Path,
    kind: str,
    spec_id: str,
    title: str,
    owner: str,
    summary: str = "",
    template: str | None = None,
    extra: dict[str, str] | None = None,
) -> Path:
    root = Path(root).resolve()
    template_path = root / TEMPLATE_DIR / f"{template or kind}.md"
    if not template_path.exists():
        raise FileNotFoundError(f"template not found: {template_path}")
    path = root / "specs" / kind / f"{spec_id}.md"
    if path.exists():
        raise FileExistsError(f"spec already exists: {path}")

    values = {
        "id": spec_id,
        "kind": kind,
        "title": title,
        "summary": summary or title,
        "owner": owner,
        "date": now_iso()[:10],
        "version": "0.1.0",
        "level": {"system": "L0", "domain": "L1", "service": "L2"}.get(kind, ""),
        "domain": "",
        "type": "openapi",
        "contract_path": "",
    }
    values.update(extra or {})
    text = _render_template(template_path.read_text(encoding="utf-8"), values)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    append_event(root, "new", spec=spec_id, kind=kind, owner=owner)
    return path
