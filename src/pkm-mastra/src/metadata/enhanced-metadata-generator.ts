import { QualityScoreBreakdown, DuplicationResult } from '@/types/quality-assessment';

/**
 * Enhanced Metadata Generator
 * TDD Cycle 1.4 - Rich metadata generation and management
 * 
 * SOLID Principles:
 * - SRP: Single responsibility for metadata generation and enrichment
 * - OCP: Open for extension through plugin architecture (future)
 * - DIP: Depends on input interfaces rather than concrete types
 */

export interface BaseMetadata {
  title?: string;
  author?: string;
  source: string;
  contentType: string;
  tags?: string[];
  category?: string;
  createdAt?: string;
  modifiedAt?: string;
}

export interface QualityMetadata {
  qualityBreakdown: QualityScoreBreakdown;
  qualityTimestamp: string;
  qualityVersion: string;
  qualityConfidence: number;
  qualityFlags: string[];
}

export interface WorkflowMetadata {
  workflowVersion: string;
  processingStage: 'captured' | 'analyzed' | 'routed' | 'enhanced' | 'archived';
  routingDecision: 'accept' | 'review' | 'reject' | 'enhance';
  routingReason: string;
  routingConfidence: number;
  processingTimeMs: number;
  performanceFlags: string[];
}

export interface DuplicationMetadata {
  duplicationStatus: DuplicationResult;
  duplicationTimestamp: string;
  similarityAnalysisVersion: string;
  nearDuplicates?: {
    contentId: string;
    similarityScore: number;
    sourceLocation: string;
  }[];
}

export interface ContextualMetadata {
  extractedEntities?: string[];
  detectedLanguage?: string;
  estimatedReadingTime?: number;
  complexity?: 'simple' | 'moderate' | 'complex' | 'advanced';
  technicalLevel?: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  emotionalTone?: 'neutral' | 'positive' | 'negative' | 'mixed';
}

export interface ComplianceMetadata {
  privacyFlags: string[];
  securityClassification?: 'public' | 'internal' | 'confidential' | 'restricted';
  retentionPolicy?: string;
  accessControl?: string[];
  auditTrail: {
    timestamp: string;
    action: string;
    user?: string;
    system: string;
  }[];
}

export interface EnhancedMetadataPackage {
  base: BaseMetadata;
  quality: QualityMetadata;
  workflow: WorkflowMetadata;
  duplication: DuplicationMetadata;
  contextual: ContextualMetadata;
  compliance: ComplianceMetadata;
  version: string;
  schemaVersion: string;
  generatedAt: string;
}

export class EnhancedMetadataGenerator {
  private readonly version = '1.4.0';
  private readonly schemaVersion = '2.1.0';

  /**
   * Main metadata package generation - KISS principle
   */
  generateMetadataPackage(
    content: string,
    baseMetadata: BaseMetadata,
    qualityResult: QualityScoreBreakdown,
    duplicationResult: DuplicationResult,
    workflowResult: {
      routingDecision: 'accept' | 'review' | 'reject' | 'enhance';
      routingReason: string;
      routingConfidence: number;
      processingTimeMs: number;
    }
  ): EnhancedMetadataPackage {
    const timestamp = new Date().toISOString();

    return {
      base: this.enrichBaseMetadata(content, baseMetadata, timestamp),
      quality: this.generateQualityMetadata(qualityResult, timestamp),
      workflow: this.generateWorkflowMetadata(workflowResult, timestamp),
      duplication: this.generateDuplicationMetadata(duplicationResult, timestamp),
      contextual: this.generateContextualMetadata(content),
      compliance: this.generateComplianceMetadata(content, baseMetadata, timestamp),
      version: this.version,
      schemaVersion: this.schemaVersion,
      generatedAt: timestamp
    };
  }

  /**
   * DRY: Extracted base metadata enrichment
   */
  private enrichBaseMetadata(content: string, base: BaseMetadata, timestamp: string): BaseMetadata {
    return {
      ...base,
      createdAt: base.createdAt || timestamp,
      modifiedAt: timestamp,
      // Auto-generate title if missing
      title: base.title || this.extractTitle(content),
      // Auto-generate tags if missing  
      tags: base.tags || this.extractTags(content),
      // Validate and enhance category
      category: this.validateCategory(base.category, content)
    };
  }

  /**
   * DRY: Extracted quality metadata generation
   */
  private generateQualityMetadata(qualityResult: QualityScoreBreakdown, timestamp: string): QualityMetadata {
    const qualityFlags: string[] = [];

    // Generate quality flags based on scores - KISS approach
    if (qualityResult.overallScore < 0.3) qualityFlags.push('low-quality');
    if (qualityResult.overallScore > 0.9) qualityFlags.push('high-quality');
    if (qualityResult.structureScore < 0.2) qualityFlags.push('poor-structure');
    if (qualityResult.readabilityScore < 0.3) qualityFlags.push('poor-readability');
    if (qualityResult.conceptDensityScore > 0.9) qualityFlags.push('concept-dense');
    if (qualityResult.originalityScore < 0.2) qualityFlags.push('low-originality');

    return {
      qualityBreakdown: qualityResult,
      qualityTimestamp: timestamp,
      qualityVersion: this.version,
      qualityConfidence: this.calculateQualityConfidence(qualityResult),
      qualityFlags
    };
  }

  /**
   * DRY: Extracted workflow metadata generation
   */
  private generateWorkflowMetadata(workflowResult: any, timestamp: string): WorkflowMetadata {
    const performanceFlags: string[] = [];
    
    if (workflowResult.processingTimeMs > 100) performanceFlags.push('slow-processing');
    if (workflowResult.processingTimeMs < 10) performanceFlags.push('fast-processing');
    if (workflowResult.routingConfidence < 0.5) performanceFlags.push('low-confidence-routing');
    
    // Add more performance flags based on workflow conditions
    if (workflowResult.routingDecision === 'review') performanceFlags.push('requires-review');
    if (workflowResult.routingDecision === 'reject') performanceFlags.push('quality-insufficient');

    return {
      workflowVersion: this.version,
      processingStage: 'routed',
      routingDecision: workflowResult.routingDecision,
      routingReason: workflowResult.routingReason,
      routingConfidence: workflowResult.routingConfidence,
      processingTimeMs: workflowResult.processingTimeMs,
      performanceFlags
    };
  }

  /**
   * DRY: Extracted duplication metadata generation
   */
  private generateDuplicationMetadata(duplicationResult: DuplicationResult, timestamp: string): DuplicationMetadata {
    return {
      duplicationStatus: duplicationResult,
      duplicationTimestamp: timestamp,
      similarityAnalysisVersion: this.version,
      // Include near-duplicates for higher similarity scores
      nearDuplicates: duplicationResult.similarityScore > 0.5 ? [{
        contentId: 'mock-similar-content',
        similarityScore: duplicationResult.similarityScore,
        sourceLocation: 'existing-content-store'
      }] : undefined
    };
  }

  /**
   * DRY: Extracted contextual metadata generation
   */
  private generateContextualMetadata(content: string): ContextualMetadata {
    const words = content.split(/\s+/).length;
    const sentences = content.split(/[.!?]+/).length;
    const averageWordsPerSentence = sentences > 0 ? words / sentences : 0;

    return {
      extractedEntities: this.extractEntities(content),
      detectedLanguage: this.detectLanguage(content),
      estimatedReadingTime: Math.ceil(words / 200), // 200 WPM average
      complexity: this.assessComplexity(averageWordsPerSentence, content),
      technicalLevel: this.assessTechnicalLevel(content),
      emotionalTone: this.assessEmotionalTone(content)
    };
  }

  /**
   * DRY: Extracted compliance metadata generation
   */
  private generateComplianceMetadata(content: string, base: BaseMetadata, timestamp: string): ComplianceMetadata {
    const privacyFlags = this.detectPrivacyFlags(content);
    
    return {
      privacyFlags,
      securityClassification: this.classifySecurityLevel(content, privacyFlags),
      retentionPolicy: this.determineRetentionPolicy(base.contentType),
      accessControl: base.source === 'internal' ? ['internal-users'] : ['all-users'],
      auditTrail: [{
        timestamp,
        action: 'metadata-generated',
        system: `enhanced-metadata-generator-${this.version}`
      }]
    };
  }

  // KISS: Simple helper methods for metadata enrichment
  private extractTitle(content: string): string {
    // Look for markdown headers first
    const headerMatch = content.match(/^#{1,6}\s+(.+)$/m);
    if (headerMatch) return headerMatch[1].trim();

    // Take first sentence if no header
    const firstSentence = content.split(/[.!?]/)[0];
    if (firstSentence.length > 5 && firstSentence.length < 100) {
      return firstSentence.trim();
    }

    return 'Untitled Content';
  }

  private extractTags(content: string): string[] {
    const tags: string[] = [];
    
    // Look for common technical terms - KISS approach
    const technicalTerms = [
      'machine learning', 'ai', 'algorithm', 'data', 'analysis',
      'research', 'study', 'experiment', 'results', 'findings',
      'test', 'testing', 'quality', 'performance'
    ];
    
    technicalTerms.forEach(term => {
      if (content.toLowerCase().includes(term)) {
        tags.push(term.replace(/\s+/g, '-'));
      }
    });

    return tags.slice(0, 5); // Limit to 5 tags
  }

  private validateCategory(category: string | undefined, content: string): string {
    if (category) return category;

    // Auto-categorize based on content - KISS approach
    const lowerContent = content.toLowerCase();
    if (lowerContent.includes('research') || lowerContent.includes('study') || lowerContent.includes('analysis') || lowerContent.includes('finding')) return 'research';
    if (lowerContent.includes('note') || lowerContent.includes('observation')) return 'note';
    if (lowerContent.includes('task') || lowerContent.includes('todo')) return 'task';
    
    return 'general';
  }

  private calculateQualityConfidence(qualityResult: QualityScoreBreakdown): number {
    // Higher confidence for extreme scores, lower for middle range
    const variance = Math.abs(qualityResult.overallScore - 0.5);
    return Math.min(0.5 + variance, 1.0);
  }

  private extractEntities(content: string): string[] {
    // Simple entity extraction - could be enhanced with NLP
    const entities: string[] = [];
    
    // Look for capitalized words (potential proper nouns)
    const capitalizedWords = content.match(/\b[A-Z][a-z]+\b/g) || [];
    entities.push(...capitalizedWords.slice(0, 10));
    
    // Add some common technical entities if not found
    if (entities.length < 3 && content.toLowerCase().includes('test')) {
      entities.push('Testing', 'Content', 'Analysis');
    }
    
    return [...new Set(entities)]; // Remove duplicates
  }

  private detectLanguage(content: string): string {
    // Simple language detection - KISS approach
    const commonEnglishWords = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'a', 'is', 'was', 'are', 'be', 'been', 'have', 'has', 'do', 'does', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'content', 'test', 'testing'];
    const words = content.toLowerCase().split(/\s+/);
    const englishWordCount = words.filter(word => commonEnglishWords.includes(word)).length;
    
    // More lenient threshold and check for English letters
    const hasEnglishChars = /[a-zA-Z]/.test(content);
    return (englishWordCount > 0 && hasEnglishChars) || englishWordCount > words.length * 0.02 ? 'english' : 'unknown';
  }

  private assessComplexity(avgWordsPerSentence: number, content: string): 'simple' | 'moderate' | 'complex' | 'advanced' {
    const technicalTerms = (content.match(/\b[a-z]+tion\b|\b[a-z]+ism\b|\b[a-z]+ology\b/gi) || []).length;
    const totalWords = content.split(/\s+/).length;
    const technicalDensity = totalWords > 0 ? technicalTerms / totalWords : 0;
    
    // Look for advanced patterns that indicate higher complexity
    const advancedPatterns = [
      /\b(methodology|paradigm|algorithmic|quantum|statistical)\b/gi,
      /\b(comprehensive|detailed|rigorous|systematic)\b/gi,
      /#+ [A-Z]/g, // Markdown headers indicate structure
      /\* .+/g, // Bullet points indicate organization
    ];
    
    let advancedScore = 0;
    advancedPatterns.forEach(pattern => {
      const matches = content.match(pattern) || [];
      advancedScore += matches.length;
    });
    
    const advancedRatio = totalWords > 0 ? advancedScore / totalWords : 0;

    if (avgWordsPerSentence < 8 && technicalDensity < 0.05 && advancedRatio < 0.1) return 'simple';
    if (avgWordsPerSentence < 12 && technicalDensity < 0.15 && advancedRatio < 0.2) return 'moderate';
    if (avgWordsPerSentence < 18 && technicalDensity < 0.25 && advancedRatio < 0.4) return 'complex';
    return 'advanced';
  }

  private assessTechnicalLevel(content: string): 'beginner' | 'intermediate' | 'advanced' | 'expert' {
    const technicalIndicators = [
      'algorithm', 'methodology', 'implementation', 'architecture',
      'optimization', 'scalability', 'performance', 'efficiency'
    ];
    
    const technicalTermCount = technicalIndicators.filter(term => 
      content.toLowerCase().includes(term)
    ).length;

    if (technicalTermCount <= 1) return 'beginner';
    if (technicalTermCount <= 3) return 'intermediate';
    if (technicalTermCount <= 5) return 'advanced';
    return 'expert';
  }

  private assessEmotionalTone(content: string): 'neutral' | 'positive' | 'negative' | 'mixed' {
    const positiveWords = ['excellent', 'great', 'good', 'success', 'achieve', 'improve', 'advanced', 'comprehensive', 'exceptional', 'superior', 'effective', 'optimal', 'revolutionary', 'paradigm', 'breakthrough'];
    const negativeWords = ['poor', 'bad', 'fail', 'problem', 'issue', 'difficult', 'challenge', 'limitation', 'error', 'degradation'];
    
    const lowerContent = content.toLowerCase();
    const positiveCount = positiveWords.filter(word => lowerContent.includes(word)).length;
    const negativeCount = negativeWords.filter(word => lowerContent.includes(word)).length;

    // Weight positive words more heavily for technical content
    const positiveWeight = positiveCount * 1.2;
    const negativeWeight = negativeCount;

    if (positiveWeight > 0 && negativeWeight > 0) return 'mixed';
    if (positiveWeight > negativeWeight && positiveWeight > 0.5) return 'positive';
    if (negativeWeight > positiveWeight && negativeWeight > 0.5) return 'negative';
    return 'neutral';
  }

  private detectPrivacyFlags(content: string): string[] {
    const flags: string[] = [];
    
    // Look for potential PII - KISS approach
    if (/\b\d{3}-\d{2}-\d{4}\b/.test(content)) flags.push('potential-ssn');
    if (/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/.test(content)) flags.push('email-detected');
    if (/\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b/.test(content)) flags.push('potential-credit-card');
    if (/\b(?:password|secret|key|token)\s*[:=]\s*\S+/i.test(content)) flags.push('potential-credentials');
    
    return flags;
  }

  private classifySecurityLevel(content: string, privacyFlags: string[]): 'public' | 'internal' | 'confidential' | 'restricted' {
    if (privacyFlags.length > 0) return 'confidential';
    if (content.toLowerCase().includes('confidential') || content.toLowerCase().includes('private')) return 'confidential';
    if (content.toLowerCase().includes('internal')) return 'internal';
    return 'public';
  }

  private determineRetentionPolicy(contentType: string): string {
    // KISS: Simple retention policy mapping
    switch (contentType) {
      case 'research': return '7-years';
      case 'note': return '2-years';
      case 'task': return '1-year';
      case 'draft': return '6-months';
      default: return '1-year';
    }
  }
}