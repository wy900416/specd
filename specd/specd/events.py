"""Append-only event log used for drift checks and usage telemetry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import now_iso


def append_event(root: Path, event: str, **fields: Any) -> None:
    directory = Path(root) / ".specd"
    directory.mkdir(parents=True, exist_ok=True)
    record = {"event": event, "at": now_iso(), **fields}
    with (directory / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_events(root: Path) -> list[dict[str, Any]]:
    path = Path(root) / ".specd" / "events.jsonl"
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events
