"""Core data model for specd.

A spec is a Markdown file with a YAML front-matter block. The front-matter
carries identity and lifecycle metadata; the body carries intent, behaviour,
contracts and decisions. Requirements inside the body use stable IDs so that
code, tests and other specs can reference them.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

KINDS = ("system", "domain", "service", "contract", "flow", "nfr", "adr", "standard")
STATUSES = ("draft", "proposed", "approved", "deprecated")
BUMPS = ("none", "patch", "minor", "major")

RELS = (
    "implements",
    "part-of",
    "depends-on",
    "exposes",
    "publishes",
    "consumes",
    "constrained-by",
    "decided-by",
    "supersedes",
    "superseded-by",
    "documents",
    "relates-to",
    "owned-by",
)

REL_LABELS = {
    "implements": "implements",
    "part-of": "part of",
    "depends-on": "depends on",
    "exposes": "exposes",
    "publishes": "publishes",
    "consumes": "consumes",
    "constrained-by": "constrained by",
    "decided-by": "decided by",
    "supersedes": "supersedes",
    "superseded-by": "superseded by",
    "documents": "documents",
    "relates-to": "relates to",
    "owned-by": "owned by",
}

FRONT_MATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n?", re.S)
REQ_RE = re.compile(r"^###\s+(REQ-[A-Z][A-Z0-9]*-\d{3,})\s*(.*?)\s*$", re.M)
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?$")
SPEC_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
REQ_ID_RE = re.compile(r"^REQ-[A-Z][A-Z0-9]*-\d{3,}$")

META_ORDER = [
    "id",
    "kind",
    "title",
    "summary",
    "version",
    "status",
    "owner",
    "domain",
    "level",
    "pinned",
    "applies_to",
    "tags",
    "created",
    "updated",
    "approved_by",
    "approved_at",
    "links",
    # change-proposal fields
    "target",
    "base_version",
    "bump",
    "author",
    "spec",
]

PRIORITY_VALUES = ("must", "should", "may")

_FIELD_RE = {
    "priority": re.compile(r"^\s*[-*]?\s*\*\*Priority:?\*\*\s*([A-Za-z]+)", re.I),
    "normative": re.compile(r"^\s*[-*]?\s*\*\*Normative:?\*\*\s*([A-Za-z]+)", re.I),
    "given": re.compile(r"^\s*[-*]?\s*\*\*Given:?\*\*\s*(.+?)\s*$", re.I),
    "when": re.compile(r"^\s*[-*]?\s*\*\*When:?\*\*\s*(.+?)\s*$", re.I),
    "then": re.compile(r"^\s*[-*]?\s*\*\*Then:?\*\*\s*(.+?)\s*$", re.I),
    "traces": re.compile(r"^\s*[-*]?\s*\*\*Traces:?\*\*\s*(.+?)\s*$", re.I),
}


class SpecError(Exception):
    """Raised when a spec cannot be parsed."""


@dataclass
class Requirement:
    id: str
    title: str
    priority: str = "must"
    normative: bool = True
    given: str = ""
    when: str = ""
    then: str = ""
    traces: list[str] = field(default_factory=list)
    body: str = ""

    @property
    def has_acceptance(self) -> bool:
        return bool(self.given and self.when and self.then)


@dataclass
class Spec:
    path: Path
    meta: dict[str, Any]
    body: str
    requirements: list[Requirement] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return str(self.meta.get("id", ""))

    @property
    def kind(self) -> str:
        return str(self.meta.get("kind", ""))

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.id))

    @property
    def summary(self) -> str:
        return str(self.meta.get("summary", ""))

    @property
    def version(self) -> str:
        return str(self.meta.get("version", "0.0.0"))

    @property
    def status(self) -> str:
        return str(self.meta.get("status", "draft"))

    @property
    def owner(self) -> str:
        return str(self.meta.get("owner", ""))

    @property
    def domain(self) -> str:
        return str(self.meta.get("domain", ""))

    @property
    def level(self) -> str:
        return str(self.meta.get("level", ""))

    @property
    def pinned(self) -> bool:
        return bool(self.meta.get("pinned", False))

    @property
    def applies_to(self) -> list[str]:
        value = self.meta.get("applies_to") or []
        return [str(v) for v in value] if isinstance(value, list) else [str(value)]

    @property
    def tags(self) -> list[str]:
        value = self.meta.get("tags") or []
        return [str(v) for v in value] if isinstance(value, list) else [str(value)]

    @property
    def links(self) -> list[dict[str, str]]:
        raw = self.meta.get("links") or []
        out: list[dict[str, str]] = []
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict) and item.get("rel") and item.get("target"):
                    out.append({"rel": str(item["rel"]), "target": str(item["target"])})
        return out

    def link_targets(self, *rels: str) -> list[str]:
        wanted = set(rels)
        return [link["target"] for link in self.links if not wanted or link["rel"] in wanted]

    def link_rels(self) -> set[str]:
        return {link["rel"] for link in self.links}

    def content_hash(self) -> str:
        return hashlib.sha256(self.body.strip().encode("utf-8")).hexdigest()

    def requirement_ids(self) -> list[str]:
        return [r.id for r in self.requirements]

    def to_summary(self, root: Path) -> dict[str, Any]:
        try:
            rel = str(self.path.relative_to(root))
        except ValueError:
            rel = str(self.path)
        return {
            "id": self.id,
            "kind": self.kind,
            "title": self.title,
            "summary": self.summary,
            "version": self.version,
            "status": self.status,
            "owner": self.owner,
            "domain": self.domain,
            "level": self.level,
            "pinned": self.pinned,
            "applies_to": self.applies_to,
            "tags": self.tags,
            "path": rel,
            "requirements": self.requirement_ids(),
            "requirement_count": len(self.requirements),
            "open_questions": len(self.open_questions),
            "content_hash": self.content_hash(),
            "links": self.links,
        }


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def _parse_front_matter(text: str, path: Path) -> tuple[dict[str, Any], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise SpecError(f"{path}: missing YAML front-matter (expected a leading '---' block)")
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise SpecError(f"{path}: invalid YAML front-matter: {exc}") from exc
    if not isinstance(meta, dict):
        raise SpecError(f"{path}: front-matter must be a YAML mapping")
    body = text[match.end():].lstrip("\n")
    return meta, body


def _parse_requirement(req_id: str, title: str, block: str) -> Requirement:
    req = Requirement(id=req_id, title=title.strip(), body=block.strip())
    for line in block.splitlines():
        for name, pattern in _FIELD_RE.items():
            match = pattern.match(line)
            if not match:
                continue
            value = match.group(1).strip()
            if name == "priority":
                req.priority = value.lower()
            elif name == "normative":
                req.normative = value.lower() in ("true", "yes", "1", "required")
            elif name == "traces":
                parts = re.split(r"[,;]", value)
                req.traces = [p.strip().strip("`") for p in parts if p.strip()]
            else:
                setattr(req, name, value)
    return req


def _extract_open_questions(body: str) -> list[str]:
    questions: list[str] = []
    in_section = False
    for line in body.splitlines():
        if re.match(r"^##\s+Open Questions\s*$", line, re.I):
            in_section = True
            continue
        if in_section and re.match(r"^##\s+\S", line):
            break
        if in_section:
            match = re.match(r"^\s*[-*]\s+(?:\[[ xX]\]\s*)?(.+?)\s*$", line)
            if match:
                questions.append(match.group(1).strip())
    return questions


def _extract_requirements(body: str) -> list[Requirement]:
    matches = list(REQ_RE.finditer(body))
    requirements: list[Requirement] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        block = body[match.end():end]
        # A requirement belongs to its section; stop at the next level-2 heading.
        cut = re.search(r"^##\s+\S", block, re.M)
        if cut:
            block = block[:cut.start()]
        requirements.append(_parse_requirement(match.group(1), match.group(2), block))
    return requirements


def parse_spec(text: str, path: Path) -> Spec:
    meta, body = _parse_front_matter(text, path)
    return Spec(
        path=path,
        meta=meta,
        body=body,
        requirements=_extract_requirements(body),
        open_questions=_extract_open_questions(body),
    )


def load_spec(path: Path) -> Spec:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SpecError(f"{path}: cannot read: {exc}") from exc
    return parse_spec(text, path)


def iter_specs(root: Path) -> list[Path]:
    base = root / "specs"
    if not base.exists():
        return []
    paths = []
    for path in sorted(base.rglob("*.md")):
        if "changes" in path.parts:
            continue
        paths.append(path)
    return paths


def iter_proposals(root: Path, include_archive: bool = False) -> list[Path]:
    base = root / "changes"
    if not base.exists():
        return []
    paths = []
    for path in sorted(base.rglob("*.md")):
        if not include_archive and "archive" in path.parts:
            continue
        paths.append(path)
    return paths


def load_all(root: Path) -> tuple[dict[str, Spec], list[str]]:
    specs: dict[str, Spec] = {}
    duplicates: list[str] = []
    for path in iter_specs(root):
        spec = load_spec(path)
        if spec.id in specs:
            duplicates.append(spec.id)
            continue
        specs[spec.id] = spec
    return specs, duplicates


def find_spec(root: Path, spec_id: str) -> Spec | None:
    for path in iter_specs(root):
        if path.stem == spec_id:
            return load_spec(path)
    specs, _ = load_all(root)
    return specs.get(spec_id)


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def ordered_meta(meta: dict[str, Any]) -> dict[str, Any]:
    ordered: dict[str, Any] = {}
    for key in META_ORDER:
        if key in meta:
            ordered[key] = meta[key]
    for key, value in meta.items():
        if key not in ordered and not key.startswith("_"):
            ordered[key] = value
    return ordered


def dump_spec(meta: dict[str, Any], body: str) -> str:
    front = yaml.safe_dump(
        ordered_meta(meta),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    ).strip()
    return f"---\n{front}\n---\n\n{body.strip()}\n"


def write_spec(path: Path, meta: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_spec(meta, body), encoding="utf-8")


# ---------------------------------------------------------------------------
# Versions and time
# ---------------------------------------------------------------------------


def parse_version(version: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(str(version))
    if not match:
        raise ValueError(f"not a semantic version: {version!r}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def is_semver(version: str) -> bool:
    return bool(SEMVER_RE.match(str(version)))


def bump_version(version: str, bump: str) -> str:
    """Return the next version. `none` keeps the version unchanged."""
    if bump not in BUMPS:
        raise ValueError(f"unknown bump: {bump!r}")
    if bump == "none":
        return version
    major, minor, patch = parse_version(version)
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def relpath(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]
