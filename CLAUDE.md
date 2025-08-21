# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive research knowledge base repository designed for deep research, experimentation, and knowledge management. The repository includes a sophisticated multi-agent research system integrated with Claude Code's official agent framework.

## Official Claude Code Integration

This repository includes a complete `.claude/` folder structure following [Claude Code's official documentation](https://docs.anthropic.com/en/docs/claude-code):

### Agent System (`.claude/agents/`)
- **deep-research.md**: Comprehensive research capabilities with multi-source validation
- **peer-review.md**: Systematic quality assurance and peer review
- **synthesis.md**: Cross-domain integration and framework development

### Configuration (`.claude/settings.json`)
Project-level settings following [Claude Code Settings](https://docs.anthropic.com/en/docs/claude-code/settings) specification with:
- Agent configurations and quality standards
- Hook automation for research commands
- Permission management and security controls
- Environment variables and model selection

### Hook System (`.claude/hooks/`)
Automation scripts following [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) patterns:
- `research_command_handler.sh`: Routes research commands to appropriate agents
- `quality_check.sh`: Automatic quality validation after content creation

## Research Commands

### Deep Research
- `/research-deep "topic"` - Comprehensive research with multi-source validation
- `/research-validate "finding"` - Multi-source validation with confidence scoring
- `/research-gap "domain"` - Systematic research gap identification

### Quality Assurance  
- `/peer-review "file.md"` - Comprehensive systematic review
- `/review-methodology "file.md"` - Methodology validation
- `/validate-sources "file.md"` - Source quality assessment
- `/detect-bias "file.md"` - Multi-dimensional bias detection

### Synthesis
- `/research-synthesize` - Cross-domain research integration
- `/framework-develop "domain"` - Theoretical/practical framework development
- `/pattern-analyze "collection"` - Pattern identification and analysis

## Repository Structure

- `docs/`: Research documentation, methodologies, findings, and references
- `experiments/`: Experimental code, data, and analysis notebooks
- `knowledge-base/`: Structured knowledge including concepts, frameworks, and tools
- `resources/`: Supporting materials like papers, datasets, and templates
- `.claude/`: **Official Claude Code agent integration and configuration**

## Research Workflow

### Standard Research Process
1. **Initialize**: `/research-deep "topic"` for comprehensive analysis
2. **Validate**: `/research-validate "key findings"` for verification
3. **Review**: `/peer-review "output.md"` for quality assurance
4. **Synthesize**: `/research-synthesize` for cross-domain integration
5. **Document**: Store in appropriate repository structure

### Quality Standards
- **Evidence Level**: Academic standards with peer review
- **Source Diversity**: Minimum 3 independent sources for critical claims
- **Bias Assessment**: Multi-dimensional bias detection and mitigation
- **Reproducibility**: Complete methodology documentation and audit trails

## Development Standards

### Research Excellence
- All research must be reproducible with complete documentation
- Multi-source validation required for critical findings
- Systematic bias detection and mitigation protocols
- Peer review validation for substantial research outputs

### Technical Standards
- Follow Claude Code's official agent patterns and configurations
- Use structured research workflows with quality gates
- Maintain comprehensive audit trails and version control
- Implement security and privacy best practices

### Documentation Requirements
- Research methodologies must be fully documented
- All findings require source attribution and validation
- Quality assessments and peer review reports included
- Clear naming conventions and organizational structure

## Code and Notebook Management

- Experimental code should include comprehensive documentation
- Jupyter notebooks require markdown explanations for each analytical step
- Data files must include metadata, source information, and validation
- Results documentation includes analysis, conclusions, and quality metrics
- All outputs subject to automatic quality validation when substantial

## Integration with Official Claude Code

This repository leverages Claude Code's official capabilities:

- **[Settings Management](https://docs.anthropic.com/en/docs/claude-code/settings)**: Hierarchical configuration
- **[Agent Framework](https://docs.anthropic.com/en/docs/claude-code/mcp)**: Specialized research agents
- **[Hook System](https://docs.anthropic.com/en/docs/claude-code/hooks)**: Automated workflows
- **[CLI Integration](https://docs.anthropic.com/en/docs/claude-code/cli-reference)**: Custom commands

For detailed information about the agent system, see `.claude/README.md`.