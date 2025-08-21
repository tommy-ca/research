#!/bin/bash
# PKM Auto-Processing Hook
# Automatically processes PKM vault changes

# Check if file is in inbox
if [[ "$1" == *"vault/0-inbox"* ]]; then
    echo "Processing inbox item: $1"
    # Extract concepts and suggest categorization
    claude-code --silent "/pkm-process '$1'"
fi

# Check if file is a daily note
if [[ "$1" == *"vault/daily"* ]]; then
    echo "Daily note detected: $1"
    # Extract tasks and update project tracking
    claude-code --silent "/pkm-extract-tasks '$1'"
fi

# Check for new zettelkasten note
if [[ "$1" == *"vault/permanent/notes"* ]]; then
    echo "Zettelkasten note created: $1"
    # Update index and create bidirectional links
    claude-code --silent "/pkm-update-index '$1'"
    claude-code --silent "/pkm-link-suggest '$1'"
fi

# Weekly review reminder (Sundays at 5pm)
if [[ "$(date +%u)" == "7" ]] && [[ "$(date +%H)" == "17" ]]; then
    echo "Weekly review time!"
    claude-code "/pkm-review weekly"
fi

# Daily note creation (9am every day)
if [[ "$(date +%H:%M)" == "09:00" ]]; then
    echo "Creating daily note..."
    claude-code "/pkm-daily"
fi

# Git auto-commit for vault changes
if [[ "$1" == *"vault/"* ]]; then
    cd "$(dirname "$1")"
    git add "$1"
    git commit -m "PKM: Auto-save $(basename "$1")" --quiet
fi