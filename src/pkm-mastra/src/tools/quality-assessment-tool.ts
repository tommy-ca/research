import { 
  QualityScoreBreakdown, 
  QualityAssessmentConfig,
  QualityAssessmentToolInterface,
  QualityAssessmentError
} from '@/types/quality-assessment';

/**
 * Quality Assessment Tool - SRP: Only handles quality assessment
 * Follows SOLID principles and KISS methodology
 */
export class QualityAssessmentTool implements QualityAssessmentToolInterface {
  // DRY: Extract constants for better maintainability
  private static readonly DEFAULT_WEIGHTS = {
    readabilityWeight: 0.3,
    structureWeight: 0.3,
    conceptDensityWeight: 0.2,
    originalityWeight: 0.2
  } as const;

  // Readability scoring constants
  private static readonly READABILITY = {
    BASE_SCORE: 0.3,
    SENTENCE_LENGTH_BONUS: 0.2,
    PUNCTUATION_BONUS: 0.3,
    PUNCTUATION_PENALTY: 0.1,
    MIN_WORDS_PER_SENTENCE: 8,
    MAX_WORDS_PER_SENTENCE: 25
  } as const;

  // Structure scoring constants
  private static readonly STRUCTURE = {
    HEADER_BONUS: 0.35,
    LIST_BONUS: 0.3,
    PARAGRAPH_BONUS: 0.2,
    EMPHASIS_BONUS: 0.15,
    MULTI_ELEMENT_BONUS: 0.1,
    MIN_ELEMENTS_FOR_BONUS: 3
  } as const;

  private readonly config: QualityAssessmentConfig;

  constructor(config?: Partial<QualityAssessmentConfig>) {
    // Merge with defaults following DRY principle
    this.config = {
      ...QualityAssessmentTool.DEFAULT_WEIGHTS,
      ...config
    };

    this.validateConfiguration();
  }

  /**
   * SRP: Single responsibility - assess content quality only
   * KISS: Simple quality assessment algorithm
   */
  async assessQuality(content: string): Promise<QualityScoreBreakdown> {
    try {
      // Handle edge case: empty content
      if (!content || content.trim().length === 0) {
        return this.createEmptyContentResult();
      }

      // Calculate individual quality scores
      const readabilityScore = this.calculateReadabilityScore(content);
      const structureScore = this.calculateStructureScore(content);
      const conceptDensityScore = this.calculateConceptDensityScore(content);
      const originalityScore = this.calculateOriginalityScore(content);

      // Calculate weighted overall score
      const overallScore = this.calculateWeightedScore({
        readabilityScore,
        structureScore,
        conceptDensityScore,
        originalityScore
      });

      // Generate metrics for analysis
      const metrics = this.generateMetrics(content);

      return {
        overallScore,
        readabilityScore,
        structureScore,
        conceptDensityScore,
        originalityScore,
        metrics
      };

    } catch (error) {
      throw new QualityAssessmentError(
        `Quality assessment failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'assessQuality',
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * KISS: Simple readability calculation based on sentence length and structure
   */
  private calculateReadabilityScore(content: string): number {
    const sentences = this.extractSentences(content);
    if (sentences.length === 0) return 0;

    const words = content.split(/\s+/);
    const averageWordsPerSentence = words.length / sentences.length;

    // Use constants for consistent scoring
    let score = QualityAssessmentTool.READABILITY.BASE_SCORE;

    // Bonus for optimal sentence length
    if (averageWordsPerSentence >= QualityAssessmentTool.READABILITY.MIN_WORDS_PER_SENTENCE && 
        averageWordsPerSentence <= QualityAssessmentTool.READABILITY.MAX_WORDS_PER_SENTENCE) {
      score += QualityAssessmentTool.READABILITY.SENTENCE_LENGTH_BONUS;
    }

    // Bonus for proper punctuation (required for good readability)
    if (/[.!?]/.test(content)) {
      score += QualityAssessmentTool.READABILITY.PUNCTUATION_BONUS;
    } else {
      // Penalize content without proper sentence endings
      score -= QualityAssessmentTool.READABILITY.PUNCTUATION_PENALTY;
    }

    return Math.max(0, Math.min(1, score));
  }

  /**
   * KISS: Simple structure assessment based on markdown elements
   */
  private calculateStructureScore(content: string): number {
    let score = 0;

    // Check for headers
    if (/^#{1,6}\s+.+$/m.test(content)) {
      score += QualityAssessmentTool.STRUCTURE.HEADER_BONUS;
    }

    // Check for lists
    if (/^[\*\-\+]\s+.+$/m.test(content) || /^\d+\.\s+.+$/m.test(content)) {
      score += QualityAssessmentTool.STRUCTURE.LIST_BONUS;
    }

    // Check for paragraphs (double line breaks)
    if (/\n\s*\n/.test(content)) {
      score += QualityAssessmentTool.STRUCTURE.PARAGRAPH_BONUS;
    }

    // Check for emphasis (bold/italic)
    if (/\*\*.+\*\*|\*.+\*/.test(content)) {
      score += QualityAssessmentTool.STRUCTURE.EMPHASIS_BONUS;
    }

    // Bonus for well-structured content with multiple elements
    const structuralElements = this.countStructuralElements(content);
    if (structuralElements >= QualityAssessmentTool.STRUCTURE.MIN_ELEMENTS_FOR_BONUS) {
      score += QualityAssessmentTool.STRUCTURE.MULTI_ELEMENT_BONUS;
    }

    return Math.max(0, Math.min(1, score));
  }

  /**
   * DRY: Count structural elements
   */
  private countStructuralElements(content: string): number {
    let count = 0;
    if (/^#{1,6}\s+.+$/m.test(content)) count++;
    if (/^[\*\-\+]\s+.+$/m.test(content)) count++;
    if (/^\d+\.\s+.+$/m.test(content)) count++;
    if (/\*\*.+\*\*/.test(content)) count++;
    if (/\*.+\*/.test(content)) count++;
    return count;
  }

  /**
   * KISS: Simple concept density based on unique words and content length
   */
  private calculateConceptDensityScore(content: string): number {
    const words = this.extractWords(content);
    if (words.length === 0) return 0;

    const uniqueWords = new Set(words.map(word => word.toLowerCase()));
    const uniqueRatio = uniqueWords.size / words.length;

    // Start with unique ratio but apply more conservative scoring
    let score = uniqueRatio * 0.6; // Reduce impact of pure uniqueness

    // Bonus for reasonable content length with structure
    if (words.length >= 20 && words.length <= 500) {
      score += 0.3;
    } else if (words.length >= 10) {
      score += 0.1; // Smaller bonus for shorter content
    }

    // Additional penalty for very short or potentially incoherent content
    if (words.length < 10 || uniqueRatio > 0.95) {
      score *= 0.7; // Reduce score for likely low-quality content
    }

    return Math.max(0, Math.min(1, score));
  }

  /**
   * KISS: Simple originality assessment (placeholder for GREEN phase)
   */
  private calculateOriginalityScore(content: string): number {
    // Minimal implementation for GREEN phase
    // In REFACTOR phase, this would integrate with duplicate detection
    const words = this.extractWords(content);
    
    // Check for coherence and meaningful content
    const sentences = this.extractSentences(content);
    const avgWordsPerSentence = sentences.length > 0 ? words.length / sentences.length : 0;
    
    let score = 0.2; // Base score
    
    // Penalize very short or incoherent content
    if (words.length < 5 || avgWordsPerSentence < 2) {
      score = 0.1;
    }
    // Reward longer, more structured content
    else if (words.length > 50 && avgWordsPerSentence > 5) {
      score = 0.8;
    } else if (words.length > 20 && avgWordsPerSentence > 3) {
      score = 0.6;
    } else if (words.length > 10) {
      score = 0.4;
    }
    
    return score;
  }

  /**
   * DRY: Extracted weighted score calculation
   */
  private calculateWeightedScore(scores: {
    readabilityScore: number;
    structureScore: number;
    conceptDensityScore: number;
    originalityScore: number;
  }): number {
    return (
      scores.readabilityScore * this.config.readabilityWeight +
      scores.structureScore * this.config.structureWeight +
      scores.conceptDensityScore * this.config.conceptDensityWeight +
      scores.originalityScore * this.config.originalityWeight
    );
  }

  /**
   * DRY: Extracted sentence extraction logic
   */
  private extractSentences(content: string): string[] {
    return content.split(/[.!?]+/).filter(s => s.trim().length > 0);
  }

  /**
   * DRY: Extracted word extraction logic
   */
  private extractWords(content: string): string[] {
    return content.trim().split(/\s+/).filter(word => word.length > 0);
  }

  /**
   * DRY: Extracted metrics generation
   */
  private generateMetrics(content: string) {
    const words = this.extractWords(content);
    const sentences = this.extractSentences(content);
    const paragraphs = content.split(/\n\s*\n/).filter(p => p.trim().length > 0);

    return {
      wordCount: words.length,
      sentenceCount: sentences.length,
      paragraphCount: paragraphs.length,
      averageWordsPerSentence: sentences.length > 0 ? words.length / sentences.length : 0,
      structuralElements: this.identifyStructuralElements(content),
      conceptCount: new Set(words.map(w => w.toLowerCase())).size
    };
  }

  /**
   * DRY: Extracted structural elements identification
   */
  private identifyStructuralElements(content: string): string[] {
    const elements: string[] = [];

    if (/^#{1,6}\s+.+$/m.test(content)) elements.push('headers');
    if (/^[\*\-\+]\s+.+$/m.test(content)) elements.push('bullet_lists');
    if (/^\d+\.\s+.+$/m.test(content)) elements.push('numbered_lists');
    if (/\*\*.+\*\*/.test(content)) elements.push('bold_text');
    if (/\*.+\*/.test(content)) elements.push('italic_text');

    return elements;
  }

  /**
   * DRY: Extracted empty content result creation
   */
  private createEmptyContentResult(): QualityScoreBreakdown {
    return {
      overallScore: 0,
      readabilityScore: 0,
      structureScore: 0,
      conceptDensityScore: 0,
      originalityScore: 0,
      metrics: {
        wordCount: 0,
        sentenceCount: 0,
        paragraphCount: 0,
        averageWordsPerSentence: 0,
        structuralElements: [],
        conceptCount: 0
      }
    };
  }

  /**
   * DRY: Extracted configuration validation
   */
  private validateConfiguration(): void {
    this.validateWeights();
    this.validateWeightRanges();
  }

  /**
   * DRY: Extracted weight sum validation
   */
  private validateWeights(): void {
    const totalWeight = 
      this.config.readabilityWeight +
      this.config.structureWeight + 
      this.config.conceptDensityWeight +
      this.config.originalityWeight;

    if (Math.abs(totalWeight - 1.0) > 0.01) {
      throw new Error(`Quality assessment weights must sum to 1.0, got ${totalWeight.toFixed(3)}`);
    }
  }

  /**
   * DRY: Extracted weight range validation
   */
  private validateWeightRanges(): void {
    const weights = [
      { name: 'readabilityWeight', value: this.config.readabilityWeight },
      { name: 'structureWeight', value: this.config.structureWeight },
      { name: 'conceptDensityWeight', value: this.config.conceptDensityWeight },
      { name: 'originalityWeight', value: this.config.originalityWeight }
    ];

    for (const weight of weights) {
      if (weight.value < 0 || weight.value > 1) {
        throw new Error(`${weight.name} must be between 0 and 1, got ${weight.value}`);
      }
    }
  }
}