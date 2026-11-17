"""Validation rules for specs and change proposals."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .issues import Issue
from .model import (
    BUMPS,
    KINDS,
    RELS,
    REQ_ID_RE,
    SPEC_ID_RE,
    STATUSES,
    Spec,
    SpecError,
    is_semver,
    iter_proposals,
    iter_specs,
    load_spec,
    relpath,
)

CONTRACT_TYPES = {"openapi", "asyncapi", "schema", "proto", "graphql", "grpc", "other"}
PROPOSAL_ID_RE = re.compile(r"^CHG-[A-Za-z0-9][A-Za-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")
ALLOWED_OVERRIDE_KEYS = {
    "title",
    "summary",
    "owner",
    "domain",
    "level",
    "tags",
    "links",
    "applies_to",
    "pinned",
}


def _issue(severity: str, code: str, message: str, path: Path | str = "") -> Issue:
    return Issue(severity=severity, code=code, message=message, path=str(path))


def _check_meta(spec: Spec, issues: list[Issue], path: str = "") -> None:

    if not spec.id:
        issues.append(_issue("error", "E001", "missing required field: id", path))
    elif not SPEC_ID_RE.match(spec.id):
        issues.append(_issue("error", "E002", f"invalid id {spec.id!r} (use lower-kebab-case)", path))

    if not spec.kind:
        issues.append(_issue("error", "E003", "missing required field: kind", path))
    elif spec.kind not in KINDS:
        issues.append(_issue("error", "E004", f"unknown kind {spec.kind!r}", path))

    if not spec.title:
        issues.append(_issue("error", "E005", "missing required field: title", path))
    if not spec.version:
        issues.append(_issue("error", "E006", "missing required field: version", path))
    elif not is_semver(spec.version):
        issues.append(_issue("error", "E007", f"version {spec.version!r} is not semver (MAJOR.MINOR.PATCH)", path))
    if not spec.status:
        issues.append(_issue("error", "E008", "missing required field: status", path))
    elif spec.status not in STATUSES:
        issues.append(_issue("error", "E009", f"unknown status {spec.status!r}", path))
    if not spec.owner:
        issues.append(_issue("error", "E010", "missing required field: owner", path))

    if spec.status == "approved":
        if not spec.meta.get("approved_by"):
            issues.append(_issue("error", "E011", "approved spec must have approved_by", path))
        if not spec.meta.get("approved_at"):
            issues.append(_issue("error", "E012", "approved spec must have approved_at", path))
    elif spec.status in ("draft", "proposed"):
        if spec.meta.get("approved_by"):
            issues.append(_issue("warning", "W001", "draft/proposed spec carries approved_by", path))

    if spec.meta.get("created") and not DATE_RE.match(str(spec.meta["created"])):
        issues.append(_issue("warning", "W002", "created should start with YYYY-MM-DD", path))
    if spec.meta.get("updated") and not DATE_RE.match(str(spec.meta["updated"])):
        issues.append(_issue("warning", "W003", "updated should start with YYYY-MM-DD", path))

    if spec.kind == "contract":
        contract_type = spec.meta.get("type")
        if not contract_type:
            issues.append(_issue("warning", "W004", "contract spec should declare type", path))
        elif str(contract_type) not in CONTRACT_TYPES:
            issues.append(_issue("warning", "W005", f"unknown contract type {contract_type!r}", path))
        contract_path = spec.meta.get("path")
        if contract_path:
            resolved = spec.path.parent / str(contract_path)
            if not resolved.exists():
                issues.append(_issue("error", "E013", f"contract file not found: {contract_path}", path))
        elif contract_type in ("openapi", "asyncapi"):
            issues.append(_issue("warning", "W006", "contract spec has no path to the schema file", path))

    if spec.kind == "standard":
        if spec.pinned and not spec.applies_to:
            issues.append(_issue("warning", "W007", "pinned standard should declare applies_to", path))
        if spec.pinned and spec.status != "approved":
            issues.append(_issue("warning", "W008", "pinned standard should be approved", path))

    if spec.kind == "service":
        domains = spec.link_targets("implements")
        if not domains:
            issues.append(_issue("warning", "W009", "service does not implement a domain", path))
        elif len(domains) > 1:
            issues.append(_issue("warning", "W010", "service implements more than one domain", path))
        constraints = spec.link_targets("constrained-by")
        if not constraints:
            issues.append(_issue("warning", "W011", "service has no constrained-by standard", path))

    if spec.kind == "nfr" and not spec.applies_to:
        issues.append(_issue("warning", "W012", "nfr should declare applies_to", path))

    if spec.kind == "flow":
        related = spec.link_targets("part-of", "relates-to", "documents")
        if not related:
            issues.append(_issue("warning", "W013", "flow has no part-of / relates-to links", path))


def _check_links(spec: Spec, specs: dict[str, Spec], issues: list[Issue], path: str = "") -> None:
    for link in spec.links:
        rel = link["rel"]
        target = link["target"]
        if rel not in RELS:
            issues.append(_issue("error", "E020", f"unknown link relation {rel!r}", path))
            continue
        if target.startswith("http://") or target.startswith("https://"):
            continue
        if target == spec.id:
            issues.append(_issue("error", "E021", f"self-link {rel} -> {target}", path))
            continue
        if target not in specs:
            issues.append(_issue("error", "E022", f"broken link {rel} -> {target}", path))
            continue
        other = specs[target]
        if spec.status == "approved" and other.status == "deprecated":
            issues.append(_issue("warning", "W020", f"approved spec links to deprecated {target}", path))
        if spec.status == "approved" and other.status in ("draft", "proposed"):
            issues.append(_issue("warning", "W021", f"approved spec links to unapproved {target}", path))


def _check_requirements(spec: Spec, req_owner: dict[str, str], issues: list[Issue], root: Path, path: str = "") -> None:
    seen: set[str] = set()
    for requirement in spec.requirements:
        if requirement.id in seen:
            issues.append(_issue("error", "E030", f"duplicate requirement in spec: {requirement.id}", path))
        seen.add(requirement.id)
        if not REQ_ID_RE.match(requirement.id):
            issues.append(_issue("error", "E031", f"invalid requirement id {requirement.id!r}", path))
        if requirement.id in req_owner and req_owner[requirement.id] != spec.id:
            issues.append(
                _issue(
                    "error",
                    "E032",
                    f"requirement {requirement.id} also used by {req_owner[requirement.id]}",
                    path,
                )
            )
        req_owner.setdefault(requirement.id, spec.id)

        if requirement.priority not in ("must", "should", "may"):
            issues.append(
                _issue("warning", "W030", f"{requirement.id}: priority should be must/should/may", path)
            )
        if requirement.normative and not requirement.has_acceptance:
            issues.append(
                _issue("warning", "W031", f"{requirement.id}: normative requirement has no Given/When/Then", path)
            )
        for trace in requirement.traces:
            candidate = root / trace
            if "/" in trace and not candidate.exists():
                issues.append(_issue("warning", "W032", f"{requirement.id}: trace target not found: {trace}", path))


def _check_proposals(root: Path, specs: dict[str, Spec], issues: list[Issue]) -> None:
    proposals_seen: dict[str, int] = {}
    for path in iter_proposals(root):
        rel = relpath(path, root)
        try:
            proposal = load_spec(path)
        except SpecError as exc:
            issues.append(_issue("error", "E040", str(exc), rel))
            continue

        if proposal.kind != "change":
            issues.append(_issue("error", "E041", "proposal kind must be 'change'", rel))
        if not proposal.id or not PROPOSAL_ID_RE.match(proposal.id):
            issues.append(_issue("error", "E042", f"invalid proposal id {proposal.id!r} (CHG-...)", rel))
        target_id = str(proposal.meta.get("target", ""))
        if not target_id:
            issues.append(_issue("error", "E043", "proposal missing target", rel))
        elif target_id not in specs:
            issues.append(_issue("error", "E044", f"proposal target not found: {target_id}", rel))

        base = str(proposal.meta.get("base_version", ""))
        if not base:
            issues.append(_issue("error", "E045", "proposal missing base_version", rel))
        elif not is_semver(base):
            issues.append(_issue("error", "E046", f"base_version {base!r} is not semver", rel))
        elif target_id in specs and base != specs[target_id].version:
            issues.append(
                _issue(
                    "error",
                    "E047",
                    f"stale proposal: base_version {base} != current {specs[target_id].version}",
                    rel,
                )
            )

        bump = str(proposal.meta.get("bump", ""))
        if bump not in BUMPS:
            issues.append(_issue("error", "E048", f"bump must be one of {BUMPS}", rel))
        if proposal.status not in ("proposed", "draft"):
            issues.append(_issue("warning", "W040", f"open proposal has status {proposal.status!r}", rel))
        if not proposal.meta.get("summary"):
            issues.append(_issue("warning", "W041", "proposal has no summary", rel))

        overrides = proposal.meta.get("spec") or {}
        if overrides and not isinstance(overrides, dict):
            issues.append(_issue("error", "E049", "proposal 'spec' must be a mapping", rel))
        elif isinstance(overrides, dict):
            unknown = set(overrides) - ALLOWED_OVERRIDE_KEYS
            if unknown:
                issues.append(
                    _issue("error", "E050", f"proposal overrides unsupported fields: {sorted(unknown)}", rel)
                )

        proposals_seen[target_id] = proposals_seen.get(target_id, 0) + 1

        req_ids: set[str] = set()
        for requirement in proposal.requirements:
            if requirement.id in req_ids:
                issues.append(_issue("error", "E051", f"duplicate requirement in proposal: {requirement.id}", rel))
            req_ids.add(requirement.id)
            if target_id in specs and requirement.id in specs[target_id].requirement_ids():
                continue
            if not REQ_ID_RE.match(requirement.id):
                issues.append(_issue("error", "E052", f"invalid requirement id {requirement.id!r}", rel))

        if target_id in specs and proposal.body.strip() == specs[target_id].body.strip():
            issues.append(_issue("warning", "W042", "proposal body is identical to the target spec", rel))

    for target_id, count in proposals_seen.items():
        if count > 1:
            issues.append(
                _issue("warning", "W043", f"{count} open proposals for {target_id}; release or close them", "")
            )


def _check_index_drift(root: Path, specs: dict[str, Spec], issues: list[Issue]) -> None:
    index_path = root / "index.json"
    if not index_path.exists():
        return
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return

    released: set[tuple[str, str]] = set()
    events_path = root / ".specd" / "events.jsonl"
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("event") == "release":
                released.add((str(event.get("spec", "")), str(event.get("version", ""))))

    old_specs = index.get("specs", {})
    for spec_id, old in old_specs.items():
        if spec_id not in specs:
            issues.append(_issue("warning", "W050", f"spec {spec_id} disappeared since last index", ""))
            continue
        current = specs[spec_id]
        rel = relpath(current.path, root)
        old_hash = old.get("content_hash")
        if (
            old_hash
            and old_hash != current.content_hash()
            and old.get("version") == current.version
            and current.status == "approved"
        ):
            issues.append(
                _issue(
                    "warning",
                    "W051",
                    "approved spec body changed without a version bump; use a change proposal + release",
                    rel,
                )
            )
        if old.get("version") != current.version and (spec_id, current.version) not in released:
            issues.append(
                _issue(
                    "warning",
                    "W052",
                    f"version changed {old.get('version')} -> {current.version} outside `specd release`",
                    rel,
                )
            )
        if old.get("status") == "approved" and current.status in ("draft", "proposed"):
            issues.append(
                _issue("warning", "W053", "published spec moved back to draft/proposed", rel)
            )


def validate(root: Path, strict: bool = False) -> list[Issue]:
    root = Path(root).resolve()
    issues: list[Issue] = []
    specs: dict[str, Spec] = {}
    duplicates: set[str] = set()

    for path in iter_specs(root):
        try:
            spec = load_spec(path)
        except SpecError as exc:
            issues.append(_issue("error", "E000", str(exc), relpath(path, root)))
            continue
        if spec.id in specs:
            duplicates.add(spec.id)
            issues.append(
                _issue("error", "E023", f"duplicate spec id {spec.id} ({relpath(path, root)})", relpath(path, root))
            )
            continue
        specs[spec.id] = spec

    for spec in specs.values():
        rel = relpath(spec.path, root)
        _check_meta(spec, issues, rel)
        _check_links(spec, specs, issues, rel)
        if spec.path.stem != spec.id:
            issues.append(_issue("warning", "W014", f"filename {spec.path.stem!r} != id {spec.id!r}", rel))

    req_owner: dict[str, str] = {}
    for spec in specs.values():
        _check_requirements(spec, req_owner, issues, root, relpath(spec.path, root))

    _check_proposals(root, specs, issues)
    _check_index_drift(root, specs, issues)

    incoming: dict[str, int] = {spec_id: 0 for spec_id in specs}
    for spec in specs.values():
        for link in spec.links:
            if link["target"] in incoming:
                incoming[link["target"]] += 1
    for spec in specs.values():
        if spec.kind in ("system", "standard"):
            continue
        if incoming.get(spec.id, 0) == 0:
            issues.append(
                _issue("warning", "W060", "orphan spec: nothing links to it", relpath(spec.path, root))
            )

    if strict:
        for issue in issues:
            if issue.severity == "warning":
                issue.severity = "error"

    issues.sort(key=lambda issue: (0 if issue.severity == "error" else 1, issue.path, issue.code))
    return issues


def format_issues(issues: list[Issue]) -> str:
    if not issues:
        return "OK: no issues found"
    return "\n".join(str(issue) for issue in issues)
