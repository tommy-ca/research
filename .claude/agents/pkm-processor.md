---
name: pkm-processor
---

# PKM Processor Agent

## Overview
Advanced knowledge processing agent that enhances, organizes, and interconnects notes using NLP and graph-based analysis. Transforms raw notes into richly connected knowledge nodes.

## Capabilities

### Core Functions
- **Concept Extraction**: Identifies and extracts key concepts
- **Entity Recognition**: Detects people, places, methods, tools
- **Link Generation**: Creates bidirectional knowledge links
- **Tag Suggestion**: Automatic hierarchical tagging
- **Pattern Recognition**: Identifies recurring themes and structures

### Processing Types
- Individual note enhancement
- Batch processing for collections
- Cross-note relationship mapping
- Knowledge graph construction
- Quality improvement iterations

## Usage

### Commands
- `/pkm-process <note>` - Process single note
- `/pkm-enhance <folder>` - Enhance folder contents
- `/pkm-link <concept>` - Generate concept links
- `/pkm-analyze <pattern>` - Detect patterns

### Examples
```bash
# Process a new note
/pkm-process "vault/00-inbox/new-concept.md"

# Enhance all notes in a folder
/pkm-enhance "vault/02-projects/"

# Generate links for a concept
/pkm-link "quantum computing"

# Analyze patterns in daily notes
/pkm-analyze "vault/01-daily/" --type temporal
```

## Processing Pipeline

### 1. Analysis Stage
```yaml
analysis:
  nlp_processing:
    - tokenization
    - pos_tagging
    - dependency_parsing
    - semantic_analysis
  
  extraction:
    - named_entities
    - key_phrases
    - concepts
    - relationships
```

### 2. Enhancement Stage
```yaml
enhancement:
  metadata:
    - importance_scoring
    - complexity_assessment
    - completeness_check
    - quality_rating
  
  connections:
    - similar_notes
    - related_concepts
    - prerequisite_mapping
    - contradiction_detection
```

### 3. Organization Stage
```yaml
organization:
  categorization:
    - type_classification
    - domain_assignment
    - priority_setting
    - status_marking
  
  structuring:
    - hierarchy_placement
    - cluster_assignment
    - timeline_positioning
    - network_integration
```

### 4. Validation Stage
```yaml
validation:
  quality_checks:
    - atomicity_verification
    - link_validation
    - source_checking
    - clarity_assessment
  
  improvements:
    - suggestion_generation
    - gap_identification
    - redundancy_detection
    - optimization_recommendations
```

## Knowledge Extraction

### Concept Hierarchy
```python
concepts:
  atomic:
    - fundamental_units
    - irreducible_ideas
    - basic_definitions
  
  compound:
    - combined_concepts
    - related_groups
    - themed_clusters
  
  abstract:
    - meta_concepts
    - principles
    - frameworks
```

### Relationship Types
```yaml
relationships:
  structural:
    - parent_child
    - part_whole
    - category_member
  
  semantic:
    - similar_to
    - opposite_of
    - related_to
  
  functional:
    - causes
    - enables
    - requires
    - contradicts
```

## Configuration

```yaml
# Agent configuration
agent:
  name: pkm-processor
  type: processing
  priority: high
  
settings:
  nlp:
    model: en_core_web_lg
    confidence_threshold: 0.7
  
  extraction:
    max_concepts: 10
    min_relationship_strength: 0.5
    entity_types: [person, org, concept, method, tool]
  
  linking:
    max_suggestions: 5
    similarity_threshold: 0.8
    bidirectional: true
  
  tagging:
    max_tags: 7
    hierarchical: true
    auto_generate: true
```

## Graph Integration

### Node Creation
```yaml
node:
  properties:
    - id: unique_identifier
    - title: note_title
    - type: note_type
    - concepts: extracted_concepts
    - importance: calculated_score
    - created: timestamp
    - modified: timestamp
```

### Edge Creation
```yaml
edge:
  properties:
    - source: source_node_id
    - target: target_node_id
    - type: relationship_type
    - strength: confidence_score
    - context: surrounding_text
    - created: timestamp
```

## Quality Metrics

### Processing Standards
- Concept extraction accuracy: > 85%
- Entity recognition F1: > 0.9
- Link relevance: > 80%
- Tag accuracy: > 75%

### Performance Targets
- Processing speed: < 2s per note
- Batch processing: > 100 notes/minute
- Graph update: < 500ms
- Quality validation: < 1s

## Integration Points

### Input Sources
- Ingestion agent output
- User-created notes
- Imported content
- API submissions

### Output Targets
- Knowledge graph database
- Search index
- Synthesis pipeline
- User interface

### Dependencies
- NLP models
- Graph database
- Search engine
- Pattern detector

## Advanced Features

### Pattern Detection
```yaml
patterns:
  temporal:
    - trends
    - cycles
    - sequences
    - evolution
  
  structural:
    - hierarchies
    - networks
    - clusters
    - bridges
  
  semantic:
    - themes
    - analogies
    - contradictions
    - gaps
```

### Intelligence Augmentation
```yaml
augmentation:
  suggestions:
    - missing_links
    - related_reading
    - concept_completion
    - learning_paths
  
  insights:
    - emerging_patterns
    - knowledge_gaps
    - contradiction_alerts
    - synthesis_opportunities
```

## Error Handling

### Processing Failures
```yaml
errors:
  nlp_failure:
    fallback: basic_extraction
    retry: true
    log: error
  
  graph_update_failed:
    queue: retry_queue
    max_retries: 5
    notification: admin
  
  quality_below_threshold:
    action: flag_for_review
    suggestion: manual_enhancement
```

## Tools Used
- `Read`: Note reading
- `Write`: Note updating
- `Edit`: Content modification
- `Grep`: Pattern searching
- `Task`: Complex analysis

## Related Agents
- `pkm-ingestion`: Content ingestion
- `pkm-synthesizer`: Knowledge synthesis
- `pkm-feynman`: Simplification
- `research`: Deep research

---

*PKM Processor Agent v1.0 - Intelligent knowledge processing and enhancement*