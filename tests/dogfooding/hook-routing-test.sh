#!/bin/bash
# Hook Routing Test for Knowledge Management Commands

echo "=== Knowledge Management Hook Routing Test ==="
echo ""

# Test KB commands routing
echo "Test 1: KB Add Command Routing"
RESULT=$(.claude/hooks/knowledge-router.sh "/kb-add test")
if [[ $RESULT == *"Knowledge Base Agent activated"* ]]; then
    echo "✅ PASS: /kb-add routes to knowledge-base agent"
else
    echo "❌ FAIL: /kb-add routing failed"
fi

echo ""
echo "Test 2: KB Search Command Routing"
RESULT=$(.claude/hooks/knowledge-router.sh "/kb-search query")
if [[ $RESULT == *"Knowledge Base Agent activated"* ]]; then
    echo "✅ PASS: /kb-search routes to knowledge-base agent"
else
    echo "❌ FAIL: /kb-search routing failed"
fi

# Test KG commands routing
echo ""
echo "Test 3: KG Build Command Routing"
RESULT=$(.claude/hooks/knowledge-router.sh "/kg-build domain")
if [[ $RESULT == *"Knowledge Graph Agent activated"* ]]; then
    echo "✅ PASS: /kg-build routes to knowledge-graph agent"
else
    echo "❌ FAIL: /kg-build routing failed"
fi

echo ""
echo "Test 4: KG Path Command Routing"
RESULT=$(.claude/hooks/knowledge-router.sh "/kg-path start end")
if [[ $RESULT == *"Knowledge Graph Agent activated"* ]]; then
    echo "✅ PASS: /kg-path routes to knowledge-graph agent"
else
    echo "❌ FAIL: /kg-path routing failed"
fi

# Test KC commands routing
echo ""
echo "Test 5: KC Validate Command Routing"
RESULT=$(.claude/hooks/knowledge-router.sh "/kc-validate entry")
if [[ $RESULT == *"Knowledge Curator Agent activated"* ]]; then
    echo "✅ PASS: /kc-validate routes to knowledge-curator agent"
else
    echo "❌ FAIL: /kc-validate routing failed"
fi

echo ""
echo "Test 6: KC Enrich Command Routing"
RESULT=$(.claude/hooks/knowledge-router.sh "/kc-enrich topic")
if [[ $RESULT == *"Knowledge Curator Agent activated"* ]]; then
    echo "✅ PASS: /kc-enrich routes to knowledge-curator agent"
else
    echo "❌ FAIL: /kc-enrich routing failed"
fi

# Test invalid command
echo ""
echo "Test 7: Invalid Command Handling"
RESULT=$(.claude/hooks/knowledge-router.sh "/invalid-command" 2>&1)
if [[ $RESULT == *"Unknown knowledge command"* ]]; then
    echo "✅ PASS: Invalid command handled correctly"
else
    echo "❌ FAIL: Invalid command not handled properly"
fi

echo ""
echo "=== Hook Routing Test Complete ==="