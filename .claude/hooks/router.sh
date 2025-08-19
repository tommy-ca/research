#!/bin/bash
# Simple command router for Claude Code agents

set -euo pipefail

# Get command from input
COMMAND="${1:-}"

# Simple logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Route commands to agents
route_command() {
    case "$COMMAND" in
        /research*)
            log "Routing to research agent"
            AGENT="research"
            ;;
        /synthesize*)
            log "Routing to synthesis agent"
            AGENT="synthesis"
            ;;
        *)
            log "Unknown command: $COMMAND"
            echo "Available commands:"
            echo "  /research [topic]     - Research with quality validation"
            echo "  /synthesize [sources] - Synthesize insights from sources"
            exit 1
            ;;
    esac
    
    # Execute agent
    log "Executing $AGENT agent"
    exec_agent "$AGENT" "$COMMAND"
}

# Execute the selected agent
exec_agent() {
    local agent="$1"
    local command="$2"
    
    AGENT_FILE=".claude/agents/${agent}.md"
    
    if [[ -f "$AGENT_FILE" ]]; then
        log "Agent $agent processing: $command"
        # Agent will handle the actual execution
        echo "Agent: $agent"
        echo "Command: $command"
    else
        log "Agent file not found: $AGENT_FILE"
        exit 1
    fi
}

# Main execution
route_command