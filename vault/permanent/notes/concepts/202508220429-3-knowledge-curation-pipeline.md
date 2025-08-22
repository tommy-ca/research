---
id: 202508220429
title: "3. Knowledge Curation Pipeline"
date: 2025-08-22
type: atomic
source: knowledge-management-workflows.md
extraction_method: header_split
created: 2025-08-22T04:29:54.171841
---

# 3. Knowledge Curation Pipeline

```mermaid
graph TD
    A[Knowledge Entry] --> B[/kc-validate]
    B --> C{Accuracy Check}
    C -->|Issues| D[/kc-enrich]
    C -->|Valid| E[Quality Score]
    D --> F[Source Addition]
    F --> G[Context Enhancement]
    G --> E
    E --> H[/kc-merge]
    H --> I[Deduplicated KB]
```

## Connections
- Related concepts: [[to-be-linked]]
