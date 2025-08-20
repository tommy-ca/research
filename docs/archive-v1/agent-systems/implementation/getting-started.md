# Getting Started Guide
## Claude Code Multi-Agent Research System

### Table of Contents
1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [First Steps](#first-steps)
5. [Basic Usage](#basic-usage)
6. [Validation](#validation)
7. [Next Steps](#next-steps)
8. [Troubleshooting](#troubleshooting)

## Quick Start

**Get up and running in 5 minutes:**

```bash
# 1. Verify Claude Code installation
claude --version

# 2. Check system status
ls -la .claude/

# 3. Test compliance validation
.claude/hooks/specification_compliance_hook.sh

# 4. Run your first research command
/research-deep "artificial intelligence impact on healthcare" --quality=academic

# 5. Check results
/research-status --format=dashboard
```

## Prerequisites

### System Requirements

#### Software Dependencies
- **Claude Code CLI**: Latest version
- **Node.js**: 18+ (for Claude Code)
- **Python**: 3.8+ (for validation tools)
- **Bash**: 4.0+ (for hooks)
- **Git**: 2.0+ (for version control)

#### Environment Setup
```bash
# Verify Claude Code installation
claude --version

# Check required tools
python3 --version
bash --version
git --version

# Verify project structure
ls -la .claude/
```

#### Hardware Requirements
- **CPU**: 4+ cores recommended
- **Memory**: 8GB+ RAM
- **Storage**: 10GB+ available space
- **Network**: High-speed internet connection

### Knowledge Prerequisites

#### Recommended Background
- **Claude Code Familiarity**: Basic understanding of Claude Code CLI
- **YAML/JSON**: Knowledge of configuration file formats
- **Research Methodology**: Understanding of research processes
- **Quality Assurance**: Basic QA concepts

#### Learning Resources
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [YAML Tutorial](https://yaml.org/spec/1.2/spec.html)
- [JSON Schema Guide](https://json-schema.org/learn/)
- [Research Methodology Basics](https://en.wikipedia.org/wiki/Research_methodology)

## Installation

### Automated Setup

#### Quick Installation Script
```bash
#!/bin/bash
# setup.sh - Automated setup for multi-agent research system

echo "🚀 Setting up Claude Code Multi-Agent Research System..."

# Verify prerequisites
echo "📋 Checking prerequisites..."
command -v claude >/dev/null 2>&1 || { echo "❌ Claude Code not found. Please install first."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 not found."; exit 1; }

# Verify directory structure
echo "📁 Verifying directory structure..."
if [ ! -d ".claude" ]; then
    echo "❌ .claude directory not found. Please run from project root."
    exit 1
fi

# Check specifications
echo "📋 Checking specifications..."
if [ ! -f ".claude/specifications/README.md" ]; then
    echo "❌ Specifications not found. Please ensure complete installation."
    exit 1
fi

# Verify agents
echo "🤖 Checking agents..."
if [ ! -f ".claude/agents/deep-research-v2.md" ]; then
    echo "❌ Deep research agent not found."
    exit 1
fi

# Test hooks
echo "🔧 Testing hooks..."
if [ -x ".claude/hooks/specification_compliance_hook.sh" ]; then
    echo "✅ Compliance hook executable"
else
    echo "🔧 Making hooks executable..."
    chmod +x .claude/hooks/*.sh
fi

# Create logs directory
echo "📊 Setting up logging..."
mkdir -p .claude/logs

# Validate installation
echo "✅ Running validation..."
.claude/hooks/specification_compliance_hook.sh

echo "🎉 Setup complete! Ready to use the multi-agent research system."
echo "📖 See docs/research/agent-systems/implementation/getting-started.md for usage guide."
```

#### Run Setup
```bash
# Make setup script executable
chmod +x setup.sh

# Run automated setup
./setup.sh
```

### Manual Setup

#### Step 1: Verify Structure
```bash
# Check project structure
tree .claude/
# Expected structure:
# .claude/
# ├── agents/
# ├── hooks/
# ├── specifications/
# └── settings.json (if configured)
```

#### Step 2: Configure Permissions
```bash
# Make hooks executable
chmod +x .claude/hooks/*.sh

# Verify permissions
ls -la .claude/hooks/
```

#### Step 3: Create Directories
```bash
# Create required directories
mkdir -p .claude/logs
mkdir -p docs/research/agent-systems

# Verify creation
ls -la .claude/
```

#### Step 4: Test Installation
```bash
# Test compliance validation
.claude/hooks/specification_compliance_hook.sh

# Check agent accessibility
head .claude/agents/deep-research-v2.md
```

## First Steps

### 1. System Validation

#### Check System Health
```bash
# Comprehensive system check
echo "🔍 System Health Check"
echo "==================="

# Check Claude Code
echo "📋 Claude Code Status:"
claude --version

# Check specifications
echo "📋 Specifications Status:"
ls -la .claude/specifications/

# Check agents
echo "🤖 Agents Status:"
ls -la .claude/agents/

# Check hooks
echo "🔧 Hooks Status:"
ls -la .claude/hooks/

# Test compliance
echo "✅ Compliance Check:"
.claude/hooks/specification_compliance_hook.sh
```

#### Validation Results
```bash
# Expected output indicators:
# ✅ Claude Code version displayed
# ✅ Specifications directory exists with files
# ✅ Agents directory contains deep-research-v2.md
# ✅ Hooks are executable
# ✅ Compliance validation passes
```

### 2. Configuration Check

#### Review Settings
```bash
# Check Claude Code settings (if configured)
if [ -f ".claude/settings.json" ]; then
    echo "📋 Current Settings:"
    cat .claude/settings.json | jq '.'
else
    echo "📋 No custom settings found (using defaults)"
fi
```

#### Environment Variables
```bash
# Check relevant environment variables
echo "🔧 Environment Configuration:"
echo "CLAUDE_PROJECT_DIR: ${CLAUDE_PROJECT_DIR:-not_set}"
echo "TOOL_NAME: ${TOOL_NAME:-not_set}"
echo "FILE_PATH: ${FILE_PATH:-not_set}"
```

### 3. Basic Functionality Test

#### Simple Research Test
```bash
# Test basic agent functionality
echo "🔬 Testing Basic Research Functionality..."

# Note: This is a conceptual test - actual implementation would depend on 
# how the research commands are integrated with Claude Code
echo "/research-deep \"test topic\" --depth=shallow --quality=draft"
```

## Basic Usage

### Core Commands

#### Research Commands
```bash
# Basic research
/research-deep "your research topic"

# Advanced research with options
/research-deep "climate change impact on agriculture" \
  --depth=comprehensive \
  --sources=academic,government \
  --geography=global \
  --timeline=14 \
  --quality=academic \
  --collaboration=peer-review

# Quick research for immediate needs
/research-deep "fintech trends 2024" \
  --depth=moderate \
  --timeline=3 \
  --quality=standard
```

#### Validation Commands
```bash
# Validate specific findings
/research-validate "specific claim or finding" \
  --sources=5 \
  --confidence=0.90 \
  --diversity=geographical,temporal

# Quick validation
/research-validate "AI improves diagnostic accuracy" \
  --sources=3 \
  --confidence=0.85
```

#### Status and Monitoring
```bash
# Check research status
/research-status research-12345

# Detailed status with compliance
/research-status research-12345 \
  --detail=comprehensive \
  --format=compliance-report

# Dashboard view
/research-status --format=dashboard
```

### Workflow Examples

#### Standard Research Workflow
```bash
# Step 1: Plan research
/research-plan "sustainable energy adoption in developing countries" \
  --template=academic \
  --complexity=high

# Step 2: Execute research
/research-execute plan-67890 \
  --monitor=detailed \
  --adapt=dynamic

# Step 3: Validate findings
/research-validate "solar adoption increased 300% in 5 years" \
  --sources=7 \
  --diversity=all

# Step 4: Check status
/research-status research-67890 \
  --format=comprehensive
```

#### Quality-Focused Workflow
```bash
# High-quality academic research
/research-deep "machine learning bias in healthcare applications" \
  --depth=exhaustive \
  --sources=academic \
  --quality=publication \
  --collaboration=expert-panel \
  --bias-sensitivity=maximum \
  --reproducibility=academic

# Continuous quality monitoring
/research-status research-id --format=quality-dashboard
```

### Configuration Usage

#### Using Different Quality Standards
```bash
# Draft quality (fast, basic validation)
/research-deep "topic" --quality=draft

# Standard quality (balanced speed/quality)
/research-deep "topic" --quality=standard

# Academic quality (thorough validation)
/research-deep "topic" --quality=academic

# Publication quality (highest standards)
/research-deep "topic" --quality=publication
```

#### Source Configuration
```bash
# Academic sources only
/research-deep "topic" --sources=academic

# Government and academic
/research-deep "topic" --sources=government,academic

# Comprehensive source mix
/research-deep "topic" --sources=academic,industry,government,journalistic

# All available sources
/research-deep "topic" --sources=mixed
```

## Validation

### Compliance Validation

#### Automatic Validation
```bash
# Compliance validation runs automatically on file changes
# via .claude/hooks/specification_compliance_hook.sh

# Manual compliance check
.claude/hooks/specification_compliance_hook.sh

# Check specific agent compliance
.claude/hooks/specification_compliance_hook.sh \
  --file=.claude/agents/deep-research-v2.md
```

#### Validation Reports
```bash
# View compliance reports
ls -la .claude/agents/*_compliance_report.md

# Read latest compliance report
cat .claude/agents/deep-research-v2_compliance_report.md
```

### Quality Validation

#### Research Quality Checks
```bash
# Check research quality metrics
/research-status research-id --format=quality-report

# Validate specific quality aspects
/research-validate "finding" \
  --bias-check=all \
  --confidence=0.95
```

#### Performance Validation
```bash
# Check system performance
/research-status --format=performance-dashboard

# Validate timing and efficiency
/research-status research-id --detail=timing
```

### Error Checking

#### Common Validation Errors
```bash
# Check for common issues:

# 1. Missing specifications
ls -la .claude/specifications/

# 2. Hook permissions
ls -la .claude/hooks/*.sh

# 3. Agent format issues
head -20 .claude/agents/deep-research-v2.md

# 4. Compliance scores
grep -r "compliance_score" .claude/logs/
```

#### Troubleshooting Validation
```bash
# Enable verbose validation
VALIDATION_DEBUG=true .claude/hooks/specification_compliance_hook.sh

# Check validation logs
tail -f .claude/logs/compliance_validation.log

# Verify file permissions
find .claude/ -type f -name "*.sh" -not -executable
```

## Next Steps

### Learning Path

#### Beginner Path (First Week)
1. **Day 1-2**: Complete basic setup and run first research commands
2. **Day 3-4**: Explore different research options and quality levels
3. **Day 5-6**: Practice validation commands and status monitoring
4. **Day 7**: Review compliance reports and understand quality metrics

#### Intermediate Path (Second Week)
1. **Day 8-10**: Learn advanced research parameters and workflows
2. **Day 11-12**: Understand specification framework and compliance
3. **Day 13-14**: Practice complex research scenarios and multi-stage workflows

#### Advanced Path (Third Week)
1. **Day 15-17**: Study specification documents and architecture
2. **Day 18-19**: Understand compliance validation and quality frameworks
3. **Day 20-21**: Learn best practices and optimization techniques

### Advanced Features

#### Specification Understanding
```bash
# Study core specifications
cat .claude/specifications/README.md

# Review interface specifications
cat .claude/specifications/interfaces/agent-interface-specification.json

# Understand behavior patterns
cat .claude/specifications/behaviors/research-behavior-specification.yaml
```

#### Quality Mastery
```bash
# Deep dive into quality framework
cat .claude/specifications/quality/quality-assurance-specification.yaml

# Understand quality metrics
grep -r "target_threshold" .claude/specifications/

# Learn compliance validation
cat docs/research/agent-systems/implementation/development-guide.md
```

### Integration Options

#### Claude Code Integration
```bash
# Configure Claude Code settings
# Edit .claude/settings.json for custom configuration

# Set up hooks for automatic validation
# Hooks are already configured in .claude/hooks/

# Customize agent behavior
# Review and modify .claude/agents/deep-research-v2.md if needed
```

#### External Tool Integration
```bash
# Consider integrating with:
# - Project management tools
# - Documentation systems
# - Quality assurance platforms
# - Compliance tracking systems
```

## Troubleshooting

### Common Issues

#### Installation Issues
```bash
# Issue: Claude Code not found
# Solution: Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Issue: Permissions denied
# Solution: Fix file permissions
chmod +x .claude/hooks/*.sh

# Issue: Directory structure missing
# Solution: Verify project setup
ls -la .claude/
```

#### Runtime Issues
```bash
# Issue: Compliance validation fails
# Solution: Check file format and content
.claude/hooks/specification_compliance_hook.sh --debug

# Issue: Research commands not working
# Solution: Verify agent configuration
head .claude/agents/deep-research-v2.md

# Issue: Quality validation errors
# Solution: Check quality thresholds
grep -r "threshold" .claude/specifications/quality/
```

#### Performance Issues
```bash
# Issue: Slow response times
# Solution: Check system resources and network
top
ping google.com

# Issue: High memory usage
# Solution: Monitor process usage
ps aux | grep claude

# Issue: Disk space issues
# Solution: Clean up logs and temporary files
du -sh .claude/logs/
```

### Getting Help

#### Documentation Resources
- **Architecture Guide**: `docs/research/agent-systems/architecture/`
- **Implementation Guide**: `docs/research/agent-systems/implementation/`
- **Specification Guide**: `docs/research/agent-systems/specifications/`

#### Support Channels
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Comprehensive guides and references
- **Community**: Share experiences and best practices

#### Self-Help Tools
```bash
# Check system health
./setup.sh

# Validate configuration
.claude/hooks/specification_compliance_hook.sh

# Review logs
tail -f .claude/logs/*.log

# Test basic functionality
/research-status --format=system-check
```

---

🎉 **Congratulations!** You're now ready to use the Claude Code Multi-Agent Research System. Start with simple research commands and gradually explore the advanced features as you become more comfortable with the system.

For detailed implementation guidance, see the [Development Guide](development-guide.md).
For architectural understanding, review the [System Architecture](../architecture/system-architecture.md).
For specification details, explore the [Framework Overview](../specifications/framework-overview.md).