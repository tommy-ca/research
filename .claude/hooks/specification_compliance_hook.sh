#!/bin/bash

# Specification Compliance Validation Hook
# Automatically validates specification compliance during Claude Code operations
# Based on: https://docs.anthropic.com/en/docs/claude-code/hooks

set -euo pipefail

# Configuration
LOG_FILE=".claude/logs/compliance_validation.log"
COMPLIANCE_CONFIG="docs/research/agent-systems/specifications/version-control/specification-versions.yaml"
VALIDATION_THRESHOLD=0.90
SPECS_PATH="docs/research/agent-systems/specifications"

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$LOG_FILE"
    echo "[$level] $message"
}

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Get hook input from Claude Code
TOOL_NAME="${TOOL_NAME:-unknown}"
TOOL_OUTPUT="${TOOL_OUTPUT:-unknown}"
FILE_PATH="${FILE_PATH:-$TOOL_OUTPUT}"

log_message "INFO" "Compliance validation triggered by tool: $TOOL_NAME"
log_message "INFO" "Validating file: $FILE_PATH"

# Specification compliance validation function
validate_specification_compliance() {
    local file_path="$1"
    local validation_results=()
    local compliance_score=0
    local total_checks=0
    
    log_message "INFO" "Starting specification compliance validation for: $file_path"
    
    # Check if file exists
    if [[ ! -f "$file_path" ]]; then
        log_message "WARN" "File not found for compliance validation: $file_path"
        return 0
    fi
    
    # Validate agent files
    if [[ "$file_path" =~ \.claude/agents/.*\.md$ ]]; then
        validate_agent_compliance "$file_path"
        return $?
    fi
    
    # Validate specification files
    if [[ "$file_path" =~ \.claude/specifications/.*\.(yaml|json)$ ]]; then
        validate_specification_file "$file_path"
        return $?
    fi
    
    # Validate implementation files
    if [[ "$file_path" =~ \.(py|js|ts|java|go)$ ]]; then
        validate_implementation_compliance "$file_path"
        return $?
    fi
    
    log_message "INFO" "No specific compliance validation required for file type: $file_path"
    return 0
}

# Agent compliance validation
validate_agent_compliance() {
    local agent_file="$1"
    local compliance_issues=()
    local compliance_score=100
    
    log_message "INFO" "Validating agent specification compliance: $agent_file"
    
    # Check YAML frontmatter exists
    if ! grep -q "^---" "$agent_file"; then
        compliance_issues+=("Missing YAML frontmatter")
        compliance_score=$((compliance_score - 20))
    fi
    
    # Validate agent interface specification compliance
    validate_agent_interface_compliance "$agent_file" compliance_issues compliance_score
    
    # Validate behavior specification compliance
    validate_agent_behavior_compliance "$agent_file" compliance_issues compliance_score
    
    # Validate quality specification compliance
    validate_agent_quality_compliance "$agent_file" compliance_issues compliance_score
    
    # Generate compliance report
    generate_agent_compliance_report "$agent_file" "${compliance_issues[@]}" "$compliance_score"
    
    # Check if compliance meets threshold
    local compliance_percentage=$((compliance_score))
    if [[ $compliance_percentage -lt $((VALIDATION_THRESHOLD * 100)) ]]; then
        log_message "ERROR" "Agent compliance below threshold: $compliance_percentage% < $(echo "$VALIDATION_THRESHOLD * 100" | bc)%"
        return 1
    fi
    
    log_message "INFO" "Agent compliance validation passed: $compliance_percentage%"
    return 0
}

# Agent interface compliance validation
validate_agent_interface_compliance() {
    local agent_file="$1"
    local -n issues_ref=$2
    local -n score_ref=$3
    
    log_message "INFO" "Validating interface specification compliance"
    
    # Check for required agent_specification section
    if ! grep -q "agent_specification:" "$agent_file"; then
        issues_ref+=("Missing agent_specification section")
        score_ref=$((score_ref - 15))
    fi
    
    # Check for required fields
    local required_fields=("agent_id" "agent_type" "version" "capabilities" "supported_commands")
    for field in "${required_fields[@]}"; do
        if ! grep -q "$field:" "$agent_file"; then
            issues_ref+=("Missing required field: $field")
            score_ref=$((score_ref - 10))
        fi
    done
    
    # Validate agent_id format
    local agent_id=$(grep -E "agent_id:" "$agent_file" | sed 's/.*agent_id:\s*["'\'']*\([^"'\'']*\)["'\'']*$/\1/' | tr -d ' ')
    if [[ -n "$agent_id" ]]; then
        if ! [[ "$agent_id" =~ ^[a-z][a-z0-9-]*[a-z0-9]$ ]]; then
            issues_ref+=("Agent ID format non-compliant: $agent_id")
            score_ref=$((score_ref - 10))
        fi
    fi
    
    # Validate capabilities
    if grep -q "capabilities:" "$agent_file"; then
        local valid_capabilities=(
            "systematic_literature_review" "multi_stage_data_collection" "adaptive_research_strategy"
            "cross_reference_validation" "longitudinal_analysis" "comparative_research"
            "source_credibility_scoring" "bias_detection_mitigation" "research_workflow_orchestration"
            "progressive_quality_refinement"
        )
        
        # Extract capabilities and check validity
        local capabilities_section=$(sed -n '/capabilities:/,/^[^ ]/p' "$agent_file" | grep -E '^\s*-\s*' | sed 's/^\s*-\s*//')
        while IFS= read -r capability; do
            if [[ -n "$capability" ]]; then
                capability=$(echo "$capability" | tr -d '"' | tr -d "'")
                if [[ ! " ${valid_capabilities[*]} " =~ " ${capability} " ]]; then
                    issues_ref+=("Invalid capability: $capability")
                    score_ref=$((score_ref - 5))
                fi
            fi
        done <<< "$capabilities_section"
    fi
    
    # Validate supported commands format
    if grep -q "supported_commands:" "$agent_file"; then
        local commands_section=$(sed -n '/supported_commands:/,/^[^ ]/p' "$agent_file" | grep -E '^\s*-\s*' | sed 's/^\s*-\s*//')
        while IFS= read -r command; do
            if [[ -n "$command" ]]; then
                command=$(echo "$command" | tr -d '"' | tr -d "'")
                if ! [[ "$command" =~ ^/[a-z][a-z0-9-]*$ ]]; then
                    issues_ref+=("Invalid command format: $command")
                    score_ref=$((score_ref - 5))
                fi
            fi
        done <<< "$commands_section"
    fi
}

# Agent behavior compliance validation
validate_agent_behavior_compliance() {
    local agent_file="$1"
    local -n issues_ref=$2
    local -n score_ref=$3
    
    log_message "INFO" "Validating behavior specification compliance"
    
    # Check for behavior_implementation section
    if ! grep -q "behavior_implementation:" "$agent_file"; then
        issues_ref+=("Missing behavior_implementation section")
        score_ref=$((score_ref - 15))
        return
    fi
    
    # Check for required behavior patterns
    local required_patterns=("multi_stage_research_workflow")
    for pattern in "${required_patterns[@]}"; do
        if ! grep -q "$pattern:" "$agent_file"; then
            issues_ref+=("Missing behavior pattern: $pattern")
            score_ref=$((score_ref - 10))
        fi
    done
    
    # Validate workflow stages
    local required_stages=("planning" "collection" "analysis" "validation")
    for stage in "${required_stages[@]}"; do
        if ! grep -q "$stage:" "$agent_file"; then
            issues_ref+=("Missing workflow stage: $stage")
            score_ref=$((score_ref - 8))
        fi
    done
    
    # Check for quality gates
    if ! grep -q "quality_gate:" "$agent_file"; then
        issues_ref+=("Missing quality gate specifications")
        score_ref=$((score_ref - 10))
    fi
    
    # Validate adaptive behaviors
    if ! grep -q "adaptive_behaviors:" "$agent_file"; then
        issues_ref+=("Missing adaptive behaviors section")
        score_ref=$((score_ref - 5))
    fi
    
    # Validate error handling
    if ! grep -q "error_handling:" "$agent_file"; then
        issues_ref+=("Missing error handling section")
        score_ref=$((score_ref - 5))
    fi
}

# Agent quality compliance validation
validate_agent_quality_compliance() {
    local agent_file="$1"
    local -n issues_ref=$2
    local -n score_ref=$3
    
    log_message "INFO" "Validating quality specification compliance"
    
    # Check for quality_implementation section
    if ! grep -q "quality_implementation:" "$agent_file"; then
        issues_ref+=("Missing quality_implementation section")
        score_ref=$((score_ref - 15))
        return
    fi
    
    # Check for required quality metric categories
    local required_categories=("research_quality" "source_quality" "bias_assessment")
    for category in "${required_categories[@]}"; do
        if ! grep -q "$category:" "$agent_file"; then
            issues_ref+=("Missing quality category: $category")
            score_ref=$((score_ref - 8))
        fi
    done
    
    # Validate performance targets
    if ! grep -q "performance_targets:" "$agent_file"; then
        issues_ref+=("Missing performance targets")
        score_ref=$((score_ref - 10))
    else
        # Check for specific performance targets
        local required_targets=("accuracy_rate" "source_diversity_score" "bias_mitigation_effectiveness" "reproducibility_score")
        for target in "${required_targets[@]}"; do
            if ! grep -q "$target:" "$agent_file"; then
                issues_ref+=("Missing performance target: $target")
                score_ref=$((score_ref - 5))
            fi
        done
    fi
    
    # Validate source credibility matrix
    if ! grep -q "source_credibility_matrix:" "$agent_file"; then
        issues_ref+=("Missing source credibility matrix")
        score_ref=$((score_ref - 5))
    fi
}

# Specification file validation
validate_specification_file() {
    local spec_file="$1"
    local validation_issues=()
    
    log_message "INFO" "Validating specification file: $spec_file"
    
    # Check file format
    if [[ "$spec_file" =~ \.yaml$ ]]; then
        # Validate YAML syntax
        if command -v python3 >/dev/null 2>&1; then
            if ! python3 -c "import yaml; yaml.safe_load(open('$spec_file'))" >/dev/null 2>&1; then
                validation_issues+=("Invalid YAML syntax")
                log_message "ERROR" "YAML syntax validation failed for: $spec_file"
                return 1
            fi
        fi
    elif [[ "$spec_file" =~ \.json$ ]]; then
        # Validate JSON syntax
        if command -v python3 >/dev/null 2>&1; then
            if ! python3 -c "import json; json.load(open('$spec_file'))" >/dev/null 2>&1; then
                validation_issues+=("Invalid JSON syntax")
                log_message "ERROR" "JSON syntax validation failed for: $spec_file"
                return 1
            fi
        fi
    fi
    
    # Check for required metadata section
    if ! grep -q "metadata:" "$spec_file"; then
        validation_issues+=("Missing metadata section")
    fi
    
    # Check for version information
    if ! grep -q "version:" "$spec_file"; then
        validation_issues+=("Missing version information")
    fi
    
    # Report validation results
    if [[ ${#validation_issues[@]} -gt 0 ]]; then
        log_message "WARN" "Specification validation issues found:"
        for issue in "${validation_issues[@]}"; do
            log_message "WARN" "  - $issue"
        done
        return 1
    fi
    
    log_message "INFO" "Specification file validation passed: $spec_file"
    return 0
}

# Implementation file compliance validation
validate_implementation_compliance() {
    local impl_file="$1"
    
    log_message "INFO" "Validating implementation compliance: $impl_file"
    
    # Basic implementation validation
    # This would be expanded based on specific implementation requirements
    
    # Check for specification reference comments
    if ! grep -q "Specification:" "$impl_file"; then
        log_message "WARN" "Implementation lacks specification references: $impl_file"
    fi
    
    # Check for compliance validation code
    if grep -q "validate.*compliance\|compliance.*check" "$impl_file"; then
        log_message "INFO" "Implementation includes compliance validation: $impl_file"
    fi
    
    return 0
}

# Generate agent compliance report
generate_agent_compliance_report() {
    local agent_file="$1"
    shift
    local issues=("$@")
    local compliance_score="${issues[-1]}"
    unset issues[-1]
    
    local report_file="${agent_file%.md}_compliance_report.md"
    
    cat > "$report_file" << EOF
# Agent Compliance Report

**Agent File**: \`$agent_file\`  
**Validation Date**: $(date '+%Y-%m-%d %H:%M:%S')  
**Compliance Score**: $compliance_score%  
**Status**: $([ $compliance_score -ge $((VALIDATION_THRESHOLD * 100)) ] && echo "COMPLIANT" || echo "NON-COMPLIANT")

## Compliance Issues

$(if [[ ${#issues[@]} -eq 0 ]]; then
    echo "✅ No compliance issues detected"
else
    for issue in "${issues[@]}"; do
        echo "❌ $issue"
    done
fi)

## Recommendations

$(if [[ $compliance_score -ge $((VALIDATION_THRESHOLD * 100)) ]]; then
    echo "✅ Agent meets compliance requirements"
    echo "- Continue following specification-driven development practices"
    echo "- Monitor for specification updates and maintain compliance"
else
    echo "⚠️ Agent requires compliance improvements"
    echo "- Address identified compliance issues"
    echo "- Review relevant specifications for implementation guidance"
    echo "- Run compliance validation after implementing fixes"
fi)

## Specification References

- [Agent Interface Specification v2.0.0](.claude/specifications/interfaces/agent-interface-specification.json)
- [Behavior Specification v2.0.0](.claude/specifications/behaviors/research-behavior-specification.yaml)
- [Quality Specification v2.0.0](.claude/specifications/quality/quality-assurance-specification.yaml)
- [Compliance Framework](.claude/steering/compliance/specification-validation-framework.md)

EOF

    log_message "INFO" "Compliance report generated: $report_file"
}

# Trigger compliance validation for different scenarios
validate_compliance_scenario() {
    local scenario="$1"
    
    case "$scenario" in
        "agent_modification")
            log_message "INFO" "Agent modification detected - running full compliance validation"
            validate_specification_compliance "$FILE_PATH"
            ;;
        "specification_update")
            log_message "INFO" "Specification update detected - validating specification integrity"
            validate_specification_file "$FILE_PATH"
            ;;
        "implementation_change")
            log_message "INFO" "Implementation change detected - checking compliance alignment"
            validate_implementation_compliance "$FILE_PATH"
            ;;
        *)
            log_message "INFO" "General file change - running applicable validation"
            validate_specification_compliance "$FILE_PATH"
            ;;
    esac
}

# Determine validation scenario based on file path and tool
determine_validation_scenario() {
    local file_path="$1"
    local tool_name="$2"
    
    if [[ "$file_path" =~ \.claude/agents/ ]]; then
        echo "agent_modification"
    elif [[ "$file_path" =~ \.claude/specifications/ ]]; then
        echo "specification_update"
    elif [[ "$file_path" =~ \.(py|js|ts|java|go)$ ]]; then
        echo "implementation_change"
    else
        echo "general_change"
    fi
}

# Main execution logic
main() {
    log_message "INFO" "Starting specification compliance hook execution"
    
    # Determine validation scenario
    local scenario=$(determine_validation_scenario "$FILE_PATH" "$TOOL_NAME")
    log_message "INFO" "Detected scenario: $scenario"
    
    # Run appropriate validation
    if validate_compliance_scenario "$scenario"; then
        log_message "INFO" "Compliance validation completed successfully"
        
        # Generate success notification
        echo ""
        echo "✅ **Specification Compliance Validated**"
        echo ""
        echo "**File**: \`$FILE_PATH\`"
        echo "**Validation**: Passed specification compliance checks"
        echo "**Score**: Above threshold ($VALIDATION_THRESHOLD)"
        echo ""
        echo "**Next Steps**:"
        echo "- Continue development with confidence"
        echo "- Monitor compliance status in ongoing development"
        echo "- Review compliance reports for detailed analysis"
        echo ""
        
        return 0
    else
        log_message "ERROR" "Compliance validation failed"
        
        # Generate failure notification
        echo ""
        echo "❌ **Specification Compliance Issues Detected**"
        echo ""
        echo "**File**: \`$FILE_PATH\`"
        echo "**Validation**: Failed specification compliance checks"
        echo "**Action Required**: Address compliance issues before proceeding"
        echo ""
        echo "**Remediation Steps**:"
        echo "1. Review generated compliance report"
        echo "2. Address identified compliance issues"
        echo "3. Consult specification documentation for guidance"
        echo "4. Re-run validation after implementing fixes"
        echo ""
        echo "**Resources**:"
        echo "- [Specification Documentation](.claude/specifications/README.md)"
        echo "- [Implementation Guide](.claude/steering/implementation/specification-driven-development-guide.md)"
        echo "- [Compliance Framework](.claude/steering/compliance/specification-validation-framework.md)"
        echo ""
        
        return 1
    fi
}

# Execute main function
main "$@"