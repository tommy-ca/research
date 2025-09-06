import { describe, it, expect, beforeEach, vi } from 'vitest';
import { DuplicateDetectionTool } from '@/tools/duplicate-detection-tool';
import { QualityAssessmentTool } from '@/tools/quality-assessment-tool';
import { SimilarityCalculatorInterface } from '@/types/quality-assessment';

describe('Quality Assessment Tools - TDD Cycle 1.3', () => {
  describe('DuplicateDetectionTool', () => {
    let duplicateDetectionTool: DuplicateDetectionTool;
    let mockSimilarityCalculator: SimilarityCalculatorInterface;

    beforeEach(() => {
      // DIP: Dependency injection for testability
      mockSimilarityCalculator = {
        calculateSimilarity: vi.fn(),
        calculateBatch: vi.fn(),
        calculateWithEarlyTermination: vi.fn()
      };
      
      duplicateDetectionTool = new DuplicateDetectionTool(
        mockSimilarityCalculator,
        0.85 // Default threshold
      );
    });

    describe('SOLID Principles Compliance', () => {
      it('should follow Single Responsibility Principle - only detect duplicates', async () => {
        // SRP Test: Tool should only handle duplicate detection, not processing or storage
        const content = 'Test content for duplication check';
        const existingContent = ['Different content', 'Another piece of content'];
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.2, 0.3]);

        const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

        expect(result).toHaveProperty('isDuplicate');
        expect(result).toHaveProperty('similarityScore');
        expect(result).toHaveProperty('duplicateIndex');
        expect(result).toHaveProperty('consolidationRecommendation');
        
        // Should not have properties related to other concerns
        expect(result).not.toHaveProperty('processedContent');
        expect(result).not.toHaveProperty('storedLocation');
      });

      it('should follow Interface Segregation Principle - focused interface', async () => {
        // ISP Test: Interface should only expose duplicate detection methods
        const toolInterface = Object.getOwnPropertyNames(Object.getPrototypeOf(duplicateDetectionTool));
        
        expect(toolInterface).toContain('detectDuplicate');
        expect(toolInterface).toContain('constructor');
        
        // Should not contain methods unrelated to duplicate detection
        expect(toolInterface).not.toContain('processContent');
        expect(toolInterface).not.toContain('storeContent');
        expect(toolInterface).not.toContain('retrieveContent');
      });

      it('should follow Dependency Inversion Principle - depend on abstractions', () => {
        // DIP Test: Should accept similarity calculator interface, not concrete implementation
        expect(duplicateDetectionTool).toBeDefined();
        // Constructor should accept interface, allowing for different implementations
        expect(() => new DuplicateDetectionTool(mockSimilarityCalculator, 0.5)).not.toThrow();
      });
    });

    describe('Duplicate Detection Core Functionality', () => {
      it('should detect identical content as duplicate with 1.0 similarity', async () => {
        const content = 'This is identical content';
        const existingContent = ['Different content', 'This is identical content', 'Another content'];
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1, 1.0, 0.2]);

        const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

        expect(result.isDuplicate).toBe(true);
        expect(result.similarityScore).toBe(1.0);
        expect(result.duplicateIndex).toBe(1);
        expect(result.consolidationRecommendation).toBeDefined();
      });

      it('should detect semantic duplicates above threshold', async () => {
        const content = 'Machine learning is a subset of AI';
        const existingContent = [
          'Different topic entirely',
          'AI includes machine learning as a subset',
          'Completely unrelated content'
        ];
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1, 0.92, 0.05]);

        const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

        expect(result.isDuplicate).toBe(true);
        expect(result.similarityScore).toBe(0.92);
        expect(result.duplicateIndex).toBe(1);
        expect(result.consolidationRecommendation).toBeDefined();
      });

      it('should not detect duplicates below threshold', async () => {
        const content = 'Neural networks are computational models';
        const existingContent = [
          'Weather patterns in the Pacific',
          'Cooking recipes for Italian cuisine',
          'Historical events in Medieval Europe'
        ];
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.05, 0.03, 0.08]);

        const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

        expect(result.isDuplicate).toBe(false);
        expect(result.similarityScore).toBe(0.08); // Highest similarity found
        expect(result.duplicateIndex).toBeUndefined();
        expect(result.consolidationRecommendation).toBeUndefined();
      });
    });

    describe('Configurable Threshold Functionality', () => {
      it('should respect custom threshold configuration', async () => {
        const strictTool = new DuplicateDetectionTool(mockSimilarityCalculator, 0.95);
        const content = 'Test content';
        const existingContent = ['Similar test content'];
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.90]);

        const result = await strictTool.detectDuplicate(content, existingContent);

        expect(result.isDuplicate).toBe(false); // Below 0.95 threshold
        expect(result.similarityScore).toBe(0.90);
      });

      it('should validate threshold range boundaries', () => {
        expect(() => new DuplicateDetectionTool(mockSimilarityCalculator, -0.1)).toThrow('Threshold must be between 0 and 1');
        expect(() => new DuplicateDetectionTool(mockSimilarityCalculator, 1.1)).toThrow('Threshold must be between 0 and 1');
        expect(() => new DuplicateDetectionTool(mockSimilarityCalculator, 0.0)).not.toThrow();
        expect(() => new DuplicateDetectionTool(mockSimilarityCalculator, 1.0)).not.toThrow();
      });
    });

    describe('Performance Requirements (<50ms)', () => {
      it('should complete duplicate detection within 50ms for standard content', async () => {
        const content = 'Standard content for performance testing';
        const existingContent = Array.from({ length: 100 }, (_, i) => `Content item ${i}`);
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue(
          Array.from({ length: 100 }, () => Math.random() * 0.5)
        );

        const startTime = performance.now();
        await duplicateDetectionTool.detectDuplicate(content, existingContent);
        const endTime = performance.now();

        expect(endTime - startTime).toBeLessThan(50); // <50ms requirement
      });

      it('should handle early termination for performance optimization', async () => {
        const content = 'Test content';
        const existingContent = Array.from({ length: 1000 }, (_, i) => `Content ${i}`);
        
        // Mock early termination when high similarity found
        mockSimilarityCalculator.calculateWithEarlyTermination = vi.fn().mockResolvedValue({
          maxSimilarity: 0.95,
          maxIndex: 50,
          processed: 51 // Early termination after 51 items
        });

        const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

        expect(mockSimilarityCalculator.calculateWithEarlyTermination).toHaveBeenCalledWith(
          content,
          existingContent,
          0.85
        );
        expect(result.isDuplicate).toBe(true);
      });
    });

    describe('Edge Cases and Error Handling', () => {
      it('should handle empty content gracefully', async () => {
        const content = '';
        const existingContent = ['Some content'];
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.0]);

        const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

        expect(result.isDuplicate).toBe(false);
        expect(result.similarityScore).toBe(0.0);
      });

      it('should handle empty existing content array', async () => {
        const content = 'Some content to check';
        const existingContent: string[] = [];
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue([]);

        const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

        expect(result.isDuplicate).toBe(false);
        expect(result.similarityScore).toBe(0);
        expect(result.duplicateIndex).toBeUndefined();
      });

      it('should handle very long content without performance degradation', async () => {
        const content = 'A'.repeat(10000); // 10K character content
        const existingContent = ['Short content'];
        
        mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1]);

        const startTime = performance.now();
        const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);
        const endTime = performance.now();

        expect(endTime - startTime).toBeLessThan(50);
        expect(result).toBeDefined();
      });

      it('should handle similarity calculator errors gracefully', async () => {
        const content = 'Test content';
        const existingContent = ['Existing content'];
        
        mockSimilarityCalculator.calculateBatch.mockRejectedValue(new Error('Similarity calculation failed'));

        await expect(duplicateDetectionTool.detectDuplicate(content, existingContent))
          .rejects.toThrow('Duplicate detection failed: Similarity calculation failed');
      });
    });
  });

  describe('QualityAssessmentTool', () => {
    let qualityAssessmentTool: QualityAssessmentTool;

    beforeEach(() => {
      qualityAssessmentTool = new QualityAssessmentTool({
        readabilityWeight: 0.3,
        structureWeight: 0.3,
        conceptDensityWeight: 0.2,
        originalityWeight: 0.2
      });
    });

    describe('SOLID Principles Compliance', () => {
      it('should follow Single Responsibility Principle - only assess quality', async () => {
        const content = '# Test Content\n\nThis is structured content with clear sections.';
        
        const result = await qualityAssessmentTool.assessQuality(content);

        expect(result).toHaveProperty('overallScore');
        expect(result).toHaveProperty('readabilityScore');
        expect(result).toHaveProperty('structureScore');
        expect(result).toHaveProperty('conceptDensityScore');
        expect(result).toHaveProperty('originalityScore');
        
        // Should not handle unrelated concerns
        expect(result).not.toHaveProperty('duplicateStatus');
        expect(result).not.toHaveProperty('processedContent');
      });
    });

    describe('Quality Scoring Functionality', () => {
      it('should assign high quality score to well-structured content', async () => {
        const wellStructuredContent = `# Research on Neural Networks

## Introduction
Neural networks are computational models inspired by biological neural networks.

## Key Concepts
- Artificial neurons and their connections
- Backpropagation algorithm for training
- Deep learning architectures

## Applications
1. Image recognition and computer vision
2. Natural language processing
3. Recommendation systems

## Conclusion
Neural networks represent a powerful approach to machine learning with wide applications.`;

        const result = await qualityAssessmentTool.assessQuality(wellStructuredContent);

        expect(result.overallScore).toBeGreaterThan(0.7);
        expect(result.structureScore).toBeGreaterThan(0.8);
        expect(result.readabilityScore).toBeGreaterThan(0.6);
        expect(result.conceptDensityScore).toBeGreaterThan(0.5);
      });

      it('should assign lower quality score to poor content', async () => {
        const poorContent = 'random words here and there no structure unclear meaning jumbled thoughts';

        const result = await qualityAssessmentTool.assessQuality(poorContent);

        expect(result.overallScore).toBeLessThan(0.5);
        expect(result.structureScore).toBeLessThan(0.3);
        expect(result.readabilityScore).toBeLessThan(0.6);
      });

      it('should calculate weighted overall score correctly', async () => {
        const content = 'Test content for scoring';
        
        // Mock individual scores
        const mockScores = {
          readability: 0.8,
          structure: 0.6,
          conceptDensity: 0.7,
          originality: 0.9
        };

        vi.spyOn(qualityAssessmentTool as any, 'calculateReadabilityScore').mockReturnValue(mockScores.readability);
        vi.spyOn(qualityAssessmentTool as any, 'calculateStructureScore').mockReturnValue(mockScores.structure);
        vi.spyOn(qualityAssessmentTool as any, 'calculateConceptDensityScore').mockReturnValue(mockScores.conceptDensity);
        vi.spyOn(qualityAssessmentTool as any, 'calculateOriginalityScore').mockReturnValue(mockScores.originality);

        const result = await qualityAssessmentTool.assessQuality(content);

        const expectedOverallScore = (
          mockScores.readability * 0.3 +
          mockScores.structure * 0.3 +
          mockScores.conceptDensity * 0.2 +
          mockScores.originality * 0.2
        );

        expect(result.overallScore).toBeCloseTo(expectedOverallScore, 2);
      });
    });

    describe('Performance Requirements (<50ms)', () => {
      it('should complete quality assessment within 50ms', async () => {
        const content = 'Content for performance testing with reasonable length for quality assessment';

        const startTime = performance.now();
        await qualityAssessmentTool.assessQuality(content);
        const endTime = performance.now();

        expect(endTime - startTime).toBeLessThan(50);
      });
    });

    describe('Edge Cases and Error Handling', () => {
      it('should handle empty content', async () => {
        const result = await qualityAssessmentTool.assessQuality('');

        expect(result.overallScore).toBe(0);
        expect(result.readabilityScore).toBe(0);
        expect(result.structureScore).toBe(0);
        expect(result.conceptDensityScore).toBe(0);
      });

      it('should handle very short content', async () => {
        const result = await qualityAssessmentTool.assessQuality('Short.');

        expect(result).toBeDefined();
        expect(result.overallScore).toBeLessThan(0.5);
      });

      it('should handle very long content without performance issues', async () => {
        const longContent = Array.from({ length: 1000 }, (_, i) => 
          `Sentence ${i} with meaningful content about various topics.`
        ).join(' ');

        const startTime = performance.now();
        const result = await qualityAssessmentTool.assessQuality(longContent);
        const endTime = performance.now();

        expect(endTime - startTime).toBeLessThan(50);
        expect(result).toBeDefined();
      });
    });
  });

  describe('Integration with Existing Capture Agent', () => {
    it('should integrate seamlessly with existing capture pipeline', async () => {
      // Create mock similarity calculator for this integration test
      const integrationMockCalculator: SimilarityCalculatorInterface = {
        calculateSimilarity: vi.fn().mockResolvedValue(0.3),
        calculateBatch: vi.fn().mockResolvedValue([0.1, 0.3, 0.2]),
        calculateWithEarlyTermination: vi.fn().mockResolvedValue({
          maxSimilarity: 0.3,
          maxIndex: 1,
          processed: 3
        })
      };

      // Integration test to ensure quality tools work with existing capture agent
      const mockCaptureOutput = {
        id: 'test-capture-123',
        content: '# Test Content\n\nThis is test content for integration.',
        source: 'test-source',
        type: 'text',
        extractedMetadata: {},
        qualityScore: 0, // Will be updated by quality assessment
        timestamp: new Date().toISOString(),
        processed: true
      };

      const duplicateTool = new DuplicateDetectionTool(integrationMockCalculator);
      const qualityTool = new QualityAssessmentTool();
      
      // Should enhance capture output with quality assessment
      const qualityResult = await qualityTool.assessQuality(mockCaptureOutput.content);
      const enhancedOutput = {
        ...mockCaptureOutput,
        qualityScore: qualityResult.overallScore,
        extractedMetadata: {
          ...mockCaptureOutput.extractedMetadata,
          qualityBreakdown: qualityResult
        }
      };

      expect(enhancedOutput.qualityScore).toBeGreaterThan(0);
      expect(enhancedOutput.extractedMetadata.qualityBreakdown).toBeDefined();
    });
  });
});