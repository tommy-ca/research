import { describe, test, expect } from 'vitest';
import { createDefaultModelSelector } from '../../src/providers/model-selector-optimized.js';
import { TaskType } from '../../src/types/model-types.js';

describe('Claude Code Integration Tests', () => {
  const selector = createDefaultModelSelector();

  describe('Model Selection Logic', () => {
    test('selects Sonnet for simple content capture tasks', () => {
      const task: TaskType = 'content-capture';
      const content = 'Simple note: Remember to review the quarterly budget report.';
      
      const result = selector.selectModel(task, content);
      const reasoning = selector.getSelectionReasoning(task, content);
      
      expect(result).toBe('sonnet');
      expect(reasoning.confidence).toBeGreaterThan(0.7);
      expect(reasoning.reasons).toContain(expect.stringContaining('Simple task optimized for speed'));
    });

    test('selects Opus for research analysis tasks', () => {
      const task: TaskType = 'research-analysis';
      const content = `
        Analyze the impact of remote work on productivity metrics across different industries.
        Consider the following factors:
        - Employee satisfaction surveys
        - Output measurements 
        - Communication effectiveness
        - Long-term career development
        
        Provide recommendations for optimizing hybrid work models.
      `;
      
      const result = selector.selectModel(task, content);
      const reasoning = selector.getSelectionReasoning(task, content);
      
      expect(result).toBe('opus');
      expect(reasoning.confidence).toBeGreaterThan(0.8);
      expect(reasoning.reasons).toContain(expect.stringContaining('requires high-quality analysis'));
    });

    test('selects Opus for large content regardless of task type', () => {
      const task: TaskType = 'content-capture';
      const content = 'x'.repeat(6000); // Exceeds 5000 char threshold
      
      const result = selector.selectModel(task, content);
      const reasoning = selector.getSelectionReasoning(task, content);
      
      expect(result).toBe('opus');
      expect(reasoning.confidence).toBeGreaterThan(0.85);
      expect(reasoning.reasons).toContain(expect.stringContaining('Content length'));
    });

    test('respects quality requirement overrides', () => {
      const task: TaskType = 'metadata-generation';
      const content = 'Generate metadata for research paper';
      const context = { qualityRequirement: 0.98 };
      
      const result = selector.selectModel(task, content, context);
      const reasoning = selector.getSelectionReasoning(task, content, context);
      
      expect(result).toBe('opus');
      expect(reasoning.confidence).toBeGreaterThan(0.9);
      expect(reasoning.reasons).toContain(expect.stringContaining('High quality requirement'));
    });
  });

  describe('Real-world PKM Scenarios', () => {
    test('daily note capture should use Sonnet', () => {
      const task: TaskType = 'content-capture';
      const dailyNoteContent = `
        # 2025-09-06 Daily Note
        
        ## Tasks
        - Review PKM system integration tests
        - Update documentation for Claude Code provider
        - Meeting with team at 2 PM
        
        ## Ideas
        - Consider adding more model selection criteria
        - Look into performance optimization
        
        ## Notes
        - Claude Code integration working well
        - Need to test with larger content volumes
      `;
      
      const result = selector.selectModel(task, dailyNoteContent);
      
      expect(result).toBe('sonnet');
    });

    test('complex research synthesis should use Opus', () => {
      const task: TaskType = 'complex-synthesis';
      const researchContent = `
        Synthesize findings from multiple research papers on AI model selection:
        
        Paper 1: "Adaptive Model Selection in Production AI Systems" (2024)
        - Key finding: Dynamic selection improves performance by 23%
        - Methodology: A/B testing with 10,000+ requests
        - Limitations: Limited to NLP tasks
        
        Paper 2: "Cost-Quality Tradeoffs in LLM Deployment" (2024)
        - Key finding: 80% of tasks can use smaller models without quality loss
        - Methodology: Quality scoring across diverse task types
        - Limitations: Single domain (customer service)
        
        Paper 3: "Real-time Model Routing Architecture" (2024)
        - Key finding: Latency overhead <5ms for routing decisions
        - Methodology: Production deployment with 1M+ daily requests
        - Limitations: Requires significant infrastructure
        
        Synthesis Requirements:
        - Identify common patterns across papers
        - Reconcile conflicting findings
        - Propose unified framework
        - Consider practical implementation challenges
      `;
      
      const result = selector.selectModel(task, researchContent);
      const reasoning = selector.getSelectionReasoning(task, researchContent);
      
      expect(result).toBe('opus');
      expect(reasoning.reasons).toContain(expect.stringContaining('Content length'));
      expect(reasoning.reasons).toContain(expect.stringContaining('requires high-quality analysis'));
    });

    test('quality assessment should use Opus with high confidence', () => {
      const task: TaskType = 'quality-assessment';
      const assessmentContent = `
        Assess the quality of the following PKM system implementation:
        
        Code quality metrics:
        - Test coverage: 95%
        - Cyclomatic complexity: Average 3.2
        - Function length: Average 12 lines
        - Documentation: 89% coverage
        
        Architecture assessment needed for:
        - SOLID principles compliance
        - Performance characteristics
        - Maintainability score
        - Security considerations
      `;
      
      const result = selector.selectModel(task, assessmentContent);
      const reasoning = selector.getSelectionReasoning(task, assessmentContent);
      
      expect(result).toBe('opus');
      expect(reasoning.confidence).toBeGreaterThan(0.85);
      expect(reasoning.fallbackApplied).toBe(false);
    });
  });

  describe('Edge Cases and Error Handling', () => {
    test('handles empty content gracefully', () => {
      const result = selector.selectModel('content-capture', '');
      
      expect(result).toBe('sonnet'); // Safe fallback
    });

    test('handles very long content efficiently', () => {
      const veryLongContent = Array(100000).fill('word').join(' '); // ~500KB of text
      
      const startTime = performance.now();
      const result = selector.selectModel('content-capture', veryLongContent);
      const duration = performance.now() - startTime;
      
      expect(result).toBe('opus');
      expect(duration).toBeLessThan(50); // Should be fast even with large content
    });

    test('provides consistent results for identical inputs', () => {
      const task: TaskType = 'research-analysis';
      const content = 'Analyze the data trends';
      
      const results = Array(10).fill(0).map(() => selector.selectModel(task, content));
      
      // All results should be identical
      expect(new Set(results).size).toBe(1);
      expect(results[0]).toBe('opus');
    });
  });

  describe('Performance Validation', () => {
    test('model selection is performant at scale', () => {
      const tasks: TaskType[] = [
        'content-capture',
        'metadata-generation', 
        'research-analysis',
        'quality-assessment'
      ];
      
      const startTime = performance.now();
      
      // Simulate 1000 selection decisions
      for (let i = 0; i < 1000; i++) {
        const task = tasks[i % tasks.length];
        const content = `Test content ${i} with some variable length text`;
        selector.selectModel(task, content);
      }
      
      const duration = performance.now() - startTime;
      const avgTimePerSelection = duration / 1000;
      
      expect(avgTimePerSelection).toBeLessThan(0.1); // <0.1ms per selection
    });

    test('reasoning generation is efficient', () => {
      const startTime = performance.now();
      
      // Generate reasoning 100 times
      for (let i = 0; i < 100; i++) {
        selector.getSelectionReasoning(
          'research-analysis',
          `Content ${i} for analysis`,
          { qualityRequirement: 0.95 }
        );
      }
      
      const duration = performance.now() - startTime;
      
      expect(duration).toBeLessThan(50); // Should complete 100 reasoning generations in <50ms
    });
  });

  describe('Configuration Validation', () => {
    test('validates model selection rules comprehensively', () => {
      const selector = createDefaultModelSelector();
      const rules = selector.getRules();
      
      // Validate task mappings exist for all expected task types
      const expectedTasks: TaskType[] = [
        'content-capture',
        'metadata-generation',
        'basic-organization', 
        'research-analysis',
        'complex-synthesis',
        'quality-assessment',
        'deep-reasoning'
      ];
      
      expectedTasks.forEach(task => {
        expect(rules.taskTypeMapping[task]).toBeDefined();
        expect(['sonnet', 'opus']).toContain(rules.taskTypeMapping[task]);
      });
      
      // Validate thresholds are reasonable
      expect(rules.complexityThresholds.contentLength).toBeGreaterThan(1000);
      expect(rules.complexityThresholds.contentLength).toBeLessThan(50000);
      expect(rules.complexityThresholds.qualityRequirement).toBeGreaterThan(0.8);
      expect(rules.complexityThresholds.qualityRequirement).toBeLessThan(1.0);
      
      // Validate performance constraints
      expect(rules.performanceConstraints.maxResponseTime.sonnet).toBeLessThan(
        rules.performanceConstraints.maxResponseTime.opus
      );
    });
  });
});