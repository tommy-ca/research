#!/bin/bash
# Simple command router for Claude Code agents with custom command support

set -euo pipefail

# Get command from input
COMMAND="${1:-}"

# Custom commands registry
declare -A CUSTOM_COMMANDS

# Simple logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Load custom commands from .claude/commands/*.md
load_custom_commands() {
    if [[ -d ".claude/commands" ]]; then
        for cmd_file in .claude/commands/*.md; do
            [[ -f "$cmd_file" ]] || continue
            pattern=$(grep "^pattern:" "$cmd_file" | sed 's/pattern: *//')
            agent=$(grep "^agent:" "$cmd_file" | sed 's/agent: *//')
            if [[ -n "$pattern" && -n "$agent" ]]; then
                CUSTOM_COMMANDS["$pattern"]="$agent"
                log "Loaded custom command: $pattern -> $agent"
            fi
        done
    fi
}

# Route commands to agents
route_command() {
    # Check custom commands first
    for pattern in "${!CUSTOM_COMMANDS[@]}"; do
        if [[ "$COMMAND" == $pattern* ]]; then
            AGENT="${CUSTOM_COMMANDS[$pattern]}"
            log "Routing to $AGENT agent via custom command $pattern"
            exec_agent "$AGENT" "$COMMAND"
            return
        fi
    done
    
    # Default built-in commands
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
            for pattern in "${!CUSTOM_COMMANDS[@]}"; do
                echo "  $pattern [args]      - Custom command"
            done
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
load_custom_commands
route_command