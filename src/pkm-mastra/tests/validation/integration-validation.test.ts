import { describe, it, expect, beforeEach, vi } from 'vitest';
import { DuplicateDetectionTool } from '@/tools/duplicate-detection-tool';
import { QualityAssessmentTool } from '@/tools/quality-assessment-tool';
import { SimilarityCalculatorInterface } from '@/types/quality-assessment';

describe('VALIDATE Phase - Integration & Functional Requirements', () => {
  let mockSimilarityCalculator: SimilarityCalculatorInterface;
  let duplicateDetectionTool: DuplicateDetectionTool;
  let qualityAssessmentTool: QualityAssessmentTool;

  beforeEach(() => {
    mockSimilarityCalculator = {
      calculateSimilarity: vi.fn(),
      calculateBatch: vi.fn(),
      calculateWithEarlyTermination: vi.fn()
    };
    
    duplicateDetectionTool = new DuplicateDetectionTool(mockSimilarityCalculator);
    qualityAssessmentTool = new QualityAssessmentTool();
  });

  describe('Functional Requirements Validation', () => {
    it('should correctly assess quality for high-quality research content', async () => {
      const researchContent = `# Neural Networks in Machine Learning

## Abstract

Neural networks represent a powerful paradigm in artificial intelligence, mimicking biological neural networks to solve complex computational problems.

## Introduction

Artificial neural networks (ANNs) are computational models inspired by biological neural networks. These systems learn to perform tasks by considering examples, generally without task-specific programming.

## Key Components

1. **Neurons (Nodes)**: Basic processing units
2. **Weights**: Connection strengths between neurons
3. **Activation Functions**: Determine neuron output
4. **Layers**: Input, hidden, and output layers

## Applications

- Image recognition and computer vision
- Natural language processing
- Speech recognition
- Autonomous vehicles

## Conclusion

Neural networks continue to evolve, with deep learning architectures achieving remarkable performance across diverse domains.`;

      const result = await qualityAssessmentTool.assessQuality(researchContent);

      expect(result.overallScore).toBeGreaterThan(0.7);
      expect(result.structureScore).toBeGreaterThan(0.8);
      expect(result.readabilityScore).toBeGreaterThan(0.7);
      expect(result.conceptDensityScore).toBeGreaterThan(0.5);
      expect(result.originalityScore).toBeGreaterThan(0.6);
      
      console.log(`✅ High-quality content assessment: ${result.overallScore.toFixed(3)}`);
    });

    it('should correctly identify exact duplicates', async () => {
      const content = 'This is a test document about machine learning algorithms';
      const existingContent = [
        'Different content about cooking',
        'This is a test document about machine learning algorithms', // Exact match
        'Another unrelated piece of content'
      ];

      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1, 1.0, 0.05]);

      const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

      expect(result.isDuplicate).toBe(true);
      expect(result.similarityScore).toBe(1.0);
      expect(result.duplicateIndex).toBe(1);
      expect(result.consolidationRecommendation).toBeDefined();
      
      console.log(`✅ Exact duplicate detection: ${result.similarityScore}`);
    });

    it('should correctly identify semantic duplicates', async () => {
      const content = 'Machine learning algorithms can solve complex problems';
      const existingContent = [
        'Weather patterns in the ocean',
        'Complex problems can be solved using ML algorithms', // Semantic match
        'Cooking recipes for beginners'
      ];

      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1, 0.89, 0.03]);

      const result = await duplicateDetectionTool.detectDuplicate(content, existingContent);

      expect(result.isDuplicate).toBe(true);
      expect(result.similarityScore).toBe(0.89);
      expect(result.duplicateIndex).toBe(1);
      
      console.log(`✅ Semantic duplicate detection: ${result.similarityScore}`);
    });

    it('should handle edge cases gracefully', async () => {
      // Empty content
      const emptyResult = await qualityAssessmentTool.assessQuality('');
      expect(emptyResult.overallScore).toBe(0);

      // Empty existing content
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([]);
      const noDuplicateResult = await duplicateDetectionTool.detectDuplicate('test', []);
      expect(noDuplicateResult.isDuplicate).toBe(false);

      console.log(`✅ Edge cases handled correctly`);
    });
  });

  describe('Integration Requirements Validation', () => {
    it('should integrate with existing capture pipeline', async () => {
      // Simulate existing capture output structure
      const mockCaptureOutput = {
        id: 'test-capture-456',
        content: `# Research Findings

## Background
Recent studies in quantum computing show promising results.

## Key Insights
- Quantum supremacy achieved in specific domains
- Error correction remains a challenge  
- Commercial applications emerging

## Conclusion
The field is rapidly evolving with significant implications.`,
        source: 'research-paper',
        type: 'text',
        extractedMetadata: {},
        qualityScore: 0,
        timestamp: new Date().toISOString(),
        processed: false
      };

      // Simulate processing pipeline
      const qualityResult = await qualityAssessmentTool.assessQuality(mockCaptureOutput.content);
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.2, 0.3, 0.15]);
      const duplicateResult = await duplicateDetectionTool.detectDuplicate(
        mockCaptureOutput.content, 
        ['Existing content 1', 'Existing content 2', 'Existing content 3']
      );

      // Enhanced capture output with quality assessment
      const enhancedOutput = {
        ...mockCaptureOutput,
        qualityScore: qualityResult.overallScore,
        extractedMetadata: {
          ...mockCaptureOutput.extractedMetadata,
          qualityBreakdown: qualityResult,
          duplicationStatus: duplicateResult
        },
        processed: true
      };

      expect(enhancedOutput.qualityScore).toBeGreaterThan(0);
      expect(enhancedOutput.extractedMetadata.qualityBreakdown).toBeDefined();
      expect(enhancedOutput.extractedMetadata.duplicationStatus).toBeDefined();
      expect(enhancedOutput.processed).toBe(true);

      console.log(`✅ Pipeline integration: Quality=${qualityResult.overallScore.toFixed(3)}, Duplicate=${duplicateResult.isDuplicate}`);
    });

    it('should maintain type safety across all operations', async () => {
      const content = 'Type safety validation content';
      
      // All operations should return properly typed results
      const qualityResult = await qualityAssessmentTool.assessQuality(content);
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.4]);
      const duplicateResult = await duplicateDetectionTool.detectDuplicate(content, ['test']);

      // TypeScript compilation ensures type safety, but verify runtime types
      expect(typeof qualityResult.overallScore).toBe('number');
      expect(typeof qualityResult.readabilityScore).toBe('number');
      expect(typeof qualityResult.structureScore).toBe('number');
      expect(typeof qualityResult.conceptDensityScore).toBe('number');
      expect(typeof qualityResult.originalityScore).toBe('number');
      
      expect(typeof duplicateResult.isDuplicate).toBe('boolean');
      expect(typeof duplicateResult.similarityScore).toBe('number');

      console.log(`✅ Type safety maintained across operations`);
    });
  });

  describe('Non-Functional Requirements Validation', () => {
    it('should handle concurrent operations safely', async () => {
      const testContent = 'Concurrent processing test content';
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.3]);

      // Simulate concurrent operations
      const operations = Array.from({ length: 10 }, async (_, i) => {
        const [qualityResult, duplicateResult] = await Promise.all([
          qualityAssessmentTool.assessQuality(`${testContent} ${i}`),
          duplicateDetectionTool.detectDuplicate(`${testContent} ${i}`, ['existing'])
        ]);
        
        return { quality: qualityResult.overallScore, duplicate: duplicateResult.isDuplicate };
      });

      const results = await Promise.all(operations);
      
      expect(results).toHaveLength(10);
      results.forEach(result => {
        expect(typeof result.quality).toBe('number');
        expect(typeof result.duplicate).toBe('boolean');
      });

      console.log(`✅ Concurrent operations handled safely: ${results.length} operations`);
    });

    it('should provide consistent results for identical inputs', async () => {
      const testContent = 'Consistency test content with standard formatting';
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.25]);

      // Run same operation multiple times
      const results = await Promise.all([
        qualityAssessmentTool.assessQuality(testContent),
        qualityAssessmentTool.assessQuality(testContent),
        qualityAssessmentTool.assessQuality(testContent)
      ]);

      // All results should be identical
      expect(results[0].overallScore).toBe(results[1].overallScore);
      expect(results[1].overallScore).toBe(results[2].overallScore);
      expect(results[0].structureScore).toBe(results[2].structureScore);

      console.log(`✅ Consistent results for identical inputs: ${results[0].overallScore.toFixed(3)}`);
    });
  });
});