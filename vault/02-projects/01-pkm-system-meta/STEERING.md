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

## Priorities (Current - Post TDD Ingestion Pipeline Design)
1. **PKM Claude Code SDK Ingestion Implementation**: Core system foundation
   - Execute TDD cycle for comprehensive ingestion pipeline (FR-PKM-INGEST-001 through 004)
   - Implement model selection logic with Sonnet/Opus optimization
   - Create atomic note generation with quality validation pipeline
   - Target: 95%+ test coverage, <3s processing time, 90%+ atomicity compliance

2. **Ingestion Pipeline TDD Phases**: Systematic implementation approach
   - **Phase 1**: Foundation - Model selection + content complexity analysis (Week 1-2)
   - **Phase 2**: Core Pipeline - Content processing + atomic note generation (Week 3-4)
   - **Phase 3**: Quality & Validation - Assessment pipeline + error handling (Week 5-6)
   - **Phase 4**: Integration & Production - End-to-end testing + deployment (Week 7-8)

3. **Claude Code SDK Integration**: Subscription-first architecture
   - Leverage Claude Pro/Max subscriptions with intelligent fallbacks
   - Optimize cost efficiency with smart Sonnet/Opus selection
   - Implement graceful degradation for provider failures
   - Target: >30% cost savings, >99% uptime

4. **PKM Agent System Implementation**: Transform specifications into working code
   - Convert existing agent specifications to Claude Code SDK implementation
   - Integrate with Mastra.ai workflow orchestration
   - Establish comprehensive testing and quality gates
   - Target: Production-ready PKM ingestion by end of implementation cycle

## Definitions of Done
- Passing tests at all levels, updated docs, telemetry enabled
- Reproducible behavior on sample vault

## Artifacts
- Specs: `specifications/`
- Planning: `planning/`
- Tasks: `implementation/tasks/`
- Metrics: `metrics/`

