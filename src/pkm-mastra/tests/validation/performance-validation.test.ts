import { describe, it, expect, beforeEach, vi } from 'vitest';
import { DuplicateDetectionTool } from '@/tools/duplicate-detection-tool';
import { QualityAssessmentTool } from '@/tools/quality-assessment-tool';
import { SimilarityCalculatorInterface } from '@/types/quality-assessment';

describe('VALIDATE Phase - Performance Requirements', () => {
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

  it('should meet <50ms performance requirement for duplicate detection', async () => {
    const testContent = 'Sample content for performance testing with reasonable length';
    const existingContent = Array.from({ length: 100 }, (_, i) => `Content item ${i}`);
    
    mockSimilarityCalculator.calculateBatch.mockResolvedValue(
      Array.from({ length: 100 }, () => Math.random() * 0.5)
    );

    const startTime = performance.now();
    await duplicateDetectionTool.detectDuplicate(testContent, existingContent);
    const duration = performance.now() - startTime;

    expect(duration).toBeLessThan(50);
    console.log(`✅ Duplicate Detection: ${duration.toFixed(2)}ms (target: <50ms)`);
  });

  it('should meet <50ms performance requirement for quality assessment', async () => {
    const qualityTestContent = `# Sample Content

This is test content with proper structure and formatting.

## Section

- List item 1  
- List item 2

The content has multiple paragraphs with good structure and readability.`;

    const startTime = performance.now();
    const result = await qualityAssessmentTool.assessQuality(qualityTestContent);
    const duration = performance.now() - startTime;

    expect(duration).toBeLessThan(50);
    expect(result).toBeDefined();
    expect(result.overallScore).toBeGreaterThan(0);
    console.log(`✅ Quality Assessment: ${duration.toFixed(2)}ms (target: <50ms)`);
  });

  it('should meet <100ms performance requirement for combined operations', async () => {
    const testContent = 'Performance test content with adequate length for testing';
    const existingContent = Array.from({ length: 50 }, (_, i) => `Existing content ${i}`);
    
    mockSimilarityCalculator.calculateBatch.mockResolvedValue(
      Array.from({ length: 50 }, () => Math.random() * 0.4)
    );

    const startTime = performance.now();
    
    // Simulate typical workflow: quality assessment + duplicate detection
    const [qualityResult, duplicateResult] = await Promise.all([
      qualityAssessmentTool.assessQuality(testContent),
      duplicateDetectionTool.detectDuplicate(testContent, existingContent)
    ]);
    
    const duration = performance.now() - startTime;

    expect(duration).toBeLessThan(100);
    expect(qualityResult).toBeDefined();
    expect(duplicateResult).toBeDefined();
    console.log(`✅ Combined Operations: ${duration.toFixed(2)}ms (target: <100ms)`);
  });

  it('should handle large content efficiently', async () => {
    // Test with larger content (1000 words)
    const largeContent = Array.from({ length: 1000 }, (_, i) => `word${i}`).join(' ');
    
    const startTime = performance.now();
    const result = await qualityAssessmentTool.assessQuality(largeContent);
    const duration = performance.now() - startTime;

    expect(duration).toBeLessThan(100); // Allow more time for large content
    expect(result).toBeDefined();
    console.log(`✅ Large Content Processing: ${duration.toFixed(2)}ms (1000 words)`);
  });
});