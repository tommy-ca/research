# PR: Add Compound Engineering Agent and Commands

## Summary
Introduces a new `compound` agent that orchestrates compound engineering workflows (plan → execute → review → ship), plus supporting `/ce-*` commands and routing.

## Changes
- Added agent: `.claude/agents/compound-engineer.md`
- Added commands:
  - `.claude/commands/ce-plan.md`
  - `.claude/commands/ce-exec.md`
  - `.claude/commands/ce-review.md`
  - `.claude/commands/ce-pr.md`
- Updated router: `.claude/hooks/router.sh` to handle `/ce-*`
- Updated settings: `.claude/settings.json` to register `compound` agent and hooks

## Rationale
- Enable compound engineering practice directly in Claude Code
- Provide clear, minimal commands mapped to tight feedback loops
- Reuse existing research/synthesis agents via orchestration, keeping KISS

## Acceptance Criteria
- `/ce-plan "goal"` returns a 3–7 step plan with acceptance criteria
- `/ce-exec` shows step execution with checkpoints and sub-agent handoffs
- `/ce-review` critiques a target and lists fix-forward actions
- `/ce-pr` generates a concise PR summary

## Risks and Mitigations
- Scope creep → Keep commands minimal; orchestration logic lives in agent behavior
- Overlap with existing commands → Namespaced under `ce-*` to avoid collisions

## Next Steps
- Optional: add tests/docs examples for typical CE flows
- Collect feedback and refine command copy

## Review Comments

- `.claude/agents/compound-engineer.md`: Introduces a lightweight orchestrator spec that delegates domain work to existing agents (research, synthesis, PKM). Keeps orchestration principles simple (FR-first, TDD, KISS) to avoid over-engineering.
- `.claude/commands/ce-plan.md`: Intentionally minimal; focuses on producing 3–7 atomic steps and explicit acceptance criteria to enable tight loops.
- `.claude/commands/ce-exec.md`: Describes execution checkpoints and sub-agent handoffs without embedding logic in the command itself, consistent with the repo’s “commands are routing” philosophy.
- `.claude/commands/ce-review.md`: Establishes structured critique outputs (findings, severity, fixes, go/no-go) that can be applied across domains.
- `.claude/commands/ce-pr.md`: Provides a clear PR summary output to streamline shipping; complements existing research/synthesis flows.
- `.claude/hooks/router.sh`: Adds `/ce-*` patterns and help text while preserving existing behavior. Verified shell syntax with `bash -n`.
- `.claude/settings.json`: Registers a new `compound` agent and adds `/ce-*` to hooks. JSON validated with `jq`.
- `.claude/commands/SPECIFICATION.md`: Extends agent list to include `compound` and documents when to use it.
- `.claude/README.md`: Documents new CE commands in the quick start section.

Design decision: Keep all intelligence in agents; commands only route. The compound agent coordinates flows rather than duplicating research/synthesis logic, aligning with KISS and DRY.
