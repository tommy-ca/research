# Knowledge Extraction & Retrieval (Silver Layer) Specification

## Purpose
Define the silver-layer contracts and quality gates for converting processed PKM content into normalized knowledge artifacts and retrieval services that feed gold-layer content generation.

## Silver Artifacts
- Atomic Note (Markdown + YAML):
  - id: ULID
  - title, date, type, tags[], links[]
  - sections: Summary, Feynman (ELI5), Evidence, Notes
- Knowledge Graph (JSONL): nodes (id, title, tags), edges (src, dst, type, weight)
- Indexes: inverted index for content/metadata, similarity cache

## Extraction Pipeline
1. Normalize: ensure frontmatter, kebab-case tags, ULID assignment
2. Enrich: auto-summary, Feynman explanation, key points
3. Link: parse wikilinks, suggest missing backlinks, compute similarities
4. Index: update content/metadata/similarity indexes
5. Validate: acceptance checks + telemetry

## Retrieval API (Local)
- `search(query, type?, tags?, limit?, format?) -> Results[]`
- `get(ident:path|ULID|#tag) -> Note`
- `links(ident, threshold=0.6, limit=20) -> Related[]`

Result fields: score, id, title, path, type, tags, snippet, rationale

## Acceptance Criteria
- Every atomic note has ULID, required fields, and Feynman
- Link graph is consistent (no missing targets) and bidirectional where appropriate
- Retrieval latency p95 < 100ms on sample vault (configurable)
- Deterministic ordering: score desc, tie → path asc
- Response envelope present with metrics and next_actions

## Telemetry
Append JSON lines to `vault/.pkm/metrics/retrieval.log` with query, latency_ms, result_count, errors.

## Testing (TDD)
- Fixtures: small sample vault with ~200 notes
- Tests:
  - Extractor normalizes and enriches (summary + ELI5 present)
  - Graph builds correct edges from wikilinks
  - Search returns ranked, stable results
  - Links returns rationale with confidence
  - Get resolves ULID/path/tag

## Interfaces to Gold Layer
- Provide provenance handles (note ids) for every brief/outline section
- Export cluster summaries as candidate section intros
- Provide ELI5 blocks for “explain like I’m new” subsections

## Non-Goals (Now)
- Embeddings/semantic search at scale (future phase)
- Multi-user collaboration features
