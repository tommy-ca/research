# PKM Workflow Reorg Plan

## Objectives
- Consolidate PKM workflows under a consistent, minimal command set
- Remove duplicate/legacy flows and hooks
- Align folder conventions with PARA and templates

## Scope
- `.claude/hooks/` routing simplification and hardening
- Standardize command help and examples
- Normalize vault paths and templates used by commands

## Changes
1. Commands
   - Keep: `/pkm-daily`, `/pkm-capture`, `/pkm-process`, `/pkm-review`, `/pkm-zettel`, `/pkm-link`, `/pkm-search`, `/pkm-get`, `/pkm-tag`, `/pkm-organize`, `/pkm-archive`, `/pkm-index`
   - Deprecate: any overlapping legacy commands (add stubs returning deprecation message)
2. Hooks
   - Replace ad-hoc scripts with `simple-router.sh` equivalents where possible
   - Enforce dry-run default, `--apply` required for mutations
3. Vault
   - Ensure daily template in `vault/templates/daily.md`
   - Ensure permanent index `vault/permanent/INDEX.md` managed by `/pkm-index`
4. Validation
   - Add PARA validator to block invalid moves
   - Add link checker before archive operations

## Milestones
- M1: Command parity map + deprecation stubs
- M2: Hook simplification complete
- M3: PARA validator + index rebuild
- M4: Docs updated; examples validated

## Task Links
- See `../implementation/tasks/claude-commands-and-subagents.md`

## Risks & Mitigations
- Risk: Data moves cause breakage → Mitigate with dry-run and backups
- Risk: Hidden legacy usage → Emit deprecation notices with alternatives

## Acceptance
- All commands return uniform envelopes and helpful errors
- No orphan/invalid paths after organize/archive
- Index deterministic and reproducible
