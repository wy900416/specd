"""Command line interface for specd."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .context import build_context, compute_impact, context_text
from .events import append_event
from .fitness import check_fitness
from .index import build_index
from .issues import counts, has_errors
from .lifecycle import diff_proposal, list_proposals, new_spec, propose, release
from .model import KINDS, BUMPS
from .openapi import import_openapi
from .render import build_site
from .scan import scan
from .stats import stats
from .trace import trace
from .validate import format_issues, validate


def _root(args: argparse.Namespace) -> Path:
    if getattr(args, "root", None):
        return Path(args.root).resolve()
    cwd = Path.cwd()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / "specs").is_dir() and (candidate / "templates").is_dir():
            return candidate
    return cwd


def _color(text: str, code: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def _print_issues(issues: list[Any]) -> None:
    for issue in issues:
        if issue.severity == "error":
            print(_color(str(issue), "31"))
        elif issue.severity == "warning":
            print(_color(str(issue), "33"))
        else:
            print(str(issue))


def cmd_validate(args: argparse.Namespace) -> int:
    root = _root(args)
    issues = validate(root, strict=args.strict)
    if args.json:
        print(json.dumps([issue.as_dict() for issue in issues], indent=2, ensure_ascii=False))
    else:
        _print_issues(issues)
        summary = counts(issues)
        print(
            f"\n{summary['error']} error(s), {summary['warning']} warning(s), "
            f"{summary['info']} info"
        )
        if not issues:
            print(_color("OK: spec graph is valid", "32"))
    return 1 if has_errors(issues) else 0


def cmd_index(args: argparse.Namespace) -> int:
    root = _root(args)
    index = build_index(root)
    stats_data = index["stats"]
    print(f"indexed {stats_data['specs']} specs, {stats_data['requirements']} requirements")
    print(f"edges: {len(index['edges'])}, broken links: {len(index['broken_links'])}, proposals: {len(index['proposals'])}")
    print(f"wrote {root / 'index.json'}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    root = _root(args)
    out = Path(args.out).resolve() if args.out else root / "dist"
    build_site(root, out)
    print(f"built viewer at {out / 'index.html'}")
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    root = _root(args)
    try:
        pack = build_context(
            root,
            args.id,
            task=args.task or "",
            depth=args.depth,
            budget=args.budget,
            fmt=args.format,
        )
    except KeyError as exc:
        print(_color(str(exc), "31"), file=sys.stderr)
        return 2
    text = context_text(pack, fmt=args.format)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"wrote context pack to {args.out}")
    else:
        print(text)
    append_event(root, "context", spec=args.id, task=args.task or "", used=pack.used, budget=pack.budget)
    return 0


def cmd_impact(args: argparse.Namespace) -> int:
    root = _root(args)
    try:
        results = compute_impact(root, args.id)
    except KeyError as exc:
        print(_color(str(exc), "31"), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0
    if not results:
        print(f"no dependents found for {args.id}")
        return 0
    print(f"impact of {args.id}: {len(results)} dependent spec(s)\n")
    for item in results:
        indent = "  " * (item["depth"] - 1)
        print(
            f"{indent}- {item['id']} ({item['kind']}, {item['status']}) "
            f"via {item['rel']} from {item['via']}"
        )
    return 0


def cmd_trace(args: argparse.Namespace) -> int:
    root = _root(args)
    paths = args.path or ["src", "tests"]
    missing = [path for path in paths if not (root / path).exists()]
    for path in missing:
        print(_color(f"warning: path does not exist: {path}", "33"), file=sys.stderr)
    result = trace(root, paths)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    print(
        f"requirements: {result['requirements']}, referenced: {result['covered']}, "
        f"unreferenced: {result['uncovered']} ({result['coverage'] * 100:.0f}%)"
    )
    if result["uncovered_ids"]:
        print("\nunreferenced:")
        for req_id in result["uncovered_ids"]:
            print(f"  - {req_id}")
    if result["unknown_ids"]:
        print("\nunknown requirement IDs in code:")
        for req_id, paths_list in result["unknown_ids"].items():
            print(f"  - {req_id}: {', '.join(paths_list)}")
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    root = _root(args)
    findings = scan(root)
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2, ensure_ascii=False))
    else:
        for finding in findings:
            print(
                f"{finding.severity.upper():8} {finding.code} {finding.path}:{finding.line}  "
                f"{finding.message}\n         {finding.excerpt}"
            )
        if not findings:
            print(_color("OK: no suspicious content found", "32"))
        else:
            severe = [item for item in findings if item.severity in ("critical", "high")]
            print(f"\n{len(findings)} finding(s), {len(severe)} critical/high")
    if args.strict:
        return 1 if any(item.severity in ("critical", "high") for item in findings) else 0
    return 0


def cmd_fitness(args: argparse.Namespace) -> int:
    root = _root(args)
    issues = check_fitness(root)
    _print_issues(issues)
    summary = counts(issues)
    print(f"\n{summary['error']} error(s), {summary['warning']} warning(s)")
    return 1 if has_errors(issues) else 0


def cmd_propose(args: argparse.Namespace) -> int:
    root = _root(args)
    try:
        path, proposal = propose(
            root,
            args.id,
            bump=args.bump,
            summary=args.summary,
            author=args.author,
            title=args.title,
        )
    except (KeyError, ValueError) as exc:
        print(_color(str(exc), "31"), file=sys.stderr)
        return 2
    print(f"created proposal {proposal.id}")
    print(f"  target: {proposal.meta.get('target')} @ {proposal.meta.get('base_version')}")
    print(f"  bump:   {proposal.meta.get('bump')}")
    print(f"  file:   {path}")
    print("\nnext: edit the proposal body, then `specd diff <proposal>` and `specd release <proposal> --by <name>`")
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    root = _root(args)
    try:
        print(diff_proposal(root, Path(args.proposal)))
    except (KeyError, FileNotFoundError) as exc:
        print(_color(str(exc), "31"), file=sys.stderr)
        return 2
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    root = _root(args)
    if not args.force:
        issues = validate(root)
        errors = [issue for issue in issues if issue.severity == "error"]
        if errors:
            print(_color("refusing to release: validation errors", "31"), file=sys.stderr)
            _print_issues(errors)
            return 1
    try:
        result = release(root, Path(args.proposal), approved_by=args.by)
    except (KeyError, ValueError, FileNotFoundError) as exc:
        print(_color(str(exc), "31"), file=sys.stderr)
        return 2
    build_index(root)
    print(
        f"released {result['proposal']}: {result['spec']} -> v{result['version']} "
        f"(approved by {args.by})"
    )
    return 0


def cmd_proposals(args: argparse.Namespace) -> int:
    root = _root(args)
    proposals = list_proposals(root)
    if args.json:
        print(json.dumps(proposals, indent=2, ensure_ascii=False))
        return 0
    if not proposals:
        print("no open proposals")
        return 0
    for proposal in proposals:
        print(
            f"{proposal['id']}  {proposal['target']}  bump={proposal['bump']}  "
            f"status={proposal['status']}  author={proposal['author']}"
        )
        print(f"  {proposal['summary']}")
        print(f"  {proposal['path']}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    root = _root(args)
    print(json.dumps(stats(root), indent=2, ensure_ascii=False))
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    root = _root(args)
    extra: dict[str, str] = {}
    if args.type:
        extra["type"] = args.type
    if args.contract_path:
        extra["contract_path"] = args.contract_path
    if args.domain:
        extra["domain"] = args.domain
    if args.level:
        extra["level"] = args.level
    try:
        path = new_spec(
            root,
            kind=args.kind,
            spec_id=args.id,
            title=args.title,
            owner=args.owner,
            summary=args.summary or "",
            template=args.template,
            extra=extra,
        )
    except (FileNotFoundError, FileExistsError) as exc:
        print(_color(str(exc), "31"), file=sys.stderr)
        return 2
    print(f"created {path}")
    print("next: fill the draft, then validate. Drafts do not need a proposal until they are approved.")
    return 0


def cmd_import_openapi(args: argparse.Namespace) -> int:
    root = _root(args)
    try:
        path = import_openapi(
            root,
            Path(args.file),
            service_id=args.service,
            owner=args.owner,
            spec_id=args.id,
        )
    except (FileNotFoundError, ValueError, FileExistsError) as exc:
        print(_color(str(exc), "31"), file=sys.stderr)
        return 2
    print(f"imported OpenAPI contract -> {path}")
    print("note: the draft is not linked to the service yet; add an `exposes` link via a change proposal.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="specd",
        description="Validate, index, pack, release and render a spec graph.",
    )
    parser.add_argument("--root", help="project root (default: nearest ancestor with specs/ and templates/)")
    parser.add_argument("--version", action="version", version=f"specd {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="validate specs and proposals")
    p.add_argument("--strict", action="store_true", help="treat warnings as errors")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("index", help="build index.json")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("build", help="build the static viewer")
    p.add_argument("--out", help="output directory (default: dist/)")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("context", help="pack a bounded context for an agent")
    p.add_argument("id")
    p.add_argument("--task", default="")
    p.add_argument("--depth", type=int, default=2)
    p.add_argument("--budget", type=int, default=12000, help="character budget")
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--out")
    p.set_defaults(func=cmd_context)

    p = sub.add_parser("impact", help="list specs affected by a change")
    p.add_argument("id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_impact)

    p = sub.add_parser("trace", help="trace requirements into code/tests")
    p.add_argument("--path", action="append", help="file or directory to scan (repeatable)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_trace)

    p = sub.add_parser("scan", help="scan specs for injection/secrets/internal endpoints")
    p.add_argument("--strict", action="store_true", help="exit 1 on critical/high findings")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("fitness", help="run architecture fitness functions")
    p.set_defaults(func=cmd_fitness)

    p = sub.add_parser("propose", help="create a change proposal from a published spec")
    p.add_argument("id")
    p.add_argument("--bump", choices=BUMPS, required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--author", default="agent")
    p.add_argument("--title")
    p.set_defaults(func=cmd_propose)

    p = sub.add_parser("diff", help="diff a proposal against its target")
    p.add_argument("proposal")
    p.set_defaults(func=cmd_diff)

    p = sub.add_parser("release", help="apply a proposal, bump the version and archive it")
    p.add_argument("proposal")
    p.add_argument("--by", required=True, help="human approver")
    p.add_argument("--force", action="store_true", help="skip validation")
    p.set_defaults(func=cmd_release)

    p = sub.add_parser("proposals", help="list open proposals")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_proposals)

    p = sub.add_parser("stats", help="show usage telemetry")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("new", help="create a spec from a template")
    p.add_argument("kind", choices=KINDS)
    p.add_argument("id")
    p.add_argument("--title", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--summary", default="")
    p.add_argument("--template")
    p.add_argument("--domain")
    p.add_argument("--level")
    p.add_argument("--type", dest="type")
    p.add_argument("--contract-path", dest="contract_path")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("import-openapi", help="import an OpenAPI document as a draft contract spec")
    p.add_argument("file")
    p.add_argument("--service", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--id", dest="id")
    p.set_defaults(func=cmd_import_openapi)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
