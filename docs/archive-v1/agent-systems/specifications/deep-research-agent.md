# Deep Research Agent Specification

## Overview

The Deep Research Agent is a specialized Claude Code subagent designed for comprehensive, systematic research across complex domains. It integrates with the Claude Code ecosystem to provide automated research capabilities with built-in quality control and collaborative workflows.

## Agent Definition

### Core Identity
```yaml
agent_name: "deep-research"
agent_type: "research-specialist"
version: "1.0.0"
description: "Comprehensive research agent for deep domain analysis"
specialization: "multi-domain research, source analysis, systematic investigation"
capabilities:
  - literature_review
  - data_collection
  - cross_reference_validation
  - gap_analysis
  - hypothesis_generation
  - systematic_methodology
```

### Claude Code Integration

#### Subagent Configuration
```json
{
  "subagent_type": "deep-research",
  "name": "Deep Research Specialist",
  "description": "Conducts comprehensive research with systematic methodology",
  "tools": [
    "WebSearch", "WebFetch", "Read", "Write", "Edit", "Glob", "Grep",
    "Task", "TodoWrite", "Bash"
  ],
  "specialized_capabilities": [
    "source_verification",
    "cross_reference_analysis", 
    "systematic_literature_review",
    "research_gap_identification",
    "methodology_validation"
  ],
  "quality_standards": {
    "evidence_level": "academic",
    "source_diversity": "minimum_3_independent",
    "fact_checking": "required",
    "bias_assessment": "mandatory"
  }
}
```

## Research Methodology Framework

### Phase 1: Research Planning
```yaml
planning_process:
  1. objective_clarification:
     - define_research_questions
     - establish_scope_boundaries
     - identify_success_criteria
  
  2. methodology_design:
     - select_research_approaches
     - identify_required_sources
     - plan_validation_steps
  
  3. resource_planning:
     - estimate_time_requirements
     - identify_tool_needs
     - plan_collaboration_points
```

### Phase 2: Information Gathering
```yaml
gathering_strategy:
  primary_sources:
    - academic_databases
    - government_publications
    - industry_reports
    - expert_interviews
  
  secondary_sources:
    - news_articles
    - analysis_reports
    - opinion_pieces
    - social_media_sentiment
  
  validation_sources:
    - peer_reviewed_studies
    - official_statistics
    - regulatory_filings
    - cross_cultural_perspectives
```

### Phase 3: Analysis and Synthesis
```yaml
analysis_framework:
  data_analysis:
    - quantitative_analysis
    - qualitative_coding
    - trend_identification
    - pattern_recognition
  
  synthesis_methods:
    - framework_development
    - theory_building
    - model_creation
    - insight_generation
```

## Custom Claude Code Commands

### /research-deep
**Purpose**: Initiate comprehensive deep research on specified topic

**Syntax**:
```
/research-deep <topic> [--depth=<level>] [--timeframe=<duration>] [--sources=<types>] [--output=<format>]
```

**Parameters**:
- `topic`: Research subject (required)
- `depth`: surface|moderate|deep|comprehensive (default: deep)
- `timeframe`: Research timeline in days (default: 7)
- `sources`: academic|industry|government|all (default: all)
- `output`: report|presentation|dashboard|paper (default: report)

**Example**:
```
/research-deep "artificial intelligence impact on financial markets" --depth=comprehensive --timeframe=14 --sources=academic,industry --output=report
```

**Agent Workflow**:
1. Parse research parameters and validate scope
2. Create research plan with methodology
3. Execute systematic information gathering
4. Perform cross-reference validation
5. Conduct analysis and synthesis
6. Generate comprehensive research output
7. Submit for peer review validation

### /research-validate
**Purpose**: Validate research findings through multiple sources

**Syntax**:
```
/research-validate <finding> [--sources=<count>] [--confidence=<level>]
```

**Parameters**:
- `finding`: Specific claim or finding to validate
- `sources`: Number of independent sources required (default: 3)
- `confidence`: low|medium|high|academic (default: high)

**Example**:
```
/research-validate "Central bank digital currencies will reduce commercial bank profits by 15-25%" --sources=5 --confidence=academic
```

### /research-gap
**Purpose**: Identify research gaps and opportunities

**Syntax**:
```
/research-gap <domain> [--literature-period=<years>] [--gap-type=<type>]
```

**Parameters**:
- `domain`: Research field to analyze
- `literature-period`: Years of literature to review (default: 5)
- `gap-type`: methodological|empirical|theoretical|practical (default: all)

**Example**:
```
/research-gap "cryptocurrency regulation" --literature-period=3 --gap-type=empirical
```

### /research-synthesis
**Purpose**: Synthesize findings across multiple research streams

**Syntax**:
```
/research-synthesis [--inputs=<sources>] [--framework=<type>] [--output=<format>]
```

**Parameters**:
- `inputs`: List of research files or findings
- `framework`: systematic|thematic|chronological|causal (default: systematic)
- `output`: executive-summary|full-report|framework (default: full-report)

**Example**:
```
/research-synthesis --inputs="economic-analysis.md,market-study.md,policy-review.md" --framework=causal --output=executive-summary
```

## Research Quality Standards

### Source Quality Framework
```yaml
tier_1_sources:
  - peer_reviewed_journals
  - government_statistical_agencies
  - central_bank_publications
  - international_organizations
  confidence_level: 95-100%

tier_2_sources:
  - industry_research_reports
  - think_tank_publications
  - professional_journalism
  - academic_working_papers
  confidence_level: 80-95%

tier_3_sources:
  - news_articles
  - opinion_pieces
  - blog_posts
  - social_media
  confidence_level: 60-80%

validation_requirements:
  tier_1_minimum: 2_sources
  tier_2_minimum: 3_sources
  tier_3_minimum: 5_sources
  cross_tier_validation: required
```

### Fact-Checking Protocol
```yaml
verification_steps:
  1. source_credibility_check:
     - author_expertise_validation
     - publication_reputation_assessment
     - bias_detection_analysis
  
  2. claim_substantiation:
     - primary_source_verification
     - methodology_evaluation
     - data_accuracy_check
  
  3. cross_reference_validation:
     - independent_source_confirmation
     - contradictory_evidence_assessment
     - consensus_level_evaluation
  
  4. temporal_relevance:
     - publication_date_verification
     - information_currency_check
     - update_status_confirmation
```

### Bias Mitigation Framework
```yaml
bias_types:
  selection_bias:
    detection: source_diversity_analysis
    mitigation: systematic_sampling
  
  confirmation_bias:
    detection: contradictory_evidence_search
    mitigation: devil_advocate_analysis
  
  cultural_bias:
    detection: geographic_source_distribution
    mitigation: multi_cultural_perspectives
  
  temporal_bias:
    detection: publication_date_analysis
    mitigation: historical_trend_context
```

## Collaboration Protocols

### Inter-Agent Communication
```yaml
message_types:
  research_request:
    format: |
      {
        "task_id": "unique_identifier",
        "research_topic": "specific_subject",
        "depth_required": "surface|moderate|deep|comprehensive",
        "timeline": "completion_deadline",
        "quality_standards": "evidence_requirements",
        "collaboration_points": "peer_review_stages"
      }
  
  research_update:
    format: |
      {
        "task_id": "reference_identifier", 
        "progress_percentage": "completion_status",
        "findings_summary": "key_discoveries",
        "challenges_encountered": "obstacles_faced",
        "resource_needs": "additional_requirements"
      }
  
  validation_request:
    format: |
      {
        "finding_to_validate": "specific_claim",
        "evidence_provided": "supporting_materials",
        "confidence_level": "current_assessment",
        "validation_urgency": "priority_level"
      }
```

### Human-Agent Interface
```yaml
research_brief_template:
  research_title: "Clear, descriptive title"
  primary_objectives:
    - "Specific goal 1"
    - "Specific goal 2"
  research_questions:
    - "Question requiring investigation"
  scope_definition:
    included: "Areas to cover"
    excluded: "Areas to avoid"
  quality_requirements:
    evidence_standard: "academic|industry|government"
    source_diversity: "geographic|temporal|methodological"
    peer_review: "required|optional|expedited"
  deliverables:
    - format: "report|presentation|dashboard"
    - timeline: "delivery_date"
    - audience: "target_stakeholders"
```

## Implementation Specifications

### Technical Requirements
```yaml
computational_resources:
  processing_power: "multi_core_parallel_processing"
  memory_allocation: "minimum_8gb_ram"
  storage_requirements: "100gb_research_data"
  network_bandwidth: "high_speed_web_access"

software_dependencies:
  core_libraries:
    - natural_language_processing
    - web_scraping_frameworks
    - data_analysis_tools
    - visualization_libraries
  
  external_integrations:
    - academic_database_apis
    - government_data_sources
    - news_aggregation_services
    - fact_checking_platforms
```

### Performance Metrics
```yaml
quality_metrics:
  accuracy_rate: "target_95_percent"
  source_diversity: "minimum_3_independent"
  completion_timeliness: "target_90_percent_on_time"
  peer_review_score: "minimum_4_5_out_of_5"

efficiency_metrics:
  research_throughput: "projects_per_week"
  resource_utilization: "computational_efficiency"
  collaboration_effectiveness: "inter_agent_coordination"
  human_satisfaction: "stakeholder_feedback_score"
```

### Error Handling and Recovery
```yaml
error_scenarios:
  source_unavailability:
    detection: "connection_timeout_monitoring"
    response: "alternative_source_activation"
    recovery: "cached_data_utilization"
  
  information_conflicts:
    detection: "contradiction_identification"
    response: "additional_source_consultation"
    recovery: "uncertainty_quantification"
  
  quality_standard_failures:
    detection: "automated_quality_checks"
    response: "research_methodology_revision"
    recovery: "human_expert_consultation"
```

## Training and Calibration

### Initial Training Protocol
```yaml
training_phases:
  phase_1_basic_research:
    duration: "2_weeks"
    tasks: "simple_fact_finding"
    validation: "accuracy_assessment"
  
  phase_2_complex_analysis:
    duration: "4_weeks" 
    tasks: "multi_source_synthesis"
    validation: "peer_review_simulation"
  
  phase_3_domain_specialization:
    duration: "6_weeks"
    tasks: "subject_matter_expertise"
    validation: "expert_evaluation"
```

### Continuous Learning Framework
```yaml
learning_mechanisms:
  feedback_integration:
    - peer_review_scores
    - human_expert_ratings
    - accuracy_measurements
    - efficiency_assessments
  
  methodology_refinement:
    - successful_approach_identification
    - failure_pattern_analysis
    - best_practice_extraction
    - process_optimization
  
  knowledge_updates:
    - new_source_integration
    - methodology_improvements
    - domain_knowledge_expansion
    - quality_standard_evolution
```

## Deployment and Scaling

### Deployment Strategy
```yaml
rollout_phases:
  pilot_deployment:
    scope: "single_domain_testing"
    duration: "1_month"
    metrics: "baseline_performance"
  
  limited_production:
    scope: "multi_domain_expansion"
    duration: "3_months"
    metrics: "scalability_assessment"
  
  full_deployment:
    scope: "enterprise_wide_rollout"
    duration: "ongoing"
    metrics: "comprehensive_evaluation"
```

### Scaling Considerations
```yaml
horizontal_scaling:
  multiple_agent_instances: "load_distribution"
  specialized_domain_variants: "expertise_optimization"
  geographic_distribution: "local_source_access"

vertical_scaling:
  enhanced_computational_power: "complex_analysis_capability"
  expanded_memory_allocation: "large_dataset_handling"
  advanced_ai_capabilities: "sophisticated_reasoning"
```

This specification provides the foundation for implementing a comprehensive deep research agent within the Claude Code ecosystem, with built-in quality controls, collaborative capabilities, and systematic methodology.