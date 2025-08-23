---
date: 2025-08-23
type: zettel
tags: [llm-limitations, information-architecture, content-analysis, ai-challenges]
status: active
links: ["[[202508231435-claude-code-for-information-architecture]]", "[[202508231437-agentic-tools-for-ia]]"]
---

# LLM Forest vs Trees Problem

Large Language Models excel at granular tasks but struggle with broader, holistic views - they have difficulty "seeing the forest for the trees" when dealing with large information sets.

## The Challenge

LLMs are naturally optimized for:
- Summarizing individual documents
- Drafting specific content pieces
- Translating discrete texts
- Analyzing focused chunks of information

However, they struggle with:
- Summarizing entire books or large corpora
- Understanding overarching patterns across many documents
- Maintaining context across extensive content sets
- Providing architectural-level insights

## Why This Matters for Information Architecture

Information architecture fundamentally concerns itself with:
- **The forest view**: Overall organization and structure
- **Relationships between content**: How pieces connect
- **Patterns across collections**: Emergent themes and categories
- **Holistic understanding**: The whole being greater than parts

## Current Workarounds

1. **Graph RAG**: Builds knowledge graphs but often echoes existing structure
2. **Chunking strategies**: Break large content into manageable pieces
3. **Hierarchical summarization**: Bottom-up aggregation of insights
4. **Specialized tools**: Like Claude Code that build internal representations

The limitation drives the need for specialized approaches and tools designed to work at the architectural level rather than the document level.