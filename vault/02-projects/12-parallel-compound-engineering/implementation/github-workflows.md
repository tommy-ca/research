---
date: 2025-08-24
type: implementation
status: draft
tags: [github-actions, workflows, ci-cd, automation]
project: parallel-compound-engineering
links: ["[[github-actions-integration]]", "[[roadmap]]"]
---

# GitHub Actions Workflow Specifications

## Complete Workflow Implementations

### 1. Core Parallel CE Workflow

```yaml
# .github/workflows/parallel-compound-engineering.yml
name: Parallel Compound Engineering

on:
  issue_comment:
    types: [created]
  workflow_dispatch:
    inputs:
      feature_description:
        description: 'Feature to implement using Parallel CE'
        required: true
        type: string
      complexity:
        description: 'Feature complexity level'
        required: true
        default: 'medium'
        type: choice
        options:
        - simple
        - medium
        - complex

env:
  CE_WORKSPACE: .ce-workspace
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

jobs:
  # Job 1: Parse and Validate Input
  parse-input:
    runs-on: ubuntu-latest
    if: |
      (github.event_name == 'workflow_dispatch') ||
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude ce-parallel'))
    outputs:
      feature: ${{ steps.parse.outputs.feature }}
      complexity: ${{ steps.parse.outputs.complexity }}
      valid: ${{ steps.parse.outputs.valid }}
      
    steps:
      - name: Parse Input
        id: parse
        run: |
          if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
            echo "feature=${{ github.event.inputs.feature_description }}" >> $GITHUB_OUTPUT
            echo "complexity=${{ github.event.inputs.complexity }}" >> $GITHUB_OUTPUT
          else
            # Parse from comment: @claude ce-parallel "feature description" --complexity=medium
            COMMENT="${{ github.event.comment.body }}"
            FEATURE=$(echo "$COMMENT" | sed -n 's/.*@claude ce-parallel "\([^"]*\)".*/\1/p')
            COMPLEXITY=$(echo "$COMMENT" | sed -n 's/.*--complexity=\([^ ]*\).*/\1/p')
            echo "feature=${FEATURE:-'Feature from comment'}" >> $GITHUB_OUTPUT
            echo "complexity=${COMPLEXITY:-'medium'}" >> $GITHUB_OUTPUT
          fi
          echo "valid=true" >> $GITHUB_OUTPUT

  # Job 2: Planners Pool - Parallel Planning Phase
  planners-pool:
    runs-on: ubuntu-latest
    needs: parse-input
    if: needs.parse-input.outputs.valid == 'true'
    strategy:
      matrix:
        planner: [architect, requirements, dependencies, timeline]
      max-parallel: 4
      fail-fast: false
      
    outputs:
      planning-complete: ${{ steps.planning-status.outputs.complete }}
      
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        
      - name: Setup CE Workspace
        run: |
          mkdir -p ${{ env.CE_WORKSPACE }}/{events,state,artifacts,progress}
          echo "Planning started: $(date)" > ${{ env.CE_WORKSPACE }}/progress/planning-${{ matrix.planner }}.log
          
      - name: Execute Planning Agent
        id: planning
        uses: anthropics/claude-code-action@v1
        with:
          agent: "ce-planners-pool"
          role: ${{ matrix.planner }}
          input: |
            Feature: ${{ needs.parse-input.outputs.feature }}
            Complexity: ${{ needs.parse-input.outputs.complexity }}
            Role: ${{ matrix.planner }}
            
            Execute planning for this feature from the ${{ matrix.planner }} perspective.
            Output structured planning artifacts for the builders pool.
          timeout: 600
          
      - name: Save Planning Artifacts
        run: |
          mkdir -p ${{ env.CE_WORKSPACE }}/artifacts/planning/
          echo '${{ steps.planning.outputs.result }}' > ${{ env.CE_WORKSPACE }}/artifacts/planning/${{ matrix.planner }}.md
          
      - name: Upload Planning Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: planning-${{ matrix.planner }}
          path: ${{ env.CE_WORKSPACE }}/artifacts/planning/${{ matrix.planner }}.md
          
      - name: Update Planning Status
        id: planning-status
        run: |
          echo "complete=true" >> $GITHUB_OUTPUT
          echo "Planning complete for ${{ matrix.planner }}: $(date)" >> ${{ env.CE_WORKSPACE }}/progress/planning-${{ matrix.planner }}.log

  # Job 3: Planning Quality Gate
  planning-quality-gate:
    runs-on: ubuntu-latest
    needs: [parse-input, planners-pool]
    outputs:
      planning-approved: ${{ steps.gate-check.outputs.approved }}
      
    steps:
      - name: Download All Planning Artifacts
        uses: actions/download-artifact@v4
        with:
          pattern: planning-*
          path: ./planning-artifacts/
          merge-multiple: true
          
      - name: Planning Quality Gate Check
        id: gate-check
        uses: anthropics/claude-code-action@v1
        with:
          agent: "ce-coordinator"
          command: "validate-planning-phase"
          input: |
            Validate that all planning dimensions are complete and consistent:
            
            Feature: ${{ needs.parse-input.outputs.feature }}
            
            Planning Artifacts:
            $(find ./planning-artifacts/ -name "*.md" -exec echo "=== {} ===" \; -exec cat {} \;)
            
            Check for:
            1. Architecture completeness and feasibility
            2. Requirements coverage and clarity  
            3. Dependency analysis and resolution
            4. Timeline realism and resource allocation
            
            Output: APPROVED or REJECTED with specific feedback.
            
      - name: Post Planning Results
        if: github.event_name == 'issue_comment'
        uses: actions/github-script@v7
        with:
          script: |
            const result = `${{ steps.gate-check.outputs.result }}`;
            const approved = result.includes('APPROVED');
            
            github.rest.issues.createComment({
              issue_number: ${{ github.event.issue.number }},
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 📋 Planning Phase ${approved ? '✅ Complete' : '❌ Issues Found'}
              
              ${result}
              
              ${approved ? 'Proceeding to Building Phase...' : 'Please address the issues above before continuing.'}`
            });

  # Job 4: Builders Pool - Parallel Building Phase  
  builders-pool:
    runs-on: ubuntu-latest
    needs: [parse-input, planners-pool, planning-quality-gate]
    if: needs.planning-quality-gate.outputs.planning-approved == 'APPROVED'
    strategy:
      matrix:
        builder: [implementation, testing, integration, documentation]
      max-parallel: 4
      fail-fast: false
      
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        
      - name: Download Planning Artifacts
        uses: actions/download-artifact@v4
        with:
          pattern: planning-*
          path: ./planning-inputs/
          merge-multiple: true
          
      - name: Execute Building Agent
        id: building
        uses: anthropics/claude-code-action@v1
        with:
          agent: "ce-builders-pool"
          role: ${{ matrix.builder }}
          input: |
            Feature: ${{ needs.parse-input.outputs.feature }}
            Role: ${{ matrix.builder }}
            
            Planning Context:
            $(find ./planning-inputs/ -name "*.md" -exec cat {} \;)
            
            Execute building tasks for this feature from the ${{ matrix.builder }} perspective.
            Generate concrete implementation artifacts.
          timeout: 900
          
      - name: Save Building Artifacts
        run: |
          mkdir -p ${{ env.CE_WORKSPACE }}/artifacts/building/
          echo '${{ steps.building.outputs.result }}' > ${{ env.CE_WORKSPACE }}/artifacts/building/${{ matrix.builder }}.md
          
      - name: Upload Building Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: building-${{ matrix.builder }}
          path: ${{ env.CE_WORKSPACE }}/artifacts/building/${{ matrix.builder }}.md

  # Job 5: Building Quality Gate
  building-quality-gate:
    runs-on: ubuntu-latest
    needs: [parse-input, builders-pool]
    outputs:
      building-approved: ${{ steps.gate-check.outputs.approved }}
      
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        
      - name: Download Building Artifacts
        uses: actions/download-artifact@v4
        with:
          pattern: building-*
          path: ./building-artifacts/
          merge-multiple: true
          
      - name: Building Quality Gate Check
        id: gate-check
        uses: anthropics/claude-code-action@v1
        with:
          agent: "ce-coordinator"
          command: "validate-building-phase"
          input: |
            Validate building phase completion and quality:
            
            Feature: ${{ needs.parse-input.outputs.feature }}
            
            Building Artifacts:
            $(find ./building-artifacts/ -name "*.md" -exec echo "=== {} ===" \; -exec cat {} \;)
            
            Check for:
            1. Implementation completeness and correctness
            2. Test coverage and quality
            3. Integration readiness
            4. Documentation completeness
            
            Output: APPROVED or REJECTED with specific feedback.

  # Job 6: Reviewers Pool - Parallel Review Phase
  reviewers-pool:
    runs-on: ubuntu-latest
    needs: [parse-input, builders-pool, building-quality-gate]
    if: needs.building-quality-gate.outputs.building-approved == 'APPROVED'
    strategy:
      matrix:
        reviewer: [quality, security, performance, usability]
      max-parallel: 4
      fail-fast: false
      
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        
      - name: Download All Artifacts
        uses: actions/download-artifact@v4
        with:
          pattern: "*-*"
          path: ./all-artifacts/
          merge-multiple: true
          
      - name: Execute Review Agent
        id: review
        uses: anthropics/claude-code-action@v1
        with:
          agent: "ce-reviewers-pool"
          role: ${{ matrix.reviewer }}
          input: |
            Feature: ${{ needs.parse-input.outputs.feature }}
            Review Dimension: ${{ matrix.reviewer }}
            
            All Project Artifacts:
            $(find ./all-artifacts/ -name "*.md" -exec echo "=== {} ===" \; -exec cat {} \;)
            
            Conduct comprehensive ${{ matrix.reviewer }} review.
            Provide specific feedback, approval status, and recommendations.
          timeout: 600
          
      - name: Upload Review Results
        uses: actions/upload-artifact@v4
        with:
          name: review-${{ matrix.reviewer }}
          path: ${{ env.CE_WORKSPACE }}/artifacts/review/${{ matrix.reviewer }}.md

  # Job 7: Final Review Quality Gate & PR Creation
  final-review-and-pr:
    runs-on: ubuntu-latest
    needs: [parse-input, reviewers-pool]
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        
      - name: Download All Artifacts
        uses: actions/download-artifact@v4
        with:
          pattern: "*-*"
          path: ./final-artifacts/
          merge-multiple: true
          
      - name: Final Quality Gate
        id: final-gate
        uses: anthropics/claude-code-action@v1
        with:
          agent: "ce-coordinator"
          command: "final-approval"
          input: |
            Conduct final review and create deployment decision:
            
            Feature: ${{ needs.parse-input.outputs.feature }}
            
            All Artifacts:
            $(find ./final-artifacts/ -name "*.md" -exec echo "=== {} ===" \; -exec cat {} \;)
            
            Provide:
            1. Final approval status
            2. Summary of all phases
            3. Risk assessment
            4. Deployment recommendation
            
      - name: Create Implementation PR
        if: contains(steps.final-gate.outputs.result, 'APPROVED')
        uses: anthropics/claude-code-action@v1
        with:
          agent: "compound-parallel"
          command: "ce-pr"
          input: |
            Create a comprehensive PR for this parallel compound engineering implementation:
            
            Feature: ${{ needs.parse-input.outputs.feature }}
            
            Include:
            - Clear PR title and description
            - Summary of planning, building, and review phases
            - Implementation details and changes
            - Testing and validation performed
            - Deployment instructions
            
            All artifacts:
            $(find ./final-artifacts/ -name "*.md" -exec cat {} \;)
            
      - name: Post Final Results
        if: github.event_name == 'issue_comment'
        uses: actions/github-script@v7
        with:
          script: |
            const result = `${{ steps.final-gate.outputs.result }}`;
            const approved = result.includes('APPROVED');
            
            github.rest.issues.createComment({
              issue_number: ${{ github.event.issue.number }},
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🚀 Parallel Compound Engineering ${approved ? '✅ Complete' : '⚠️ Review Required'}
              
              ${result}
              
              ${approved ? '**Ready for deployment!** 🎉' : '**Manual review required before deployment.**'}`
            });
```

### 2. Simplified Feature Development Workflow

```yaml
# .github/workflows/ce-feature-dev.yml
name: CE Feature Development

on:
  issue_comment:
    types: [created]

jobs:
  feature-development:
    if: contains(github.event.comment.body, '@claude implement')
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Parallel CE Implementation
        uses: anthropics/claude-code-action@v1
        with:
          agent: "compound-parallel"
          input: ${{ github.event.comment.body }}
          
      - name: Create Feature Branch
        run: |
          BRANCH="feature/ce-$(date +%s)"
          git checkout -b "$BRANCH"
          git add .
          git commit -m "Parallel CE: ${{ github.event.comment.body }}"
          git push origin "$BRANCH"
```

### 3. Quality Assurance Workflow

```yaml
# .github/workflows/ce-quality-review.yml  
name: CE Quality Review

on:
  pull_request:
    types: [opened, synchronize]
    
jobs:
  parallel-quality-review:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        dimension: [code-quality, security, performance, documentation]
        
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: Quality Review
        uses: anthropics/claude-code-action@v1
        with:
          agent: "ce-reviewers-pool"
          role: ${{ matrix.dimension }}
          input: |
            Review this PR for ${{ matrix.dimension }}:
            
            PR Title: ${{ github.event.pull_request.title }}
            PR Body: ${{ github.event.pull_request.body }}
            
            Changed Files:
            ${{ github.event.pull_request.changed_files }}
            
      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.pulls.createReview({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: ${{ github.event.pull_request.number }},
              body: `## ${{ matrix.dimension }} Review\n\n${{ steps.review.outputs.result }}`,
              event: 'COMMENT'
            });
```

## Workflow Configuration Files

### Repository Setup

```yaml
# .github/ce-config.yml
parallel_ce:
  default_complexity: medium
  timeout_minutes:
    planning: 10
    building: 15
    review: 10
  
  agent_pools:
    planners:
      agents: ["research", "synthesis"]
      max_parallel: 4
      
    builders:
      agents: ["knowledge", "pkm-processor"]  
      max_parallel: 4
      
    reviewers:
      agents: ["synthesis", "pkm-feynman"]
      max_parallel: 4
      
  quality_gates:
    planning:
      - architecture_complete
      - requirements_defined
      - dependencies_resolved
      
    building:
      - implementation_complete
      - tests_passing
      - integration_working
      
    review:
      - quality_validated
      - security_cleared
      - performance_approved
```

### Environment Setup

```bash
# .github/scripts/setup-ce-environment.sh
#!/bin/bash

# Create CE workspace
mkdir -p .ce-workspace/{events,state,artifacts,progress}

# Copy Claude configuration
cp .claude/settings.json .ce-workspace/

# Set up logging
echo "CE Environment initialized: $(date)" > .ce-workspace/setup.log

# Configure GitHub CLI for PR creation
gh auth status || echo "GitHub CLI not authenticated"

echo "Parallel CE environment ready"
```

---

*These workflow specifications provide complete GitHub Actions integration for parallel compound engineering, enabling automated Plan → Build → Review cycles with quality gates and artifact management.*