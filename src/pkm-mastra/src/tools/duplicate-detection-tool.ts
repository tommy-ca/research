import { 
  DuplicationResult, 
  SimilarityCalculatorInterface,
  DuplicateDetectionToolInterface,
  DuplicateDetectionError
} from '@/types/quality-assessment';

/**
 * Duplicate Detection Tool - SRP: Only handles duplicate detection
 * Follows SOLID principles and KISS methodology for minimal complexity
 */
export class DuplicateDetectionTool implements DuplicateDetectionToolInterface {
  // DRY: Extract constants for better maintainability
  private static readonly DEFAULT_THRESHOLD = 0.85;
  private static readonly MIN_THRESHOLD = 0.0;
  private static readonly MAX_THRESHOLD = 1.0;
  
  private readonly threshold: number;
  private readonly similarityCalculator: SimilarityCalculatorInterface;

  constructor(
    similarityCalculator: SimilarityCalculatorInterface, // DIP: Depend on abstraction
    threshold: number = DuplicateDetectionTool.DEFAULT_THRESHOLD
  ) {
    this.validateThreshold(threshold);
    this.validateSimilarityCalculator(similarityCalculator);
    this.similarityCalculator = similarityCalculator;
    this.threshold = threshold;
  }

  /**
   * SRP: Single responsibility - detect duplicates only
   * KISS: Simple, straightforward duplicate detection logic
   */
  async detectDuplicate(content: string, existingContent: string[]): Promise<DuplicationResult> {
    try {
      // Handle edge case: empty existing content
      if (existingContent.length === 0) {
        return this.createNoDuplicateResult();
      }

      // Try early termination first for better performance
      const earlyResult = await this.tryEarlyTermination(content, existingContent);
      if (earlyResult) {
        return earlyResult;
      }

      // Fallback to batch calculation
      return await this.performBatchCalculation(content, existingContent);

    } catch (error) {
      throw new DuplicateDetectionError(
        `Duplicate detection failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        this.threshold,
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * SRP: Handle early termination calculation
   * DRY: Extracted early termination logic
   */
  private async tryEarlyTermination(content: string, existingContent: string[]): Promise<DuplicationResult | null> {
    // Check if early termination method is available
    if (!this.similarityCalculator.calculateWithEarlyTermination) {
      return null;
    }

    const result = await this.similarityCalculator.calculateWithEarlyTermination(
      content, 
      existingContent, 
      this.threshold
    );
    
    // Only use early termination result if it's properly defined
    if (!result || result.maxSimilarity === undefined) {
      return null;
    }

    return this.createDuplicationResult(result.maxSimilarity, result.maxIndex, content, existingContent);
  }

  /**
   * SRP: Handle batch similarity calculation
   * DRY: Extracted batch calculation logic
   */
  private async performBatchCalculation(content: string, existingContent: string[]): Promise<DuplicationResult> {
    const similarities = await this.similarityCalculator.calculateBatch(content, existingContent);
    
    // Find maximum similarity
    const maxSimilarity = Math.max(...similarities);
    const maxIndex = similarities.indexOf(maxSimilarity);
    
    return this.createDuplicationResult(maxSimilarity, maxIndex, content, existingContent);
  }

  /**
   * DRY: Extracted result creation logic
   */
  private async createDuplicationResult(
    maxSimilarity: number, 
    maxIndex: number, 
    content: string, 
    existingContent: string[]
  ): Promise<DuplicationResult> {
    const isDuplicate = maxSimilarity >= this.threshold;
    
    return {
      isDuplicate,
      similarityScore: maxSimilarity,
      duplicateIndex: isDuplicate ? maxIndex : undefined,
      consolidationRecommendation: isDuplicate 
        ? await this.generateConsolidationRecommendation(content, existingContent[maxIndex])
        : undefined
    };
  }

  /**
   * DRY: Extracted validation logic
   */
  private validateThreshold(threshold: number): void {
    if (threshold < DuplicateDetectionTool.MIN_THRESHOLD || threshold > DuplicateDetectionTool.MAX_THRESHOLD) {
      throw new Error(
        `Threshold must be between ${DuplicateDetectionTool.MIN_THRESHOLD} and ${DuplicateDetectionTool.MAX_THRESHOLD}, got ${threshold}`
      );
    }
  }

  /**
   * DRY: Extracted similarity calculator validation
   */
  private validateSimilarityCalculator(calculator: SimilarityCalculatorInterface): void {
    if (!calculator) {
      throw new Error('Similarity calculator is required');
    }
    if (typeof calculator.calculateBatch !== 'function') {
      throw new Error('Similarity calculator must implement calculateBatch method');
    }
  }

  /**
   * DRY: Extracted no-duplicate result creation
   */
  private createNoDuplicateResult(): DuplicationResult {
    return {
      isDuplicate: false,
      similarityScore: 0,
      duplicateIndex: undefined,
      consolidationRecommendation: undefined
    };
  }

  /**
   * KISS: Simple consolidation recommendation generation
   */
  private async generateConsolidationRecommendation(
    newContent: string, 
    existingContent: string
  ): Promise<string> {
    // Minimal implementation for GREEN phase
    const shorter = newContent.length < existingContent.length ? newContent : existingContent;
    const longer = newContent.length >= existingContent.length ? newContent : existingContent;
    
    return `Consider consolidating: Keep the longer version (${longer.length} chars) and review the shorter version (${shorter.length} chars) for additional insights.`;
  }
}