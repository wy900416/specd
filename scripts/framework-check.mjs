#!/usr/bin/env node
/**
 * Framework self-check for the specd seed.
 *
 * This is not the spec-validator. It is a small mechanical checker that keeps the
 * framework's own fixtures honest: front-matter, ids, links, conflicts, the
 * canonical hash boundary, and the change review artifacts.
 *
 * Usage:
 *   node scripts/framework-check.mjs
 *   node scripts/framework-check.mjs --hash <spec>
 *   node scripts/framework-check.mjs --proposal-hash <change>
 *
 * No dependencies. It intentionally checks only the rules the fixtures exercise;
 * semantic validation stays with the agent and the checklists.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const KINDS = new Set(['system', 'domain', 'service', 'contract', 'flow', 'nfr', 'adr', 'standard']);
const STAGES = new Set(['poc', 'mature']);
const POC_STATUS = new Set(['draft', 'validated', 'deprecated']);
const MATURE_STATUS = new Set(['draft', 'validated', 'approved', 'deprecated']);
const SOURCE_RE = /^(user|assumption|repo:[^\s:]+:\d+|global-skill:[a-z0-9-]+)$/;

function normalize(text) {
  return text.replace(/\r\n/g, '\n');
}

function sha256(text) {
  return crypto.createHash('sha256').update(text, 'utf8').digest('hex');
}

function filteredText(text, mode) {
  const lines = normalize(text).split('\n');
  if (lines[lines.length - 1] === '') lines.pop();
  const out = [];
  let block = false;
  let body = false;
  for (const line of lines) {
    if (mode === 'spec') {
      if (/^<!-- BEGIN VALIDATION -->\s*$/.test(line)) { block = true; continue; }
      if (/^<!-- END VALIDATION -->\s*$/.test(line)) { block = false; continue; }
      if (block) continue;
      if (/^(validated_(by|at|sha)|approved_sha):/.test(line)) continue;
    } else {
      if (/^<!-- BEGIN PROPOSED BODY -->\s*$/.test(line)) { body = true; continue; }
      if (/^<!-- END PROPOSED BODY -->\s*$/.test(line)) { body = false; continue; }
      if (!body) continue;
    }
    out.push(line);
  }
  return out.length ? out.join('\n') + '\n' : '';
}

function canonicalHash(text) {
  return sha256(filteredText(text, 'spec'));
}

function proposalHash(text) {
  return sha256(filteredText(text, 'proposal'));
}

function parseScalar(raw) {
  let value = raw.trim();
  if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }
  if (value === '[]') return [];
  if (value === '{}') return {};
  if (value === 'true') return true;
  if (value === 'false') return false;
  if (/^\[.*\]$/.test(value)) {
    return value.slice(1, -1).split(',').map((v) => v.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
  }
  return value;
}

function parseListItem(lines) {
  const first = lines[0].replace(/^\s*-\s+/, '');
  const obj = {};
  const m = /^([A-Za-z0-9_-]+):\s*(.*)$/.exec(first);
  if (!m) return parseScalar(first);
  obj[m[1]] = parseScalar(m[2]);
  for (const line of lines.slice(1)) {
    const item = /^\s*([A-Za-z0-9_-]+):\s*(.*)$/.exec(line);
    if (item) obj[item[1]] = parseScalar(item[2]);
  }
  return obj;
}

function parseYamlish(src) {
  const lines = src.split('\n');
  const fm = {};
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim() || line.trim().startsWith('#')) { i++; continue; }
    const m = /^([A-Za-z0-9_-]+):\s*(.*)$/.exec(line);
    if (!m) { i++; continue; }
    const key = m[1];
    const value = m[2].trim();
    if (value !== '') { fm[key] = parseScalar(value); i++; continue; }
    const items = [];
    let j = i + 1;
    while (j < lines.length) {
      if (/^\s*-\s+/.test(lines[j])) {
        const itemLines = [lines[j]];
        j++;
        while (j < lines.length && /^\s{2,}[A-Za-z0-9_-]+:/.test(lines[j]) && !/^\s*-\s+/.test(lines[j])) {
          itemLines.push(lines[j]);
          j++;
        }
        items.push(parseListItem(itemLines));
      } else if (/^\s+/.test(lines[j])) {
        j++;
      } else {
        break;
      }
    }
    fm[key] = items;
    i = j;
  }
  return fm;
}

function splitFrontMatter(text) {
  const normalized = normalize(text);
  const m = /^---\n([\s\S]*?)\n---(?:\n|$)/.exec(normalized);
  if (!m) return { fm: null, body: normalized };
  return { fm: parseYamlish(m[1]), body: normalized.slice(m[0].length) };
}

function sectionsOf(body) {
  const sections = {};
  let current = null;
  for (const line of normalize(body).split('\n')) {
    const m = /^##\s+(.+?)\s*$/.exec(line);
    if (m) {
      current = m[1];
      sections[current] = [];
    } else if (current !== null) {
      sections[current].push(line);
    }
  }
  return Object.fromEntries(Object.entries(sections).map(([k, v]) => [k, v.join('\n')]));
}

function validationBlock(text) {
  const lines = normalize(text).split('\n');
  const begin = lines.findIndex((l) => /^<!-- BEGIN VALIDATION -->\s*$/.test(l));
  const end = lines.findIndex((l) => /^<!-- END VALIDATION -->\s*$/.test(l));
  if (begin === -1 && end === -1) return null;
  if (begin === -1 || end === -1 || end < begin) {
    return { block: begin === -1 ? '' : lines.slice(begin + 1).join('\n'), afterEnd: '', malformed: true };
  }
  return {
    block: lines.slice(begin + 1, end).join('\n'),
    afterEnd: lines.slice(end + 1).join('\n'),
    malformed: false,
  };
}

function hasDataRow(section) {
  if (!section) return false;
  const rows = section.split('\n').filter((line) => /^\s*\|/.test(line));
  return rows.slice(2).some((line) => line.replace(/[|:\-\s]/g, '') !== '');
}

function parseRequirements(body) {
  const lines = normalize(body).split('\n');
  const out = [];
  let current = null;
  for (const line of lines) {
    const m = /^###\s+(REQ-[A-Z0-9-]+):\s*(.+?)\s*$/.exec(line);
    if (m) {
      current = { id: m[1], title: m[2], lines: [] };
      out.push(current);
    } else if (/^##\s+/.test(line)) {
      current = null;
    } else if (current) {
      current.lines.push(line);
    }
  }
  return out;
}

function reqField(req, name) {
  const re = new RegExp(`^\\s*-\\s*\\*\\*${name}:\\*\\*\\s*(.+?)\\s*$`, 'm');
  const m = re.exec(req.lines.join('\n'));
  return m ? m[1] : '';
}

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else if (entry.isFile() && entry.name.endsWith('.md')) out.push(full);
  }
  return out;
}

function rel(file) {
  return path.relative(ROOT, file).split(path.sep).join('/');
}

function finding(level, code, file, message) {
  return { level, code, file: rel(file), message };
}

function checkSpec(file, allSpecs, findings) {
  const text = fs.readFileSync(file, 'utf8');
  const { fm, body } = splitFrontMatter(text);
  const add = (code, message) => findings.push(finding('block', code, file, message));
  if (!fm) { add('FRONT_MATTER_MISSING', 'no closed YAML front-matter'); return; }

  for (const key of ['id', 'kind', 'title', 'version', 'status', 'owner']) {
    if (!fm[key]) add('REQUIRED_FIELD', `missing ${key}`);
  }
  const id = String(fm.id || '');
  const kind = String(fm.kind || '');
  const stage = fm.stage ? String(fm.stage) : 'poc';
  const status = String(fm.status || '');
  const version = String(fm.version || '');
  const base = path.basename(file, '.md');

  if (id && id !== base) add('ID_FILENAME', `id ${id} does not match ${base}.md`);
  if (!KINDS.has(kind)) add('KIND_INVALID', `kind ${kind} is not a spec kind`);
  if (!STAGES.has(stage)) add('STAGE_INVALID', `stage ${stage} is invalid`);

  if (stage === 'poc') {
    if (version !== '0.1.0') add('POC_VERSION', `POC version is ${version}, expected 0.1.0`);
    if (!POC_STATUS.has(status)) add('STATUS_INVALID', `POC status ${status} is invalid`);
  } else {
    if (!MATURE_STATUS.has(status)) add('STATUS_INVALID', `mature status ${status} is invalid`);
    if (status === 'approved' && !/^\d+\.\d+\.\d+$/.test(version)) {
      add('APPROVED_VERSION', `approved version is ${version}`);
    }
  }

  if (status === 'approved') {
    for (const key of ['approved_by', 'approved_at', 'approved_sha']) {
      if (!fm[key]) add('APPROVED_FIELDS', `approved spec is missing ${key}`);
    }
    if (fm.validated_by || fm.validated_at || fm.validated_sha) {
      add('APPROVED_FIELDS', 'approved spec carries validated_* fields');
    }
  } else if (fm.approved_by || fm.approved_at || fm.approved_sha) {
    add('APPROVED_FIELDS', `${status} spec carries approved_* fields`);
  }
  if (status === 'validated') {
    for (const key of ['validated_by', 'validated_at', 'validated_sha']) {
      if (!fm[key]) add('VALIDATED_FIELDS', `validated spec is missing ${key}`);
    }
  }

  const sections = sectionsOf(body);
  for (const name of ['Source', 'Repo Profile', 'Context', 'Requirements', 'Assumptions', 'Agent Decisions', 'Conflicts']) {
    if (!sections[name]) add('SECTION_MISSING', `no ## ${name} section`);
  }
  if (sections['Open Questions'] && /^\s*-\s*\[\s\]\s+\S/m.test(sections['Open Questions'])) {
    add('OPEN_QUESTION', '## Open Questions has an unchecked item');
  }

  const requirements = parseRequirements(body);
  if (requirements.length === 0) add('REQ_NONE', 'no requirements');
  const seen = new Set();
  for (const req of requirements) {
    if (!/^REQ-[A-Z][A-Z0-9]*-[0-9]{3,}$/.test(req.id)) add('REQ_ID', `${req.id} is not a valid requirement id`);
    if (seen.has(req.id)) add('REQ_DUP', `${req.id} is duplicated`);
    seen.add(req.id);
    const source = reqField(req, 'Source');
    if (!source) add('REQ_SOURCE', `${req.id} has no Source`);
    else if (!SOURCE_RE.test(source)) add('REQ_SOURCE', `${req.id} has invalid Source ${source}`);
    if (reqField(req, 'Normative') === 'true') {
      for (const key of ['Given', 'When', 'Then']) {
        if (!reqField(req, key)) add('REQ_GWT', `${req.id} has no ${key}`);
      }
    }
    if (source === 'assumption' && !hasDataRow(sections.Assumptions)) {
      add('REQ_SOURCE', `${req.id} cites an assumption but ## Assumptions is empty`);
    }
  }

  if (sections.Conflicts) {
    const rows = sections.Conflicts.split('\n').filter((line) => /^\s*\|/.test(line)).slice(2);
    for (const row of rows) {
      const cells = row.split('|').map((c) => c.trim()).filter(Boolean);
      if (cells.length && /^open$/i.test(cells[cells.length - 1])) {
        add('CONFLICT_OPEN', '## Conflicts has an open resolution');
      }
    }
  }

  const links = Array.isArray(fm.links) ? fm.links : [];
  for (const link of links) {
    if (!link || typeof link !== 'object' || !link.target) continue;
    const target = String(link.target);
    if (/^https?:\/\//.test(target)) continue;
    if (!allSpecs.has(target)) add('LINK_TARGET', `link target ${target} does not exist`);
  }

  const linkTargets = links
    .filter((l) => l && typeof l === 'object' && l.target)
    .map((l) => ({ rel: l.rel, id: String(l.target), kind: allSpecs.get(String(l.target))?.fm.kind }));
  const hasEdge = (rel, kind) => linkTargets.some((l) => l.rel === rel && l.kind === kind);
  if (kind === 'domain' && !hasEdge('part-of', 'system')) {
    add('KIND_EDGE', 'domain has no part-of -> system');
  }
  if (kind === 'service') {
    const implementsDomains = linkTargets.filter((l) => l.rel === 'implements' && l.kind === 'domain');
    if (implementsDomains.length !== 1) add('KIND_EDGE', 'service must implement exactly one domain');
    if (!['exposes', 'publishes', 'consumes'].some((rel) => hasEdge(rel, 'contract'))) {
      add('KIND_EDGE', 'service has no exposes/publishes/consumes -> contract');
    }
  }
  if (kind === 'contract' && !hasEdge('part-of', 'service')) {
    add('KIND_EDGE', 'contract has no part-of -> service');
  }
  if (kind === 'flow') {
    const services = linkTargets.filter((l) => ['part-of', 'relates-to'].includes(l.rel) && l.kind === 'service');
    if (services.length < 2) add('KIND_EDGE', 'flow needs part-of/relates-to to at least two services');
  }
  if ((kind === 'standard' || kind === 'nfr') && !(Array.isArray(fm.applies_to) && fm.applies_to.length)) {
    add('KIND_EDGE', `${kind} has an empty applies_to`);
  }
  if (kind === 'adr') {
    const incoming = [...allSpecs.entries()].some(([otherId, other]) => {
      if (otherId === id) return false;
      const otherLinks = Array.isArray(other.fm.links) ? other.fm.links : [];
      return otherLinks.some((l) => l && l.rel === 'decided-by' && String(l.target) === id);
    });
    if (!incoming) add('KIND_EDGE', 'adr has no incoming decided-by link');
  }

  const hasAssumptions = hasDataRow(sections.Assumptions);
  const hasDecisions = hasDataRow(sections['Agent Decisions']);
  if ((hasAssumptions || hasDecisions) && fm.decision_mode !== 'agent-assisted') {
    add('DECISION_MODE', 'spec has inference rows but decision_mode is not agent-assisted');
  }

  const val = validationBlock(text);
  if (status === 'validated') {
    if (!val || val.malformed) {
      add('VALIDATION_MARKERS', 'validated spec has no closed validation block');
    } else {
      if (val.afterEnd.trim()) add('VALIDATION_TRAILING', 'content follows <!-- END VALIDATION -->');
      if (!/^## Validation\s*$/m.test(val.block)) add('VALIDATION_SECTION', 'block has no ## Validation heading');
      if (/^###\s+REQ-/m.test(val.block)) add('VALIDATION_CONTENT', 'validation block contains a requirement');
      if (!/^\s*-\s*Result:\s*pass\s*$/m.test(val.block)) add('VALIDATION_RESULT', 'validation Result is not pass');
      if (fm.validated_sha && fm.validated_sha !== canonicalHash(text)) {
        add('VALIDATION_HASH', 'validated_sha does not match the canonical hash');
      }
    }
  }
  if (status === 'approved') {
    if (val) add('APPROVED_VALIDATION', 'approved spec carries a validation block');
    if (fm.approved_sha && fm.approved_sha !== canonicalHash(text)) {
      add('APPROVED_HASH', 'approved_sha does not match the canonical hash');
    }
  }
}

function checkChange(file, allSpecs, findings) {
  const text = fs.readFileSync(file, 'utf8');
  const { fm, body } = splitFrontMatter(text);
  const add = (code, message) => findings.push(finding('block', code, file, message));
  if (!fm) { add('CHANGE_FRONT_MATTER', 'no closed YAML front-matter'); return; }
  for (const key of ['id', 'kind', 'title', 'target', 'base_version', 'base_sha', 'bump', 'risk', 'compatibility', 'result_status', 'status', 'owner', 'proposal_sha']) {
    if (!fm[key]) add('CHANGE_FIELDS', `change is missing ${key}`);
  }
  if (fm.kind !== 'change') add('CHANGE_KIND', `kind is ${fm.kind}, expected change`);
  if (fm.status !== 'proposed') add('CHANGE_STATUS', `status is ${fm.status}, expected proposed`);
  if (!['approved', 'deprecated'].includes(fm.result_status)) {
    add('CHANGE_RESULT_STATUS', `result_status is ${fm.result_status}`);
  }

  const target = allSpecs.get(String(fm.target || ''));
  if (!target) {
    add('CHANGE_TARGET', `target ${fm.target} does not exist`);
  } else {
    if (target.fm.stage !== 'mature' || target.fm.status !== 'approved') {
      add('CHANGE_TARGET', 'target is not a mature approved baseline');
    }
    if (String(fm.base_version) !== String(target.fm.version)) {
      add('CHANGE_BASE_VERSION', 'base_version does not match the target version');
    }
    if (String(fm.base_sha) !== String(target.fm.approved_sha)) {
      add('CHANGE_BASE_SHA', 'base_sha does not match the target approved_sha');
    }
  }

  const lines = normalize(text).split('\n');
  const begin = lines.findIndex((l) => /^<!-- BEGIN PROPOSED BODY -->\s*$/.test(l));
  const end = lines.findIndex((l) => /^<!-- END PROPOSED BODY -->\s*$/.test(l));
  if (begin === -1 || end === -1 || end < begin) {
    add('CHANGE_BODY_MARKERS', 'missing or malformed proposed-body markers');
  } else {
    if (fm.proposal_sha && fm.proposal_sha !== proposalHash(text)) {
      add('CHANGE_PROPOSAL_SHA', 'proposal_sha does not match the proposed body');
    }
    const proposedBody = lines.slice(begin + 1, end).join('\n');
    if (/^<!-- BEGIN VALIDATION -->\s*$/m.test(proposedBody) || /^## Validation\s*$/m.test(proposedBody)) {
      add('CHANGE_BODY_VALIDATION', 'proposed body carries a validation block');
    }
    if (!/^## Source\s*$/m.test(proposedBody) || !/^## Requirements\s*$/m.test(proposedBody)) {
      add('CHANGE_BODY_INCOMPLETE', 'proposed body is not the full target body');
    }
  }

  const sections = sectionsOf(body);
  if (!sections['Test Strategy']) {
    add('CHANGE_TEST_STRATEGY', 'no ## Test Strategy section');
  }
  const proposed = sections['Proposal validation'];
  if (!proposed) {
    add('CHANGE_VALIDATION_MISSING', 'no ## Proposal validation section');
  } else {
    if (!/^\s*-\s*Result:\s*pass\s*$/m.test(proposed)) {
      add('CHANGE_VALIDATION_RESULT', 'Proposal validation Result is not pass');
    }
    const baseLine = /^\s*-\s*base_sha:\s*(\S+)\s*$/m.exec(proposed);
    if (baseLine && String(fm.base_sha) !== baseLine[1]) {
      add('CHANGE_VALIDATION_BASE_SHA', 'Proposal validation base_sha does not match the CHG');
    }
    const proposalLine = /^\s*-\s*proposal_sha:\s*(\S+)\s*$/m.exec(proposed);
    if (proposalLine && String(fm.proposal_sha) !== proposalLine[1]) {
      add('CHANGE_VALIDATION_PROPOSAL_SHA', 'Proposal validation proposal_sha does not match the CHG');
    }
  }
  const review = sections.Review;
  if (!review) {
    add('CHANGE_REVIEW_MISSING', 'no ## Review section');
  } else if (!/(ready to release|recommendation:\s*ready)/i.test(review)) {
    add('CHANGE_REVIEW_RESULT', 'Review does not recommend ready to release');
  }

  const approvals = Array.isArray(fm.approvals) ? fm.approvals : [];
  for (const approval of approvals) {
    if (!approval || typeof approval !== 'object' || !approval.role || !approval.name || !approval.date || !approval.scope) {
      add('CHANGE_APPROVALS', 'approval entry is missing role, name, date, or scope');
    }
  }
}

function checkWorkspace(dir) {
  const findings = [];
  const specFiles = walk(path.join(dir, 'specs'));
  const specs = new Map();
  for (const file of specFiles) {
    const { fm } = splitFrontMatter(fs.readFileSync(file, 'utf8'));
    if (fm && fm.id) specs.set(String(fm.id), { file, fm });
  }
  for (const file of specFiles) checkSpec(file, specs, findings);
  for (const file of walk(path.join(dir, 'changes'))) checkChange(file, specs, findings);
  if (specFiles.length === 0) findings.push(finding('block', 'EMPTY_CASE', dir, 'no specs in case'));
  return findings;
}

function checkStatic(spec) {
  const findings = [];
  for (const item of spec.files) {
    const file = path.join(ROOT, item.path);
    if (!fs.existsSync(file)) {
      findings.push(finding('block', 'STATIC_FILE', file, 'file does not exist'));
      continue;
    }
    const text = fs.readFileSync(file, 'utf8');
    for (const needle of item.includes || []) {
      if (!text.includes(needle)) {
        findings.push(finding('block', 'STATIC_INCLUDES', file, `missing ${JSON.stringify(needle)}`));
      }
    }
    for (const needle of item.excludes || []) {
      if (text.includes(needle)) {
        findings.push(finding('block', 'STATIC_EXCLUDES', file, `must not contain ${JSON.stringify(needle)}`));
      }
    }
    if (item.brief) {
      const m = /`?(agents\/[a-z-]+\.md)`?/.exec(text);
      if (!m) {
        findings.push(finding('block', 'STATIC_BRIEF', file, 'no agents/*.md reference'));
      } else {
        const brief = path.join(ROOT, m[1]);
        if (!fs.existsSync(brief)) {
          findings.push(finding('block', 'STATIC_BRIEF', file, `missing ${m[1]}`));
        }
      }
    }
  }
  return findings;
}

function report(name, expect, findings, expectedCodes) {
  const blocks = findings.filter((f) => f.level === 'block');
  const codes = new Set(blocks.map((f) => f.code));
  const matched = expectedCodes ? expectedCodes.every((c) => codes.has(c)) : blocks.length > 0;
  const extra = expectedCodes ? [...codes].filter((c) => !expectedCodes.includes(c)) : [];
  const ok = expect === 'pass'
    ? blocks.length === 0
    : blocks.length > 0 && matched && extra.length === 0;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`);
  if (!ok) {
    for (const f of blocks) console.log(`  block ${f.code}: ${f.file}: ${f.message}`);
    if (expect === 'block' && expectedCodes) {
      console.log(`  expected codes: ${expectedCodes.join(', ')}`);
      if (extra.length) console.log(`  unexpected codes: ${extra.join(', ')}`);
    }
  }
  return ok;
}

const argv = process.argv.slice(2);
if (argv[0] === '--hash' && argv[1]) {
  console.log(canonicalHash(fs.readFileSync(argv[1], 'utf8')));
  process.exit(0);
}
if (argv[0] === '--proposal-hash' && argv[1]) {
  console.log(proposalHash(fs.readFileSync(argv[1], 'utf8')));
  process.exit(0);
}

const manifestFile = path.join(ROOT, 'fixtures/manifest.json');
if (!fs.existsSync(manifestFile)) {
  console.error('missing fixtures/manifest.json');
  process.exit(2);
}
const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
let failed = 0;
for (const test of manifest.cases) {
  const findings = test.type === 'static'
    ? checkStatic(test)
    : checkWorkspace(path.join(ROOT, test.dir));
  if (!report(test.name, test.expect, findings, test.codes)) failed++;
}
if (failed) {
  console.error(`\n${failed} framework case(s) failed`);
  process.exit(1);
}
console.log('\nall framework cases passed');
