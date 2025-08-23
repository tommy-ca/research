---
date: 2025-08-23
type: zettel
tags: [development, methodology, specifications, sdd]
status: active
links: ["[[202401210002-tdd-specs-principles]]", "[[Test-Driven Development]]", "[[FR-First Development]]"]
---

# Specification-Driven Development (SDD)

A development methodology that ensures enterprise-grade quality by creating formal specifications before implementation, establishing clear requirements and acceptance criteria upfront.

## Core Principles

1. **Specification First**: Write complete specs before code
2. **Formal Requirements**: Define functional and non-functional requirements
3. **Acceptance Criteria**: Clear, testable success conditions
4. **Validation Framework**: Built-in quality gates

## SDD Workflow

```
1. SPECIFY: Create formal specification document
2. REVIEW: Validate requirements and acceptance criteria
3. IMPLEMENT: Build according to specification
4. VALIDATE: Verify against original spec
```

## Benefits in PKM/Agent Systems

- **Clarity**: Unambiguous requirements prevent scope creep
- **Quality**: Built-in validation ensures compliance
- **Maintainability**: Specs serve as living documentation
- **Scalability**: New features follow established patterns

## Integration with TDD

SDD complements TDD by:
- Specs define the "what", tests define the "how"
- Requirements drive test creation
- Acceptance criteria become test cases
- Validation ensures both spec and test compliance

## Related Concepts
- [[Behavior-Driven Development]]
- [[Requirements Engineering]]
- [[Formal Methods]]
- [[Quality-Driven Development]]