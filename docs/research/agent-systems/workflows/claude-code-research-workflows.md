# Claude Code Research Workflows

## Overview

This document defines comprehensive research workflows integrated with Claude Code's subagent system and custom commands. The workflows leverage specialized research agents to provide systematic, high-quality research outputs with built-in collaboration and quality assurance.

## Workflow Architecture

### Core Workflow Components

```yaml
workflow_structure:
  orchestration_layer:
    - master_research_orchestrator
    - workflow_manager
    - progress_monitor
    - quality_gate_controller
  
  execution_layer:
    - deep_research_agents
    - domain_expert_agents  
    - analysis_synthesis_agents
    - data_collection_agents
  
  quality_layer:
    - peer_review_agents
    - fact_verification_agents
    - bias_detection_agents
    - ethics_review_agents
  
  output_layer:
    - writing_documentation_agents
    - visualization_agents
    - presentation_agents
    - translation_agents
```

### Command Integration Framework

```yaml
command_categories:
  research_initiation:
    - /research-deep
    - /research-domain-expert
    - /research-literature-review
    - /research-data-collect
  
  analysis_synthesis:
    - /research-analyze
    - /research-synthesize
    - /research-model
    - /research-visualize
  
  quality_assurance:
    - /peer-review
    - /validate-sources
    - /detect-bias
    - /fact-check
  
  collaboration_coordination:
    - /research-assign
    - /research-status
    - /research-collaborate
    - /research-merge
  
  output_generation:
    - /research-report
    - /research-present
    - /research-publish
    - /research-export
```

## Standard Research Workflows

### 1. Comprehensive Research Project Workflow

#### Phase 1: Project Initialization
```bash
# Initialize research project
/research-init "Real Currency Valuation Framework" \
  --objectives="Develop comprehensive currency valuation model" \
  --timeline=30 \
  --quality-standard=academic \
  --team-size=5

# Create project structure
/research-structure \
  --phases="planning,execution,analysis,review,delivery" \
  --deliverables="framework,documentation,validation,presentation"

# Assign research team
/research-assign \
  --lead-researcher=deep-research-001 \
  --domain-experts=economics-001,finance-002 \
  --peer-reviewers=review-001,review-002 \
  --analysts=analysis-001,synthesis-001
```

#### Phase 2: Research Planning and Decomposition
```bash
# Decompose research into tasks
/research-decompose "Real Currency Valuation Framework" \
  --methodology=systematic \
  --depth=comprehensive \
  --domains=economics,finance,markets,policy

# Plan research methodology
/research-methodology \
  --approach=mixed-methods \
  --evidence-standards=academic \
  --validation-requirements=peer-review \
  --bias-mitigation=multi-perspective

# Establish quality gates
/research-quality-gates \
  --checkpoints=weekly \
  --review-triggers=milestone-completion \
  --approval-thresholds=0.85 \
  --escalation-protocols=enabled
```

#### Phase 3: Systematic Research Execution
```bash
# Execute deep research across domains
/research-deep "currency valuation theories" \
  --depth=comprehensive \
  --sources=academic,central-banks,industry \
  --validation=peer-review \
  --agent=economics-001

/research-deep "money supply analysis" \
  --depth=comprehensive \
  --sources=government,academic,statistical \
  --validation=fact-check \
  --agent=economics-001

/research-deep "FX market microstructure" \
  --depth=comprehensive \
  --sources=industry,academic,regulatory \
  --validation=expert-review \
  --agent=finance-002

# Collect and analyze data
/research-data-collect \
  --sources=fred,bis,imf,ecb \
  --timeframe=10-years \
  --frequency=daily \
  --validation=automated

# Conduct literature review
/research-literature-review "currency valuation" \
  --period=2015-2024 \
  --databases=jstor,pubmed,google-scholar \
  --quality-filter=peer-reviewed \
  --synthesis-method=systematic
```

#### Phase 4: Analysis and Synthesis
```bash
# Analyze collected research
/research-analyze \
  --methods=quantitative,qualitative,comparative \
  --frameworks=first-principles,empirical \
  --validation=statistical \
  --confidence=0.95

# Synthesize findings across domains
/research-synthesize \
  --inputs=theories,data-analysis,market-structure \
  --framework=systematic \
  --methodology=cross-domain \
  --output=integrated-framework

# Develop models and frameworks
/research-model \
  --type=mathematical,conceptual \
  --validation=empirical,theoretical \
  --testing=backtesting,stress-testing \
  --documentation=comprehensive

# Create visualizations
/research-visualize \
  --types=charts,diagrams,infographics,dashboards \
  --formats=static,interactive \
  --audiences=academic,professional,general \
  --accessibility=wcag-compliant
```

#### Phase 5: Quality Assurance and Review
```bash
# Execute comprehensive peer review
/peer-review research-output.md \
  --criteria=all \
  --standard=academic \
  --reviewers=multiple \
  --consensus-required=true

# Validate sources and facts
/validate-sources research-output.md \
  --threshold=0.9 \
  --diversity=all \
  --cross-reference=mandatory \
  --update-check=current

# Detect and mitigate bias
/detect-bias research-output.md \
  --types=all \
  --sensitivity=maximum \
  --mitigation=automatic \
  --documentation=detailed

# Check reproducibility
/review-reproducibility research-output.md \
  --components=all \
  --standard=gold \
  --documentation=complete \
  --validation=independent
```

#### Phase 6: Output Generation and Delivery
```bash
# Generate comprehensive report
/research-report \
  --template=academic \
  --sections=all \
  --citations=apa \
  --appendices=data,methodology,supplementary

# Create presentation materials
/research-present \
  --audience=academic \
  --format=slides,handouts \
  --duration=45-minutes \
  --interactivity=enabled

# Publish to repository
/research-publish \
  --repository=github \
  --license=cc-by-4.0 \
  --documentation=complete \
  --version-control=git

# Export to multiple formats
/research-export \
  --formats=pdf,docx,html,markdown \
  --quality=print-ready \
  --accessibility=compliant \
  --distribution=stakeholders
```

### 2. Rapid Research Workflow (Crisis/Urgent)

#### Accelerated Timeline Workflow
```bash
# Initialize rapid research
/research-rapid "COVID-19 Economic Impact Analysis" \
  --urgency=critical \
  --timeline=72-hours \
  --quality=expedited \
  --resources=maximum

# Deploy multiple agents in parallel
/research-parallel \
  --agents=economics-001,finance-002,policy-003 \
  --coordination=real-time \
  --updates=hourly \
  --quality-checks=continuous

# Execute concurrent research streams
/research-deep "economic indicators" --timeline=24h --agent=economics-001 &
/research-deep "market reactions" --timeline=24h --agent=finance-002 &
/research-deep "policy responses" --timeline=24h --agent=policy-003 &

# Real-time synthesis and updates
/research-synthesize \
  --mode=continuous \
  --updates=real-time \
  --integration=automatic \
  --alerts=stakeholders

# Expedited review process
/peer-review-expedited \
  --reviewers=senior-experts \
  --timeline=6-hours \
  --focus=critical-findings \
  --approval=conditional
```

### 3. Domain-Specific Research Workflow

#### Financial Markets Research
```bash
# Initialize financial research project
/research-financial "Cryptocurrency Market Analysis" \
  --markets=crypto,traditional,derivatives \
  --timeframe=5-years \
  --frequency=high-frequency \
  --risk-analysis=comprehensive

# Collect market data
/research-data-financial \
  --sources=bloomberg,reuters,coinbase,binance \
  --instruments=btc,eth,traditional-fx \
  --metrics=price,volume,volatility,sentiment

# Analyze market microstructure
/research-microstructure \
  --focus=liquidity,order-flow,price-discovery \
  --methods=high-frequency-econometrics \
  --validation=empirical

# Risk assessment and modeling
/research-risk-model \
  --types=market,credit,liquidity,operational \
  --methods=var,expected-shortfall,stress-testing \
  --scenarios=historical,hypothetical,extreme
```

### 4. Collaborative Multi-Institution Workflow

#### Cross-Organization Research
```bash
# Initialize collaborative research
/research-collaborate \
  --institutions=university-a,bank-b,think-tank-c \
  --coordination=distributed \
  --data-sharing=secure \
  --ip-management=defined

# Setup secure collaboration channels
/research-secure-channels \
  --encryption=end-to-end \
  --access-control=role-based \
  --audit-logging=comprehensive \
  --compliance=gdpr,hipaa

# Coordinate distributed research
/research-coordinate \
  --assignments=institution-specific \
  --integration-points=defined \
  --quality-standards=harmonized \
  --timeline-synchronization=enabled

# Merge distributed outputs
/research-merge \
  --inputs=institution-outputs \
  --methodology=systematic \
  --conflict-resolution=consensus \
  --attribution=proper
```

## Specialized Workflow Templates

### Academic Research Workflow Template
```yaml
academic_workflow:
  initialization:
    - literature_review_protocol
    - methodology_design
    - ethics_approval
    - peer_review_setup
  
  execution:
    - systematic_data_collection
    - rigorous_analysis
    - hypothesis_testing
    - replication_validation
  
  validation:
    - peer_review_process
    - statistical_validation
    - reproducibility_check
    - bias_assessment
  
  publication:
    - manuscript_preparation
    - journal_submission
    - revision_cycles
    - final_publication
```

### Industry Research Workflow Template
```yaml
industry_workflow:
  initialization:
    - business_objective_alignment
    - stakeholder_requirement_gathering
    - competitive_analysis_setup
    - roi_framework_development
  
  execution:
    - market_research
    - customer_analysis
    - technology_assessment
    - business_impact_modeling
  
  validation:
    - expert_validation
    - stakeholder_review
    - business_case_validation
    - risk_assessment
  
  delivery:
    - executive_summary
    - detailed_recommendations
    - implementation_roadmap
    - success_metrics
```

### Policy Research Workflow Template
```yaml
policy_workflow:
  initialization:
    - policy_objective_clarification
    - stakeholder_mapping
    - regulatory_landscape_analysis
    - public_interest_assessment
  
  execution:
    - evidence_gathering
    - impact_assessment
    - cost_benefit_analysis
    - implementation_feasibility
  
  validation:
    - expert_panel_review
    - public_consultation
    - legal_compliance_check
    - unintended_consequence_analysis
  
  recommendation:
    - policy_option_development
    - implementation_guidance
    - monitoring_framework
    - evaluation_metrics
```

## Quality Control Integration

### Automated Quality Gates
```bash
# Setup automated quality monitoring
/research-quality-monitor \
  --metrics=accuracy,completeness,bias,reproducibility \
  --thresholds=configurable \
  --alerts=real-time \
  --escalation=automatic

# Continuous bias monitoring
/bias-monitor \
  --types=all \
  --sensitivity=high \
  --correction=suggestions \
  --reporting=detailed

# Fact-checking integration
/fact-check-continuous \
  --sources=trusted-databases \
  --validation=real-time \
  --conflicts=flagged \
  --resolution=manual-review
```

### Review Checkpoint Automation
```bash
# Setup milestone reviews
/research-milestones \
  --checkpoints=25%,50%,75%,completion \
  --criteria=methodology,progress,quality \
  --reviewers=assigned \
  --approval-required=true

# Automated progress tracking
/research-progress-track \
  --metrics=completion,quality,timeline \
  --reporting=daily \
  --stakeholders=defined \
  --escalation=delays
```

## Command Reference Quick Guide

### Core Research Commands
```bash
# Research initiation
/research-deep <topic> [options]          # Comprehensive research
/research-rapid <topic> [options]         # Urgent research
/research-domain <topic> <domain>         # Domain-specific research

# Analysis and synthesis  
/research-analyze <data> [methods]        # Data analysis
/research-synthesize [inputs] [framework] # Cross-source synthesis
/research-model [type] [validation]       # Model development

# Quality assurance
/peer-review <file> [criteria]            # Peer review process
/validate-sources <file> [threshold]      # Source validation
/detect-bias <file> [types]               # Bias detection
/fact-check <claims> [sources]            # Fact verification

# Collaboration and management
/research-assign <tasks> <agents>         # Task assignment
/research-status [project]                # Progress status
/research-collaborate [partners]          # Multi-party research
/research-merge <inputs> [method]         # Output integration

# Output generation
/research-report [template] [format]      # Report generation
/research-present [audience] [format]     # Presentation creation
/research-export [formats] [quality]      # Multi-format export
/research-publish [repository] [license]  # Publication workflow
```

### Advanced Workflow Commands
```bash
# Workflow orchestration
/workflow-create <template> <parameters>  # Create custom workflow
/workflow-execute <workflow> [options]    # Execute workflow
/workflow-monitor <workflow> [alerts]     # Monitor execution
/workflow-optimize <workflow> [metrics]   # Performance optimization

# Agent coordination
/agent-deploy <type> <count> [config]     # Deploy agent pool
/agent-coordinate <agents> <protocol>     # Setup coordination
/agent-monitor <agents> [metrics]         # Agent performance
/agent-scale <agents> <demand>            # Dynamic scaling

# Quality management
/quality-framework <standards> [custom]   # Setup quality framework
/quality-gate <checkpoint> <criteria>     # Create quality gates
/quality-metrics <kpis> [targets]         # Define quality metrics
/quality-report <period> [stakeholders]   # Generate quality reports
```

## Integration with External Systems

### Data Source Integration
```yaml
data_integrations:
  academic_databases:
    - jstor_api_integration
    - pubmed_access
    - google_scholar_automation
    - institutional_subscriptions
  
  financial_data:
    - bloomberg_terminal_api
    - reuters_datafeed
    - central_bank_apis
    - market_data_vendors
  
  government_sources:
    - statistical_agency_apis
    - regulatory_filings
    - policy_databases
    - official_publications
  
  real_time_feeds:
    - news_wire_services
    - social_media_apis
    - market_data_streams
    - sensor_data_feeds
```

### Collaboration Platform Integration
```yaml
collaboration_integrations:
  communication:
    - slack_integration
    - microsoft_teams
    - discord_research_channels
    - email_automation
  
  project_management:
    - jira_integration
    - asana_workflows
    - trello_boards
    - monday_com_tracking
  
  document_management:
    - sharepoint_integration
    - google_workspace
    - dropbox_business
    - box_enterprise
  
  version_control:
    - github_integration
    - gitlab_workflows
    - bitbucket_coordination
    - svn_legacy_support
```

## Performance Optimization

### Workflow Efficiency Metrics
```yaml
performance_kpis:
  speed_metrics:
    - research_completion_time
    - agent_response_time
    - workflow_throughput
    - parallel_processing_efficiency
  
  quality_metrics:
    - accuracy_scores
    - peer_review_ratings
    - revision_rates
    - stakeholder_satisfaction
  
  resource_metrics:
    - computational_utilization
    - agent_productivity
    - cost_per_research_hour
    - roi_measurement
  
  collaboration_metrics:
    - coordination_effectiveness
    - communication_efficiency
    - conflict_resolution_time
    - knowledge_sharing_rate
```

### Scalability Considerations
```yaml
scaling_strategies:
  horizontal_scaling:
    - agent_pool_expansion
    - distributed_processing
    - load_balancing
    - regional_deployment
  
  vertical_scaling:
    - enhanced_agent_capabilities
    - increased_computational_power
    - expanded_memory_allocation
    - advanced_ai_integration
  
  elastic_scaling:
    - demand_based_provisioning
    - automatic_resource_adjustment
    - cost_optimization
    - performance_maintenance
```

This comprehensive workflow documentation provides the foundation for implementing systematic, high-quality research processes using Claude Code's subagent ecosystem with built-in quality assurance, collaboration, and optimization capabilities.