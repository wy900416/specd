"""Static site viewer for the spec graph.

One source of truth (the Markdown files), several projections: a dashboard, one
page per spec, a dependency graph and a traceability view. No server, no CDN.
"""

from __future__ import annotations

import html
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from . import md
from .index import build_index, load_index
from .model import SpecError, iter_specs, load_spec, relpath

STATUS_CLASS = {
    "draft": "draft",
    "proposed": "proposed",
    "approved": "approved",
    "deprecated": "deprecated",
}

KIND_CLASS = {
    "system": "system",
    "domain": "domain",
    "service": "service",
    "contract": "contract",
    "flow": "flow",
    "nfr": "nfr",
    "adr": "adr",
    "standard": "standard",
}

LEVEL = {"system": 0, "domain": 1, "service": 2, "contract": 3, "flow": 3, "adr": 4, "nfr": 4, "standard": 4}

REL_COLORS = {
    "implements": "#64748b",
    "part-of": "#94a3b8",
    "depends-on": "#d97706",
    "exposes": "#2563eb",
    "publishes": "#7c3aed",
    "consumes": "#0891b2",
    "constrained-by": "#dc2626",
    "decided-by": "#059669",
    "supersedes": "#be123c",
    "superseded-by": "#be123c",
    "documents": "#475569",
    "relates-to": "#475569",
    "owned-by": "#475569",
}

CSS = """
:root {
  --bg: #f7f7f5;
  --panel: #ffffff;
  --ink: #1c1917;
  --muted: #78716c;
  --line: #e7e5e4;
  --accent: #1d4ed8;
  --accent-soft: #eff6ff;
  --green: #15803d;
  --green-soft: #f0fdf4;
  --amber: #b45309;
  --amber-soft: #fffbeb;
  --red: #b91c1c;
  --red-soft: #fef2f2;
  --violet: #6d28d9;
  --violet-soft: #f5f3ff;
  --radius: 10px;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: var(--sans); font-size: 15px; line-height: 1.6;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code, pre { font-family: var(--mono); font-size: 0.88em; }
code { background: #f1f0ee; padding: 1px 5px; border-radius: 4px; }
pre { background: #1c1917; color: #e7e5e4; padding: 16px 18px; border-radius: var(--radius); overflow-x: auto; line-height: 1.5; }
pre code { background: transparent; padding: 0; color: inherit; }
.topbar {
  position: sticky; top: 0; z-index: 20;
  display: flex; align-items: center; gap: 24px;
  padding: 0 28px; height: 56px;
  background: rgba(247,247,245,0.92); backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line);
}
.brand { font-weight: 700; font-size: 17px; letter-spacing: -0.02em; color: var(--ink); }
.brand span { color: var(--accent); }
.topbar nav { display: flex; gap: 4px; }
.topbar nav a { color: var(--muted); padding: 6px 10px; border-radius: 6px; font-size: 14px; }
.topbar nav a:hover { background: #edece9; text-decoration: none; }
.topbar nav a.active { color: var(--ink); background: #e7e5e4; font-weight: 600; }
.page { max-width: 1180px; margin: 0 auto; padding: 32px 28px 64px; }
.page.narrow { max-width: 900px; }
h1 { font-size: 28px; line-height: 1.2; letter-spacing: -0.02em; margin: 0 0 8px; }
h2 { font-size: 20px; letter-spacing: -0.01em; margin: 36px 0 12px; }
h3 { font-size: 16px; margin: 28px 0 8px; }
h4 { font-size: 14px; margin: 20px 0 6px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
p { margin: 0 0 12px; }
ul, ol { margin: 0 0 14px; padding-left: 22px; }
li { margin: 3px 0; }
hr { border: 0; border-top: 1px solid var(--line); margin: 24px 0; }
blockquote { margin: 16px 0; padding: 10px 16px; border-left: 3px solid var(--accent); background: var(--accent-soft); color: #1e3a8a; border-radius: 0 8px 8px 0; }
blockquote p:last-child { margin-bottom: 0; }
.subtitle { color: var(--muted); font-size: 15px; margin: 0 0 24px; }
.badges { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.badge { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; border: 1px solid transparent; }
.badge.approved { background: var(--green-soft); color: var(--green); border-color: #bbf7d0; }
.badge.draft { background: #f5f5f4; color: #57534e; border-color: #e7e5e4; }
.badge.proposed { background: var(--amber-soft); color: var(--amber); border-color: #fde68a; }
.badge.deprecated { background: var(--red-soft); color: var(--red); border-color: #fecaca; }
.badge.kind { background: var(--accent-soft); color: var(--accent); border-color: #bfdbfe; }
.badge.version { background: #fafaf9; color: var(--muted); border-color: var(--line); font-family: var(--mono); font-weight: 500; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 20px 0 8px; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 16px 18px; }
.card .num { font-size: 26px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.1; }
.card .label { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px; }
.spec-card { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 18px; display: flex; flex-direction: column; gap: 8px; transition: border-color .15s, box-shadow .15s, transform .15s; }
.spec-card:hover { border-color: #c7c3bd; box-shadow: 0 6px 20px rgba(28,25,23,0.06); transform: translateY(-1px); }
.spec-card h3 { margin: 0; font-size: 16px; }
.spec-card .id { font-family: var(--mono); font-size: 12px; color: var(--muted); }
.spec-card .desc { color: var(--muted); font-size: 13px; flex: 1; }
.spec-card .foot { display: flex; justify-content: space-between; align-items: center; gap: 8px; font-size: 12px; color: var(--muted); }
.toolbar { display: flex; gap: 10px; align-items: center; margin: 18px 0; flex-wrap: wrap; }
input[type="search"], input[type="text"], select {
  background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
  padding: 9px 12px; font: inherit; font-size: 14px; color: var(--ink); min-width: 240px;
}
input:focus, select:focus { outline: 2px solid #bfdbfe; border-color: var(--accent); }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 20px 22px; margin: 16px 0; }
.panel.warn { border-color: #fde68a; background: var(--amber-soft); }
.panel.danger { border-color: #fecaca; background: var(--red-soft); }
.panel h3 { margin-top: 0; }
.meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px 24px; margin: 18px 0; }
.meta .k { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; }
.meta .v { font-size: 14px; word-break: break-word; }
.layout { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 28px; align-items: start; }
.sidebar { position: sticky; top: 80px; }
.sidebar .panel { margin: 0 0 14px; padding: 16px 18px; }
.sidebar h4 { margin-top: 0; }
.sidebar ul { list-style: none; padding: 0; margin: 0; }
.sidebar li { margin: 6px 0; font-size: 13px; }
.rel { color: var(--muted); font-size: 12px; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
.table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: var(--radius); margin: 16px 0; }
table th, table td { padding: 10px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
table th { background: #fafaf9; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); font-weight: 600; }
table tr:last-child td { border-bottom: 0; }
.task-list { list-style: none; padding-left: 0; }
.task-list input { margin-right: 6px; }
.progress { height: 8px; background: #e7e5e4; border-radius: 999px; overflow: hidden; margin: 8px 0 16px; }
.progress span { display: block; height: 100%; background: var(--green); border-radius: 999px; }
.graph-wrap { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 8px; overflow-x: auto; }
.graph-wrap svg { display: block; min-width: 1000px; }
.node rect { fill: #fff; stroke: #d6d3d1; stroke-width: 1.2; rx: 8; }
.node:hover rect, .node.active rect { stroke: var(--accent); stroke-width: 2; }
.node text { font-family: var(--sans); fill: var(--ink); }
.node .node-id { font-family: var(--mono); fill: var(--muted); font-size: 10px; }
.edge { stroke-width: 1.3; fill: none; opacity: 0.45; transition: opacity .12s, stroke-width .12s; }
.edge.active { opacity: 1; stroke-width: 2.4; }
.legend { display: flex; flex-wrap: wrap; gap: 12px 18px; margin: 14px 0; font-size: 12px; color: var(--muted); }
.legend i { display: inline-block; width: 18px; height: 2px; vertical-align: middle; margin-right: 6px; }
.empty { color: var(--muted); padding: 28px; text-align: center; border: 1px dashed var(--line); border-radius: var(--radius); }
.footer { max-width: 1180px; margin: 0 auto; padding: 24px 28px 48px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--line); }
.footer code { font-size: 11px; }
@media (max-width: 860px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { position: static; }
  .topbar { padding: 0 16px; gap: 10px; overflow-x: auto; }
  .page { padding: 24px 16px 48px; }
}
"""

APP_JS = """
(function () {
  var filter = document.getElementById('filter');
  if (filter) {
    filter.addEventListener('input', function () {
      var q = filter.value.toLowerCase().trim();
      document.querySelectorAll('[data-search]').forEach(function (el) {
        el.style.display = !q || el.getAttribute('data-search').toLowerCase().indexOf(q) !== -1 ? '' : 'none';
      });
    });
  }

  var nodes = document.querySelectorAll('.node');
  var edges = document.querySelectorAll('.edge');
  function clear() {
    nodes.forEach(function (n) { n.classList.remove('active'); });
    edges.forEach(function (e) { e.classList.remove('active'); });
  }
  nodes.forEach(function (node) {
    node.addEventListener('mouseenter', function () {
      clear();
      var id = node.getAttribute('data-id');
      node.classList.add('active');
      edges.forEach(function (edge) {
        if (edge.getAttribute('data-from') === id || edge.getAttribute('data-to') === id) {
          edge.classList.add('active');
        }
      });
    });
    node.addEventListener('mouseleave', clear);
  });
})();
"""


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _page(title: str, content: str, root_rel: str = "", active: str = "") -> str:
    def nav_item(label: str, href: str, key: str) -> str:
        css = " class=\"active\"" if key == active else ""
        return f'<a href="{root_rel}{href}"{css}>{esc(label)}</a>'

    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(title)} · specd</title>\n"
        f'<link rel="stylesheet" href="{root_rel}style.css">\n'
        "</head>\n<body>\n"
        '<header class="topbar">\n'
        f'<a class="brand" href="{root_rel}index.html">spec<span>d</span></a>\n'
        "<nav>"
        + nav_item("Overview", "index.html", "overview")
        + nav_item("Graph", "graph.html", "graph")
        + nav_item("Trace", "trace.html", "trace")
        + nav_item("Proposals", "proposals.html", "proposals")
        + "</nav>\n</header>\n"
        f'<main class="page">{content}</main>\n'
        '<footer class="footer">Generated by specd. The Markdown files are the source of truth; '
        "this site is a projection. Rebuild with <code>specd build</code>.</footer>\n"
        f'<script src="{root_rel}app.js"></script>\n'
        "</body>\n</html>\n"
    )


def _badges(summary: dict[str, Any]) -> str:
    status = str(summary.get("status", "draft"))
    kind = str(summary.get("kind", ""))
    return (
        '<div class="badges">'
        f'<span class="badge kind">{esc(kind)}</span>'
        f'<span class="badge {esc(STATUS_CLASS.get(status, ""))}">{esc(status)}</span>'
        f'<span class="badge version">v{esc(summary.get("version", "0.0.0"))}</span>'
        "</div>"
    )


def _spec_card(summary: dict[str, Any], root_rel: str = "") -> str:
    search = " ".join(
        [
            str(summary.get("id", "")),
            str(summary.get("title", "")),
            str(summary.get("summary", "")),
            str(summary.get("kind", "")),
            str(summary.get("owner", "")),
            " ".join(summary.get("tags", []) or []),
        ]
    )
    return (
        f'<a class="spec-card" data-search="{esc(search)}" href="{root_rel}spec/{esc(summary["id"])}.html">'
        f'<div class="id">{esc(summary["id"])}</div>'
        f'<h3>{esc(summary["title"])}</h3>'
        f'<div class="desc">{esc(summary.get("summary") or "No summary yet.")}</div>'
        f"{_badges(summary)}"
        f'<div class="foot"><span>{esc(summary.get("owner") or "unowned")}</span>'
        f'<span>{summary.get("requirement_count", 0)} req · {summary.get("open_questions", 0)} open</span></div>'
        "</a>"
    )


def _dashboard(index: dict[str, Any], trace: dict[str, Any] | None) -> str:
    stats = index.get("stats", {})
    specs = index.get("specs", {})
    proposals = index.get("proposals", [])
    broken = index.get("broken_links", [])
    duplicates = index.get("duplicates", [])
    errors = index.get("errors", [])
    orphans = stats.get("orphans", [])

    parts = [
        "<h1>Spec graph</h1>",
        '<p class="subtitle">Every spec is a node. Every link is an edge. '
        "The Markdown files are the source of truth; this page is one projection of them.</p>",
        '<div class="cards">',
        f'<div class="card"><div class="num">{stats.get("specs", 0)}</div><div class="label">specs</div></div>',
        f'<div class="card"><div class="num">{stats.get("requirements", 0)}</div><div class="label">requirements</div></div>',
        f'<div class="card"><div class="num">{stats.get("open_questions", 0)}</div><div class="label">open questions</div></div>',
        f'<div class="card"><div class="num">{len(proposals)}</div><div class="label">open proposals</div></div>',
        f'<div class="card"><div class="num">{len(broken)}</div><div class="label">broken links</div></div>',
        "</div>",
    ]

    if trace:
        coverage = int(round(float(trace.get("coverage", 0)) * 100))
        parts.extend(
            [
                f"<h2>Requirement coverage</h2>",
                f'<div class="progress"><span style="width:{coverage}%"></span></div>',
                f'<p class="subtitle">{trace.get("covered", 0)} of {trace.get("requirements", 0)} requirements are referenced '
                f"by a source, test or config file ({coverage}%).</p>",
            ]
        )

    issues: list[str] = []
    for edge in broken:
        issues.append(f'<li>Broken link: <code>{esc(edge.get("from"))}</code> → <code>{esc(edge.get("to"))}</code> ({esc(edge.get("rel"))})</li>')
    for spec_id in orphans:
        issues.append(f'<li>Orphan: <a href="spec/{esc(spec_id)}.html"><code>{esc(spec_id)}</code></a> has no incoming links</li>')
    for spec_id in duplicates:
        issues.append(f'<li>Duplicate spec id: <code>{esc(spec_id)}</code></li>')
    for error in errors:
        issues.append(f"<li>Parse error: {esc(error)}</li>")
    if issues:
        parts.append('<div class="panel warn"><h3>Needs attention</h3><ul>' + "".join(issues) + "</ul></div>")

    parts.append("<h2>Specs</h2>")
    parts.append('<div class="toolbar"><input id="filter" type="search" placeholder="Filter by id, kind, owner, tag…"></div>')
    parts.append('<div class="grid">')
    for summary in sorted(specs.values(), key=lambda item: (item.get("kind", ""), item.get("id", ""))):
        parts.append(_spec_card(summary))
    parts.append("</div>")

    if proposals:
        parts.append("<h2>Open proposals</h2>")
        parts.append('<div class="panel"><ul>')
        for proposal in proposals:
            target = proposal.get("target", "")
            parts.append(
                f'<li><code>{esc(proposal.get("id"))}</code> — {esc(proposal.get("summary"))} '
                f'(<a href="spec/{esc(target)}.html">{esc(target)}</a>, bump: {esc(proposal.get("bump"))})</li>'
            )
        parts.append("</ul></div>")

    return "\n".join(parts)


def _spec_page(
    spec: Any,
    summary: dict[str, Any],
    incoming: list[dict[str, str]],
    specs: dict[str, Any],
    root_rel: str,
    root: Path,
) -> str:
    body = md.render(spec.body)
    links = summary.get("links", [])
    link_items = []
    for link in links:
        target = link["target"]
        if target in specs:
            link_items.append(
                f'<li><span class="rel">{esc(link["rel"])}</span><br><a href="{root_rel}spec/{esc(target)}.html">{esc(target)}</a></li>'
            )
        else:
            link_items.append(f'<li><span class="rel">{esc(link["rel"])}</span><br><code>{esc(target)}</code></li>')
    incoming_items = [
        f'<li><span class="rel">{esc(item["rel"])}</span><br>'
        f'<a href="{root_rel}spec/{esc(item["from"])}.html">{esc(item["from"])}</a></li>'
        for item in incoming
    ]

    meta = spec.meta
    rows = [
        ("Owner", esc(meta.get("owner", "—"))),
        ("Domain", esc(meta.get("domain", "—"))),
        ("Level", esc(meta.get("level", "—"))),
        ("Updated", esc(meta.get("updated", "—"))),
        ("Approved by", esc(meta.get("approved_by", "—"))),
        ("File", f"<code>{esc(relpath(spec.path, root))}</code>"),
    ]
    if spec.kind == "contract":
        rows.append(("Schema", f"<code>{esc(meta.get('path', '—'))}</code>"))
        rows.append(("Contract type", esc(meta.get("type", "—"))))

    meta_html = "".join(f'<div><div class="k">{key}</div><div class="v">{value}</div></div>' for key, value in rows)

    requirement_rows = []
    for requirement in spec.requirements:
        anchor = md.slugify(f"{requirement.id} {requirement.title}")
        acceptance = "yes" if requirement.has_acceptance else "<span style=\"color:#b45309\">missing</span>"
        requirement_rows.append(
            f'<tr><td><a href="#{anchor}"><code>{esc(requirement.id)}</code></a></td>'
            f"<td>{esc(requirement.title)}</td><td>{esc(requirement.priority)}</td>"
            f"<td>{acceptance}</td><td>{len(requirement.traces)}</td></tr>"
        )
    if requirement_rows:
        requirements_html = (
            '<div class="table-wrap"><table><thead><tr><th>ID</th><th>Requirement</th>'
            "<th>Priority</th><th>Given/When/Then</th><th>Traces</th></tr></thead><tbody>"
            + "".join(requirement_rows)
            + "</tbody></table></div>"
        )
    else:
        requirements_html = '<p class="empty">No requirements yet. Add <code>### REQ-XXX-001 …</code> sections.</p>'

    questions = "".join(f"<li>{esc(question)}</li>" for question in spec.open_questions)
    questions_html = (
        f'<div class="panel warn"><h3>Open questions ({len(spec.open_questions)})</h3><ul>{questions}</ul></div>'
        if spec.open_questions
        else ""
    )

    pending = ""
    if spec.status != "approved":
        pending = (
            '<div class="panel warn"><strong>Pending.</strong> This spec is not approved. '
            "Agents must treat it as a proposal, not as truth.</div>"
        )

    sidebar_links = "".join(link_items) or '<li class="rel">No outgoing links.</li>'
    sidebar_incoming = "".join(incoming_items) or '<li class="rel">No incoming links.</li>'

    content = f"""
<div class="layout">
  <div>
    <p class="subtitle"><a href="{root_rel}index.html">Overview</a> / {esc(spec.kind)} / {esc(spec.id)}</p>
    <h1>{esc(spec.title)}</h1>
    <div class="badges">{_badges(summary)}</div>
    {pending}
    <div class="meta">{meta_html}</div>
    {questions_html}
    <h2>Requirements</h2>
    {requirements_html}
    <h2>Specification</h2>
    <article>{body}</article>
  </div>
  <aside class="sidebar">
    <div class="panel"><h4>Identity</h4>
      <div class="k">id</div><div class="v"><code>{esc(spec.id)}</code></div>
      <div class="k" style="margin-top:8px">version</div><div class="v"><code>{esc(spec.version)}</code></div>
      <div class="k" style="margin-top:8px">status</div><div class="v">{esc(spec.status)}</div>
    </div>
    <div class="panel"><h4>Outgoing links</h4><ul>{sidebar_links}</ul></div>
    <div class="panel"><h4>Incoming links</h4><ul>{sidebar_incoming}</ul></div>
    <div class="panel"><h4>Agent context</h4>
      <p class="rel">Pack a bounded context for an agent:</p>
      <pre><code>specd context {esc(spec.id)} \\\n  --task "your task"</code></pre>
    </div>
  </aside>
</div>
"""
    return _page(spec.title, content, root_rel=root_rel, active="overview")


def _graph(index: dict[str, Any], specs: dict[str, Any]) -> str:
    summaries = index.get("specs", {})
    if not summaries:
        return _page("Graph", '<h1>Graph</h1><p class="empty">No specs yet.</p>', active="graph")

    layers: dict[int, list[str]] = defaultdict(list)
    for spec_id, summary in summaries.items():
        layers[LEVEL.get(str(summary.get("kind", "")), 3)].append(spec_id)
    for layer in layers.values():
        layer.sort()

    node_w, node_h, gap = 190, 58, 22
    max_count = max(len(items) for items in layers.values())
    width = max(1100, max_count * (node_w + gap) + 80)
    height = (max(layers) + 1) * 150 + 60
    positions: dict[str, tuple[float, float]] = {}
    for level, items in sorted(layers.items()):
        row_width = len(items) * (node_w + gap) - gap
        start = (width - row_width) / 2
        for index_in_row, spec_id in enumerate(items):
            positions[spec_id] = (start + index_in_row * (node_w + gap), 40 + level * 150)

    edges = []
    for edge in index.get("edges", []):
        source, target = edge.get("from"), edge.get("to")
        if source not in positions or target not in positions:
            continue
        x1, y1 = positions[source]
        x2, y2 = positions[target]
        sx, sy = x1 + node_w / 2, y1 + node_h
        tx, ty = x2 + node_w / 2, y2
        if abs(y1 - y2) < 10:
            sy, ty = y1 + node_h / 2, y2 + node_h / 2
            path = f"M {sx} {sy} C {sx + 60} {sy - 40}, {tx - 60} {ty - 40}, {tx} {ty}"
        else:
            mid = (sy + ty) / 2
            path = f"M {sx} {sy} C {sx} {mid}, {tx} {mid}, {tx} {ty}"
        color = REL_COLORS.get(str(edge.get("rel")), "#94a3b8")
        edges.append(
            f'<path class="edge" data-from="{esc(source)}" data-to="{esc(target)}" '
            f'd="{path}" stroke="{color}" marker-end="url(#arrow-{esc(edge.get("rel"))})" />'
        )

    markers = []
    for rel, color in REL_COLORS.items():
        markers.append(
            f'<marker id="arrow-{esc(rel)}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}" /></marker>'
        )

    node_svg = []
    for spec_id, (x, y) in positions.items():
        summary = summaries[spec_id]
        kind = str(summary.get("kind", ""))
        color = REL_COLORS.get("implements", "#64748b") if kind == "service" else "#94a3b8"
        fill = "#ffffff"
        if kind == "system":
            fill = "#eff6ff"
        elif kind == "domain":
            fill = "#f8fafc"
        elif kind == "contract":
            fill = "#faf5ff"
        elif kind in ("nfr", "standard"):
            fill = "#fff7ed"
        node_svg.append(
            f'<a href="spec/{esc(spec_id)}.html"><g class="node" data-id="{esc(spec_id)}">'
            f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" fill="{fill}" />'
            f'<text x="{x + 12}" y="{y + 20}" font-size="12" font-weight="600">{esc(str(summary.get("title", spec_id))[:28])}</text>'
            f'<text class="node-id" x="{x + 12}" y="{y + 36}">{esc(spec_id)}</text>'
            f'<text class="node-id" x="{x + 12}" y="{y + 49}">v{esc(summary.get("version", ""))} · {esc(summary.get("status", ""))}</text>'
            "</g></a>"
        )

    legend = "".join(
        f'<span><i style="background:{color}"></i>{esc(rel)}</span>' for rel, color in REL_COLORS.items()
    )

    content = f"""
<h1>Dependency graph</h1>
<p class="subtitle">Layers follow the C4-ish levels: system → domain → service → contract/flow → cross-cutting.
Hover a node to highlight its edges. {len(summaries)} nodes, {len(edges)} edges.</p>
<div class="legend">{legend}</div>
<div class="graph-wrap">
<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="Spec dependency graph">
  <defs>{''.join(markers)}</defs>
  {''.join(edges)}
  {''.join(node_svg)}
</svg>
</div>
"""
    return _page("Graph", content, active="graph")


def _trace_page(trace: dict[str, Any] | None) -> str:
    if not trace:
        content = (
            "<h1>Traceability</h1>"
            '<p class="empty">No trace data yet. Run <code>specd trace --path src --path tests</code> '
            "and rebuild.</p>"
        )
        return _page("Trace", content, active="trace")

    coverage = int(round(float(trace.get("coverage", 0)) * 100))
    covered_rows = []
    for req_id, paths in trace.get("references", {}).items():
        if paths:
            covered_rows.append(
                f"<tr><td><code>{esc(req_id)}</code></td><td>{esc(', '.join(paths))}</td></tr>"
            )
    uncovered = trace.get("uncovered_ids", [])
    unknown = trace.get("unknown_ids", {})
    unknown_html = ""
    if unknown:
        items = "".join(f"<li><code>{esc(req_id)}</code> in {esc(', '.join(paths))}</li>" for req_id, paths in unknown.items())
        unknown_html = f'<div class="panel danger"><h3>Unknown requirement IDs in code</h3><ul>{items}</ul></div>'

    content = f"""
<h1>Traceability</h1>
<p class="subtitle">Which requirements are referenced by code, tests or config, and which exist only on paper.</p>
<div class="cards">
  <div class="card"><div class="num">{trace.get("requirements", 0)}</div><div class="label">requirements</div></div>
  <div class="card"><div class="num">{trace.get("covered", 0)}</div><div class="label">referenced</div></div>
  <div class="card"><div class="num">{trace.get("uncovered", 0)}</div><div class="label">unreferenced</div></div>
  <div class="card"><div class="num">{coverage}%</div><div class="label">coverage</div></div>
</div>
<div class="progress"><span style="width:{coverage}%"></span></div>
{unknown_html}
<h2>Referenced requirements</h2>
<div class="table-wrap"><table><thead><tr><th>Requirement</th><th>Artifacts</th></tr></thead>
<tbody>{''.join(covered_rows) or '<tr><td colspan="2">No references found.</td></tr>'}</tbody></table></div>
<h2>Unreferenced requirements</h2>
<div class="panel"><p>{', '.join(f'<code>{esc(item)}</code>' for item in uncovered) or 'None. Every requirement has a trace.'}</p></div>
"""
    return _page("Trace", content, active="trace")


def _proposals_page(index: dict[str, Any]) -> str:
    proposals = index.get("proposals", [])
    if not proposals:
        content = (
            "<h1>Proposals</h1>"
            '<p class="empty">No open proposals. Agents write to <code>changes/</code>; '
            "a human releases them with <code>specd release</code>.</p>"
        )
        return _page("Proposals", content, active="proposals")

    rows = "".join(
        f"<tr><td><code>{esc(item.get('id'))}</code></td>"
        f"<td>{esc(item.get('summary'))}</td>"
        f"<td><a href=\"spec/{esc(item.get('target'))}.html\">{esc(item.get('target'))}</a></td>"
        f"<td>{esc(item.get('bump'))}</td><td>{esc(item.get('status'))}</td>"
        f"<td>{esc(item.get('author'))}</td></tr>"
        for item in proposals
    )
    content = f"""
<h1>Proposals</h1>
<p class="subtitle">Published specs are read-only for agents. Changes wait here until a human releases them.</p>
<div class="table-wrap"><table><thead><tr><th>ID</th><th>Summary</th><th>Target</th><th>Bump</th><th>Status</th><th>Author</th></tr></thead>
<tbody>{rows}</tbody></table></div>
"""
    return _page("Proposals", content, active="proposals")


def build_site(root: Path, out: Path | None = None) -> Path:
    root = Path(root).resolve()
    out = Path(out or (root / "dist")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "spec").mkdir(parents=True, exist_ok=True)

    index = build_index(root)
    specs: dict[str, Any] = {}
    for path in iter_specs(root):
        try:
            spec = load_spec(path)
        except SpecError:
            continue
        specs.setdefault(spec.id, spec)

    trace_path = root / ".specd" / "trace.json"
    trace = None
    if trace_path.exists():
        try:
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            trace = None

    (out / "style.css").write_text(CSS, encoding="utf-8")
    (out / "app.js").write_text(APP_JS, encoding="utf-8")
    (out / "data.json").write_text(
        json.dumps({"index": index, "trace": trace}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    (out / "index.html").write_text(_page("Overview", _dashboard(index, trace), active="overview"), encoding="utf-8")
    (out / "graph.html").write_text(_graph(index, specs), encoding="utf-8")
    (out / "trace.html").write_text(_trace_page(trace), encoding="utf-8")
    (out / "proposals.html").write_text(_proposals_page(index), encoding="utf-8")

    for spec_id, spec in specs.items():
        summary = index["specs"].get(spec_id, spec.to_summary(root))
        incoming = index.get("incoming", {}).get(spec_id, [])
        page = _spec_page(spec, summary, incoming, specs, root_rel="../", root=root)
        (out / "spec" / f"{spec_id}.html").write_text(page, encoding="utf-8")

    return out
