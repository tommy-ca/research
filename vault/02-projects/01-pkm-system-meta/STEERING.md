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

## Priorities (Current - Post TDD Cycle 1.4)
1. **REFACTOR Phase Completion**: Achieve 95%+ test pass rate (currently 90.7%)
   - Resolve 11 critical test failures in enhanced capture workflow
   - Performance optimization for <80ms end-to-end processing
   - Documentation sprint for Mastra AI integration

2. **TDD Cycle 1.5 Preparation**: Advanced Analytics Integration
   - Semantic analysis engine with AI-driven content understanding
   - Predictive workflow recommendations and optimization
   - Enhanced Mastra AI agent coordination and communication

3. **Legacy Command Integration**: Bridging enhanced workflow with existing commands
   - `/pkm-search` integration with semantic knowledge graph
   - `/pkm-get` enhancement with predictive metadata
   - `/pkm-links` upgrade with AI-driven relationship mapping

4. **Production Readiness**: Enterprise-grade reliability and scalability
   - 99.9% uptime requirements with graceful degradation
   - 1000+ concurrent operations capacity
   - Advanced monitoring and observability

## Definitions of Done
- Passing tests at all levels, updated docs, telemetry enabled
- Reproducible behavior on sample vault

## Artifacts
- Specs: `specifications/`
- Planning: `planning/`
- Tasks: `implementation/tasks/`
- Metrics: `metrics/`

