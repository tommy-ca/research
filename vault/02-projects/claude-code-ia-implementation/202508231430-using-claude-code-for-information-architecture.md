---
author: Jorge Arango
category: 01-projects
date: 2025-08-23
links:
- '[[202508231435-claude-code-for-information-architecture]]'
- '[[202401210001-pkm-dogfooding]]'
- '[[202401210006-zettelkasten-principles]]'
- '[[202408220442-dual-interface-architecture]]'
- '[[PKM-SYSTEM-ARCHITECTURE]]'
- '[[CLAUDE-INTERFACE-SPECIFICATION]]'
processed_by: pkm-inbox-processor
processed_date: '2025-08-23'
source: https://jarango.com/2025/07/01/using-claude-code-for-information-architecture/
status: draft
tags:
- information-architecture
- claude-code
- ai-tools
- pkm
- taxonomy
- content-organization
type: capture
---

# Using Claude Code for Information Architecture

Source: https://jarango.com/2025/07/01/using-claude-code-for-information-architecture/
Author: Jorge Arango
Captured: 2025-08-23

## Key Points

Jorge Arango explores using Claude Code (an agentic coding assistant by Anthropic) for information architecture tasks, specifically for understanding and organizing large unstructured information sets.

### Main Challenge
- LLMs struggle with broader tasks (seeing the forest for the trees)
- Traditional approaches like graph RAG are expensive, time-consuming, and produce mixed results for IA use cases

### Two Primary IA Tasks
1. Understanding large unstructured information sets during early project stages
2. Producing draft taxonomies to organize large unstructured information sets

### Claude Code Approach
- Originally designed for software development
- Can ingest and index entire codebases, developing internal representation of architecture
- Key insight: **Code is just text** - what if we fed it website content instead?

### Experiment with jarango.com
- Used Jekyll site (content stored as Markdown files)
- Claude Code treated Markdown files as "software code"
- Initial ingestion was very fast (~3 minutes, 64k tokens)

### Results
1. **Initial Analysis**: Claude correctly identified the site's nature and content focus
2. **Taxonomy Generation**: Provided three categorization approaches:
   - Primary hybrid (content type + subject domain)
   - Audience-centered taxonomy
   - Content format-based taxonomy
3. **Strategic Pivot Support**: Successfully adapted taxonomies for business leader audience and AI focus

### Proposed "Business-Focused + AI Forward" Taxonomy
- Architecting Intelligence - AI/IA intersection
- Business Strategy - Strategic value of IA for leaders
- Systems Leadership - Systems thinking for executives
- Learning Insights - Books, observations, thought leadership
- Methods Frameworks - Practical tools for business application
- Reflections - Quick insights and commentary

### Advantages over Graph RAG
- Easier to use
- Faster and more efficient (cost and energy)
- Can potentially modify content/metadata (not just read)
- Better results for taxonomy generation

### Limitations and Considerations
- Scalability questions for larger sites (10x size)
- Primarily works with text files (PDFs need conversion)
- Requires backup before any modification attempts
- Results need refinement (not ready to use as-is)

### Key Takeaway
Claude Code shows promise as a powerful tool in the information architect's toolbox for "quick and dirty" operations on entire content corpora, provided content is accessible as plain text.

## Relevance to Our PKM System

This article is highly relevant to our PKM system implementation as it:
1. Demonstrates using Claude Code for content organization (core PKM function)
2. Shows practical taxonomy generation approach
3. Validates our approach of using Claude Code for PKM tasks
4. Provides insights on working with entire content corpora
5. Suggests potential enhancements for our PKM categorization workflows

## Action Items
- [ ] Experiment with using Claude Code for our vault taxonomy generation
- [ ] Consider implementing similar approach for PKM content analysis
- [ ] Explore potential for automated categorization suggestions
- [ ] Test scalability with our growing vault size
- [ ] Document learnings for PKM system enhancement