---
title: TDD Cycle 6 — Refactor & Cleanup
status: active
type: specification
date: 2025-08-22
tags: [tdd, refactor, cleanup, qa, docs]
---

# TDD Cycle 6 — Refactor & Cleanup

## Objective
Stabilize the codebase and documentation after migration and ingestion changes. Ensure module boundaries are clean, imports are correct, scripts are consistent, and tests/quality gates run green.

## Scope
- Separate maintenance tooling under `src/pkm_maintenance/` (complete) and fix any lingering references.
- Standardize scripts (shebangs, flags, output), esp. test and ingestion scripts.
- Tighten processors to meet current unit tests with minimal logic (GREEN), deferring complexity.
- Refresh docs (specs, steering, tasks) to reflect the new structure and roadmap.

## Deliverables
- All references updated to `src/pkm_maintenance/migration/*` where applicable.
- Scripts use clear CLI flags (e.g., `--gist-url`) and predictable stdout for automation.
- Unit + integration tests pass locally with clean `PYTHONPATH` and plugin isolation.
- Quality gates pass (coverage thresholds met); reports generated when pipeline runs.

## Acceptance Criteria
- [ ] No stale imports to deprecated modules
- [ ] Tests: green for unit + integration on dev machine
- [ ] Quality gates: PASS (>=80% line, >=70% branch coverage)
- [ ] Steering/Tasks/Specs updated with Cycle 6 plan and next cycles

## Test Strategy
- Run targeted unit tests for modified processors
- Run integration tests for gist ingestion
- Use `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and set `PYTHONPATH` to isolate env

## Out of Scope (to later cycles)
- CI integration and pipeline performance (Cycle 7)
- Enrichment/validation hardening (Cycle 8)
- Link graph/backlinks improvements (Cycle 9)

