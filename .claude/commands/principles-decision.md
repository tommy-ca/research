# Principles Decision Command

## Purpose
Provide systematic decision support using Ray Dalio's principle-based frameworks with automatic template population, stakeholder analysis, and structured evaluation processes.

## Command Structure
```bash
/principles-decision "situation description" [domain] [urgency]
```

### Parameters
- `situation description`: Clear description of the decision to be made (required)
- `domain`: Decision context (personal, work, family, mixed) - auto-detected if not provided
- `urgency`: Timeline pressure (immediate, urgent, planned, strategic) - auto-assessed if not provided

## Functionality

### Core Process
1. **Situation Analysis**
   - Parse decision description and extract key elements
   - Classify decision type and complexity level
   - Identify affected stakeholders and impact scope
   - Assess timeline and resource constraints

2. **Domain Classification & Principle Selection**
   - Automatically classify as personal, work, family, or mixed decision
   - Select relevant Ray Dalio principles for the decision type
   - Identify cross-domain considerations if applicable
   - Prioritize principles based on situation characteristics

3. **Template Population**
   - Auto-populate appropriate decision framework template
   - Fill in known context and constraints
   - Identify information gathering requirements
   - Create stakeholder input plan with credibility assessments

4. **Systematic Evaluation Support**
   - Provide structured analysis framework
   - Generate option evaluation criteria
   - Create decision documentation for outcome tracking
   - Set up follow-up and review processes

### Decision Framework Templates

#### Personal Decision Framework
```yaml
Decision Context:
  Situation: [Auto-populated from description]
  Decision Type: [Goal-setting, relationship, health, financial, growth, etc.]
  Timeline: [When decision is needed]
  Impact Level: [Low, medium, high stakes]

Relevant Ray Dalio Principles:
  Primary Principles:
    - Embrace Reality: [Current reality assessment needed]
    - Pain + Reflection = Progress: [Learning opportunity aspects]
    - Radical Open-Mindedness: [Perspectives to seek, assumptions to question]
    - Evolve or Die: [Growth and adaptation implications]
  
  Supporting Principles:
    - [Additional relevant principles based on situation type]

Reality Assessment:
  Current Situation:
    - Objective facts: [What is actually true about current state]
    - Resources available: [Capabilities, time, support, finances]
    - Constraints: [Limitations and obstacles to consider]
    - Stakeholders affected: [Who will be impacted and how]
  
  Desired Outcome:
    - Primary objectives: [What success looks like]
    - Success metrics: [How to measure positive outcome]
    - Timeline expectations: [When results are expected]

Information Gathering Plan:
  Data Needed:
    - [Specific information required for informed decision]
    - [Research or analysis needed]
    - [Metrics or measurements to collect]
  
  Credible Input Sources:
    - [Person/Source]: [Why their input is valuable, track record relevance]
    - [Expert/Advisor]: [Specific expertise and credibility in this area]
    - [Experience/Data]: [Historical or comparative information sources]

Option Generation:
  Option 1: [Description]
    - Principle alignment: [How this aligns with relevant principles]
    - Pros: [Advantages and positive aspects]
    - Cons: [Disadvantages and risks]
    - Resource requirements: [What this option demands]
  
  Option 2: [Repeat structure]
  Option 3: [Repeat structure]

Decision Evaluation:
  Evaluation Criteria:
    - [Criterion 1]: [How to measure this factor]
    - [Criterion 2]: [Assessment approach]
    - [Criterion 3]: [Evaluation method]
  
  Systematic Analysis:
    - Best principles-based choice: [Option that best aligns with principles]
    - Risk assessment: [What could go wrong with preferred option]
    - Mitigation strategies: [How to reduce risks]

Implementation Planning:
  Next Steps:
    - Immediate actions: [What to do first]
    - Information gathering: [Specific research/consultation needed]
    - Timeline: [When to complete each step]
  
  Success Monitoring:
    - Key indicators: [Early signs of success/failure]
    - Review schedule: [When to assess outcomes]
    - Adjustment triggers: [What would require changing course]
```

#### Work Decision Framework
```yaml
Decision Context:
  Situation: [Auto-populated from description]
  Decision Type: [Strategy, hiring, project, conflict, process, etc.]
  Organizational Impact: [Team, department, company-wide]
  Timeline: [Decision urgency and implementation timeline]

Relevant Ray Dalio Principles:
  Primary Principles:
    - Idea Meritocracy: [Focus on best ideas regardless of source]
    - Believability-Weighted Decision Making: [Credible input prioritization]
    - Radical Transparency: [Open communication and information sharing]
    - Match People to Roles: [Leverage individual strengths effectively]
  
  Supporting Principles:
    - [Additional work-specific principles based on situation]

Stakeholder Analysis:
  Decision Makers:
    - [Person/Role]: [Authority level, relevant credibility, track record]
    - [Person/Role]: [Expertise area, decision-making history]
  
  Key Input Sources:
    - [Stakeholder]: [Relevant expertise, believability weight, input needed]
    - [Expert]: [Why their perspective matters, credibility factors]
  
  Affected Parties:
    - [Individual/Group]: [How they'll be impacted, concerns to address]
    - [Team/Department]: [Implementation implications, change management needs]

Information Requirements:
  Data Analysis Needed:
    - [Metrics/Analytics]: [What data to analyze and why]
    - [Comparative Analysis]: [Benchmarks or historical comparisons]
    - [Impact Assessment]: [How to measure potential outcomes]
  
  Expert Consultation:
    - [Domain Expert]: [Specific questions to ask, credibility assessment]
    - [Experienced Colleague]: [Relevant experience, input needed]

Systematic Evaluation:
  Option Analysis:
    Option 1: [Description]
      - Idea meritocracy assessment: [Is this objectively the best idea?]
      - Resource requirements: [Time, budget, people needed]
      - Risk factors: [What could go wrong, probability and impact]
      - Success probability: [Based on evidence and expert input]
    
    [Repeat for additional options]
  
  Believability-Weighted Input Summary:
    - Highest credibility recommendation: [Most credible source suggests...]
    - Consensus among experts: [Areas of agreement among credible sources]
    - Dissenting views: [Important contrary opinions to consider]

Transparency and Communication:
  Information Sharing Plan:
    - What to communicate: [Decision rationale and supporting information]
    - Who to inform: [Stakeholders who need to know decision and reasoning]
    - Communication timeline: [When to share information]
  
  Feedback Mechanisms:
    - Input channels: [How stakeholders can provide ongoing feedback]
    - Review processes: [Regular check-ins and adjustment opportunities]

Implementation Strategy:
  Execution Plan:
    - Phase 1: [Initial steps and timeline]
    - Phase 2: [Follow-up actions and milestones]
    - Success metrics: [How to measure effectiveness]
  
  People-Role Matching:
    - [Task/Responsibility]: [Person best suited based on strengths]
    - [Project Element]: [Individual with relevant capabilities]
```

#### Family Decision Framework
```yaml
Decision Context:
  Situation: [Auto-populated from description]  
  Decision Type: [Parenting, finances, activities, conflicts, education, etc.]
  Family Members Affected: [Who is impacted and how]
  Age Considerations: [Developmental appropriateness factors]

Relevant Ray Dalio Principles:
  Primary Principles:
    - Co-Create Family Values: [How shared principles apply to this decision]
    - Age-Appropriate Transparency: [How to communicate openly with each member]
    - Family Learning System: [How this can be a collective learning opportunity]
    - Individual Strengths: [How to leverage each person's capabilities]
  
  Supporting Principles:
    - [Additional family-specific principles based on situation]

Family Values Alignment:
  Relevant Family Principles:
    - [Family Value]: [How this decision relates to shared family principle]
    - [Core Belief]: [Connection to established family priorities]
  
  Value Conflicts:
    - [Competing Value]: [How different family values might conflict in this decision]
    - [Resolution Approach]: [How to balance competing priorities]

Family Input Process:
  Age-Appropriate Involvement:
    - [Family Member]: [How to include them in decision process appropriately]
    - [Child/Teen]: [Developmental considerations for their participation]
    - [Adult Member]: [Full participation role and responsibilities]
  
  Communication Strategy:
    - Information sharing: [How to explain situation to each family member]
    - Gathering perspectives: [How to collect input from everyone]
    - Building consensus: [Process for reaching family agreement]

Individual Strengths Utilization:
  Family Member Capabilities:
    - [Person]: [Their strengths relevant to this decision/implementation]
    - [Member]: [How their abilities can contribute to best outcome]
  
  Role Assignments:
    - [Responsibility]: [Person best suited based on natural strengths]
    - [Task]: [Individual with relevant skills or interests]

Decision Options Analysis:
  Option 1: [Description]
    - Family values alignment: [How this option supports shared principles]
    - Individual impact: [Effect on each family member]
    - Implementation feasibility: [Practical considerations for family]
    - Learning opportunity: [How this choice provides growth for family]
  
  [Repeat for additional options]

Collective Learning Integration:
  Learning Opportunities:
    - For Family: [What the family can learn together from this decision]
    - Individual Growth: [How each person can develop through this process]
    - Process Improvement: [How family decision-making can get better]
  
  Teaching Moments:
    - [Concept]: [What this decision teaches about life/values]
    - [Skill]: [Capabilities this process helps family members develop]

Implementation Planning:
  Family Roles and Responsibilities:
    - [Family Member]: [Their specific role in implementing decision]
    - [Person]: [Tasks aligned with their strengths and development needs]
  
  Communication and Check-ins:
    - Progress reviews: [How family will assess how decision is working]
    - Adjustment process: [How to modify approach if needed]
    - Learning capture: [How to document insights for future decisions]
```

## Advanced Decision Support Features

### Automatic Context Analysis
```python
def analyze_decision_context(situation_description):
    """Automatically analyze decision context and populate relevant framework"""
    
    context_analysis = {
        'decision_type': classify_decision_type(situation_description),
        'domain': identify_primary_domain(situation_description),
        'complexity': assess_decision_complexity(situation_description),
        'stakeholders': extract_affected_stakeholders(situation_description),
        'timeline': infer_decision_timeline(situation_description),
        'constraints': identify_constraints_and_limitations(situation_description)
    }
    
    relevant_principles = select_principles_for_context(context_analysis)
    framework_template = choose_appropriate_template(context_analysis)
    
    return populate_framework_with_context(framework_template, context_analysis, relevant_principles)
```

### Credibility Assessment Support
```python
def generate_credibility_assessment_guide(stakeholders, decision_type):
    """Help assess believability weighting for stakeholder input"""
    
    credibility_factors = {
        'relevant_experience': assess_experience_relevance(stakeholders, decision_type),
        'track_record': evaluate_historical_success_rates(stakeholders),
        'domain_expertise': measure_subject_matter_knowledge(stakeholders),
        'objectivity': assess_bias_and_conflicts_of_interest(stakeholders),
        'reasoning_ability': evaluate_logical_thinking_capacity(stakeholders)
    }
    
    return generate_credibility_scoring_framework(credibility_factors)
```

## Integration with PKM System

### Decision Tracking
- Create decision nodes in knowledge graph with full context
- Link to relevant principle permanent notes
- Track decision outcomes for effectiveness analysis
- Build database of decision patterns and results

### Learning Integration
- Capture decision-making process insights
- Update principle effectiveness based on outcomes
- Create cross-references to similar historical decisions
- Generate learning summaries for future reference

### Automated Follow-up
- Set calendar reminders for decision outcome assessment
- Create follow-up tasks for information gathering
- Generate review schedules based on decision timeline
- Update decision effectiveness tracking database

## Command Processing Logic

```python
def execute_principles_decision(situation, domain=None, urgency=None):
    """Execute systematic decision support with principle-based frameworks"""
    
    # 1. Situation Analysis
    context_analysis = analyze_decision_context(situation)
    if not domain:
        domain = context_analysis['primary_domain']
    if not urgency:
        urgency = context_analysis['timeline_pressure']
    
    # 2. Principle Selection
    relevant_principles = select_principles_for_decision(context_analysis, domain)
    
    # 3. Framework Selection and Population
    framework_template = select_framework_template(domain, context_analysis)
    populated_framework = populate_template_with_context(
        framework_template, context_analysis, relevant_principles
    )
    
    # 4. Stakeholder and Credibility Analysis
    credibility_assessment = generate_credibility_assessment_guide(
        context_analysis['stakeholders'], context_analysis['decision_type']
    )
    
    # 5. Decision Support Generation
    decision_support_package = create_comprehensive_decision_support(
        populated_framework, credibility_assessment, relevant_principles
    )
    
    # 6. PKM Integration
    create_decision_tracking_node(decision_support_package)
    link_to_relevant_principle_notes(relevant_principles)
    set_automated_follow_up_reminders(context_analysis['timeline'])
    
    return {
        'populated_framework': populated_framework,
        'relevant_principles': relevant_principles,
        'credibility_assessment': credibility_assessment,
        'decision_support': decision_support_package,
        'follow_up_scheduled': True
    }
```

## Usage Examples

### Basic Decision Support
```bash
/principles-decision "Should I accept the job offer from the startup or stay at my current company?"
# Automatically analyzes as personal/work decision, populates relevant frameworks
```

### Family Decision with Domain Specification
```bash
/principles-decision "We need to decide about our teenager's request to spend the summer abroad" family
# Uses family decision framework with age-appropriate transparency principles
```

### Work Decision with Urgency
```bash
/principles-decision "The team is divided on the architecture approach for the new product" work urgent
# Applies work principles with emphasis on rapid but systematic decision-making
```

### Complex Multi-Domain Decision
```bash
/principles-decision "Considering relocating for career opportunity but worried about family impact" mixed
# Uses integrated approach across personal, work, and family domains
```

## Quality Standards

### Framework Completeness
- All relevant sections populated with available context
- Clear identification of information gaps requiring research
- Systematic principle application appropriate to decision type
- Comprehensive stakeholder and credibility analysis

### Actionability
- Specific next steps for information gathering and consultation
- Clear evaluation criteria and decision-making process
- Ready-to-use frameworks for systematic analysis
- Practical implementation planning and follow-up

### Integration Quality
- Seamless PKM system integration with decision tracking
- Appropriate links to principle effectiveness data
- Automated follow-up and outcome tracking setup
- Knowledge capture for compound learning

## Success Metrics

### Decision Quality Improvement
- Better decision outcomes through systematic principle application
- Reduced decision-making time through structured frameworks
- More consistent application of principles across similar decisions
- Enhanced confidence in choices through comprehensive analysis

### Learning Integration
- Systematic capture of decision-making insights and patterns
- Building repository of effective decision frameworks
- Improved principle selection and application over time
- Compound intelligence development through decision experience

### Relationship and Communication Enhancement
- Better stakeholder involvement through credibility-weighted input
- Enhanced transparency in decision-making processes
- Improved family decision-making through systematic approaches
- Strengthened relationships through principled decision processes

---

*This command transforms decision-making from intuitive choices into systematic, principle-based processes that leverage Ray Dalio's methodologies for enhanced effectiveness, learning, and relationship building across all life domains.*