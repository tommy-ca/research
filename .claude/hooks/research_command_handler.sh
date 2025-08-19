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

# Parse the user prompt to extract command and parameters
USER_COMMAND="$1"
log_message "INFO" "Processing command: $USER_COMMAND"

# Command routing logic
case "$USER_COMMAND" in
    "/research-deep"*)
        log_message "INFO" "Routing to deep-research agent"
        AGENT="deep-research"
        COMMAND_TYPE="comprehensive_research"
        ;;
    
    "/research-validate"*)
        log_message "INFO" "Routing to deep-research agent for validation"
        AGENT="deep-research"
        COMMAND_TYPE="validation"
        ;;
    
    "/research-gap"*)
        log_message "INFO" "Routing to deep-research agent for gap analysis"
        AGENT="deep-research"
        COMMAND_TYPE="gap_analysis"
        ;;
    
    "/research-synthesize"*)
        log_message "INFO" "Routing to synthesis agent"
        AGENT="synthesis"
        COMMAND_TYPE="synthesis"
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
    
    "/peer-review"*)
        log_message "INFO" "Routing to peer-review agent"
        AGENT="peer-review"
        COMMAND_TYPE="quality_review"
        ;;
    
    "/review-methodology"*)
        log_message "INFO" "Routing to peer-review agent for methodology review"
        AGENT="peer-review"
        COMMAND_TYPE="methodology_review"
        ;;
    
    "/validate-sources"*)
        log_message "INFO" "Routing to peer-review agent for source validation"
        AGENT="peer-review"
        COMMAND_TYPE="source_validation"
        ;;
    
    "/detect-bias"*)
        log_message "INFO" "Routing to peer-review agent for bias detection"
        AGENT="peer-review"
        COMMAND_TYPE="bias_detection"
        ;;
    
    "/conflict-resolve"*)
        log_message "INFO" "Routing to synthesis agent for conflict resolution"
        AGENT="synthesis"
        COMMAND_TYPE="conflict_resolution"
        ;;
    
    *)
        log_message "WARN" "Unrecognized research command: $USER_COMMAND"
        echo "Unrecognized research command. Available commands:"
        echo "  /research-deep - Comprehensive research"
        echo "  /research-validate - Validate findings"
        echo "  /research-gap - Gap analysis"
        echo "  /research-synthesize - Synthesis research"
        echo "  /framework-develop - Develop frameworks"
        echo "  /pattern-analyze - Analyze patterns"
        echo "  /peer-review - Peer review"
        echo "  /review-methodology - Review methodology"
        echo "  /validate-sources - Validate sources"
        echo "  /detect-bias - Detect bias"
        echo "  /conflict-resolve - Resolve conflicts"
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