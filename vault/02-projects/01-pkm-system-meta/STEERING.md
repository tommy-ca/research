# PKM System Steering & Governance

## Purpose
Provide decision-making structure, priorities, and quality gates for the PKM system, especially Claude Code commands and subagents. Ensures consistent progress, safety, and simplicity.

## Principles
- Specs-first, TDD always, FR-first
- Small, reversible changes; defaults to dry-run
- PARA correctness > features
- Clear UX with predictable responses

## Roles
- Maintainer: accountable for scope, quality, releases
- Reviewer: validates specs/tests, enforces standards
- Implementer: delivers code to spec with passing tests

## Cadence
- Daily: capture + triage tasks
- Weekly: sprint review + planning
- Per Phase: gate review (see below)

## Gate Reviews
1. Spec Gate: acceptance criteria complete, test plan drafted
2. Implementation Gate: unit tests pass, coverage ≥ 90%
3. Integration Gate: end-to-end tests pass in sample vault
4. UX Gate: docs/examples complete, errors clear, dry-run defaults

## Change Control
- Changes require updated spec links and tests
- Backward-incompatible command changes require deprecation notice and migrations

## Priorities (Current)
1. Retrieval commands: `/pkm-search`, `/pkm-get`, `/pkm-links`
2. Capture/process reliability and PARA integrity
3. Index rebuild and link hygiene
4. Cleanup/reorg of workflows and hooks

## Definitions of Done
- Passing tests at all levels, updated docs, telemetry enabled
- Reproducible behavior on sample vault

## Artifacts
- Specs: `specifications/`
- Planning: `planning/`
- Tasks: `implementation/tasks/`
- Metrics: `metrics/`

