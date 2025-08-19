#!/bin/bash

# Quality Check Hook for Claude Code
# Automatically triggers quality validation after content creation
# Based on: https://docs.anthropic.com/en/docs/claude-code/hooks

set -euo pipefail

# Configuration
LOG_FILE=".claude/logs/quality_check.log"
QUALITY_THRESHOLD=100  # Minimum lines for auto-review
RESEARCH_CONFIG=".claude/settings.json"

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$LOG_FILE"
}

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Get hook input from Claude Code
TOOL_NAME="${TOOL_NAME:-unknown}"
TOOL_OUTPUT="${TOOL_OUTPUT:-unknown}"
FILE_PATH="${FILE_PATH:-$TOOL_OUTPUT}"

log_message "INFO" "Quality check triggered by tool: $TOOL_NAME"
log_message "INFO" "File path: $FILE_PATH"

# Check if file exists and is substantial
if [[ ! -f "$FILE_PATH" ]]; then
    log_message "WARN" "File not found for quality check: $FILE_PATH"
    exit 0
fi

# Get file statistics
FILE_SIZE=$(wc -c < "$FILE_PATH" 2>/dev/null || echo "0")
LINE_COUNT=$(wc -l < "$FILE_PATH" 2>/dev/null || echo "0")
WORD_COUNT=$(wc -w < "$FILE_PATH" 2>/dev/null || echo "0")

log_message "INFO" "File stats - Size: $FILE_SIZE bytes, Lines: $LINE_COUNT, Words: $WORD_COUNT"

# Determine if file warrants quality review
should_review() {
    local file_path="$1"
    local line_count="$2"
    local word_count="$3"
    
    # Check file type - only review documentation and research files
    case "$file_path" in
        *.md|*.txt|*.rst|*.adoc)
            # Markdown and text files
            ;;
        docs/*)
            # Documentation directory
            ;;
        knowledge-base/*)
            # Knowledge base files
            ;;
        experiments/*/README*|experiments/*/*.md)
            # Experiment documentation
            ;;
        *)
            log_message "INFO" "File type not subject to auto-review: $file_path"
            return 1
            ;;
    esac
    
    # Check size thresholds
    if [[ "$line_count" -lt "$QUALITY_THRESHOLD" ]]; then
        log_message "INFO" "File below line threshold ($line_count < $QUALITY_THRESHOLD)"
        return 1
    fi
    
    if [[ "$word_count" -lt 500 ]]; then
        log_message "INFO" "File below word threshold ($word_count < 500)"
        return 1
    fi
    
    return 0
}

# Check if auto-review is enabled
if command -v jq >/dev/null 2>&1 && [[ -f "$RESEARCH_CONFIG" ]]; then
    AUTO_REVIEW_ENABLED=$(jq -r ".agents.peer_review.enabled // true" "$RESEARCH_CONFIG")
    if [[ "$AUTO_REVIEW_ENABLED" != "true" ]]; then
        log_message "INFO" "Auto-review disabled in configuration"
        exit 0
    fi
fi

# Determine if review should be triggered
if should_review "$FILE_PATH" "$LINE_COUNT" "$WORD_COUNT"; then
    log_message "INFO" "Triggering automatic quality review for: $FILE_PATH"
    
    # Create review summary message
    REVIEW_MESSAGE="📋 **Automatic Quality Check Triggered**

**File**: \`$FILE_PATH\`
**Statistics**: $LINE_COUNT lines, $WORD_COUNT words, $FILE_SIZE bytes
**Trigger**: Substantial content creation/modification
**Review Type**: Automated quality validation

**Review Process**:
1. Content structure and organization assessment
2. Writing quality and clarity evaluation  
3. Factual accuracy spot-checking (where applicable)
4. Consistency with project standards
5. Recommendations for improvement

**Note**: This is an automated quality gate. For comprehensive peer review, use \`/peer-review \"$FILE_PATH\"\`"

    echo "$REVIEW_MESSAGE"
    
    # Perform basic quality checks
    perform_basic_checks() {
        local file_path="$1"
        local issues=()
        
        # Check for basic structural elements in markdown files
        if [[ "$file_path" =~ \.md$ ]]; then
            # Check for title/heading
            if ! grep -q "^# " "$file_path"; then
                issues+=("Missing main heading (H1)")
            fi
            
            # Check for very long lines (readability)
            local long_lines=$(awk 'length > 120' "$file_path" | wc -l)
            if [[ "$long_lines" -gt 5 ]]; then
                issues+=("$long_lines lines exceed 120 characters (readability concern)")
            fi
            
            # Check for TODO/FIXME markers
            local todos=$(grep -c "TODO\|FIXME\|XXX" "$file_path" 2>/dev/null || echo "0")
            if [[ "$todos" -gt 0 ]]; then
                issues+=("$todos TODO/FIXME markers found")
            fi
            
            # Check for basic spell check (if available)
            if command -v aspell >/dev/null 2>&1; then
                local misspellings=$(aspell list < "$file_path" | wc -l)
                if [[ "$misspellings" -gt 10 ]]; then
                    issues+=("$misspellings potential spelling issues detected")
                fi
            fi
        fi
        
        # Report issues
        if [[ ${#issues[@]} -gt 0 ]]; then
            echo ""
            echo "**Quality Issues Detected**:"
            for issue in "${issues[@]}"; do
                echo "- ⚠️ $issue"
            done
            echo ""
        else
            echo ""
            echo "**Basic Quality Check**: ✅ No major issues detected"
            echo ""
        fi
        
        # Log the results
        log_message "INFO" "Basic quality check completed. Issues found: ${#issues[@]}"
        for issue in "${issues[@]}"; do
            log_message "WARN" "Quality issue: $issue"
        done
    }
    
    # Perform the basic checks
    perform_basic_checks "$FILE_PATH"
    
    # Suggest next steps
    echo "**Recommended Actions**:"
    echo "- Review the content for accuracy and completeness"
    echo "- Consider running \`/peer-review \"$FILE_PATH\"\` for comprehensive validation"
    echo "- Address any quality issues identified above"
    echo "- Ensure proper citations and references where applicable"
    echo ""
    
    log_message "INFO" "Automatic quality check completed for: $FILE_PATH"
    
else
    log_message "INFO" "File does not meet criteria for automatic review: $FILE_PATH"
fi

# Always exit successfully to avoid blocking the original tool
exit 0