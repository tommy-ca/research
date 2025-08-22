---
id: 202508220429
title: "1. Knowledge Acquisition Workflow"
date: 2025-08-22
type: atomic
source: knowledge-management-workflows.md
extraction_method: header_split
created: 2025-08-22T04:29:54.171650
---

# 1. Knowledge Acquisition Workflow

```mermaid
graph TD
    A[New Information] --> B[/kb-add]
    B --> C{Auto-Categorize}
    C --> D[Tag Generation]
    D --> E[/kc-validate]
    E --> F{Quality Check}
    F -->|Pass| G[Store in KB]
    F -->|Fail| H[Request Enrichment]
    H --> I[/kc-enrich]
    I --> E
```

## Connections
- Related concepts: [[to-be-linked]]
