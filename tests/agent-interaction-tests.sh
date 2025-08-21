#!/bin/bash
# Agent Interaction Test Suite
# Tests multi-agent coordination patterns

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0

# Test workspace
TEST_WORKSPACE="/tmp/agent-test-$$"
mkdir -p "$TEST_WORKSPACE"

# Logging
log() {
    echo -e "${YELLOW}[TEST]${NC} $1"
}

pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

# Mock agent commands for testing
mock_agent() {
    local agent=$1
    local command=$2
    
    case "$agent" in
        "research")
            cat << EOF
{
  "topic": "test topic",
  "summary": "Test research output",
  "quality_score": 0.92,
  "findings": ["finding1", "finding2"]
}
EOF
            ;;
        "kb-add")
            cat << EOF
{
  "id": "kb_2024_001",
  "topic": "test topic",
  "status": "added",
  "quality_score": 0.88
}
EOF
            ;;
        "kg-expand")
            cat << EOF
{
  "nodes_added": 5,
  "edges_added": 8,
  "status": "expanded"
}
EOF
            ;;
        "kc-validate")
            cat << EOF
{
  "entry": "kb_2024_001",
  "quality_score": 0.87,
  "status": "validated"
}
EOF
            ;;
        "kc-enrich")
            cat << EOF
{
  "entry": "kb_2024_001",
  "enhancements": 3,
  "new_quality": 0.94
}
EOF
            ;;
    esac
}

# Test 1: Sequential Pipeline
test_sequential_pipeline() {
    log "Testing sequential pipeline pattern"
    
    # Simulate research → KB → Graph pipeline
    RESEARCH=$(mock_agent "research" "/research test")
    echo "$RESEARCH" > "$TEST_WORKSPACE/research.json"
    
    if [ -f "$TEST_WORKSPACE/research.json" ]; then
        KB_RESULT=$(mock_agent "kb-add" "/kb-add")
        echo "$KB_RESULT" > "$TEST_WORKSPACE/kb.json"
        
        if [ -f "$TEST_WORKSPACE/kb.json" ]; then
            GRAPH_RESULT=$(mock_agent "kg-expand" "/kg-expand")
            echo "$GRAPH_RESULT" > "$TEST_WORKSPACE/graph.json"
            
            if [ -f "$TEST_WORKSPACE/graph.json" ]; then
                pass "Sequential pipeline completed successfully"
            else
                fail "Graph expansion failed"
            fi
        else
            fail "KB addition failed"
        fi
    else
        fail "Research phase failed"
    fi
}

# Test 2: Parallel Processing
test_parallel_processing() {
    log "Testing parallel processing pattern"
    
    # Run multiple agents in parallel
    {
        mock_agent "kc-validate" "/kc-validate" > "$TEST_WORKSPACE/validate.json" &
        mock_agent "kc-enrich" "/kc-enrich" > "$TEST_WORKSPACE/enrich.json" &
        mock_agent "kg-expand" "/kg-expand" > "$TEST_WORKSPACE/expand.json" &
        wait
    }
    
    # Check all outputs exist
    if [ -f "$TEST_WORKSPACE/validate.json" ] && \
       [ -f "$TEST_WORKSPACE/enrich.json" ] && \
       [ -f "$TEST_WORKSPACE/expand.json" ]; then
        pass "Parallel processing completed successfully"
    else
        fail "One or more parallel operations failed"
    fi
}

# Test 3: Conditional Routing
test_conditional_routing() {
    log "Testing conditional routing pattern"
    
    # Get quality score
    VALIDATION=$(mock_agent "kc-validate" "/kc-validate")
    QUALITY=$(echo "$VALIDATION" | jq -r '.quality_score')
    
    if (( $(echo "$QUALITY < 0.85" | bc -l) )); then
        # Quality too low, enrich
        ENRICHED=$(mock_agent "kc-enrich" "/kc-enrich")
        NEW_QUALITY=$(echo "$ENRICHED" | jq -r '.new_quality')
        
        if (( $(echo "$NEW_QUALITY > 0.90" | bc -l) )); then
            pass "Conditional enrichment successful"
        else
            fail "Enrichment didn't improve quality enough"
        fi
    else
        pass "Quality sufficient, no enrichment needed"
    fi
}

# Test 4: Error Recovery
test_error_recovery() {
    log "Testing error recovery pattern"
    
    # Simulate failure
    set +e  # Allow errors
    
    # First attempt fails
    false  # Simulate failure
    if [ $? -ne 0 ]; then
        log "First attempt failed, trying recovery"
        
        # Recovery attempt
        RECOVERY=$(mock_agent "kc-enrich" "/kc-enrich")
        if [ ! -z "$RECOVERY" ]; then
            pass "Error recovery successful"
        else
            fail "Recovery failed"
        fi
    else
        fail "Error simulation failed"
    fi
    
    set -e  # Re-enable exit on error
}

# Test 5: Data Contract Validation
test_data_contract() {
    log "Testing data contract compliance"
    
    RESEARCH=$(mock_agent "research" "/research")
    
    # Validate required fields
    HAS_TOPIC=$(echo "$RESEARCH" | jq 'has("topic")')
    HAS_SUMMARY=$(echo "$RESEARCH" | jq 'has("summary")')
    HAS_QUALITY=$(echo "$RESEARCH" | jq 'has("quality_score")')
    
    if [ "$HAS_TOPIC" = "true" ] && \
       [ "$HAS_SUMMARY" = "true" ] && \
       [ "$HAS_QUALITY" = "true" ]; then
        pass "Data contract validation passed"
    else
        fail "Data contract validation failed"
    fi
}

# Test 6: Workflow State Management
test_workflow_state() {
    log "Testing workflow state management"
    
    # Initialize workflow state
    WORKFLOW_STATE='{
        "workflow_id": "test_workflow",
        "current_step": "research",
        "steps": []
    }'
    
    # Update state for each step
    WORKFLOW_STATE=$(echo "$WORKFLOW_STATE" | jq '.current_step = "kb_add"')
    WORKFLOW_STATE=$(echo "$WORKFLOW_STATE" | jq '.steps += [{"step": "research", "status": "completed"}]')
    
    WORKFLOW_STATE=$(echo "$WORKFLOW_STATE" | jq '.current_step = "graph_update"')
    WORKFLOW_STATE=$(echo "$WORKFLOW_STATE" | jq '.steps += [{"step": "kb_add", "status": "completed"}]')
    
    # Check final state
    STEPS_COUNT=$(echo "$WORKFLOW_STATE" | jq '.steps | length')
    if [ "$STEPS_COUNT" -eq 2 ]; then
        pass "Workflow state management successful"
    else
        fail "Workflow state management failed"
    fi
}

# Test 7: Performance Benchmarking
test_performance() {
    log "Testing performance requirements"
    
    START=$(date +%s%N)
    
    # Simulate operations
    mock_agent "research" "/research" > /dev/null
    mock_agent "kb-add" "/kb-add" > /dev/null
    mock_agent "kg-expand" "/kg-expand" > /dev/null
    
    END=$(date +%s%N)
    DURATION=$((($END - $START) / 1000000))  # Convert to milliseconds
    
    if [ "$DURATION" -lt 1000 ]; then  # Should complete in under 1 second
        pass "Performance requirement met: ${DURATION}ms"
    else
        fail "Performance requirement not met: ${DURATION}ms"
    fi
}

# Test 8: Idempotency
test_idempotency() {
    log "Testing idempotent operations"
    
    # Run same operation twice
    RESULT1=$(mock_agent "kb-add" "/kb-add")
    RESULT2=$(mock_agent "kb-add" "/kb-add")
    
    ID1=$(echo "$RESULT1" | jq -r '.id')
    ID2=$(echo "$RESULT2" | jq -r '.id')
    
    if [ "$ID1" = "$ID2" ]; then
        pass "Idempotent operation successful"
    else
        fail "Operation not idempotent"
    fi
}

# Test 9: Circuit Breaker
test_circuit_breaker() {
    log "Testing circuit breaker pattern"
    
    FAILURES=0
    MAX_FAILURES=3
    
    for i in {1..5}; do
        # Simulate random failures
        if [ $((i % 2)) -eq 0 ]; then
            ((FAILURES++))
            if [ $FAILURES -ge $MAX_FAILURES ]; then
                log "Circuit breaker triggered after $FAILURES failures"
                pass "Circuit breaker working correctly"
                return
            fi
        else
            FAILURES=0  # Reset on success
        fi
    done
    
    fail "Circuit breaker did not trigger"
}

# Test 10: Batch Processing
test_batch_processing() {
    log "Testing batch processing pattern"
    
    # Create test batch
    for i in {1..5}; do
        echo "item_$i" >> "$TEST_WORKSPACE/batch_list.txt"
    done
    
    # Process batch
    PROCESSED=0
    while read -r item; do
        mock_agent "kb-add" "/kb-add $item" > /dev/null
        ((PROCESSED++))
    done < "$TEST_WORKSPACE/batch_list.txt"
    
    if [ $PROCESSED -eq 5 ]; then
        pass "Batch processing completed: $PROCESSED items"
    else
        fail "Batch processing incomplete: $PROCESSED/5 items"
    fi
}

# Run all tests
run_all_tests() {
    echo "================================"
    echo "Agent Interaction Test Suite"
    echo "================================"
    echo ""
    
    test_sequential_pipeline
    test_parallel_processing
    test_conditional_routing
    test_error_recovery
    test_data_contract
    test_workflow_state
    test_performance
    test_idempotency
    test_circuit_breaker
    test_batch_processing
    
    echo ""
    echo "================================"
    echo "Test Results"
    echo "================================"
    echo -e "${GREEN}Passed:${NC} $PASSED"
    echo -e "${RED}Failed:${NC} $FAILED"
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}All tests passed!${NC}"
        EXITCODE=0
    else
        echo -e "${RED}Some tests failed${NC}"
        EXITCODE=1
    fi
    
    # Cleanup
    rm -rf "$TEST_WORKSPACE"
    
    exit $EXITCODE
}

# Check for specific test or run all
if [ $# -eq 0 ]; then
    run_all_tests
else
    case "$1" in
        "sequential") test_sequential_pipeline ;;
        "parallel") test_parallel_processing ;;
        "conditional") test_conditional_routing ;;
        "error") test_error_recovery ;;
        "contract") test_data_contract ;;
        "state") test_workflow_state ;;
        "performance") test_performance ;;
        "idempotent") test_idempotency ;;
        "circuit") test_circuit_breaker ;;
        "batch") test_batch_processing ;;
        *) echo "Unknown test: $1"; exit 1 ;;
    esac
    
    echo ""
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}Test passed${NC}"
        exit 0
    else
        echo -e "${RED}Test failed${NC}"
        exit 1
    fi
fi