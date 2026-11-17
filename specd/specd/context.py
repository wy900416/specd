"""Context packing for agents.

A large spec graph does not fit in a context window. This module resolves a
bounded, prioritized slice around a target spec, always injects pinned
constraints, and emits a manifest describing what was included, omitted and
why. The manifest is the audit trail for agent behaviour.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .model import Spec, now_iso, relpath, iter_proposals, load_spec, iter_specs


@dataclass
class Entry:
    spec: Spec
    reason: str
    priority: int
    required: bool = False
    depth: int = 0
    truncated: bool = False
    body: str = ""


@dataclass
class ContextPack:
    target: Spec
    task: str
    entries: list[Entry] = field(default_factory=list)
    excluded: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    budget: int = 12000
    used: int = 0

    def manifest(self) -> dict[str, Any]:
        return {
            "target": self.target.id,
            "target_version": self.target.version,
            "target_status": self.target.status,
            "task": self.task,
            "generated_at": now_iso(),
            "budget_chars": self.budget,
            "used_chars": self.used,
            "included": [
                {
                    "id": entry.spec.id,
                    "version": entry.spec.version,
                    "status": entry.spec.status,
                    "kind": entry.spec.kind,
                    "reason": entry.reason,
                    "priority": entry.priority,
                    "required": entry.required,
                    "chars": len(entry.body),
                    "truncated": entry.truncated,
                }
                for entry in self.entries
            ],
            "excluded": self.excluded,
            "warnings": self.warnings,
        }


def _load_specs(root: Path) -> dict[str, Spec]:
    specs: dict[str, Spec] = {}
    for path in iter_specs(root):
        spec = load_spec(path)
        if spec.id not in specs:
            specs[spec.id] = spec
    return specs


def _collect(pack: ContextPack, specs: dict[str, Spec], depth: int) -> None:
    seen: dict[str, Entry] = {}

    def add(spec_id: str, reason: str, priority: int, required: bool = False, depth_value: int = 0) -> None:
        if spec_id not in specs:
            return
        spec = specs[spec_id]
        if spec.status == "deprecated" and spec_id != pack.target.id:
            pack.excluded.append({"id": spec_id, "reason": f"deprecated (linked by {reason})"})
            return
        existing = seen.get(spec_id)
        if existing:
            if priority < existing.priority:
                existing.reason = reason
                existing.priority = priority
                existing.required = existing.required or required
            return
        seen[spec_id] = Entry(
            spec=spec,
            reason=reason,
            priority=priority,
            required=required,
            depth=depth_value,
            body=spec.body,
        )

    # Pinned constraints are always included when they apply to the target kind.
    for spec in specs.values():
        if not spec.pinned:
            continue
        if spec.applies_to and pack.target.kind not in spec.applies_to:
            continue
        add(spec.id, "pinned constraint", 0, required=True)

    add(pack.target.id, "target", 1, required=True)

    target = pack.target
    for link in target.links:
        rel, target_id = link["rel"], link["target"]
        if rel in ("exposes", "publishes", "consumes"):
            add(target_id, f"contract boundary ({rel})", 2)
        elif rel == "constrained-by":
            add(target_id, "constraint", 2)
        elif rel in ("implements", "part-of"):
            add(target_id, f"{rel}", 3)
        elif rel == "depends-on":
            add(target_id, f"direct dependency", 4, depth_value=1)
        elif rel == "decided-by":
            add(target_id, "decision record", 5)
        elif rel in ("relates-to", "documents", "supersedes", "superseded-by"):
            add(target_id, f"related ({rel})", 6)

    # Transitive dependencies.
    queue: list[tuple[str, int]] = [(target.id, 0)]
    visited: set[str] = {target.id}
    while queue:
        current_id, current_depth = queue.pop(0)
        if current_depth >= depth:
            continue
        current = specs.get(current_id)
        if not current:
            continue
        for dep in current.link_targets("depends-on"):
            if dep in visited:
                continue
            visited.add(dep)
            add(dep, f"dependency of {current_id} (depth {current_depth + 1})", 4 + current_depth, depth_value=current_depth + 1)
            queue.append((dep, current_depth + 1))

    # Incoming references: consumers of a contract, consumers of a service, flows.
    for spec in specs.values():
        if spec.id == target.id:
            continue
        for link in spec.links:
            if link["target"] != target.id:
                continue
            if target.kind == "contract" and link["rel"] in ("exposes", "publishes", "consumes"):
                add(spec.id, f"contract participant ({link['rel']})", 3)
            elif link["rel"] == "depends-on":
                add(spec.id, f"consumer of {target.id}", 6)
            elif link["rel"] in ("relates-to", "documents"):
                add(spec.id, f"references {target.id}", 6)

    pack.entries = sorted(seen.values(), key=lambda entry: (entry.priority, entry.spec.id))


def _render_markdown(pack: ContextPack) -> str:
    lines: list[str] = []
    lines.append(f"# Context pack: {pack.target.id}")
    lines.append("")
    lines.append(f"- target: `{pack.target.id}` v{pack.target.version} ({pack.target.status})")
    lines.append(f"- task: {pack.task or '(not specified)'}")
    lines.append(f"- budget: {pack.budget} chars, used: {pack.used}")
    lines.append("- generated by `specd context`; the manifest at the bottom is authoritative.")
    lines.append("")
    lines.append("> Treat this pack as bounded. Do not assume an omitted spec is irrelevant;")
    lines.append("> query again with a narrower target if you need more. Pinned constraints are mandatory.")
    lines.append("")

    for entry in pack.entries:
        spec = entry.spec
        lines.append(f"## [{spec.id}] {spec.title}")
        lines.append("")
        lines.append(
            f"- kind: `{spec.kind}` | version: `{spec.version}` | status: `{spec.status}` | owner: `{spec.owner}`"
        )
        lines.append(f"- included because: {entry.reason}")
        if spec.status != "approved":
            lines.append("- **PENDING**: this spec is not approved; treat it as a proposal, not truth.")
        if entry.truncated:
            lines.append(f"- **TRUNCATED**: full text at `{spec.path}`")
        lines.append("")
        lines.append(entry.body.strip())
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Context manifest")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(pack.manifest(), indent=2, ensure_ascii=False))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def build_context(
    root: Path,
    target_id: str,
    task: str = "",
    depth: int = 2,
    budget: int = 12000,
    fmt: str = "md",
) -> ContextPack:
    root = Path(root).resolve()
    specs = _load_specs(root)
    if target_id not in specs:
        raise KeyError(f"unknown spec: {target_id}")

    pack = ContextPack(target=specs[target_id], task=task, budget=budget)
    _collect(pack, specs, depth)

    # Open proposals against the target.
    for path in iter_proposals(root):
        try:
            proposal = load_spec(path)
        except Exception:
            continue
        if str(proposal.meta.get("target", "")) == target_id:
            pack.warnings.append(
                f"open proposal {proposal.id} ({proposal.meta.get('bump')}) exists for {target_id}"
            )

    # Budget: required entries are never truncated; others are cut lowest priority first.
    remaining = budget
    for entry in pack.entries:
        body = entry.body.strip()
        if entry.required:
            entry.body = body
            remaining -= len(body)
            continue
        if remaining <= 0:
            entry.body = f"… [omitted by budget; full text: {entry.spec.path}]"
            entry.truncated = True
            continue
        if len(body) > remaining:
            cut = body[:remaining]
            cut = cut[: cut.rfind("\n")] if "\n" in cut else cut
            entry.body = f"{cut}\n\n… [truncated by budget; full text: {entry.spec.path}]"
            entry.truncated = True
            remaining = 0
        else:
            entry.body = body
            remaining -= len(body)

    pack.used = sum(len(entry.body) for entry in pack.entries)
    if pack.used > budget:
        pack.warnings.append(
            f"pinned/required content alone exceeds budget ({pack.used} > {budget}); increase --budget"
        )

    if fmt == "json":
        return pack
    return pack


def context_text(pack: ContextPack, fmt: str = "md") -> str:
    if fmt == "json":
        return json.dumps(
            {
                "manifest": pack.manifest(),
                "entries": [
                    {
                        "id": entry.spec.id,
                        "reason": entry.reason,
                        "body": entry.body,
                        "truncated": entry.truncated,
                    }
                    for entry in pack.entries
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    return _render_markdown(pack)


def compute_impact(root: Path, spec_id: str) -> list[dict[str, Any]]:
    root = Path(root).resolve()
    specs = _load_specs(root)
    if spec_id not in specs:
        raise KeyError(f"unknown spec: {spec_id}")

    reverse: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for spec in specs.values():
        for link in spec.links:
            reverse[link["target"]].append((spec.id, link["rel"]))

    results: list[dict[str, Any]] = []
    seen = {spec_id}
    queue: list[tuple[str, int]] = [(spec_id, 0)]
    while queue:
        current, current_depth = queue.pop(0)
        for source, rel in reverse.get(current, []):
            if source in seen:
                continue
            seen.add(source)
            spec = specs[source]
            results.append(
                {
                    "id": source,
                    "title": spec.title,
                    "kind": spec.kind,
                    "status": spec.status,
                    "version": spec.version,
                    "rel": rel,
                    "via": current,
                    "depth": current_depth + 1,
                    "path": relpath(spec.path, root),
                }
            )
            queue.append((source, current_depth + 1))

    results.sort(key=lambda item: (item["depth"], item["id"]))
    return results
