import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { ModelSelector, ModelSelectionRules, TaskType, TaskContext, SelectionReasoning } from '../../src/providers/model-selector.js';

describe('ModelSelector', () => {
  let selector: ModelSelector;
  let defaultRules: ModelSelectionRules;

  beforeEach(() => {
    defaultRules = {
      taskTypeMapping: {
        'content-capture': 'sonnet',
        'metadata-generation': 'sonnet',
        'basic-organization': 'sonnet',
        'research-analysis': 'opus',
        'complex-synthesis': 'opus',
        'quality-assessment': 'opus',
        'deep-reasoning': 'opus',
      },
      complexityThresholds: {
        contentLength: 5000,
        processingComplexity: 0.7,
        qualityRequirement: 0.95,
      },
      performanceConstraints: {
        maxResponseTime: {
          'sonnet': 2000,
          'opus': 10000,
        },
        prioritizeSpeed: false,
      },
    };
    
    selector = new ModelSelector(defaultRules);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Basic Model Selection', () => {
    // TS-001: Sonnet Selection for Simple Tasks
    test('should select sonnet for simple capture task', () => {
      const task: TaskType = 'content-capture';
      const content = 'Simple note content to capture';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('sonnet');
    });

    test('should select sonnet for metadata generation task', () => {
      const task: TaskType = 'metadata-generation';
      const content = 'Generate metadata for this content';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('sonnet');
    });

    test('should select sonnet for basic organization task', () => {
      const task: TaskType = 'basic-organization';
      const content = 'Organize this content into categories';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('sonnet');
    });

    // TS-002: Opus Selection for Complex Tasks
    test('should select opus for research analysis task', () => {
      const task: TaskType = 'research-analysis';
      const content = 'Analyze this research data and provide insights';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('opus');
    });

    test('should select opus for complex synthesis task', () => {
      const task: TaskType = 'complex-synthesis';
      const content = 'Synthesize multiple research papers';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('opus');
    });

    test('should select opus for quality assessment task', () => {
      const task: TaskType = 'quality-assessment';
      const content = 'Assess the quality of this research';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('opus');
    });

    test('should select opus for deep reasoning task', () => {
      const task: TaskType = 'deep-reasoning';
      const content = 'Perform deep analysis of logical arguments';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('opus');
    });
  });

  describe('Content Length Override', () => {
    // TS-003: Content Length Override
    test('should override task type for large content', () => {
      const task: TaskType = 'content-capture'; // Usually Sonnet
      const content = 'X'.repeat(6000); // Exceeds 5000 char threshold
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('opus'); // Overridden due to content length
    });

    test('should use task type for small content', () => {
      const task: TaskType = 'research-analysis'; // Usually Opus
      const content = 'Short analysis request';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('opus'); // Follows task type
    });

    test('should handle edge case at threshold boundary', () => {
      const task: TaskType = 'content-capture';
      const content = 'X'.repeat(5000); // Exactly at threshold
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('sonnet'); // At boundary, not over
    });
  });

  describe('Quality Requirement Override', () => {
    // TS-004: Quality Requirement Override
    test('should override to opus for high quality requirement', () => {
      const task: TaskType = 'content-capture'; // Usually Sonnet
      const content = 'Simple content';
      const context: TaskContext = {
        qualityRequirement: 0.96, // Above 0.95 threshold
      };
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('opus'); // Overridden due to quality requirement
    });

    test('should use task type for normal quality requirement', () => {
      const task: TaskType = 'content-capture';
      const content = 'Simple content';
      const context: TaskContext = {
        qualityRequirement: 0.8, // Below 0.95 threshold
      };
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('sonnet'); // Follows task type
    });
  });

  describe('Performance Constraints', () => {
    test('should prioritize speed when configured', () => {
      const speedOptimizedRules = {
        ...defaultRules,
        performanceConstraints: {
          ...defaultRules.performanceConstraints,
          prioritizeSpeed: true,
        },
      };
      
      const speedSelector = new ModelSelector(speedOptimizedRules);
      const task: TaskType = 'research-analysis'; // Usually Opus
      const content = 'Analysis request';
      const context: TaskContext = {
        maxResponseTime: 1000, // Very tight time constraint
      };
      
      const result = speedSelector.selectModel(task, content, context);
      
      expect(result).toBe('sonnet'); // Overridden for speed
    });
  });

  describe('Selection Reasoning', () => {
    test('should provide reasoning for selection decisions', () => {
      const task: TaskType = 'content-capture';
      const content = 'X'.repeat(6000); // Large content
      const context: TaskContext = {};
      
      const reasoning = selector.getSelectionReasoning(task, content, context);
      
      expect(reasoning.selectedModel).toBe('opus');
      expect(reasoning.reasons).toContain('Content length exceeds threshold');
      expect(reasoning.confidence).toBeGreaterThan(0.8);
      expect(reasoning.fallbackApplied).toBe(false);
    });

    test('should provide reasoning for quality override', () => {
      const task: TaskType = 'metadata-generation';
      const content = 'Generate metadata';
      const context: TaskContext = {
        qualityRequirement: 0.98,
      };
      
      const reasoning = selector.getSelectionReasoning(task, content, context);
      
      expect(reasoning.selectedModel).toBe('opus');
      expect(reasoning.reasons).toContain('High quality requirement');
      expect(reasoning.confidence).toBeGreaterThan(0.9);
      expect(reasoning.fallbackApplied).toBe(false);
    });

    test('should provide reasoning for task type selection', () => {
      const task: TaskType = 'research-analysis';
      const content = 'Analyze this data';
      const context: TaskContext = {};
      
      const reasoning = selector.getSelectionReasoning(task, content, context);
      
      expect(reasoning.selectedModel).toBe('opus');
      expect(reasoning.reasons).toContain('Task type requires high-quality analysis');
      expect(reasoning.confidence).toBeGreaterThan(0.8);
      expect(reasoning.fallbackApplied).toBe(false);
    });
  });

  describe('Edge Cases and Error Handling', () => {
    test('should handle empty content', () => {
      const task: TaskType = 'content-capture';
      const content = '';
      const context: TaskContext = {};
      
      const result = selector.selectModel(task, content, context);
      
      expect(result).toBe('sonnet'); // Falls back to task type
    });

    test('should handle undefined context', () => {
      const task: TaskType = 'research-analysis';
      const content = 'Analysis request';
      
      const result = selector.selectModel(task, content, undefined);
      
      expect(result).toBe('opus'); // Uses task type mapping
    });

    test('should handle invalid task type gracefully', () => {
      const invalidTask = 'invalid-task-type' as TaskType;
      const content = 'Some content';
      const context: TaskContext = {};
      
      // Should not throw, should default to sonnet
      const result = selector.selectModel(invalidTask, content, context);
      
      expect(result).toBe('sonnet'); // Default fallback
    });
  });

  describe('Configuration Validation', () => {
    test('should validate rules on initialization', () => {
      const invalidRules = {
        ...defaultRules,
        complexityThresholds: {
          contentLength: -1, // Invalid negative threshold
          processingComplexity: 1.5, // Invalid >1.0 threshold  
          qualityRequirement: 0, // Invalid zero threshold
        },
      };
      
      expect(() => {
        new ModelSelector(invalidRules);
      }).toThrow('Invalid model selection rules');
    });

    test('should require task type mappings', () => {
      const incompleteRules = {
        ...defaultRules,
        taskTypeMapping: {}, // Empty mapping
      };
      
      expect(() => {
        new ModelSelector(incompleteRules);
      }).toThrow('Task type mappings required');
    });
  });
});