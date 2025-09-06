import { describe, it, expect, beforeEach, vi } from 'vitest';
import { QualityScoreBreakdown, DuplicationResult } from '@/types/quality-assessment';

/**
 * Enhanced Metadata Capture Test Suite
 * TDD Cycle 1.4 - Rich metadata generation and management
 */

interface BaseMetadata {
  title?: string;
  author?: string;
  source: string;
  contentType: string;
  tags?: string[];
  category?: string;
  createdAt?: string;
  modifiedAt?: string;
}

interface QualityMetadata {
  qualityBreakdown: QualityScoreBreakdown;
  qualityTimestamp: string;
  qualityVersion: string;
  qualityConfidence: number;
  qualityFlags: string[];
}

interface WorkflowMetadata {
  workflowVersion: string;
  processingStage: 'captured' | 'analyzed' | 'routed' | 'enhanced' | 'archived';
  routingDecision: 'accept' | 'review' | 'reject' | 'enhance';
  routingReason: string;
  routingConfidence: number;
  processingTimeMs: number;
  performanceFlags: string[];
}

interface DuplicationMetadata {
  duplicationStatus: DuplicationResult;
  duplicationTimestamp: string;
  similarityAnalysisVersion: string;
  nearDuplicates?: {
    contentId: string;
    similarityScore: number;
    sourceLocation: string;
  }[];
}

interface ContextualMetadata {
  extractedEntities?: string[];
  detectedLanguage?: string;
  estimatedReadingTime?: number;
  complexity?: 'simple' | 'moderate' | 'complex' | 'advanced';
  technicalLevel?: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  emotionalTone?: 'neutral' | 'positive' | 'negative' | 'mixed';
}

interface ComplianceMetadata {
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

interface EnhancedMetadataPackage {
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

class EnhancedMetadataGenerator {
  private readonly version = '1.4.0';
  private readonly schemaVersion = '2.1.0';

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

  private generateQualityMetadata(qualityResult: QualityScoreBreakdown, timestamp: string): QualityMetadata {
    const qualityFlags: string[] = [];

    // Generate quality flags based on scores
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

  private generateWorkflowMetadata(workflowResult: any, timestamp: string): WorkflowMetadata {
    const performanceFlags: string[] = [];
    
    if (workflowResult.processingTimeMs > 100) performanceFlags.push('slow-processing');
    if (workflowResult.processingTimeMs < 10) performanceFlags.push('fast-processing');
    if (workflowResult.routingConfidence < 0.5) performanceFlags.push('low-confidence-routing');

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

  private generateDuplicationMetadata(duplicationResult: DuplicationResult, timestamp: string): DuplicationMetadata {
    return {
      duplicationStatus: duplicationResult,
      duplicationTimestamp: timestamp,
      similarityAnalysisVersion: this.version,
      // Could be extended to include near-duplicates in future
      nearDuplicates: duplicationResult.similarityScore > 0.5 ? [{
        contentId: 'mock-similar-content',
        similarityScore: duplicationResult.similarityScore,
        sourceLocation: 'existing-content-store'
      }] : undefined
    };
  }

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

  // Helper methods for metadata enrichment
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
    
    // Look for common technical terms
    const technicalTerms = [
      'machine learning', 'ai', 'algorithm', 'data', 'analysis',
      'research', 'study', 'experiment', 'results', 'findings'
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

    // Auto-categorize based on content
    const lowerContent = content.toLowerCase();
    if (lowerContent.includes('research') || lowerContent.includes('study')) return 'research';
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
    // Simple entity extraction (could be enhanced with NLP)
    const entities: string[] = [];
    
    // Look for capitalized words (potential proper nouns)
    const capitalizedWords = content.match(/\b[A-Z][a-z]+\b/g) || [];
    entities.push(...capitalizedWords.slice(0, 10));
    
    return [...new Set(entities)]; // Remove duplicates
  }

  private detectLanguage(content: string): string {
    // Simple language detection (could be enhanced)
    const commonEnglishWords = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'];
    const words = content.toLowerCase().split(/\s+/);
    const englishWordCount = words.filter(word => commonEnglishWords.includes(word)).length;
    
    return englishWordCount > words.length * 0.05 ? 'english' : 'unknown';
  }

  private assessComplexity(avgWordsPerSentence: number, content: string): 'simple' | 'moderate' | 'complex' | 'advanced' {
    const technicalTerms = (content.match(/\b[a-z]+tion\b|\b[a-z]+ism\b|\b[a-z]+ology\b/gi) || []).length;
    const totalWords = content.split(/\s+/).length;
    const technicalDensity = technicalTerms / totalWords;

    if (avgWordsPerSentence < 10 && technicalDensity < 0.1) return 'simple';
    if (avgWordsPerSentence < 15 && technicalDensity < 0.2) return 'moderate';
    if (avgWordsPerSentence < 20 && technicalDensity < 0.3) return 'complex';
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
    const positiveWords = ['excellent', 'great', 'good', 'success', 'achieve', 'improve'];
    const negativeWords = ['poor', 'bad', 'fail', 'problem', 'issue', 'difficult'];
    
    const lowerContent = content.toLowerCase();
    const positiveCount = positiveWords.filter(word => lowerContent.includes(word)).length;
    const negativeCount = negativeWords.filter(word => lowerContent.includes(word)).length;

    if (positiveCount > 0 && negativeCount > 0) return 'mixed';
    if (positiveCount > 0) return 'positive';
    if (negativeCount > 0) return 'negative';
    return 'neutral';
  }

  private detectPrivacyFlags(content: string): string[] {
    const flags: string[] = [];
    
    // Look for potential PII
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
    switch (contentType) {
      case 'research': return '7-years';
      case 'note': return '2-years';
      case 'task': return '1-year';
      case 'draft': return '6-months';
      default: return '1-year';
    }
  }
}

describe('TDD Cycle 1.4 - Enhanced Metadata Capture', () => {
  let metadataGenerator: EnhancedMetadataGenerator;

  beforeEach(() => {
    metadataGenerator = new EnhancedMetadataGenerator();
  });

  describe('Base Metadata Enrichment', () => {
    it('should auto-generate missing title from content', () => {
      const content = '# Machine Learning Applications\n\nThis document explores various applications.';
      const baseMetadata: BaseMetadata = {
        source: 'document-upload',
        contentType: 'research'
      };
      
      const mockQuality: QualityScoreBreakdown = {
        overallScore: 0.8, readabilityScore: 0.7, structureScore: 0.9,
        conceptDensityScore: 0.8, originalityScore: 0.7
      };
      
      const mockDuplication: DuplicationResult = {
        isDuplicate: false, similarityScore: 0.1
      };
      
      const mockWorkflow = {
        routingDecision: 'accept' as const, routingReason: 'High quality',
        routingConfidence: 0.9, processingTimeMs: 15
      };

      const result = metadataGenerator.generateMetadataPackage(
        content, baseMetadata, mockQuality, mockDuplication, mockWorkflow
      );

      expect(result.base.title).toBe('Machine Learning Applications');
      expect(result.base.createdAt).toBeDefined();
      expect(result.base.modifiedAt).toBeDefined();
      expect(result.base.tags).toBeDefined();
      expect(result.base.category).toBe('research');

      console.log(`✅ Auto-generated title: "${result.base.title}"`);
    });

    it('should extract relevant tags from content', () => {
      const content = 'This research study focuses on machine learning algorithms and data analysis techniques.';
      const baseMetadata: BaseMetadata = {
        source: 'paper-import',
        contentType: 'research'
      };

      const mockQuality: QualityScoreBreakdown = {
        overallScore: 0.75, readabilityScore: 0.8, structureScore: 0.7,
        conceptDensityScore: 0.75, originalityScore: 0.75
      };

      const result = metadataGenerator.generateMetadataPackage(
        content, baseMetadata, mockQuality, 
        { isDuplicate: false, similarityScore: 0.05 },
        { routingDecision: 'accept', routingReason: 'Good quality', routingConfidence: 0.8, processingTimeMs: 20 }
      );

      expect(result.base.tags).toContain('machine-learning');
      expect(result.base.tags).toContain('data');
      expect(result.base.tags).toContain('research');
      expect(result.base.tags).toContain('study');

      console.log(`✅ Extracted tags: ${result.base.tags?.join(', ')}`);
    });
  });

  describe('Quality Metadata Generation', () => {
    it('should generate comprehensive quality metadata with flags', () => {
      const content = 'Test content for quality metadata';
      
      const lowQualityResult: QualityScoreBreakdown = {
        overallScore: 0.25, readabilityScore: 0.2, structureScore: 0.1,
        conceptDensityScore: 0.4, originalityScore: 0.3
      };

      const result = metadataGenerator.generateMetadataPackage(
        content, 
        { source: 'test', contentType: 'note' },
        lowQualityResult,
        { isDuplicate: false, similarityScore: 0.0 },
        { routingDecision: 'reject', routingReason: 'Low quality', routingConfidence: 0.9, processingTimeMs: 12 }
      );

      expect(result.quality.qualityBreakdown).toEqual(lowQualityResult);
      expect(result.quality.qualityFlags).toContain('low-quality');
      expect(result.quality.qualityFlags).toContain('poor-structure');
      expect(result.quality.qualityVersion).toBe('1.4.0');
      expect(result.quality.qualityConfidence).toBeLessThan(0.8);

      console.log(`✅ Quality flags generated: ${result.quality.qualityFlags.join(', ')}`);
    });

    it('should identify high-quality content with appropriate flags', () => {
      const highQualityResult: QualityScoreBreakdown = {
        overallScore: 0.95, readabilityScore: 0.9, structureScore: 0.95,
        conceptDensityScore: 0.92, originalityScore: 0.88
      };

      const result = metadataGenerator.generateMetadataPackage(
        'High quality test content',
        { source: 'test', contentType: 'research' },
        highQualityResult,
        { isDuplicate: false, similarityScore: 0.05 },
        { routingDecision: 'accept', routingReason: 'Excellent quality', routingConfidence: 0.95, processingTimeMs: 8 }
      );

      expect(result.quality.qualityFlags).toContain('high-quality');
      expect(result.quality.qualityFlags).toContain('concept-dense');
      expect(result.quality.qualityConfidence).toBeGreaterThan(0.9);

      console.log(`✅ High quality flags: ${result.quality.qualityFlags.join(', ')}`);
    });
  });

  describe('Workflow Metadata Generation', () => {
    it('should capture workflow processing details with performance flags', () => {
      const content = 'Workflow metadata test content';

      const slowProcessingWorkflow = {
        routingDecision: 'review' as const,
        routingReason: 'Moderate quality requires review',
        routingConfidence: 0.6,
        processingTimeMs: 150 // Slow processing
      };

      const result = metadataGenerator.generateMetadataPackage(
        content,
        { source: 'test', contentType: 'note' },
        { overallScore: 0.6, readabilityScore: 0.6, structureScore: 0.6, conceptDensityScore: 0.6, originalityScore: 0.6 },
        { isDuplicate: false, similarityScore: 0.1 },
        slowProcessingWorkflow
      );

      expect(result.workflow.routingDecision).toBe('review');
      expect(result.workflow.routingReason).toBe('Moderate quality requires review');
      expect(result.workflow.routingConfidence).toBe(0.6);
      expect(result.workflow.processingTimeMs).toBe(150);
      expect(result.workflow.performanceFlags).toContain('slow-processing');
      expect(result.workflow.performanceFlags).toContain('low-confidence-routing');

      console.log(`✅ Workflow flags: ${result.workflow.performanceFlags.join(', ')}`);
    });

    it('should identify fast processing with appropriate flags', () => {
      const fastProcessingWorkflow = {
        routingDecision: 'accept' as const,
        routingReason: 'High quality content',
        routingConfidence: 0.95,
        processingTimeMs: 5 // Very fast
      };

      const result = metadataGenerator.generateMetadataPackage(
        'Fast processing test',
        { source: 'test', contentType: 'note' },
        { overallScore: 0.9, readabilityScore: 0.9, structureScore: 0.9, conceptDensityScore: 0.9, originalityScore: 0.9 },
        { isDuplicate: false, similarityScore: 0.02 },
        fastProcessingWorkflow
      );

      expect(result.workflow.performanceFlags).toContain('fast-processing');
      expect(result.workflow.performanceFlags).not.toContain('slow-processing');
      expect(result.workflow.performanceFlags).not.toContain('low-confidence-routing');

      console.log(`✅ Fast processing detected: ${result.workflow.processingTimeMs}ms`);
    });
  });

  describe('Contextual Metadata Analysis', () => {
    it('should analyze content complexity and technical level', () => {
      const technicalContent = `
        The implementation utilizes advanced machine learning algorithms with optimization techniques 
        for scalability and performance enhancement. The architecture incorporates sophisticated 
        methodology for efficient processing and computational efficiency.
      `;

      const result = metadataGenerator.generateMetadataPackage(
        technicalContent,
        { source: 'technical-doc', contentType: 'research' },
        { overallScore: 0.8, readabilityScore: 0.7, structureScore: 0.8, conceptDensityScore: 0.9, originalityScore: 0.8 },
        { isDuplicate: false, similarityScore: 0.1 },
        { routingDecision: 'accept', routingReason: 'Technical content', routingConfidence: 0.85, processingTimeMs: 25 }
      );

      expect(result.contextual.complexity).toBe('advanced');
      expect(result.contextual.technicalLevel).toBe('expert');
      expect(result.contextual.detectedLanguage).toBe('english');
      expect(result.contextual.estimatedReadingTime).toBeGreaterThan(0);

      console.log(`✅ Technical analysis: ${result.contextual.complexity}/${result.contextual.technicalLevel}`);
    });

    it('should extract entities and assess emotional tone', () => {
      const content = `
        The research by Dr. Smith at Stanford University shows excellent results. 
        The team achieved great success with their innovative approach to solving complex problems.
      `;

      const result = metadataGenerator.generateMetadataPackage(
        content,
        { source: 'research-paper', contentType: 'research' },
        { overallScore: 0.85, readabilityScore: 0.8, structureScore: 0.85, conceptDensityScore: 0.8, originalityScore: 0.9 },
        { isDuplicate: false, similarityScore: 0.05 },
        { routingDecision: 'accept', routingReason: 'High quality research', routingConfidence: 0.9, processingTimeMs: 18 }
      );

      expect(result.contextual.extractedEntities).toContain('Smith');
      expect(result.contextual.extractedEntities).toContain('Stanford');
      expect(result.contextual.extractedEntities).toContain('University');
      expect(result.contextual.emotionalTone).toBe('positive');

      console.log(`✅ Entities: ${result.contextual.extractedEntities?.slice(0, 3).join(', ')}`);
      console.log(`✅ Emotional tone: ${result.contextual.emotionalTone}`);
    });
  });

  describe('Compliance and Security Metadata', () => {
    it('should detect privacy flags and classify security level', () => {
      const sensitiveContent = `
        Contact information: john.doe@example.com
        Please update the password: secret123
        Internal use only - confidential research data
      `;

      const result = metadataGenerator.generateMetadataPackage(
        sensitiveContent,
        { source: 'internal-system', contentType: 'note' },
        { overallScore: 0.6, readabilityScore: 0.6, structureScore: 0.6, conceptDensityScore: 0.6, originalityScore: 0.6 },
        { isDuplicate: false, similarityScore: 0.0 },
        { routingDecision: 'review', routingReason: 'Contains sensitive data', routingConfidence: 0.8, processingTimeMs: 30 }
      );

      expect(result.compliance.privacyFlags).toContain('email-detected');
      expect(result.compliance.privacyFlags).toContain('potential-credentials');
      expect(result.compliance.securityClassification).toBe('confidential');
      expect(result.compliance.retentionPolicy).toBe('2-years');
      expect(result.compliance.auditTrail).toHaveLength(1);

      console.log(`✅ Privacy flags: ${result.compliance.privacyFlags.join(', ')}`);
      console.log(`✅ Security level: ${result.compliance.securityClassification}`);
    });

    it('should set appropriate retention policies by content type', () => {
      const contentTypes = ['research', 'note', 'task', 'draft'];
      const expectedRetentions = ['7-years', '2-years', '1-year', '6-months'];

      contentTypes.forEach((contentType, index) => {
        const result = metadataGenerator.generateMetadataPackage(
          `Test content for ${contentType}`,
          { source: 'test', contentType },
          { overallScore: 0.7, readabilityScore: 0.7, structureScore: 0.7, conceptDensityScore: 0.7, originalityScore: 0.7 },
          { isDuplicate: false, similarityScore: 0.0 },
          { routingDecision: 'accept', routingReason: 'Standard content', routingConfidence: 0.8, processingTimeMs: 15 }
        );

        expect(result.compliance.retentionPolicy).toBe(expectedRetentions[index]);
        console.log(`✅ ${contentType} retention: ${result.compliance.retentionPolicy}`);
      });
    });
  });

  describe('Metadata Package Integrity', () => {
    it('should generate complete metadata package with all sections', () => {
      const content = 'Complete metadata package test content';
      
      const result = metadataGenerator.generateMetadataPackage(
        content,
        { source: 'test-system', contentType: 'note', author: 'test-user' },
        { overallScore: 0.7, readabilityScore: 0.7, structureScore: 0.7, conceptDensityScore: 0.7, originalityScore: 0.7 },
        { isDuplicate: false, similarityScore: 0.15 },
        { routingDecision: 'accept', routingReason: 'Good quality', routingConfidence: 0.8, processingTimeMs: 20 }
      );

      // Verify all sections are present
      expect(result.base).toBeDefined();
      expect(result.quality).toBeDefined();
      expect(result.workflow).toBeDefined();
      expect(result.duplication).toBeDefined();
      expect(result.contextual).toBeDefined();
      expect(result.compliance).toBeDefined();

      // Verify package metadata
      expect(result.version).toBe('1.4.0');
      expect(result.schemaVersion).toBe('2.1.0');
      expect(result.generatedAt).toBeDefined();

      console.log(`✅ Complete package generated with version ${result.version}`);
    });

    it('should maintain consistent timestamps across related metadata', () => {
      const content = 'Timestamp consistency test';
      
      const result = metadataGenerator.generateMetadataPackage(
        content,
        { source: 'test', contentType: 'note' },
        { overallScore: 0.8, readabilityScore: 0.8, structureScore: 0.8, conceptDensityScore: 0.8, originalityScore: 0.8 },
        { isDuplicate: false, similarityScore: 0.05 },
        { routingDecision: 'accept', routingReason: 'High quality', routingConfidence: 0.9, processingTimeMs: 12 }
      );

      // All timestamps should be very close (within same second)
      const packageTime = new Date(result.generatedAt);
      const qualityTime = new Date(result.quality.qualityTimestamp);
      const duplicationTime = new Date(result.duplication.duplicationTimestamp);

      expect(Math.abs(packageTime.getTime() - qualityTime.getTime())).toBeLessThan(1000);
      expect(Math.abs(packageTime.getTime() - duplicationTime.getTime())).toBeLessThan(1000);

      console.log(`✅ Timestamp consistency maintained within ${Math.abs(packageTime.getTime() - qualityTime.getTime())}ms`);
    });
  });
});