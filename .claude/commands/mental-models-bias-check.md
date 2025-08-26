---
command: mental-models-bias-check
description: Systematic cognitive bias recognition and mitigation using Charlie Munger's framework
agent: mental-models-coach
enabled: true
---

# Mental Models Bias Check Command

## Overview
Comprehensive cognitive bias detection and mitigation system based on Charlie Munger's "25 Standard Causes of Human Misjudgment," providing systematic protection against flawed thinking and decision-making errors.

## Usage
```bash
/mental-models-bias-check "situation or decision"
/mental-models-bias-check "thinking pattern" [bias-category]
/mental-models-bias-check "group dynamics" [social-focus]
```

## Parameters
- `situation or decision` (required): Description of thinking pattern, decision, or situation to analyze
- `bias-category` (optional): Focus area (psychological, social, economic, cognitive)
- `social-focus` (optional): Emphasis on group or interpersonal bias dynamics

## Core Functionality

### Charlie Munger's 25+ Standard Causes of Human Misjudgment

#### Reward and Punishment Super-Response Tendency
- **Detection**: Identify when incentives may be distorting judgment
- **Mitigation**: Consider how rewards/punishments might be affecting thinking
- **Applications**: Business decisions, personal choices, relationship dynamics

#### Liking/Loving and Disliking/Hating Tendency
- **Detection**: Recognize when personal feelings toward people affect objective judgment
- **Mitigation**: Separate person evaluation from idea evaluation
- **Applications**: Team decisions, vendor selection, advice evaluation

#### Doubt-Avoidance Tendency
- **Detection**: Identify rushed decisions to eliminate uncertainty
- **Mitigation**: Embrace productive uncertainty and systematic analysis
- **Applications**: Investment decisions, strategic planning, life choices

#### Inconsistency-Avoidance Tendency (Commitment and Consistency)
- **Detection**: Recognize when past commitments bias current thinking
- **Mitigation**: Permission to change mind based on new evidence
- **Applications**: Strategy pivots, relationship decisions, career changes

#### Social Proof Tendency
- **Detection**: Identify when "everyone else is doing it" affects judgment
- **Mitigation**: Independent analysis before considering social validation
- **Applications**: Investment decisions, lifestyle choices, business strategy

#### Authority-Misinfluence Tendency
- **Detection**: Recognize when expert opinions bypass critical thinking
- **Mitigation**: Evaluate expertise relevance and track record
- **Applications**: Professional advice, medical decisions, strategic guidance

#### Deprival-Super-Reaction Syndrome (Loss Aversion)
- **Detection**: Identify when fear of loss creates irrational decision-making
- **Mitigation**: Focus on opportunity cost and expected value analysis
- **Applications**: Investment decisions, career moves, relationship choices

#### Envy/Jealousy Tendency
- **Detection**: Recognize when comparative thinking distorts priorities
- **Mitigation**: Focus on absolute rather than relative outcomes
- **Applications**: Career decisions, lifestyle choices, business strategy

#### Reciprocation Tendency
- **Detection**: Identify when obligation to return favors affects judgment
- **Mitigation**: Separate gratitude from objective decision-making
- **Applications**: Business partnerships, personal relationships, vendor selection

#### Over-Influence from Mere Association
- **Detection**: Recognize when unrelated associations affect judgment
- **Mitigation**: Focus on direct causal relationships and relevant factors
- **Applications**: Investment decisions, hiring choices, strategic planning

### Advanced Bias Categories

#### Availability-Misweighing Tendency
- Recent or memorable events given excessive weight
- Mitigation: Systematic data collection and base rate consideration

#### Excessive Self-Regard Tendency
- Overconfidence in abilities, knowledge, or judgment
- Mitigation: Circle of competence assessment and external validation

#### Over-Optimism Tendency
- Systematic underestimation of risks and overestimation of benefits
- Mitigation: Inversion thinking and worst-case scenario planning

#### Contrast-Misreaction Tendency  
- Judgment distorted by immediate comparisons rather than absolute values
- Mitigation: Establish independent evaluation criteria and benchmarks

#### Lollapalooza Tendency
- Multiple biases interacting to create extreme misjudgment
- Mitigation: Systematic multi-bias analysis and cross-checking

## Command Workflows

### Individual Decision Bias Analysis
```bash
/mental-models-bias-check "I'm certain this investment opportunity is perfect"

# Systematic analysis:
# - Overconfidence (excessive self-regard)
# - Confirmation bias (seeking supporting evidence)
# - Availability bias (recent success stories)
# - Liking bias (positive feelings toward presenter)
# - Social proof (others are investing)
# - Authority misinfluence (expert endorsement)
```

### Group Decision Bias Detection
```bash
/mental-models-bias-check "Our team unanimously agrees on this strategy" social-focus

# Group dynamics analysis:
# - Social proof (everyone agreeing creates pressure)
# - Authority misinfluence (senior leader preference)
# - Commitment consistency (past strategic statements)
# - Doubt avoidance (pressure to decide quickly)
# - Reciprocation (team loyalty affecting judgment)
```

### Relationship Decision Bias Check
```bash
/mental-models-bias-check "I should hire my friend for this important role"

# Personal bias analysis:
# - Liking tendency (friendship affecting judgment)
# - Reciprocation (obligation from past favors)
# - Social proof (others have hired friends successfully)
# - Doubt avoidance (avoiding difficult hiring process)
# - Inconsistency avoidance (friend expects consideration)
```

## Output Structure

### Comprehensive Bias Analysis
```yaml
cognitive_bias_analysis:
  situation: "Considering major career change to startup opportunity"
  
  primary_biases_detected:
    excessive_self_regard:
      description: "Overconfidence in ability to succeed in startup environment"
      evidence: "Dismissing statistics about startup failure rates"
      risk_level: "high"
      mitigation: 
        - "Research actual success rates in target industry"
        - "Seek honest feedback from startup veterans"
        - "Define objective success metrics and timeline"
        
    availability_bias:
      description: "Recent success stories dominating risk assessment"
      evidence: "Focusing on recent unicorn stories rather than base rates"
      risk_level: "medium"
      mitigation:
        - "Research comprehensive startup outcome data"
        - "Consider both success and failure case studies"
        - "Analyze personal track record objectively"
        
    social_proof:
      description: "Friends' career moves influencing decision"
      evidence: "Multiple friends have made similar transitions recently"
      risk_level: "medium"
      mitigation:
        - "Evaluate personal situation independently"
        - "Consider selection bias in friend group"
        - "Define personal criteria for success"
        
  secondary_biases_identified:
    doubt_avoidance:
      description: "Pressure to make quick decision to reduce uncertainty"
      evidence: "Desire to 'just decide and move forward'"
      risk_level: "low"
      mitigation:
        - "Embrace productive uncertainty for better analysis"
        - "Set appropriate timeline for thorough evaluation"
        
    deprival_super_reaction:
      description: "Fear of missing 'limited opportunity'"
      evidence: "Startup claims this is 'last chance' to join"
      risk_level: "medium"
      mitigation:
        - "Question artificial scarcity claims"
        - "Consider if similar opportunities might arise"
        - "Evaluate opportunity cost of current position"
  
  lollapalooza_risk_assessment:
    multiple_bias_interaction: "High - several biases reinforcing same conclusion"
    compound_effect_warning: "Overconfidence + Social proof + Availability bias creating strong momentum toward risky decision"
    recommended_action: "Systematic pause and independent analysis required"
    
  mitigation_framework:
    immediate_actions:
      - "Seek disconfirming evidence about startup success"
      - "Consult with someone who chose NOT to join startup"
      - "Research comprehensive failure case studies"
      - "Define objective decision criteria independent of emotion"
      
    systematic_analysis:
      - "Circle of competence assessment for startup skills"
      - "Expected value calculation with realistic probabilities"
      - "Inversion thinking: what could go wrong scenarios"
      - "Opportunity cost analysis of current vs. startup position"
      
    decision_framework:
      - "Define specific success metrics and timeline"
      - "Establish objective evaluation criteria"
      - "Create accountability system for bias checking"
      - "Plan systematic review of decision after implementation"

  bias_mitigation_checklist:
    pre_decision:
      - [ ] Seek three sources of disconfirming evidence
      - [ ] Consult someone who made opposite choice
      - [ ] Research base rates and statistical outcomes
      - [ ] Define objective success criteria upfront
      - [ ] Consider full range of alternative options
      
    during_decision:
      - [ ] Apply inversion thinking to failure modes  
      - [ ] Check circle of competence boundaries
      - [ ] Calculate expected value with realistic probabilities
      - [ ] Separate person evaluation from opportunity evaluation
      - [ ] Consider how incentives might be affecting judgment
      
    post_decision:
      - [ ] Document reasoning and predictions for later review
      - [ ] Establish accountability for tracking outcomes
      - [ ] Plan systematic review of decision quality
      - [ ] Extract learning for future bias recognition improvement
```

## Integration Features

### PKM System Enhancement
- **Bias Pattern Database**: Track personal bias tendencies and triggers across situations
- **Decision Outcome Correlation**: Link bias recognition success to decision quality improvement  
- **Learning Integration**: Transform bias recognition experiences into systematic knowledge
- **Cross-Reference Building**: Connect bias patterns to mental model applications

### Mental Models Integration
- **Multi-Model Bias Check**: Use various disciplines to identify different bias categories
- **Circle of Competence Bias**: Recognize overconfidence in knowledge boundaries
- **Systems Thinking Bias**: Consider how biases interact and reinforce each other
- **Probabilistic Thinking**: Use mathematical models to counter cognitive bias distortions

### Ray Dalio Principles Synergy
- **Radical Transparency Enhancement**: Systematic bias recognition improves honest self-assessment
- **Believability Weighting**: Consider how biases affect credibility of input sources
- **Systematic Mistake Analysis**: Use bias framework to improve "Pain + Reflection = Progress"
- **Cross-Domain Application**: Apply bias awareness to personal/work/family decision-making

## Advanced Features

### Bias Interaction Analysis
- **Lollapalooza Detection**: Identify when multiple biases create compound misjudgment
- **Reinforcement Patterns**: Recognize how biases strengthen each other
- **Cancellation Effects**: Find cases where biases might counteract each other
- **Threshold Analysis**: Determine when bias combinations reach dangerous levels

### Personal Bias Profiling
- **Individual Tendency Mapping**: Track personal susceptibility to different bias categories
- **Situation-Specific Patterns**: Identify contexts where biases are most likely to occur
- **Historical Analysis**: Review past decisions to identify recurring bias patterns
- **Improvement Tracking**: Monitor bias recognition and mitigation success over time

### Social Bias Dynamics
- **Group Think Detection**: Identify when team dynamics create systematic bias
- **Authority Influence Mapping**: Recognize how expertise claims affect group judgment
- **Social Proof Cascades**: Detect when group consensus becomes self-reinforcing
- **Collective Delusion Prevention**: Systematic approaches to maintaining independent thinking

## Success Metrics

### Bias Recognition Improvement
- **Detection Frequency**: Increased identification of cognitive biases before they affect decisions
- **Recognition Speed**: Faster identification of bias patterns in real-time situations
- **Accuracy Rate**: Better prediction of which biases are likely to affect specific situations
- **Severity Assessment**: Improved evaluation of bias impact on decision quality

### Decision Quality Enhancement
- **Reduced Regret**: Fewer decisions affected by unrecognized cognitive biases
- **Outcome Prediction**: Better accuracy in predicting decision results through bias-aware analysis
- **Stakeholder Satisfaction**: Improved outcomes for others affected by bias-aware decisions
- **Learning Integration**: Successful extraction of bias recognition insights for future applications

---

**Command Purpose**: Systematic cognitive bias recognition and mitigation using Charlie Munger's framework
**Integration Focus**: Enhanced decision-making through bias awareness within existing PKM and principles systems
**Success Indicator**: Measurable reduction in decision-making errors through systematic bias recognition and mitigation