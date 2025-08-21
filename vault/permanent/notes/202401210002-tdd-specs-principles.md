---
id: 202401210002
title: "TDD and Specs-Driven Development Principles"
date: 2024-01-21
type: zettel
tags: [tdd, specs, development, methodology, fr-first]
links: ["[[202401210001-pkm-dogfooding]]"]
created: 2024-01-21T14:00:00Z
modified: 2024-01-21T14:00:00Z
---

# TDD and Specs-Driven Development Principles
<!-- ID: 202401210002 -->

## Core Idea
Development must follow Test-Driven Development (TDD) with specifications written first, and Functional Requirements (FRs) must always be prioritized over Non-Functional Requirements (NFRs) to deliver user value quickly.

## Context
Traditional development often leads to over-engineering, premature optimization, and building features users don't need. By combining TDD with specs-driven development and FR-first prioritization, we ensure we build the right thing (specs), build it correctly (tests), and build it quickly (FR-first).

## The Three Pillars

### 1. Test-Driven Development (TDD)
The unchangeable cycle:
- **RED**: Write a failing test that defines desired behavior
- **GREEN**: Write minimal code to make the test pass
- **REFACTOR**: Improve code quality while keeping tests green

### 2. Specs-Driven Development
Before any code:
- **Specification**: Complete requirements documentation
- **Acceptance Criteria**: Clear success definitions
- **Test Cases**: All tests defined upfront
- **Validation**: Implementation matches spec

### 3. FR-First Prioritization
Always prioritize:
- **Functional Requirements**: User-facing features that deliver value
- **Defer NFRs**: Performance, scalability, monitoring until proven necessary
- **Ship Fast**: Working features over perfect architecture
- **Iterate**: Improve based on real usage

## Why This Matters

### Quality Through Testing
- Tests define the contract
- Bugs caught immediately
- Refactoring is safe
- Documentation through tests

### Clarity Through Specs
- Requirements clear upfront
- Scope creep prevented
- Success measurable
- Communication improved

### Speed Through FR-First
- User value delivered quickly
- Over-engineering avoided
- Feedback cycles shortened
- Resources focused

## Application to PKM

In our PKM system:
1. **Every command starts with a spec** (like `/pkm-process-inbox-spec.md`)
2. **Tests written before implementation** (test files created first)
3. **Basic features ship in days** (not weeks of architecture)
4. **Optimization only when measured need** (not speculative performance)

## The Decision Framework

```
Is it user-facing? → HIGH priority → Build now
Does it enable features? → MEDIUM → Build soon  
Is it optimization? → LOW → Defer
Is it "nice to have"? → DEFER → Maybe never
```

## Common Pitfalls Avoided

- **No premature optimization**: Don't optimize until metrics prove need
- **No architecture astronauting**: Simple solutions first
- **No untested code**: Every line has test coverage
- **No scope creep**: Spec defines boundaries

## Connections
- See also: [[202401210001-pkm-dogfooding]] - Using our own system
- Contrasts with: [[traditional-waterfall]] - Big upfront design
- Builds on: [[agile-principles]] - Iterative delivery
- Leads to: [[rapid-value-delivery]] - Fast user feedback

## Evidence
Our PKM implementation demonstrates this:
- Week 1: Basic features working (FR-first)
- Week 2: Content migration (user value)
- Week 3-4: Intelligence features (enhanced value)
- Deferred: Performance optimization, monitoring, HA

## Questions
- How minimal can initial implementation be?
- When do NFRs become FRs?
- How to handle technical debt from deferral?

## Implementation Rule
**For every feature in this repository:**
1. Spec exists in `vault/1-projects/*/specs/`
2. Tests exist before implementation
3. FRs complete before any NFR work
4. User can use it within days, not weeks

---

*TDD + Specs + FR-First = Rapid delivery of correct, tested features*