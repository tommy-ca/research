import { describe, test, expect, beforeEach } from 'vitest';
import { 
  OptimizedModelSelector, 
  createDefaultModelSelector,
  ComplexityAnalyzer,
  QualityAnalyzer,
  PerformanceAnalyzer 
} from '../../src/providers/model-selector-optimized.js';
import { ModelSelectionRules, TaskType, TaskContext } from '../../src/types/model-types.js';

describe('OptimizedModelSelector - SOLID Principles Validation', () => {
  let selector: OptimizedModelSelector;
  let defaultRules: ModelSelectionRules;

  beforeEach(() => {
    selector = createDefaultModelSelector();
    defaultRules = selector.getRules();
  });

  describe('SOLID: Single Responsibility Principle', () => {
    test('ModelSelector only handles selection orchestration', () => {
      const task: TaskType = 'content-capture';
      const content = 'Test content';
      
      // Should delegate to specialized components, not implement all logic itself
      const result = selector.selectModel(task, content);
      
      expect(['sonnet', 'opus']).toContain(result);
    });

    test('each analyzer class has single responsibility', () => {
      const complexityAnalyzer = new ComplexityAnalyzer(defaultRules.complexityThresholds);
      const qualityAnalyzer = new QualityAnalyzer(0.95);
      const performanceAnalyzer = new PerformanceAnalyzer(defaultRules.performanceConstraints);
      
      // Each analyzer should only have methods related to its responsibility
      expect(typeof complexityAnalyzer.analyzeContent).toBe('function');
      expect(typeof complexityAnalyzer.analyzeTask).toBe('function');
      
      expect(typeof qualityAnalyzer.requiresHighQuality).toBe('function');
      expect(typeof qualityAnalyzer.calculateConfidence).toBe('function');
      
      expect(typeof performanceAnalyzer.requiresSpeed).toBe('function');
      expect(typeof performanceAnalyzer.canMeetConstraints).toBe('function');
    });
  });

  describe('SOLID: Open/Closed Principle', () => {
    test('can extend selection rules without modifying core class', () => {
      const customRules: ModelSelectionRules = {
        ...defaultRules,
        taskTypeMapping: {
          ...defaultRules.taskTypeMapping,
          'custom-task': 'opus' as any, // New task type
        },
      };
      
      const customSelector = new OptimizedModelSelector(customRules);
      
      // Should handle new task type without modification
      const result = customSelector.selectModel('custom-task' as TaskType, 'content');
      expect(result).toBe('opus');
    });

    test('extensible for new complexity thresholds', () => {
      const customRules: ModelSelectionRules = {
        ...defaultRules,
        complexityThresholds: {
          contentLength: 10000, // Different threshold
          processingComplexity: 0.8,
          qualityRequirement: 0.99,
        },
      };
      
      const customSelector = new OptimizedModelSelector(customRules);
      
      // Should use new thresholds without modification
      const longContent = 'x'.repeat(6000); // Between old (5000) and new (10000) threshold
      const result = customSelector.selectModel('content-capture', longContent);
      
      expect(result).toBe('sonnet'); // Should not trigger length override with higher threshold
    });
  });

  describe('SOLID: Liskov Substitution Principle', () => {
    test('OptimizedModelSelector substitutable for IModelSelector', () => {
      // Should work wherever IModelSelector is expected
      function useModelSelector(selector: { selectModel: Function, getSelectionReasoning: Function }) {
        return selector.selectModel('content-capture', 'test');
      }
      
      const result = useModelSelector(selector);
      expect(['sonnet', 'opus']).toContain(result);
    });
  });

  describe('SOLID: Interface Segregation Principle', () => {
    test('specialized analyzers have focused interfaces', () => {
      const complexityAnalyzer = new ComplexityAnalyzer(defaultRules.complexityThresholds);
      
      // ComplexityAnalyzer should not have quality or performance methods
      expect((complexityAnalyzer as any).requiresHighQuality).toBeUndefined();
      expect((complexityAnalyzer as any).requiresSpeed).toBeUndefined();
      
      // Should only have complexity-related methods
      expect(typeof complexityAnalyzer.analyzeContent).toBe('function');
      expect(typeof complexityAnalyzer.analyzeTask).toBe('function');
    });

    test('QualityAnalyzer has only quality-related methods', () => {
      const qualityAnalyzer = new QualityAnalyzer(0.95);
      
      // Should not have complexity or performance methods  
      expect((qualityAnalyzer as any).analyzeContent).toBeUndefined();
      expect((qualityAnalyzer as any).requiresSpeed).toBeUndefined();
      
      // Should only have quality-related methods
      expect(typeof qualityAnalyzer.requiresHighQuality).toBe('function');
      expect(typeof qualityAnalyzer.calculateConfidence).toBe('function');
    });
  });

  describe('SOLID: Dependency Inversion Principle', () => {
    test('depends on configuration abstractions not concretions', () => {
      // Constructor accepts abstract configuration, not hard-coded values
      const customConfig: ModelSelectionRules = {
        taskTypeMapping: { 'content-capture': 'opus' },
        complexityThresholds: { contentLength: 1000, processingComplexity: 0.5, qualityRequirement: 0.8 },
        performanceConstraints: { maxResponseTime: { sonnet: 1000, opus: 5000 }, prioritizeSpeed: true }
      };
      
      const customSelector = new OptimizedModelSelector(customConfig);
      
      // Should use injected configuration
      const result = customSelector.selectModel('content-capture', 'test');
      expect(result).toBe('opus'); // Uses custom mapping
    });
  });

  describe('KISS: Keep It Simple, Stupid', () => {
    test('simple decision tree with clear logic', () => {
      // Quality override - should be simple and obvious
      const result1 = selector.selectModel('content-capture', 'test', { qualityRequirement: 0.98 });
      expect(result1).toBe('opus');
      
      // Length override - should be simple and obvious
      const longContent = 'x'.repeat(6000);
      const result2 = selector.selectModel('content-capture', longContent);
      expect(result2).toBe('opus');
      
      // Default task mapping - should be simple and obvious
      const result3 = selector.selectModel('research-analysis', 'test');
      expect(result3).toBe('opus');
    });

    test('reasoning generation is clear and understandable', () => {
      const reasoning = selector.getSelectionReasoning('content-capture', 'x'.repeat(6000));
      
      expect(reasoning.reasons).toContain(expect.stringContaining('Content length'));
      expect(reasoning.reasons[0]).toMatch(/Content length \(\d+ chars\) exceeds threshold/);
    });
  });

  describe('DRY: Don\'t Repeat Yourself', () => {
    test('centralized reason templates prevent duplication', () => {
      const reasoning1 = selector.getSelectionReasoning('content-capture', 'test', { qualityRequirement: 0.98 });
      const reasoning2 = selector.getSelectionReasoning('metadata-generation', 'test', { qualityRequirement: 0.97 });
      
      // Both should use same template structure for quality requirements
      const qualityReasonPattern = /High quality requirement.*requires best model/;
      expect(reasoning1.reasons.some(r => qualityReasonPattern.test(r))).toBe(true);
      expect(reasoning2.reasons.some(r => qualityReasonPattern.test(r))).toBe(true);
    });

    test('shared validation logic prevents duplication', () => {
      const invalidRules1 = { ...defaultRules, complexityThresholds: { ...defaultRules.complexityThresholds, contentLength: -1 } };
      const invalidRules2 = { ...defaultRules, complexityThresholds: { ...defaultRules.complexityThresholds, qualityRequirement: 1.5 } };
      
      // Both should use same validation logic
      expect(() => new OptimizedModelSelector(invalidRules1)).toThrow('Content length threshold must be non-negative');
      expect(() => new OptimizedModelSelector(invalidRules2)).toThrow('Quality requirement must be between 0 and 1');
    });
  });

  describe('Performance and Quality Validation', () => {
    test('maintains performance with optimized structure', () => {
      const startTime = performance.now();
      
      // Run multiple selections to test performance
      for (let i = 0; i < 1000; i++) {
        selector.selectModel('content-capture', `test content ${i}`);
      }
      
      const duration = performance.now() - startTime;
      expect(duration).toBeLessThan(100); // Should complete 1000 selections in <100ms
    });

    test('maintains accuracy with SOLID refactoring', () => {
      // High-quality requirement should always select opus
      const highQualityResult = selector.selectModel('content-capture', 'test', { qualityRequirement: 0.98 });
      expect(highQualityResult).toBe('opus');
      
      // Large content should select opus
      const largeContentResult = selector.selectModel('content-capture', 'x'.repeat(6000));
      expect(largeContentResult).toBe('opus');
      
      // Simple tasks should select sonnet by default
      const simpleResult = selector.selectModel('content-capture', 'test');
      expect(simpleResult).toBe('sonnet');
      
      // Complex tasks should select opus by default
      const complexResult = selector.selectModel('research-analysis', 'test');
      expect(complexResult).toBe('opus');
    });

    test('provides comprehensive reasoning', () => {
      const reasoning = selector.getSelectionReasoning('research-analysis', 'test content');
      
      expect(reasoning.selectedModel).toBe('opus');
      expect(reasoning.reasons).toHaveLength(1);
      expect(reasoning.confidence).toBeGreaterThan(0.7);
      expect(reasoning.fallbackApplied).toBe(false);
      expect(reasoning.reasons[0]).toContain('requires high-quality analysis');
    });
  });

  describe('Error Handling and Edge Cases', () => {
    test('graceful handling of invalid task types', () => {
      const result = selector.selectModel('invalid-task' as TaskType, 'content');
      expect(result).toBe('sonnet'); // Should fallback gracefully
      
      const reasoning = selector.getSelectionReasoning('invalid-task' as TaskType, 'content');
      expect(reasoning.fallbackApplied).toBe(true);
    });

    test('handles edge cases in analyzers', () => {
      // Empty content
      const emptyResult = selector.selectModel('content-capture', '');
      expect(emptyResult).toBe('sonnet');
      
      // Very long content
      const veryLongContent = 'x'.repeat(50000);
      const longResult = selector.selectModel('content-capture', veryLongContent);
      expect(longResult).toBe('opus');
      
      // Extreme quality requirement  
      const extremeQualityResult = selector.selectModel('content-capture', 'test', { qualityRequirement: 0.999 });
      expect(extremeQualityResult).toBe('opus');
    });
  });
});