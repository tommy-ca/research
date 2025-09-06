import { SimilarityCalculatorInterface } from '@/types/quality-assessment';

/**
 * Mock Similarity Calculator for testing purposes
 * KISS: Simple implementation for GREEN phase testing
 */
export class MockSimilarityCalculator implements SimilarityCalculatorInterface {
  
  async calculateSimilarity(content1: string, content2: string): Promise<number> {
    // Simple string similarity for testing
    if (content1 === content2) return 1.0;
    if (!content1 || !content2) return 0.0;
    
    // Basic word overlap similarity
    const words1 = new Set(content1.toLowerCase().split(/\s+/));
    const words2 = new Set(content2.toLowerCase().split(/\s+/));
    
    const intersection = new Set([...words1].filter(word => words2.has(word)));
    const union = new Set([...words1, ...words2]);
    
    return union.size > 0 ? intersection.size / union.size : 0.0;
  }

  async calculateBatch(content: string, existingContent: string[]): Promise<number[]> {
    const similarities: number[] = [];
    
    for (const existing of existingContent) {
      const similarity = await this.calculateSimilarity(content, existing);
      similarities.push(similarity);
    }
    
    return similarities;
  }

  async calculateWithEarlyTermination(
    content: string, 
    existingContent: string[], 
    threshold: number
  ): Promise<{
    maxSimilarity: number;
    maxIndex: number;
    processed: number;
  }> {
    let maxSimilarity = 0;
    let maxIndex = -1;
    
    for (let i = 0; i < existingContent.length; i++) {
      const similarity = await this.calculateSimilarity(content, existingContent[i]);
      
      if (similarity > maxSimilarity) {
        maxSimilarity = similarity;
        maxIndex = i;
      }
      
      // Early termination if high similarity found
      if (similarity >= threshold) {
        return {
          maxSimilarity: similarity,
          maxIndex: i,
          processed: i + 1
        };
      }
    }
    
    return {
      maxSimilarity,
      maxIndex: maxIndex >= 0 ? maxIndex : 0,
      processed: existingContent.length
    };
  }
}