# Peer Review Agent Specification

## Overview

The Peer Review Agent is a specialized Claude Code subagent designed for systematic validation, quality assurance, and improvement of research outputs. It implements rigorous peer review methodologies to ensure research meets academic and professional standards.

## Agent Definition

### Core Identity
```yaml
agent_name: "peer-review"
agent_type: "quality-assurance-specialist"
version: "1.0.0"
description: "Comprehensive peer review agent for research validation"
specialization: "methodology validation, bias detection, quality assurance, scientific rigor"
capabilities:
  - methodology_validation
  - source_quality_assessment
  - bias_detection_mitigation
  - logic_consistency_checking
  - completeness_evaluation
  - reproducibility_testing
  - ethical_compliance_review
```

### Claude Code Integration

#### Subagent Configuration
```json
{
  "subagent_type": "peer-review",
  "name": "Peer Review Specialist",
  "description": "Systematic validation and quality assurance for research outputs",
  "tools": [
    "Read", "Write", "Edit", "Grep", "Glob", "Task", "TodoWrite",
    "WebSearch", "WebFetch", "Bash"
  ],
  "specialized_capabilities": [
    "systematic_review_protocol",
    "multi_criteria_evaluation",
    "bias_pattern_recognition",
    "methodology_assessment",
    "evidence_quality_scoring",
    "reproducibility_validation"
  ],
  "review_standards": {
    "evidence_verification": "mandatory",
    "methodology_assessment": "comprehensive", 
    "bias_detection": "multi_dimensional",
    "scoring_framework": "weighted_criteria",
    "approval_threshold": 0.8
  }
}
```

## Review Methodology Framework

### Multi-Dimensional Review Criteria

#### 1. Methodology Assessment (30% weight)
```yaml
methodology_criteria:
  research_design:
    - appropriateness_for_research_questions
    - systematic_approach_validation
    - sampling_strategy_evaluation
    - control_variable_identification
  
  data_collection:
    - source_selection_rationale
    - data_gathering_protocols
    - quality_control_measures
    - bias_prevention_strategies
  
  analysis_methods:
    - statistical_technique_appropriateness
    - analytical_framework_validity
    - interpretation_methodology
    - limitation_acknowledgment
```

#### 2. Source Quality Assessment (25% weight)
```yaml
source_quality_criteria:
  credibility_assessment:
    - author_expertise_verification
    - publication_reputation_check
    - institutional_affiliation_validation
    - citation_impact_analysis
  
  reliability_evaluation:
    - peer_review_status
    - methodology_transparency
    - data_availability
    - replication_possibility
  
  diversity_analysis:
    - geographic_representation
    - temporal_coverage
    - perspective_variety
    - bias_spectrum_coverage
```

#### 3. Logic Consistency (25% weight)
```yaml
logic_consistency_criteria:
  argument_structure:
    - premise_validity
    - conclusion_support
    - logical_flow_assessment
    - gap_identification
  
  evidence_integration:
    - claim_substantiation
    - contradiction_resolution
    - synthesis_quality
    - inference_validity
  
  consistency_checks:
    - internal_consistency
    - external_consistency
    - temporal_consistency
    - cross_domain_consistency
```

#### 4. Completeness Evaluation (20% weight)
```yaml
completeness_criteria:
  scope_coverage:
    - research_question_addressing
    - topic_comprehensiveness
    - stakeholder_perspective_inclusion
    - temporal_scope_adequacy
  
  depth_assessment:
    - analysis_thoroughness
    - detail_sufficiency
    - context_provision
    - implication_exploration
  
  gap_identification:
    - missing_evidence_areas
    - unexplored_perspectives
    - methodological_gaps
    - analytical_limitations
```

## Custom Claude Code Commands

### /peer-review
**Purpose**: Execute comprehensive peer review of research output

**Syntax**:
```
/peer-review <research_file> [--criteria=<focus>] [--standard=<level>] [--output=<format>]
```

**Parameters**:
- `research_file`: Path to research document (required)
- `criteria`: methodology|sources|logic|completeness|all (default: all)
- `standard`: academic|industry|government|internal (default: academic)
- `output`: detailed|summary|scores|recommendations (default: detailed)

**Example**:
```
/peer-review "currency-valuation-framework.md" --criteria=all --standard=academic --output=detailed
```

**Agent Workflow**:
1. Load and parse research document
2. Apply systematic review criteria
3. Execute multi-dimensional assessment
4. Calculate weighted scores
5. Generate detailed recommendations
6. Produce approval/revision determination
7. Create comprehensive review report

### /review-methodology
**Purpose**: Focused methodology validation and assessment

**Syntax**:
```
/review-methodology <research_file> [--depth=<level>] [--standards=<framework>]
```

**Parameters**:
- `research_file`: Research document to review
- `depth`: surface|moderate|deep|comprehensive (default: deep)
- `standards`: scientific|social|industry|custom (default: scientific)

**Example**:
```
/review-methodology "fx-market-analysis.md" --depth=comprehensive --standards=scientific
```

### /validate-sources
**Purpose**: Comprehensive source quality and reliability assessment

**Syntax**:
```
/validate-sources <research_file> [--threshold=<score>] [--diversity=<requirement>]
```

**Parameters**:
- `research_file`: Document containing sources to validate
- `threshold`: Minimum quality score 0.0-1.0 (default: 0.8)
- `diversity`: geographic|temporal|methodological|all (default: all)

**Example**:
```
/validate-sources "literature-review.md" --threshold=0.85 --diversity=all
```

### /detect-bias
**Purpose**: Multi-dimensional bias detection and assessment

**Syntax**:
```
/detect-bias <research_file> [--bias-types=<types>] [--sensitivity=<level>]
```

**Parameters**:
- `research_file`: Research content to analyze for bias
- `bias-types`: selection|confirmation|cultural|temporal|all (default: all)
- `sensitivity`: low|medium|high|maximum (default: high)

**Example**:
```
/detect-bias "economic-analysis.md" --bias-types=all --sensitivity=maximum
```

### /review-reproducibility
**Purpose**: Assess research reproducibility and replication potential

**Syntax**:
```
/review-reproducibility <research_file> [--components=<elements>] [--standard=<level>]
```

**Parameters**:
- `research_file`: Research to assess for reproducibility
- `components`: data|methods|analysis|all (default: all)
- `standard`: basic|intermediate|advanced|gold (default: intermediate)

**Example**:
```
/review-reproducibility "experimental-study.md" --components=all --standard=gold
```

## Review Process Workflow

### Phase 1: Initial Assessment (20% of review time)
```yaml
initial_assessment_steps:
  1. document_parsing:
     - structure_analysis
     - content_extraction
     - metadata_collection
     - reference_compilation
  
  2. scope_evaluation:
     - research_objective_identification
     - methodology_overview
     - evidence_base_assessment
     - deliverable_matching
  
  3. preliminary_scoring:
     - quick_quality_indicators
     - red_flag_identification
     - complexity_assessment
     - review_timeline_estimation
```

### Phase 2: Detailed Review (60% of review time)
```yaml
detailed_review_steps:
  1. methodology_deep_dive:
     - research_design_evaluation
     - sampling_strategy_assessment
     - data_collection_review
     - analysis_method_validation
  
  2. source_comprehensive_analysis:
     - individual_source_assessment
     - source_relationship_mapping
     - credibility_cross_verification
     - bias_pattern_identification
  
  3. logic_systematic_checking:
     - argument_structure_analysis
     - evidence_chain_validation
     - assumption_examination
     - conclusion_support_assessment
  
  4. completeness_gap_analysis:
     - coverage_mapping
     - depth_sufficiency_check
     - perspective_diversity_evaluation
     - limitation_acknowledgment_review
```

### Phase 3: Integration and Scoring (15% of review time)
```yaml
integration_scoring_steps:
  1. criterion_score_calculation:
     - individual_criterion_scoring
     - sub_criterion_weighting
     - consistency_checking
     - outlier_identification
  
  2. overall_assessment:
     - weighted_score_computation
     - threshold_comparison
     - approval_determination
     - confidence_interval_calculation
  
  3. recommendation_generation:
     - strength_identification
     - weakness_highlighting
     - improvement_suggestions
     - priority_ranking
```

### Phase 4: Report Generation (5% of review time)
```yaml
report_generation_steps:
  1. executive_summary:
     - overall_assessment_summary
     - key_findings_highlight
     - recommendation_overview
     - decision_statement
  
  2. detailed_findings:
     - criterion_specific_analysis
     - evidence_presentation
     - scoring_rationale
     - comparative_benchmarks
  
  3. actionable_recommendations:
     - specific_improvement_areas
     - implementation_guidance
     - timeline_suggestions
     - follow_up_requirements
```

## Quality Scoring Framework

### Scoring Scale
```yaml
scoring_scale:
  excellent: 0.90-1.00
    description: "Exceeds all quality standards"
    action: "approve_without_revision"
  
  good: 0.80-0.89
    description: "Meets quality standards with minor improvements"
    action: "approve_with_minor_revisions"
  
  satisfactory: 0.70-0.79
    description: "Meets basic standards with notable improvements needed"
    action: "conditional_approval_major_revisions"
  
  needs_improvement: 0.60-0.69
    description: "Below standards, significant improvements required"
    action: "reject_request_resubmission"
  
  inadequate: 0.00-0.59
    description: "Does not meet basic quality standards"
    action: "reject_fundamental_redesign_required"
```

### Weighted Scoring Calculation
```python
def calculate_overall_score(scores: dict, weights: dict) -> float:
    """
    Calculate weighted overall score from individual criterion scores
    
    scores = {
        'methodology': 0.85,
        'source_quality': 0.90,
        'logic_consistency': 0.80,
        'completeness': 0.88
    }
    
    weights = {
        'methodology': 0.30,
        'source_quality': 0.25,
        'logic_consistency': 0.25,
        'completeness': 0.20
    }
    """
    return sum(scores[criterion] * weights[criterion] for criterion in scores)
```

### Confidence Intervals
```yaml
confidence_calculation:
  factors:
    - reviewer_expertise_level
    - evidence_quality_consistency
    - methodology_complexity
    - domain_familiarity
  
  confidence_levels:
    very_high: 0.95-1.00  # High expertise, clear evidence
    high: 0.85-0.94       # Good expertise, solid evidence  
    moderate: 0.70-0.84   # Moderate expertise, mixed evidence
    low: 0.50-0.69        # Limited expertise, unclear evidence
    very_low: 0.00-0.49   # Insufficient expertise, poor evidence
```

## Bias Detection Framework

### Types of Bias Assessed
```yaml
bias_categories:
  selection_bias:
    indicators:
      - non_representative_sampling
      - cherry_picked_evidence
      - excluded_contrary_findings
      - limited_source_diversity
    
    detection_methods:
      - source_distribution_analysis
      - evidence_pattern_examination
      - contradiction_search
      - perspective_diversity_check
  
  confirmation_bias:
    indicators:
      - hypothesis_confirming_evidence_only
      - weak_contradictory_evidence_dismissal
      - strong_prior_assumption_influence
      - selective_interpretation_patterns
    
    detection_methods:
      - contrary_evidence_assessment
      - interpretation_alternative_exploration
      - assumption_examination
      - balanced_perspective_verification
  
  cultural_bias:
    indicators:
      - geographic_source_concentration
      - western_centric_perspectives
      - language_limitation_bias
      - cultural_assumption_imposition
    
    detection_methods:
      - geographic_source_mapping
      - cultural_perspective_analysis
      - assumption_cultural_validity_check
      - diverse_viewpoint_inclusion_assessment
  
  temporal_bias:
    indicators:
      - recent_information_overemphasis
      - historical_context_neglect
      - trend_extrapolation_errors
      - period_specific_conclusion_overgeneralization
    
    detection_methods:
      - temporal_source_distribution_analysis
      - historical_trend_contextualization
      - period_specific_factor_identification
      - longitudinal_validity_assessment
```

### Bias Mitigation Recommendations
```yaml
mitigation_strategies:
  source_diversification:
    - geographic_representation_expansion
    - temporal_coverage_improvement
    - methodological_approach_variation
    - perspective_spectrum_broadening
  
  systematic_contradiction_search:
    - contrary_evidence_active_seeking
    - alternative_explanation_exploration
    - assumption_challenging
    - devil_advocate_analysis
  
  methodology_enhancement:
    - sampling_strategy_improvement
    - data_collection_bias_reduction
    - analysis_method_bias_awareness
    - interpretation_objectivity_enhancement
  
  transparency_improvement:
    - assumption_explicit_statement
    - limitation_acknowledgment
    - bias_potential_discussion
    - methodology_detailed_documentation
```

## Integration with Research Workflow

### Review Trigger Points
```yaml
automatic_review_triggers:
  research_completion: "mandatory_full_review"
  milestone_completion: "checkpoint_review"
  quality_concern_flag: "targeted_review"
  stakeholder_request: "comprehensive_review"
  
review_scheduling:
  immediate: "critical_issues_priority_research"
  same_day: "high_priority_time_sensitive"
  within_24_hours: "standard_priority_research"
  within_48_hours: "low_priority_routine_research"
```

### Collaboration Protocols
```yaml
collaboration_workflow:
  1. review_request_receipt:
     - task_prioritization
     - resource_allocation
     - timeline_establishment
     - stakeholder_notification
  
  2. review_execution:
     - systematic_assessment_conduct
     - evidence_documentation
     - scoring_calculation
     - recommendation_development
  
  3. result_communication:
     - research_team_notification
     - detailed_feedback_provision
     - improvement_guidance_offer
     - follow_up_scheduling
  
  4. revision_cycle_management:
     - revision_tracking
     - resubmission_assessment
     - improvement_validation
     - final_approval_determination
```

### Quality Metrics and KPIs
```yaml
performance_metrics:
  review_quality:
    - accuracy_of_assessments
    - consistency_across_reviews
    - improvement_recommendation_effectiveness
    - false_positive_negative_rates
  
  review_efficiency:
    - average_review_turnaround_time
    - reviewer_productivity_metrics
    - resource_utilization_efficiency
    - stakeholder_satisfaction_scores
  
  impact_measurement:
    - research_quality_improvement_tracking
    - revision_success_rates
    - final_approval_rates
    - long_term_quality_trends
```

## Error Handling and Edge Cases

### Common Review Challenges
```yaml
challenge_scenarios:
  insufficient_information:
    detection: "incomplete_methodology_documentation"
    response: "clarification_request_to_research_team"
    escalation: "conditional_review_with_assumptions"
  
  conflicting_evidence:
    detection: "contradictory_source_findings"
    response: "additional_evidence_gathering"
    escalation: "uncertainty_quantification_reporting"
  
  novel_methodology:
    detection: "unrecognized_research_approach"
    response: "methodology_expert_consultation"
    escalation: "specialized_reviewer_assignment"
  
  cross_domain_complexity:
    detection: "multiple_expertise_area_requirement"
    response: "multi_disciplinary_review_team_assembly"
    escalation: "sequential_specialized_reviews"
```

### Quality Assurance for Reviews
```yaml
review_validation_process:
  1. self_assessment:
     - criterion_application_consistency
     - scoring_logic_verification
     - bias_in_review_process_check
     - recommendation_actionability_assessment
  
  2. peer_review_of_reviews:
     - second_reviewer_assessment
     - scoring_consistency_check
     - recommendation_quality_evaluation
     - bias_detection_in_review
  
  3. continuous_improvement:
     - review_outcome_tracking
     - methodology_refinement
     - training_needs_identification
     - best_practice_development
```

This specification provides a comprehensive framework for implementing a peer review agent that ensures systematic, rigorous, and consistent quality assessment of research outputs within the Claude Code ecosystem.