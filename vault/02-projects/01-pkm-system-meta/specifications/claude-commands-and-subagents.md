# Claude Code Commands & Subagents Specification

## Overview

This specification defines the PKM command surface exposed to Claude Code and the subagent architecture that powers those commands. It ensures consistent parameters, outputs, routing, error handling, and quality gates across the PKM workflows.

## Goals
- Unified, minimal command set aligned to PARA PKM workflows
- Deterministic routing to the appropriate agent/subagent with clear contracts
- Specs-first, TDD-ready acceptance criteria for each command
- Telemetry, error taxonomy, and UX consistency across interfaces

## Command Catalog

For each command below: Interface = Claude chat; Backend = local PKM services; Mode = non-destructive by default unless `--write` is provided.

### 1) `/pkm-daily`
- Purpose: Create or open today’s daily note from template (`vault/daily/YYYY-MM-DD.md`).
- Params: `[--open] [--template daily.md]`
- Output: Path + created/opened note header with links.
- Acceptance:
  - Creates file if missing with correct frontmatter and headings
  - Idempotent: opening twice does not duplicate sections
  - Returns absolute path and next actions summary

### 2) `/pkm-capture "content"`
- Purpose: Quick capture into `vault/00-inbox/` with minimal metadata.
- Params: `content` (required), `[--source SRC] [--tags t1,t2]`
- Output: Created note path + normalized frontmatter.
- Acceptance:
  - Content is preserved verbatim; metadata normalized
  - Optional tags merged; duplicates removed; kebab-case
  - File name deterministic (timestamp + hash suffix)

### 3) `/pkm-process`
- Purpose: Process inbox items via `pkm-processor` (classification, tagging, filing).
- Params: `[--limit N] [--mode dry|apply] [--rules RULESET]`
- Output: Table of actions (moved, tagged, enriched), summary metrics.
- Acceptance:
  - Dry-run lists identical actions to apply-run
  - All moves remain within vault; PARA rules enforced
  - Failing items reported with reason codes

### 4) `/pkm-review [daily|weekly|monthly]`
- Purpose: Run review workflows and produce summaries + task deltas.
- Params: `period` (enum), `[--since YYYY-MM-DD]`
- Output: Markdown summary with links; optional checklist.
- Acceptance:
  - Period windows computed correctly; links valid
  - Actionable checklist appended

### 5) `/pkm-zettel "title" "content"`
- Purpose: Create atomic note in `vault/permanent/` with stable ID.
- Params: `title`, `content`, `[--tags ...]`
- Output: Path + generated ID + backlinks section.
- Acceptance:
  - ID is stable (ULID) and included in frontmatter
  - Content stored as-is; backlinks block present

### 6) `/pkm-link "note"`
- Purpose: Suggest/create bidirectional links for a target note.
- Params: `note` (path|ID), `[--apply] [--threshold 0.6]`
- Output: Ranked suggestions; optional applied links diff.
- Acceptance:
  - Suggestions sorted by confidence; include rationale
  - `--apply` performs minimal, readable link edits only

### 7) `/pkm-search "query"`
- Purpose: Retrieve notes by hybrid search (content + tags + metadata).
- Params: `query`, `[--type daily|permanent|resource|any] [--limit N] [--format table|json|md]`
- Output: Results with score, path, title, type, tags.
- Acceptance:
  - Deterministic ordering (score DESC, tie-break by path)
  - 95th percentile latency < 100ms on sample vault

### 8) `/pkm-get IDENT`
- Purpose: Fetch a note by path, ID, or tag.
- Params: `IDENT` (path|ULID|#tag)
- Output: Note metadata + excerpt + path.
- Acceptance:
  - ULID detection, path normalization, tag expansion
  - Returns 404-style error on miss with suggestions

### 9) `/pkm-tag "note" --tags t1,t2`
- Purpose: Add or normalize tags on a note.
- Params: `note`, `--tags list`
- Output: Before/after metadata diff.
- Acceptance:
  - Tags deduplicated, kebab-case, sorted, idempotent

### 10) `/pkm-organize`
- Purpose: Organize notes into PARA-compliant locations.
- Params: `[--dry] [--rule FILE]`
- Output: Planned moves; violations report; optional apply diff.
- Acceptance:
  - No cross-vault moves; safety checks for overwrites

### 11) `/pkm-archive`
- Purpose: Move completed items to archives with redirects.
- Params: `[--type project|area|resource] [--id ...]`
- Output: Moves + backlink maintenance summary.
- Acceptance:
  - Backlinks preserved; redirects inserted where needed

### 12) `/pkm-index`
- Purpose: Rebuild permanent notes index with sections and tags.
- Params: `[--output vault/permanent/INDEX.md]`
- Output: Path + counts by tag/topic.
- Acceptance:
  - Stable ordering; reproducible output; includes timestamp

## Agent & Subagent Architecture

### Agents
- `pkm-processor`: classification, enrichment, filing
- `pkm-synthesizer`: summaries, thematic syntheses, teaching artifacts
- `pkm-feynman`: simplification, ELI5, gap analysis
- `research`: targeted research, validation
- `knowledge`: graph navigation, simple query interface
- `compound`: planning/execution/critique loops for engineering work

### Subagents (internal roles)
- `ingestion`: normalize inputs, extract metadata, assign IDs
- `enrichment`: tagging, headings, templates, link hints
- `indexer`: build/update search indexes and graphs
- `retrieval`: search/get/links with scoring and constraints
- `reviewer`: apply acceptance criteria; generate diffs

### Routing Rules
1. Parse: match `pattern` from command frontmatter in `.claude/commands/*`
2. Resolve agent: from command’s `agent` or override via settings
3. Attach subagent pipeline per command (e.g., capture → ingestion → enrichment)
4. Execute with dry-run default, apply only on explicit flag
5. Collect telemetry and emit uniform response envelope

## Response Envelope
```json
{
  "ok": true,
  "command": "/pkm-search",
  "params": {"query": "topic"},
  "result": {"items": [...]},
  "metrics": {"latency_ms": 42},
  "logs": ["..."],
  "next_actions": ["/pkm-link <id>"]
}
```

## Error Taxonomy
- `E_PARAM`: invalid/missing parameter
- `E_NOT_FOUND`: note not found
- `E_CONFLICT`: would overwrite without `--force`
- `E_RULE_VIOLATION`: PARA/validation rule prevents action
- `E_INTERNAL`: unexpected failure (include trace id)

## Telemetry
- Record: command, params (sanitized), latency, item counts, errors
- Export sink: stdout JSON line + append to `vault/.pkm/metrics/claude-commands.log`

## Acceptance & TDD

For each command, define pytest-style tests that:
- Validate parameter parsing and error cases
- Assert response envelope structure
- Verify file system side effects in a temp vault fixture
- Measure latency on a representative sample

Example (pseudo):
```python
def test_pkm_search_returns_ranked_results(sample_vault):
    r = run_command('/pkm-search "compound engineering" --limit 5')
    assert r.ok
    assert len(r.result.items) <= 5
    assert sorted(r.result.items, key=lambda x: -x.score) == r.result.items
```

## References
- `.claude/commands/` for command frontmatter and help
- `.claude/settings.json` for routing and safety defaults
- `vault/02-projects/01-pkm-system-meta/` for broader architecture

