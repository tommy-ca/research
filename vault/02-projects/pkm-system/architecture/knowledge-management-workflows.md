# Knowledge Management Workflows

## Core Workflows

### 1. Knowledge Acquisition Workflow
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

### 2. Knowledge Graph Construction
```mermaid
graph TD
    A[Knowledge Base] --> B[/kg-build]
    B --> C[Entity Extraction]
    C --> D[Relationship Mining]
    D --> E[Weight Calculation]
    E --> F[Graph Structure]
    F --> G[/kg-cluster]
    G --> H[Pattern Detection]
    H --> I[Insight Generation]
```

### 3. Knowledge Curation Pipeline
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

## Operational Workflows

### Daily Knowledge Maintenance
1. **Morning Audit** (Automated)
   ```bash
   /kc-audit
   /kb-organize
   ```

2. **Validation Queue** (Semi-automated)
   ```bash
   /kc-validate [pending entries]
   /kc-enrich [low-quality entries]
   ```

3. **Graph Update** (On-demand)
   ```bash
   /kg-build [updated domains]
   /kg-cluster
   ```

### Research Integration Workflow
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

### Knowledge Discovery Workflow
```yaml
workflow: discover_insights
steps:
  1_map:
    command: "/kg-build [domain]"
    scope: comprehensive
    
  2_analyze:
    command: "/kg-cluster"
    method: "community_detection"
    
  3_traverse:
    command: "/kg-path [concept_a] [concept_b]"
    depth: 5
    
  4_synthesize:
    command: "/synthesize"
    input: "graph_patterns"
    
  5_document:
    command: "/kb-add [insights]"
    category: "discoveries"
```

## Automation Patterns

### Event-Driven Workflows
```yaml
triggers:
  on_research_complete:
    - /kb-add [research_output]
    - /kg-expand [new_concepts]
    
  on_low_quality_detected:
    - /kc-enrich [entry]
    - /kc-validate [enriched]
    
  on_duplicate_found:
    - /kc-merge [duplicates]
    - /kg-build [affected_domain]
    
  weekly_maintenance:
    - /kc-audit
    - /kb-organize
    - /kg-cluster
```

### Quality Gates
```yaml
quality_pipeline:
  entry_point:
    gate: "format_check"
    pass: "categorization"
    fail: "rejection"
    
  categorization:
    gate: "auto_tagging"
    pass: "validation"
    fail: "manual_review"
    
  validation:
    gate: "accuracy_check"
    threshold: 0.80
    pass: "integration"
    fail: "enrichment"
    
  enrichment:
    gate: "source_verification"
    min_sources: 2
    pass: "validation"
    fail: "research"
    
  integration:
    gate: "deduplication"
    pass: "storage"
    fail: "merge"
```

## Best Practices

### 1. Knowledge Entry Standards
- Always validate before storage
- Minimum 2 credible sources
- Clear categorization required
- Version tracking enabled
- Relationship links mandatory

### 2. Graph Maintenance
- Weekly cluster analysis
- Monthly full rebuild
- Path validation after updates
- Weight recalculation triggers
- Community detection runs

### 3. Quality Assurance
- Automated validation on entry
- Enrichment for <0.85 quality
- Duplicate checks before add
- Source verification required
- Regular audit cycles

### 4. Performance Optimization
- Batch operations when possible
- Incremental graph updates
- Cached search results
- Async validation pipeline
- Parallel enrichment tasks

## Integration Points

### With Research Agent
```bash
/research "topic" | /kb-add --auto
```

### With Synthesis Agent
```bash
/kg-cluster | /synthesize --patterns
```

### With External Systems
```yaml
export_formats:
  - JSON-LD (knowledge graph)
  - RDF (semantic web)
  - GraphML (visualization)
  - Markdown (documentation)
  - YAML (structured data)
```

## Metrics and Monitoring

### Key Performance Indicators
- Knowledge base growth rate
- Average quality score
- Graph connectivity index
- Curation cycle time
- Duplicate detection rate

### Quality Metrics
```yaml
metrics:
  coverage: "domain_completeness"
  accuracy: "fact_verification_rate"
  currency: "information_freshness"
  connectivity: "graph_link_density"
  enrichment: "context_depth_score"
```

## Troubleshooting

### Common Issues
1. **Circular References**: Use `/kg-path --detect-cycles`
2. **Quality Degradation**: Run `/kc-audit --deep`
3. **Duplicate Explosion**: Execute `/kc-merge --aggressive`
4. **Graph Fragmentation**: Apply `/kg-build --reconnect`
5. **Slow Searches**: Trigger `/kb-organize --index`