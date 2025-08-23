---
date: 2025-08-23
type: zettel
tags: [interface, ux, pkm, claude-code]
status: active
links: ["[[202408220442-dual-interface-architecture]]", "[[Claude Code Integration]]", "[[Natural Language Processing]]"]
---

# Dual Interface for PKM Systems

The dual interface approach combines traditional text editing with natural language interaction to provide flexible knowledge management workflows.

## Interface Types

### 1. Text Editing Interface
- Direct markdown file manipulation
- Syntax highlighting and preview
- Keyboard shortcuts and commands
- Git-based version control

### 2. Natural Language Interface
- Conversational commands (`/pkm-capture`, `/pkm-process`)
- AI-powered understanding of intent
- Context-aware suggestions
- Semantic search and queries

## Benefits

- **Flexibility**: Users can switch between interfaces based on task
- **Accessibility**: Natural language lowers entry barrier
- **Power**: Text editing provides fine-grained control
- **Intelligence**: AI enhances both interfaces

## Implementation in Claude Code

The PKM system leverages Claude Code's dual interface by:
- Exposing slash commands for common operations
- Maintaining markdown files as source of truth
- Using AI agents to bridge between interfaces
- Providing seamless context switching

## Related Concepts
- [[User Experience Design]]
- [[Command Line vs GUI]]
- [[AI-Augmented Interfaces]]
- [[Conversational UI Patterns]]