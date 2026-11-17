"""Usage telemetry derived from the event log."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .events import read_events
from .index import load_index


def stats(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    events = read_events(root)
    by_event = Counter(event.get("event", "?") for event in events)
    context_targets = Counter(event.get("spec", "?") for event in events if event.get("event") == "context")
    release_versions = [
        {
            "spec": event.get("spec"),
            "version": event.get("version"),
            "proposal": event.get("proposal"),
            "by": event.get("by"),
            "at": event.get("at"),
        }
        for event in events
        if event.get("event") == "release"
    ]
    index = load_index(root)
    return {
        "events": len(events),
        "by_event": dict(sorted(by_event.items())),
        "context_targets": dict(context_targets.most_common(20)),
        "releases": release_versions[-20:],
        "specs": (index or {}).get("stats", {}),
    }
