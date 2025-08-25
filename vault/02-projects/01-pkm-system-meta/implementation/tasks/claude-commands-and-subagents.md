# Tasks: Claude Commands & Subagents

Status key: [ ] todo  [~] in progress  [x] done

## Sprint A: Retrieval Surface
- [ ] CMD-001: Implement `/pkm-search` end-to-end (hybrid)
- [ ] CMD-002: Implement `/pkm-get` with ID/path/tag resolution
- [ ] CMD-003: Implement `/pkm-links` with suggestions and thresholds
- [ ] CMD-004: Add uniform response envelope + telemetry
  - Depends on: SAG-003, SAG-004

## Sprint B: Capture & Processing
- [ ] CMD-010: `/pkm-daily` create/open with template
- [ ] CMD-011: `/pkm-capture` with deterministic filenames
- [ ] CMD-012: `/pkm-process` dry-run/apply with rules
- [ ] CMD-013: `/pkm-tag` normalization and diff

## Sprint C: Organization
- [ ] CMD-020: `/pkm-organize` PARA validator and planner
- [ ] CMD-021: `/pkm-archive` with backlink preservation
- [ ] CMD-022: `/pkm-index` deterministic permanent index

## Subagent Foundations
- [ ] SAG-001: ingestion: metadata extraction + ULID assigner
- [ ] SAG-002: enrichment: tag normalize, template ensure
- [ ] SAG-003: indexer: content + metadata + graph index
- [ ] SAG-004: retrieval: ranked results + constraints
- [ ] SAG-005: reviewer: acceptance criteria checks + diffs

## Roadmap Markers
- R1: Retrieval MVP (CMD-001..004, SAG-003..004)
- R2: Capture/Process complete (CMD-010..013, SAG-001..002)
- R3: Org/Archive + Index (CMD-020..022, SAG-005)

## Quality & DX
- [ ] QAX-001: pytest fixtures for temp vaults
- [ ] QAX-002: latency benchmarks (p95) on sample set
- [ ] QAX-003: error taxonomy tests (E_PARAM, E_NOT_FOUND, ...)
- [ ] QAX-004: docs: examples for each command

## Links
- Spec: `../../specifications/claude-commands-and-subagents.md`
- Steering: `../../STEERING.md`
