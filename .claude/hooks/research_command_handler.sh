#!/bin/bash

# Research Command Handler for Claude Code
# Routes research commands to appropriate specialized agents
# Based on: https://docs.anthropic.com/en/docs/claude-code/hooks

set -euo pipefail

# Configuration
CLAUDE_AGENTS_DIR=".claude/agents"
LOG_FILE=".claude/logs/command_routing.log"
RESEARCH_CONFIG=".claude/settings.json"

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$LOG_FILE"
}

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Enhanced parameter validation functions
validate_research_parameters() {
    local command="$1"
    log_message "INFO" "Validating research parameters for: $command"
    
    # Extract topic (required parameter)
    if ! echo "$command" | grep -q '"[^"]*"'; then
        log_message "ERROR" "Missing required topic parameter in quotes"
        echo "Error: Research topic must be provided in quotes"
        echo "Usage: /research \"your research topic\" [options]"
        return 1
    fi
    
    # Validate depth parameter if present
    if echo "$command" | grep -q -- "--depth="; then
        local depth=$(echo "$command" | sed -n 's/.*--depth=\([^ ]*\).*/\1/p')
        case "$depth" in
            shallow|moderate|comprehensive|exhaustive) ;;
            *) 
                log_message "ERROR" "Invalid depth parameter: $depth"
                echo "Error: --depth must be one of: shallow, moderate, comprehensive, exhaustive"
                return 1
                ;;
        esac
    fi
    
    # Validate timeline parameter if present
    if echo "$command" | grep -q -- "--timeline="; then
        local timeline=$(echo "$command" | sed -n 's/.*--timeline=\([0-9]*\).*/\1/p')
        if [[ ! "$timeline" =~ ^[0-9]+$ ]] || [[ "$timeline" -lt 1 ]] || [[ "$timeline" -gt 90 ]]; then
            log_message "ERROR" "Invalid timeline parameter: $timeline"
            echo "Error: --timeline must be a number between 1 and 90 days"
            return 1
        fi
    fi
    
    return 0
}

validate_validation_parameters() {
    local command="$1"
    log_message "INFO" "Validating validation parameters for: $command"
    
    # Extract claim/finding (required parameter)
    if ! echo "$command" | grep -q '"[^"]*"'; then
        log_message "ERROR" "Missing required claim/finding parameter in quotes"
        echo "Error: Claim or finding to validate must be provided in quotes"
        echo "Usage: /research-validate \"claim to validate\" [options]"
        return 1
    fi
    
    # Validate sources parameter if present
    if echo "$command" | grep -q -- "--sources="; then
        local sources=$(echo "$command" | sed -n 's/.*--sources=\([0-9]*\).*/\1/p')
        if [[ ! "$sources" =~ ^[0-9]+$ ]] || [[ "$sources" -lt 3 ]] || [[ "$sources" -gt 20 ]]; then
            log_message "ERROR" "Invalid sources parameter: $sources"
            echo "Error: --sources must be a number between 3 and 20"
            return 1
        fi
    fi
    
    # Validate confidence parameter if present
    if echo "$command" | grep -q -- "--confidence="; then
        local confidence=$(echo "$command" | sed -n 's/.*--confidence=\([0-9.]*\).*/\1/p')
        if ! awk "BEGIN {exit !($confidence >= 0.5 && $confidence <= 1.0)}"; then
            log_message "ERROR" "Invalid confidence parameter: $confidence"
            echo "Error: --confidence must be a decimal between 0.5 and 1.0"
            return 1
        fi
    fi
    
    return 0
}

validate_plan_id() {
    local command="$1"
    log_message "INFO" "Validating plan ID for: $command"
    
    # Extract plan ID (required parameter)
    local plan_id=$(echo "$command" | sed -n 's|/research-execute \([^ ]*\).*|\1|p')
    if [[ -z "$plan_id" ]]; then
        log_message "ERROR" "Missing required plan ID parameter"
        echo "Error: Plan ID is required for research execution"
        echo "Usage: /research-execute <plan-id> [options]"
        return 1
    fi
    
    # Validate plan ID format (should be alphanumeric with hyphens)
    if [[ ! "$plan_id" =~ ^[a-zA-Z0-9-]+$ ]]; then
        log_message "ERROR" "Invalid plan ID format: $plan_id"
        echo "Error: Plan ID must contain only letters, numbers, and hyphens"
        return 1
    fi
    
    return 0
}

validate_research_id() {
    local command="$1"
    log_message "INFO" "Validating research ID for: $command"
    
    # Extract research ID (required parameter)
    local research_id=$(echo "$command" | sed -n 's|/research-refine \([^ ]*\).*|\1|p')
    if [[ -z "$research_id" ]]; then
        log_message "ERROR" "Missing required research ID parameter"
        echo "Error: Research ID is required for refinement"
        echo "Usage: /research-refine <research-id> [options]"
        return 1
    fi
    
    return 0
}

validate_file_parameter() {
    local command="$1"
    log_message "INFO" "Validating file parameter for: $command"
    
    # Extract file path (required parameter)
    if ! echo "$command" | grep -q '"[^"]*"'; then
        log_message "ERROR" "Missing required file parameter in quotes"
        echo "Error: File path must be provided in quotes"
        echo "Usage: /review \"path/to/file.md\" [options]"
        return 1
    fi
    
    return 0
}

display_enhanced_help() {
    cat << 'EOF'
Enhanced Research Commands - Claude Code Integration

DEEP RESEARCH COMMANDS:
  /research-deep "<topic>" [options]     - Multi-stage comprehensive research
    Options:
      --depth=LEVEL                      shallow|moderate|comprehensive|exhaustive
      --sources=TYPES                    academic,industry,government,journalistic,mixed
      --geography=SCOPE                  local,national,international,global
      --timeline=DAYS                    Research deadline (1-90 days)
      --quality=STANDARD                 draft,standard,academic,publication
      --strategy=APPROACH                systematic,exploratory,targeted,comparative
      --collaboration=MODE               solo,peer-review,multi-agent,expert-panel
      --output-format=FORMAT             markdown,json,structured-report,presentation
      --progress-reporting=FREQ          none,milestone,daily,real-time
      --bias-sensitivity=LEVEL           low,moderate,high,maximum
      --reproducibility=LEVEL            basic,standard,full,academic

  /research-plan "<topic>" [options]     - Create detailed research plan
  /research-execute <plan-id> [options]  - Execute planned research
  /research-refine <research-id> [options] - Iterative research improvement
  /research-status [research-id] [options] - Progress monitoring

VALIDATION COMMANDS:
  /research-validate "<claim>" [options] - Multi-source validation
    Options:
      --sources=COUNT                    Minimum independent sources (3-20)
      --confidence=THRESHOLD             Required confidence level (0.5-1.0)
      --diversity=REQUIREMENTS           geographical,temporal,methodological,institutional
      --verification=METHOD              triangulation,expert-consensus,meta-analysis
      --bias-check=SCOPE                selection,confirmation,cultural,temporal

  /research-gap "<domain>" [options]     - Systematic gap analysis
    Options:
      --period=YEARS                     Analysis timeframe
      --gap-types=LIST                   empirical,theoretical,methodological,practical
      --priority=CRITERIA                impact,feasibility,novelty,urgency
      --scope=LEVEL                      narrow,broad,comprehensive
      --output=FORMAT                    summary,detailed,recommendations,research-proposals

QUALITY ASSURANCE COMMANDS:
  /review "<file>" [options]            - Comprehensive systematic review
  /review-methodology "<file>" [options] - Methodology validation
  /validate-sources "<file>" [options]  - Source quality assessment
  /detect-bias "<file>" [options]       - Multi-dimensional bias detection

SYNTHESIS COMMANDS:
  /research-synthesize [options]        - Cross-domain research integration
  /framework-develop "<domain>" [options] - Framework development
  /pattern-analyze "<collection>" [options] - Pattern identification
  /conflict-resolve "<sources>" [options] - Evidence-based conflict resolution

HELP AND STATUS:
  /research-help                        - Display this help
  /research-status [research-id]        - Show research progress

EXAMPLES:
  /research-deep "cryptocurrency regulation impact" --depth=comprehensive --timeline=14
  /research-validate "blockchain reduces transaction costs by 30%" --sources=5 --confidence=0.85
  /review "research-output.md" --criteria=all --standard=academic

For detailed parameter descriptions and usage examples, see: .claude/agents/research.md
EOF
}

# Parse the user prompt to extract command and parameters
USER_COMMAND="$1"
log_message "INFO" "Processing command: $USER_COMMAND"

# Enhanced command routing logic with parameter validation
case "$USER_COMMAND" in
    "/research-deep"*)
        log_message "INFO" "Routing to research agent for comprehensive research"
        AGENT="research"
        COMMAND_TYPE="multi_stage_research"
        validate_research_parameters "$USER_COMMAND"
        ;;
    
    "/research-plan"*)
        log_message "INFO" "Routing to research agent for research planning"
        AGENT="research"
        COMMAND_TYPE="research_planning"
        ;;
    
    "/research-execute"*)
        log_message "INFO" "Routing to research agent for research execution"
        AGENT="research"
        COMMAND_TYPE="research_execution"
        validate_plan_id "$USER_COMMAND"
        ;;
    
    "/research-validate"*)
        log_message "INFO" "Routing to research agent for validation"
        AGENT="research"
        COMMAND_TYPE="advanced_validation"
        validate_validation_parameters "$USER_COMMAND"
        ;;
    
    "/research-gap"*)
        log_message "INFO" "Routing to research agent for gap analysis"
        AGENT="research"
        COMMAND_TYPE="systematic_gap_analysis"
        ;;
    
    "/research-refine"*)
        log_message "INFO" "Routing to research agent for research refinement"
        AGENT="research"
        COMMAND_TYPE="iterative_refinement"
        validate_research_id "$USER_COMMAND"
        ;;
    
    "/research-status"*)
        log_message "INFO" "Routing to research agent for status monitoring"
        AGENT="research"
        COMMAND_TYPE="progress_monitoring"
        ;;
    
    "/research-synthesize"*)
        log_message "INFO" "Routing to synthesis agent"
        AGENT="synthesis"
        COMMAND_TYPE="cross_domain_synthesis"
        ;;
    
    "/framework-develop"*)
        log_message "INFO" "Routing to synthesis agent for framework development"
        AGENT="synthesis"
        COMMAND_TYPE="framework_development"
        ;;
    
    "/pattern-analyze"*)
        log_message "INFO" "Routing to synthesis agent for pattern analysis"
        AGENT="synthesis"
        COMMAND_TYPE="pattern_analysis"
        ;;
    
    "/review"*)
        log_message "INFO" "Routing to review agent"
        AGENT="review"
        COMMAND_TYPE="systematic_quality_review"
        validate_file_parameter "$USER_COMMAND"
        ;;
    
    "/review-methodology"*)
        log_message "INFO" "Routing to review agent for methodology review"
        AGENT="review"
        COMMAND_TYPE="methodology_review"
        ;;
    
    "/validate-sources"*)
        log_message "INFO" "Routing to review agent for source validation"
        AGENT="review"
        COMMAND_TYPE="source_validation"
        ;;
    
    "/detect-bias"*)
        log_message "INFO" "Routing to review agent for bias detection"
        AGENT="review"
        COMMAND_TYPE="bias_detection"
        ;;
    
    "/conflict-resolve"*)
        log_message "INFO" "Routing to synthesis agent for conflict resolution"
        AGENT="synthesis"
        COMMAND_TYPE="conflict_resolution"
        ;;
    
    "/research-help"*)
        log_message "INFO" "Displaying research command help"
        display_enhanced_help
        exit 0
        ;;
    
    *)
        log_message "WARN" "Unrecognized research command: $USER_COMMAND"
        display_enhanced_help
        exit 1
        ;;
esac

# Validate agent exists
AGENT_FILE="$CLAUDE_AGENTS_DIR/$AGENT.md"
if [[ ! -f "$AGENT_FILE" ]]; then
    log_message "ERROR" "Agent file not found: $AGENT_FILE"
    echo "Error: Agent '$AGENT' not found. Please check agent configuration."
    exit 1
fi

# Parse command parameters
parse_parameters() {
    local cmd="$1"
    # Extract parameters using pattern matching
    # This is a simplified parser - could be enhanced with proper argument parsing
    echo "$cmd" | sed 's|^/[a-z-]*||' | xargs
}

PARAMETERS=$(parse_parameters "$USER_COMMAND")
log_message "INFO" "Command parameters: $PARAMETERS"

# Set environment variables for the agent
export RESEARCH_COMMAND_TYPE="$COMMAND_TYPE"
export RESEARCH_AGENT="$AGENT"
export RESEARCH_PARAMETERS="$PARAMETERS"
export RESEARCH_TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
export RESEARCH_LOG_FILE="$LOG_FILE"

# Quality gate check - ensure agent meets requirements
quality_check() {
    local agent="$1"
    local command_type="$2"
    
    # Check if agent is enabled in settings
    if command -v jq >/dev/null 2>&1 && [[ -f "$RESEARCH_CONFIG" ]]; then
        local enabled=$(jq -r ".agents.research_agents.${agent//-/_}.enabled // true" "$RESEARCH_CONFIG")
        if [[ "$enabled" != "true" ]]; then
            log_message "WARN" "Agent $agent is disabled in configuration"
            return 1
        fi
    fi
    
    # Check minimum quality requirements
    case "$command_type" in
        "quality_review"|"methodology_review"|"source_validation"|"bias_detection")
            # Ensure research files exist before review
            if [[ "$PARAMETERS" =~ ^[[:space:]]*$ ]]; then
                log_message "ERROR" "Quality review commands require file parameter"
                echo "Error: Quality review commands require a file to review"
                return 1
            fi
            ;;
    esac
    
    return 0
}

# Perform quality check
if ! quality_check "$AGENT" "$COMMAND_TYPE"; then
    log_message "ERROR" "Quality check failed for agent $AGENT"
    exit 1
fi

# Execute the agent with proper context
log_message "INFO" "Executing agent $AGENT with command type $COMMAND_TYPE"

# Create a context message for the agent
CONTEXT_MESSAGE="I am the $AGENT agent handling a $COMMAND_TYPE request. 

Original command: $USER_COMMAND
Parameters: $PARAMETERS
Timestamp: $RESEARCH_TIMESTAMP

Based on my agent specification in $AGENT_FILE, I will:
1. Parse the command parameters according to my documented syntax
2. Execute the appropriate research workflow
3. Apply quality standards as specified in my configuration
4. Generate output according to the requested format
5. Provide actionable recommendations where applicable

Following Claude Code's official agent patterns and quality standards."

# Log the execution
log_message "INFO" "Agent execution completed for $AGENT"

# Output the context message for Claude to process
echo "$CONTEXT_MESSAGE"

# Return success
exit 0