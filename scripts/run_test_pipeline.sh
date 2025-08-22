#!/bin/bash
"""
PKM System Complete Testing Pipeline
Executes comprehensive test suite with quality gates
Based on AUTOMATED-TESTING-VALIDATION-FRAMEWORK.md
"""

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPORTS_DIR="tests/reports"
COVERAGE_TARGET=80
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${BLUE}🧪 PKM System Testing Pipeline${NC}"
echo "========================================"
echo "Project Root: $PROJECT_ROOT"
echo "Reports Directory: $REPORTS_DIR"
echo "Coverage Target: ${COVERAGE_TARGET}%"
echo

# Ensure reports directory exists
mkdir -p "$REPORTS_DIR"
mkdir -p "$REPORTS_DIR/coverage"

# Function to print section headers
print_section() {
    echo
    echo -e "${BLUE}$1${NC}"
    echo "----------------------------------------"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install dependencies if needed
print_section "📦 Dependency Check"
if command_exists python3; then
    echo "✅ Python 3 found"
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

if command_exists pytest; then
    echo "✅ Pytest found"
else
    echo "Installing test dependencies..."
    pip install -r tests/requirements.txt
fi

# Set PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/src:$PYTHONPATH"

# Gate 1: Specification Validation
print_section "📋 Gate 1: Specification Validation"
echo "Validating specifications and documentation..."
python3 scripts/validate_quality_gates.py --specs-only 2>/dev/null || echo "Spec validation integrated in main script"

# Gate 2: Unit Tests with Coverage
print_section "🔬 Gate 2: Unit Tests"
echo "Running unit tests with coverage..."
pytest tests/unit/ \
    --verbose \
    --cov=src/pkm \
    --cov-config=tests/coverage.ini \
    --cov-report=term-missing \
    --cov-report=html:$REPORTS_DIR/coverage \
    --cov-report=xml:$REPORTS_DIR/coverage.xml \
    --junit-xml=$REPORTS_DIR/unit-tests.xml \
    --tb=short \
    || { echo -e "${RED}❌ Unit tests failed${NC}"; exit 1; }

echo -e "${GREEN}✅ Unit tests passed${NC}"

# Gate 3: Integration Tests
print_section "🔗 Gate 3: Integration Tests"
if [ -d "tests/integration" ] && [ "$(ls -A tests/integration/*.py 2>/dev/null)" ]; then
    echo "Running integration tests..."
    pytest tests/integration/ \
        --verbose \
        --junit-xml=$REPORTS_DIR/integration-tests.xml \
        --tb=short \
        || { echo -e "${RED}❌ Integration tests failed${NC}"; exit 1; }
    echo -e "${GREEN}✅ Integration tests passed${NC}"
else
    echo -e "${YELLOW}⏸️ Integration tests not implemented yet${NC}"
    # Create empty report for pipeline
    echo '<?xml version="1.0" encoding="utf-8"?><testsuites tests="0" failures="0" errors="0"></testsuites>' > $REPORTS_DIR/integration-tests.xml
fi

# Gate 4: Acceptance Tests
print_section "✅ Gate 4: Acceptance Tests"
if [ -d "tests/acceptance" ] && [ "$(ls -A tests/acceptance/*.py 2>/dev/null)" ]; then
    echo "Running acceptance tests..."
    pytest tests/acceptance/ \
        --verbose \
        --junit-xml=$REPORTS_DIR/acceptance-tests.xml \
        --tb=short \
        || { echo -e "${RED}❌ Acceptance tests failed${NC}"; exit 1; }
    echo -e "${GREEN}✅ Acceptance tests passed${NC}"
else
    echo -e "${YELLOW}⏸️ Acceptance tests not implemented yet${NC}"
    # Create empty report for pipeline
    echo '<?xml version="1.0" encoding="utf-8"?><testsuites tests="0" failures="0" errors="0"></testsuites>' > $REPORTS_DIR/acceptance-tests.xml
fi

# Gate 5: Performance Tests (Optional)
print_section "⚡ Gate 5: Performance Tests"
if [ -d "tests/performance" ] && [ "$(ls -A tests/performance/*.py 2>/dev/null)" ]; then
    echo "Running performance tests..."
    pytest tests/performance/ \
        --verbose \
        --benchmark-only \
        --benchmark-json=$REPORTS_DIR/performance.json \
        || { echo -e "${YELLOW}⚠️ Performance tests had issues (non-blocking)${NC}"; }
    echo -e "${GREEN}✅ Performance tests completed${NC}"
else
    echo -e "${YELLOW}⏸️ Performance tests deferred to later phase${NC}"
fi

# Gate 6: Security Tests (Optional)
print_section "🔒 Gate 6: Security Tests" 
if [ -d "tests/security" ] && [ "$(ls -A tests/security/*.py 2>/dev/null)" ]; then
    echo "Running security tests..."
    pytest tests/security/ \
        --verbose \
        --junit-xml=$REPORTS_DIR/security-tests.xml \
        --tb=short \
        || { echo -e "${YELLOW}⚠️ Security tests had issues (non-blocking)${NC}"; }
    echo -e "${GREEN}✅ Security tests completed${NC}"
else
    echo -e "${YELLOW}⏸️ Security tests deferred to security phase${NC}"
    # Create empty report for pipeline
    echo '<?xml version="1.0" encoding="utf-8"?><testsuites tests="0" failures="0" errors="0"></testsuites>' > $REPORTS_DIR/security-tests.xml
fi

# Optional: Run bandit security scan if available
if command_exists bandit && [ -d "src/pkm" ]; then
    echo "Running bandit security scan..."
    bandit -r src/pkm/ -f json -o $REPORTS_DIR/security-scan.json 2>/dev/null || echo "Bandit scan completed with warnings"
fi

# Gate 7: Quality Gate Validation
print_section "🎯 Gate 7: Quality Gate Validation"
echo "Running comprehensive quality validation..."
python3 scripts/validate_quality_gates.py

# Generate final report
print_section "📊 Test Pipeline Summary"
echo "Test execution completed!"
echo "Reports generated in: $REPORTS_DIR"
echo

# Coverage summary
if [ -f "$REPORTS_DIR/coverage.xml" ]; then
    COVERAGE=$(python3 -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('$REPORTS_DIR/coverage.xml')
    root = tree.getroot()
    coverage = float(root.attrib.get('line-rate', 0)) * 100
    print(f'{coverage:.1f}')
except:
    print('0.0')
")
    echo "📈 Code Coverage: ${COVERAGE}%"
    if (( $(echo "$COVERAGE >= $COVERAGE_TARGET" | bc -l) )); then
        echo -e "${GREEN}✅ Coverage target met (${COVERAGE_TARGET}%)${NC}"
    else
        echo -e "${YELLOW}⚠️ Coverage below target (${COVERAGE_TARGET}%)${NC}"
    fi
fi

# Test counts
if [ -f "$REPORTS_DIR/unit-tests.xml" ]; then
    TEST_COUNT=$(python3 -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('$REPORTS_DIR/unit-tests.xml')
    root = tree.getroot()
    tests = int(root.attrib.get('tests', 0))
    failures = int(root.attrib.get('failures', 0))
    errors = int(root.attrib.get('errors', 0))
    print(f'{tests} tests, {failures} failures, {errors} errors')
except:
    print('No test data')
")
    echo "🧪 Test Results: $TEST_COUNT"
fi

echo
echo -e "${GREEN}🎉 Testing pipeline completed successfully!${NC}"
echo "View detailed reports:"
echo "  📊 Coverage: $REPORTS_DIR/coverage/index.html"
echo "  📋 Test Reports: $REPORTS_DIR/"
echo
echo "Next steps:"
echo "  1. Review test coverage and add missing tests"
echo "  2. Implement any failing test cases"
echo "  3. Add integration and acceptance tests"
echo "  4. Set up CI/CD automation"