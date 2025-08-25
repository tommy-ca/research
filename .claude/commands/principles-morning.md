# Principles Morning Command

## Purpose
Start each day with systematic principle planning based on anticipated challenges, calendar analysis, and previous day's learning integration.

## Command Structure
```bash
/principles-morning [focus-area]
```

### Optional Parameters
- `focus-area`: Specific domain to emphasize (personal, work, family, or mixed)

## Functionality

### Core Process
1. **Calendar & Activity Analysis**
   - Review today's scheduled activities and commitments
   - Identify potential decision points and challenges
   - Anticipate interpersonal interactions and meetings
   - Note high-stakes or complex situations requiring principled approaches

2. **Yesterday's Learning Integration**
   - Review previous evening's reflection for continuation items
   - Identify unresolved challenges requiring follow-up
   - Extract insights from yesterday's principle applications
   - Note patterns or trends requiring attention

3. **Principle Selection & Prioritization**
   - Match anticipated challenges to relevant Ray Dalio principles
   - Select primary principles to focus on for the day
   - Identify specific application opportunities in scheduled activities
   - Create principle-based objectives for key interactions

4. **Decision Framework Preparation**
   - Prepare decision templates for anticipated choices
   - Pre-populate frameworks with known context and constraints
   - Identify information gathering needs for complex decisions
   - Create stakeholder input plans for collaborative choices

### Decision Framework Templates

#### Personal Decision Template
```yaml
Anticipated Personal Decision: [Description]
Relevant Principles:
  - Embrace Reality: [Current situation assessment]
  - Pain + Reflection = Progress: [Learning opportunity identification]
  - Radical Open-Mindedness: [Perspectives to seek]
  - Evolve or Die: [Growth opportunity aspects]

Preparation Checklist:
  - Information needed: [Data requirements]
  - People to consult: [Credible input sources]
  - Success criteria: [How to measure outcomes]
  - Timeline: [When decision is needed]
```

#### Work Decision Template
```yaml
Anticipated Work Decision: [Description]
Relevant Principles:
  - Idea Meritocracy: [Best idea focus approach]
  - Believability-Weighted Input: [Credible stakeholders to consult]
  - Radical Transparency: [Information sharing plan]
  - Match People to Roles: [Strength utilization opportunities]

Preparation Checklist:
  - Stakeholder analysis: [Who to involve and their credibility]
  - Information requirements: [Data and analysis needed]
  - Decision criteria: [Standards for evaluation]
  - Communication plan: [How to share rationale]
```

#### Family Decision Template
```yaml
Anticipated Family Decision: [Description]
Relevant Principles:
  - Co-Created Values: [Family principles that apply]
  - Age-Appropriate Transparency: [How to communicate with each member]
  - Family Learning: [How this can be a learning opportunity]
  - Individual Strengths: [How to leverage each person's capabilities]

Preparation Checklist:
  - Family input process: [How to gather perspectives]
  - Age-appropriate communication: [Adaptation for each family member]
  - Consensus building: [How to achieve family alignment]
  - Implementation roles: [Who does what based on strengths]
```

### Output Generation

#### Daily Principle Plan
```markdown
# Daily Principle Plan: [Date]

## Morning Principle Assessment
- **Primary Focus Area**: [Personal/Work/Family/Mixed]
- **Key Challenges Anticipated**: [List of 2-3 main challenges]
- **Core Principles for Today**: [3-5 most relevant principles]

## Scheduled Decision Points
### [Time] - [Activity/Meeting]
- **Potential Decisions**: [What choices might arise]
- **Relevant Principles**: [Which frameworks apply]
- **Preparation Done**: [Information gathered, people consulted]
- **Success Criteria**: [How to measure effectiveness]

## Daily Principle Objectives
1. **[Principle 1]**: [Specific application opportunity]
2. **[Principle 2]**: [Specific application opportunity]  
3. **[Principle 3]**: [Specific application opportunity]

## Learning Integration from Yesterday
- **Insights Applied Today**: [How yesterday's lessons inform today]
- **Unresolved Items**: [Continuing challenges requiring attention]
- **Pattern Recognition**: [Recurring themes to address]

## Evening Reflection Preparation
- **Key Outcomes to Track**: [What to assess this evening]
- **Learning Questions**: [What to reflect on]
- **Tomorrow's Focus**: [Initial thoughts for next day]
```

## Integration with PKM System

### Daily Note Enhancement
- Automatically update today's daily note with principle plan
- Link to relevant permanent notes on principles and decision-making
- Create references to similar historical situations and outcomes
- Set up tracking system for evening reflection analysis

### Knowledge Graph Connections
- Link today's anticipated challenges to previous similar situations
- Connect principle selections to effectiveness tracking data
- Create references to relevant decision frameworks and templates
- Build patterns database for future principle selection optimization

### Automated Reminders
- Set calendar reminders for key decision points
- Create principle application checkpoints throughout day
- Schedule evening reflection based on morning plan
- Generate follow-up tasks for complex decisions requiring multi-day attention

## Command Processing Logic

```python
def execute_principles_morning(focus_area=None):
    """Execute comprehensive morning principle planning"""
    
    # 1. Calendar and Context Analysis
    today_schedule = analyze_calendar_for_decision_opportunities()
    current_challenges = identify_ongoing_challenges()
    yesterday_insights = review_previous_evening_reflection()
    
    # 2. Principle Selection
    anticipated_situations = extract_decision_opportunities(today_schedule)
    relevant_principles = match_principles_to_situations(
        anticipated_situations, focus_area
    )
    
    # 3. Framework Preparation
    decision_templates = prepare_decision_frameworks(
        anticipated_situations, relevant_principles
    )
    
    # 4. Plan Generation
    daily_principle_plan = create_comprehensive_daily_plan(
        today_schedule, 
        relevant_principles,
        decision_templates,
        yesterday_insights
    )
    
    # 5. PKM Integration
    update_daily_note_with_principle_plan(daily_principle_plan)
    create_knowledge_graph_connections(relevant_principles)
    set_automated_reminders(decision_templates)
    
    return {
        'daily_plan': daily_principle_plan,
        'prepared_frameworks': decision_templates,
        'principle_focus': relevant_principles,
        'integration_complete': True
    }
```

## Usage Examples

### Basic Morning Planning
```bash
/principles-morning
# Generates comprehensive morning principle plan based on calendar and yesterday's insights
```

### Work-Focused Planning
```bash
/principles-morning work
# Emphasizes work-domain principles and decision frameworks
```

### Family-Focused Planning
```bash
/principles-morning family
# Prioritizes family principles and relationship-focused frameworks
```

### Personal Development Planning
```bash
/principles-morning personal
# Focuses on personal effectiveness and growth principles
```

## Quality Standards

### Preparation Thoroughness
- All scheduled activities analyzed for decision opportunities
- Relevant principles matched to anticipated situations
- Decision frameworks pre-populated with available context
- Information gathering needs identified in advance

### Integration Completeness
- Daily note enhanced with comprehensive principle plan
- Knowledge graph connections created and updated
- Automated reminders set for key decision points
- Evening reflection preparation completed

### Actionability
- Specific principle applications identified for day
- Clear success criteria established for key decisions
- Practical preparation steps completed
- Ready-to-use decision frameworks available

## Success Metrics

### Planning Effectiveness
- Improved decision quality through systematic preparation
- Reduced decision-making time through pre-populated frameworks
- Better principle application through intentional focus
- Enhanced learning through structured daily planning

### Day Optimization
- More consistent principle application throughout day
- Better preparation for challenging decisions and interactions
- Increased alignment between daily actions and long-term values
- Systematic improvement in recurring challenging situations

---

*This command transforms morning routines into systematic principle-based planning sessions that optimize daily decision-making effectiveness and compound learning through structured preparation and intentional application.*