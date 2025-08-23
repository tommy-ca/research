---
category: 04-archives
processed_by: pkm-inbox-processor
processed_date: '2025-08-22'
---# 📥 Inbox - Capture & Triage

## Purpose
The inbox is the entry point for all new information. Everything starts here before being processed and organized into the appropriate PARA category.

## Workflow

### 1. Capture (Everything Goes Here First)
- Quick thoughts and ideas → `quick-capture/`
- Web articles and bookmarks → `web-clips/`
- Voice recordings and transcriptions → `voice-notes/`

### 2. Process (Daily/Weekly)
Use Claude Code to process inbox items:
```bash
/pkm-process inbox
```

### 3. Categorize (PARA Method)
- **Project**: Has a deadline and specific outcome → Move to `1-projects/`
- **Area**: Ongoing responsibility, no end date → Move to `2-areas/`
- **Resource**: Reference material for future → Move to `3-resources/`
- **Archive**: No longer active → Move to `4-archives/`

## Processing Checklist
- [ ] Extract key concepts
- [ ] Add metadata and tags
- [ ] Create bidirectional links
- [ ] Determine PARA category
- [ ] Move to appropriate folder
- [ ] Update index if needed

## Quick Capture Template
```markdown
---
date: {{date}}
type: capture
status: inbox
tags: []
---

# {{title}}

{{content}}

## Next Actions
- [ ] Process and categorize
- [ ] Extract key points
- [ ] Link to related notes
```

## Zero Inbox Goal
Aim to process all inbox items at least weekly. An empty inbox means all information has been properly categorized and is findable when needed.