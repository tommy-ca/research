---
id: 202508220429
title: "Research Integration Workflow"
date: 2025-08-22
type: atomic
source: knowledge-management-workflows.md
extraction_method: header_split
created: 2025-08-22T04:29:54.172004
---

# Research Integration Workflow

```yaml
workflow: research_to_knowledge
steps:
  1_research:
    command: "/research [topic]"
    output: "research_findings.md"
    
  2_extract:
    command: "/kb-add [findings]"
    validation: automatic
    
  3_connect:
    command: "/kg-expand [new_knowledge]"
    discover: relationships
    
  4_validate:
    command: "/kc-validate [new_entry]"
    threshold: 0.85
    
  5_enrich:
    command: "/kc-enrich [validated_entry]"
    sources: minimum_3
```

## Connections
- Related concepts: [[to-be-linked]]
