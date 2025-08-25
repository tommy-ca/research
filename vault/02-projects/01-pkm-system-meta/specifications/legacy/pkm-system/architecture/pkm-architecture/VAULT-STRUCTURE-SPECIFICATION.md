# PKM Vault Structure Specification

## Overview

This document defines the comprehensive vault structure for the Personal Knowledge Management system, incorporating PKM best practices, cognitive science principles, and modern storage technologies including S3, Lance, and Parquet formats.

## Core Principles

### Organizational Philosophy
1. **Progressive Disclosure**: Simple at entry, sophisticated at depth
2. **Contextual Proximity**: Related information stays together
3. **Temporal Awareness**: Time-based organization where relevant
4. **Atomic Addressability**: Every piece of knowledge has a unique location
5. **Scalable Hierarchy**: Structure that grows gracefully

### Storage Strategy
- **Local Markdown**: Human-readable notes in Git
- **S3 Object Storage**: Large files and backups
- **Lance Format**: Multimedia and vector embeddings
- **Parquet Format**: Structured analytics data

## Vault Directory Structure

```
vault/
├── 00-inbox/                 # Capture zone - unsorted input
│   ├── daily/               # Daily captures
│   ├── quick/               # Quick notes
│   ├── voice/               # Voice memos
│   └── web/                 # Web clippings
│
├── 01-notes/                 # Atomic notes (Zettelkasten)
│   ├── permanent/           # Evergreen notes
│   │   ├── concepts/        # Core concepts
│   │   ├── principles/      # Fundamental principles  
│   │   ├── methods/         # Methodologies
│   │   └── insights/        # Original insights
│   ├── literature/          # Literature notes
│   │   ├── books/          # Book notes
│   │   ├── papers/         # Academic papers
│   │   ├── articles/       # Articles
│   │   └── media/          # Videos, podcasts
│   ├── reference/           # Reference notes
│   │   ├── definitions/    # Terms and definitions
│   │   ├── facts/          # Factual information
│   │   ├── quotes/         # Notable quotes
│   │   └── sources/        # Source materials
│   └── fleeting/            # Temporary notes
│       ├── thoughts/       # Random thoughts
│       ├── questions/      # Open questions
│       └── scratch/        # Working notes
│
├── 02-projects/              # Active projects (PARA)
│   ├── research/            # Research projects
│   │   └── {project-id}/
│   │       ├── README.md   # Project overview
│   │       ├── notes/      # Project notes
│   │       ├── data/       # Project data
│   │       ├── outputs/    # Deliverables
│   │       └── archive/    # Completed items
│   ├── learning/            # Learning projects
│   │   └── {course-id}/
│   │       ├── syllabus.md
│   │       ├── notes/
│   │       ├── exercises/
│   │       └── resources/
│   └── creative/            # Creative projects
│       └── {project-id}/
│           ├── ideas/
│           ├── drafts/
│           └── final/
│
├── 03-areas/                 # Life areas (PARA)
│   ├── personal/            # Personal development
│   │   ├── health/         # Health and fitness
│   │   ├── finance/        # Financial management
│   │   ├── relationships/  # Social connections
│   │   └── growth/         # Self-improvement
│   ├── professional/        # Career and work
│   │   ├── skills/         # Skill development
│   │   ├── network/        # Professional network
│   │   ├── opportunities/  # Career opportunities
│   │   └── achievements/   # Accomplishments
│   └── interests/           # Hobbies and interests
│       ├── {interest}/     # Specific interests
│       └── exploration/    # New interests
│
├── 04-resources/             # Reference materials (PARA)
│   ├── templates/           # Note templates
│   │   ├── atomic/         # Atomic note templates
│   │   ├── projects/       # Project templates
│   │   ├── daily/          # Daily note templates
│   │   └── specialized/    # Domain-specific
│   ├── checklists/          # Reusable checklists
│   ├── frameworks/          # Mental models
│   ├── tools/               # Tool documentation
│   └── references/          # External references
│
├── 05-archives/              # Inactive content (PARA)
│   ├── projects/            # Completed projects
│   ├── areas/               # Deprecated areas
│   ├── resources/           # Outdated resources
│   └── notes/               # Archived notes
│
├── 06-synthesis/             # Generated insights
│   ├── summaries/           # Progressive summaries
│   │   ├── daily/          # Daily summaries
│   │   ├── weekly/         # Weekly reviews
│   │   ├── monthly/        # Monthly summaries
│   │   └── annual/         # Year in review
│   ├── insights/            # Extracted insights
│   │   ├── connections/    # Cross-references
│   │   ├── patterns/       # Identified patterns
│   │   ├── predictions/    # Future insights
│   │   └── emergent/       # Emergent properties
│   ├── maps/                # Knowledge maps
│   │   ├── concept/        # Concept maps
│   │   ├── mind/           # Mind maps
│   │   └── journey/        # Learning journeys
│   └── teaching/            # Teaching materials
│       ├── curricula/      # Course structures
│       ├── explanations/   # ELI5 content
│       └── exercises/      # Practice materials
│
├── 07-journal/               # Time-based entries
│   ├── daily/               # Daily notes
│   │   └── {YYYY}/{MM}/    # Year/Month folders
│   ├── reflections/         # Periodic reflections
│   ├── decisions/           # Decision logs
│   └── gratitude/           # Gratitude journal
│
├── 08-media/                 # Multimedia content
│   ├── images/              # Images and diagrams
│   ├── audio/               # Audio recordings
│   ├── video/               # Video content
│   └── documents/           # PDFs, docs, etc.
│
├── 09-data/                  # Structured data
│   ├── analytics/           # Analytics data (Parquet)
│   ├── vectors/             # Embeddings (Lance)
│   ├── graphs/              # Graph data
│   └── metrics/             # Performance metrics
│
└── .pkm/                     # System metadata
    ├── config/              # Configuration files
    ├── indices/             # Search indices
    ├── cache/               # Local cache
    └── logs/                # System logs
```

## File Naming Conventions

### Atomic Notes
```
Format: {timestamp}-{title-slug}.md
Example: 20240120-153042-feynman-technique-learning.md

Components:
- timestamp: YYYYMMDD-HHMMSS
- title-slug: kebab-case title
- extension: always .md for notes
```

### Project Files
```
Format: {project-id}-{component}-{version}.{ext}
Example: prj-001-research-plan-v2.md

Components:
- project-id: unique project identifier
- component: descriptive component name
- version: version number
- extension: appropriate file type
```

### Daily Notes
```
Format: {YYYY-MM-DD}.md
Example: 2024-01-20.md
Location: vault/07-journal/daily/2024/01/
```

## Storage Layer Architecture

### Local Storage (Git)
```yaml
local_storage:
  primary_content:
    - markdown_notes
    - text_files
    - small_images (<1MB)
    - configuration
  
  characteristics:
    versioning: git
    sync: automatic
    backup: continuous
    access: immediate
```

### S3 Object Storage
```yaml
s3_storage:
  bucket_structure:
    pkm-vault-{user-id}/
    ├── media/              # Large media files
    │   ├── images/
    │   ├── audio/
    │   └── video/
    ├── backups/            # Vault backups
    │   ├── daily/
    │   ├── weekly/
    │   └── monthly/
    ├── exports/            # Generated exports
    └── archives/           # Long-term storage
  
  configuration:
    region: us-east-1
    storage_class: INTELLIGENT_TIERING
    encryption: AES-256
    versioning: enabled
    lifecycle:
      transition_to_glacier: 90_days
      expiration: never
  
  access_patterns:
    upload: multipart_for_large_files
    download: presigned_urls
    cache: cloudfront_cdn
```

### Lance Format Storage
```yaml
lance_storage:
  use_cases:
    - vector_embeddings
    - image_embeddings
    - audio_features
    - video_analytics
  
  schema:
    embeddings_table:
      - note_id: string
      - embedding: vector[768]
      - model: string
      - timestamp: timestamp
      - metadata: json
    
    media_features:
      - media_id: string
      - features: vector[2048]
      - media_type: string
      - extracted_at: timestamp
  
  location: s3://pkm-vault-{user-id}/vectors/
  
  benefits:
    - columnar_format
    - efficient_vector_ops
    - streaming_updates
    - version_control
```

### Parquet Analytics Storage
```yaml
parquet_storage:
  use_cases:
    - note_metrics
    - usage_analytics
    - knowledge_graph_data
    - search_indices
  
  tables:
    note_metrics:
      schema:
        - note_id: string
        - created_at: timestamp
        - modified_at: timestamp
        - word_count: int
        - link_count: int
        - complexity_score: float
        - quality_score: float
      partitioning: by_month
    
    user_analytics:
      schema:
        - timestamp: timestamp
        - action: string
        - note_id: string
        - duration_ms: int
        - metadata: json
      partitioning: by_day
    
    knowledge_graph:
      schema:
        - source_id: string
        - target_id: string
        - relationship_type: string
        - strength: float
        - created_at: timestamp
      partitioning: by_relationship_type
  
  location: s3://pkm-vault-{user-id}/analytics/
  
  optimization:
    compression: snappy
    row_group_size: 100MB
    column_encoding: dictionary
```

## Metadata Standards

### Note Frontmatter
```yaml
---
id: uuid-v4
created: 2024-01-20T15:30:42Z
modified: 2024-01-20T16:45:00Z
type: concept|project|area|resource|daily|synthesis
status: fleeting|developing|evergreen|archived
tags: 
  - primary-tag
  - secondary-tag
aliases:
  - alternative-name
sources:
  - title: Source Title
    url: https://example.com
    author: Author Name
    date: 2024-01-20
related:
  - [[20240119-related-note]]
  - [[20240118-another-note]]
location: vault/01-notes/permanent/concepts/
storage:
  media: s3://pkm-vault/media/
  vectors: lance://embeddings/note-id
  analytics: parquet://metrics/2024/01/
feynman:
  level: 3
  eli5: true
  gaps: []
quality:
  completeness: 0.85
  clarity: 0.92
  atomicity: true
---
```

### Directory Metadata
```yaml
# .pkm/directory.yaml
directory: vault/02-projects/research/
metadata:
  created: 2024-01-20
  owner: user-id
  description: Research projects
  access: private
  backup: daily
  storage:
    primary: local
    secondary: s3
    analytics: parquet
  rules:
    naming: {project-id}-{component}
    required_files: [README.md]
    max_depth: 4
```

## Access Patterns

### Read Patterns
```yaml
read_access:
  hot_data:
    storage: local_cache
    latency: <10ms
    examples: [current_notes, recent_edits]
  
  warm_data:
    storage: local_vault
    latency: <100ms
    examples: [project_notes, references]
  
  cool_data:
    storage: s3_standard
    latency: <1s
    examples: [media_files, old_projects]
  
  cold_data:
    storage: s3_glacier
    latency: hours
    examples: [archives, backups]
```

### Write Patterns
```yaml
write_access:
  immediate:
    target: local_vault
    sync: git_commit
    backup: async_s3
  
  batch:
    target: staging_area
    process: batch_processor
    commit: scheduled
  
  analytics:
    target: parquet_buffer
    flush: every_1000_records
    partition: by_time
```

## Sync and Backup Strategy

### Sync Rules
```yaml
sync_strategy:
  local_to_git:
    frequency: on_save
    method: auto_commit
    message: "Auto: {action} {file}"
  
  git_to_remote:
    frequency: every_15_min
    method: push
    branches: [main, develop]
  
  local_to_s3:
    frequency: hourly
    method: incremental
    compression: gzip
  
  vectors_to_lance:
    frequency: on_processing
    method: append
    batch_size: 100
  
  analytics_to_parquet:
    frequency: daily
    method: partition_write
    optimization: compact
```

### Backup Policy
```yaml
backup_policy:
  levels:
    continuous:
      target: git
      retention: forever
    
    hourly:
      target: local_snapshots
      retention: 24_hours
    
    daily:
      target: s3_standard
      retention: 30_days
    
    weekly:
      target: s3_standard_ia
      retention: 12_weeks
    
    monthly:
      target: s3_glacier
      retention: 7_years
  
  recovery:
    rto: 1_hour
    rpo: 15_minutes
```

## Migration Paths

### Import Sources
```yaml
import_from:
  obsidian:
    preserve: [vault_structure, wikilinks, tags]
    transform: [frontmatter, attachments]
    storage: automatic_routing
  
  roam:
    preserve: [daily_notes, block_refs]
    transform: [json_to_md, attributes]
    storage: atomic_splitting
  
  notion:
    preserve: [databases, relations]
    transform: [blocks_to_md, properties]
    storage: hierarchical_placement
  
  evernote:
    preserve: [notebooks, tags]
    transform: [enex_to_md, attachments]
    storage: media_extraction
```

### Export Formats
```yaml
export_to:
  static_site:
    format: [hugo, mkdocs, gatsby]
    storage: s3_hosting
  
  backup:
    format: [tar.gz, zip]
    storage: s3_glacier
  
  analytics:
    format: parquet
    storage: s3_analytics
  
  vectors:
    format: lance
    storage: s3_vectors
```

## Performance Considerations

### Optimization Strategies
```yaml
optimization:
  indexing:
    local: sqlite_fts5
    remote: elasticsearch
    vectors: lance_indices
    analytics: parquet_statistics
  
  caching:
    hot_notes: memory_cache
    recent_media: disk_cache
    embeddings: vector_cache
    analytics: query_cache
  
  compression:
    text: lz4
    media: format_specific
    vectors: none
    analytics: snappy
  
  partitioning:
    notes: by_type_and_date
    media: by_type_and_size
    vectors: by_model
    analytics: by_time_window
```

## Security and Privacy

### Access Control
```yaml
access_control:
  levels:
    public: [templates, frameworks]
    shared: [project_outputs, teaching]
    private: [personal, journal]
    encrypted: [sensitive, financial]
  
  encryption:
    at_rest:
      local: optional
      s3: AES-256
      lance: AES-256
      parquet: AES-256
    
    in_transit:
      all: TLS_1.3
  
  authentication:
    local: system_user
    s3: IAM_roles
    api: JWT_tokens
```

### Data Governance
```yaml
governance:
  compliance:
    gdpr: enabled
    ccpa: enabled
    hipaa: optional
  
  retention:
    notes: indefinite
    media: 7_years
    analytics: 2_years
    logs: 90_days
  
  deletion:
    soft_delete: 30_days
    hard_delete: manual
    cascade: careful
```

## Monitoring and Metrics

### Vault Metrics
```yaml
metrics:
  storage:
    total_notes: count
    vault_size: GB
    media_size: GB
    vector_count: millions
  
  activity:
    daily_notes_created: count
    weekly_active_folders: count
    monthly_growth_rate: percentage
  
  quality:
    average_note_length: words
    link_density: links_per_note
    orphan_rate: percentage
    evergreen_ratio: percentage
  
  performance:
    search_latency: ms
    write_latency: ms
    sync_lag: seconds
    backup_status: success_rate
```

## Implementation Checklist

### Phase 1: Local Structure
- [ ] Create directory structure
- [ ] Implement naming conventions
- [ ] Set up Git integration
- [ ] Create template system

### Phase 2: S3 Integration
- [ ] Configure S3 buckets
- [ ] Implement upload/download
- [ ] Set up lifecycle rules
- [ ] Enable versioning

### Phase 3: Lance Integration
- [ ] Design vector schemas
- [ ] Implement embedding storage
- [ ] Create query interface
- [ ] Set up indexing

### Phase 4: Parquet Analytics
- [ ] Design analytics schemas
- [ ] Implement data collection
- [ ] Create partitioning strategy
- [ ] Build query layer

### Phase 5: Optimization
- [ ] Implement caching
- [ ] Optimize queries
- [ ] Tune performance
- [ ] Monitor metrics

---

*Vault Structure Specification v1.0 - A scalable, intelligent knowledge organization system*