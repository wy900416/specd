"""Reverse flow: import an OpenAPI document as a draft contract spec.

This is intentionally a starting point, not a full contract extractor. It turns
the parts of an existing service that are already machine-readable into a spec
skeleton, so a human or agent can review and enrich it instead of starting from
a blank page.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from .events import append_event
from .model import is_semver, now_iso, relpath, write_spec


def _slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "contract"


def _normalise_version(value: Any) -> tuple[str, str | None]:
    text = str(value or "").strip()
    if is_semver(text):
        return text, None
    major = re.match(r"^v?(\d+)", text)
    if major:
        return f"{major.group(1)}.0.0", f"source version {text!r} normalised to {major.group(1)}.0.0"
    return "0.1.0", f"source version {text!r} replaced with 0.1.0"


def _operations(document: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for path, item in sorted((document.get("paths") or {}).items()):
        if not isinstance(item, dict):
            continue
        for method in ("get", "put", "post", "delete", "patch", "options", "head", "trace"):
            operation = item.get(method)
            if not isinstance(operation, dict):
                continue
            rows.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "operation": str(operation.get("operationId", "")),
                    "summary": str(operation.get("summary", operation.get("description", ""))).split("\n")[0],
                }
            )
    return rows


def import_openapi(
    root: Path,
    source: Path,
    service_id: str,
    owner: str,
    spec_id: str | None = None,
) -> Path:
    root = Path(root).resolve()
    source = Path(source)
    text = source.read_text(encoding="utf-8")
    document = yaml.safe_load(text)
    if not isinstance(document, dict):
        raise ValueError("OpenAPI document must be a mapping")

    info = document.get("info") or {}
    title = str(info.get("title") or source.stem)
    version, note = _normalise_version(info.get("version"))

    if spec_id is None:
        service_slug = _slug(service_id.removeprefix("svc-"))
        major = version.split(".")[0]
        spec_id = f"api-{service_slug}-v{major}"

    contract_dir = root / "contracts"
    contract_dir.mkdir(parents=True, exist_ok=True)
    suffix = source.suffix if source.suffix in (".yaml", ".yml", ".json") else ".yaml"
    contract_path = contract_dir / f"{spec_id}.openapi{suffix}"
    if source.resolve() != contract_path.resolve():
        contract_path.write_text(text, encoding="utf-8")

    rows = _operations(document)
    lines = [
        "## Intent",
        "",
        f"Imported from `{relpath(source, root)}` as a starting point for the contract of `{service_id}`.",
        "This draft describes the interface that exists today; review it before approving.",
        "",
        "## Interface",
        "",
        "| Method | Path | Operation | Summary |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['method']} | `{row['path']}` | `{row['operation']}` | {row['summary']} |")
    if not rows:
        lines.append("| - | - | - | No operations found |")

    lines.extend(
        [
            "",
            "## Constraints",
            "",
            "- The schema file is the source of truth for request/response shapes.",
            "- Breaking changes require a major version bump and a change proposal.",
            "",
            "## Open Questions",
            "",
            f"- [ ] Confirm that `{owner}` owns this contract.",
            f"- [ ] Link this contract to `{service_id}` with `rel: exposes`.",
            "- [ ] Document authentication, error model and rate limits.",
        ]
    )
    if note:
        lines.extend(["", f"> Import note: {note}."])

    meta: dict[str, Any] = {
        "id": spec_id,
        "kind": "contract",
        "title": title,
        "summary": f"Imported OpenAPI contract for {service_id}",
        "type": "openapi",
        "version": version,
        "status": "draft",
        "owner": owner,
        "created": now_iso()[:10],
        "updated": now_iso()[:10],
        "path": relpath(contract_path, root),
    }
    target = root / "specs" / "contract" / f"{spec_id}.md"
    if target.exists():
        raise FileExistsError(f"spec already exists: {target}")
    write_spec(target, meta, "\n".join(lines) + "\n")
    append_event(root, "import_openapi", spec=spec_id, service=service_id, source=str(source))
    return target
