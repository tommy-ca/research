# Tasks: Content Generation (Silver → Gold)

Status: [ ] todo  [~] in progress  [x] done

## Silver Services (Extraction & Retrieval)
- [ ] SIL-001: Enforce ULID/frontmatter normalization
- [ ] SIL-002: Feynman ELI5 generation for new notes
- [ ] SIL-003: Wikilink parsing + backlink suggestions
- [ ] SIL-004: Inverted/metadata index build
- [ ] SIL-005: Similarity cache with rationale
- [ ] SIL-006: `search/get/links` API with response envelope
- [ ] SIL-007: Telemetry to `vault/.pkm/metrics/retrieval.log`
- [ ] SIL-008: Benchmarks (p95 latency checks) on sample vault

## Gold Assembly (Briefs → Outlines → Drafts)
- [ ] GLD-001: Topic Brief generator (retrieval-first)
- [ ] GLD-002: Article outline assembler with evidence mapping
- [ ] GLD-003: Draft composer with citations and review prompts
- [ ] GLD-004: Course builder (syllabus → modules → lessons)
- [ ] GLD-005: Email/social pack adapters

## Templates & Structure
- [ ] TPL-001: Brief template
- [ ] TPL-002: Outline template with ELI5 checkpoints
- [ ] TPL-003: Draft template with citation blocks
- [ ] TPL-004: Course template (syllabus, module, lesson)
- [ ] TPL-005: Email/social templates

## Claude Commands (Stubs)
- [ ] CMD-101: `/content-brief "topic"`
- [ ] CMD-102: `/content-outline <brief|topic>`
- [ ] CMD-103: `/content-draft <outline>`

## Links
- Plan: `../../planning/content-generation-pipeline.md`
- Spec: `../../specifications/knowledge-extraction-and-retrieval.md`
