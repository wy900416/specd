"""Architecture fitness functions over the spec graph.

These are the rules that keep a microservice spec graph coherent: no dependency
cycles, every contract has an owner and a consumer, domains belong to a system,
flows actually cross services, and approved specs do not still have open
questions.
"""

from __future__ import annotations

from pathlib import Path

from .issues import Issue
from .model import Spec, SpecError, iter_specs, load_spec, relpath


def _issue(severity: str, code: str, message: str, path: str = "") -> Issue:
    return Issue(severity=severity, code=code, message=message, path=path)


def _load(root: Path) -> tuple[dict[str, Spec], list[Issue]]:
    specs: dict[str, Spec] = {}
    issues: list[Issue] = []
    for path in iter_specs(root):
        try:
            spec = load_spec(path)
        except SpecError as exc:
            issues.append(_issue("error", "F000", str(exc), relpath(path, root)))
            continue
        if spec.id not in specs:
            specs[spec.id] = spec
    return specs, issues


def _find_cycles(graph: dict[str, list[str]], specs: dict[str, Spec], root: Path) -> list[Issue]:
    issues: list[Issue] = []
    color: dict[str, int] = {}
    stack: list[str] = []
    seen: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        color[node] = 1
        stack.append(node)
        for neighbour in graph.get(node, []):
            if color.get(neighbour, 0) == 1:
                start = stack.index(neighbour)
                cycle = stack[start:] + [neighbour]
                key = tuple(sorted(set(cycle)))
                if key not in seen:
                    seen.add(key)
                    issues.append(
                        _issue(
                            "error",
                            "F001",
                            "dependency cycle: " + " -> ".join(cycle),
                            relpath(specs[node].path, root),
                        )
                    )
            elif color.get(neighbour, 0) == 0:
                visit(neighbour)
        stack.pop()
        color[node] = 2

    for node in graph:
        if color.get(node, 0) == 0:
            visit(node)
    return issues


def check_fitness(root: Path) -> list[Issue]:
    root = Path(root).resolve()
    specs, issues = _load(root)

    graph: dict[str, list[str]] = {}
    for spec_id, spec in specs.items():
        if spec.kind == "service":
            graph[spec_id] = [target for target in spec.link_targets("depends-on") if target in specs]

    issues.extend(_find_cycles(graph, specs, root))

    for spec_id, spec in specs.items():
        rel = relpath(spec.path, root)

        if spec.kind == "contract":
            consumers = [
                other.id
                for other in specs.values()
                if spec_id in other.link_targets("exposes", "publishes", "consumes")
            ]
            if not consumers:
                issues.append(_issue("warning", "F002", "contract has no consuming or exposing service", rel))
            if str(spec.meta.get("type", "")) == "event":
                event_consumers = [
                    other.id for other in specs.values() if spec_id in other.link_targets("consumes")
                ]
                if not event_consumers:
                    issues.append(_issue("warning", "F003", "event is published but never consumed", rel))

        if spec.kind == "service":
            if not spec.link_targets("exposes", "publishes", "consumes"):
                issues.append(_issue("warning", "F004", "service has no contract boundary", rel))
            domains = spec.link_targets("implements")
            if len(domains) != 1:
                issues.append(
                    _issue("warning", "F005", f"service should implement exactly one domain (found {len(domains)})", rel)
                )

        if spec.kind == "domain" and not spec.link_targets("part-of"):
            issues.append(_issue("warning", "F006", "domain is not part-of a system", rel))

        if spec.kind == "flow":
            services = [
                target
                for target in spec.link_targets("part-of", "relates-to", "documents")
                if target in specs and specs[target].kind == "service"
            ]
            if len(services) < 2:
                issues.append(_issue("warning", "F007", "flow should reference at least two services", rel))

        if spec.status == "approved" and spec.open_questions:
            issues.append(
                _issue(
                    "warning",
                    "F008",
                    f"approved spec has {len(spec.open_questions)} open question(s)",
                    rel,
                )
            )

    issues.sort(key=lambda issue: (0 if issue.severity == "error" else 1, issue.path, issue.code))
    return issues
