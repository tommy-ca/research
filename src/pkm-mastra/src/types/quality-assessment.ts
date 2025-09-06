import { z } from 'zod';

// Similarity Calculator Interface (DIP - Depend on abstractions)
export interface SimilarityCalculatorInterface {
  calculateSimilarity(content1: string, content2: string): Promise<number>;
  calculateBatch(content: string, existingContent: string[]): Promise<number[]>;
  calculateWithEarlyTermination(
    content: string, 
    existingContent: string[], 
    threshold: number
  ): Promise<{
    maxSimilarity: number;
    maxIndex: number;
    processed: number;
  }>;
}

// Duplicate Detection Types
export const DuplicationRequestSchema = z.object({
  content: z.string(),
  existingContent: z.array(z.string()),
  threshold: z.number().min(0).max(1).optional().default(0.85),
});
export type DuplicationRequest = z.infer<typeof DuplicationRequestSchema>;

export const DuplicationResultSchema = z.object({
  isDuplicate: z.boolean(),
  similarityScore: z.number().min(0).max(1),
  duplicateIndex: z.number().optional(),
  consolidationRecommendation: z.string().optional(),
});
export type DuplicationResult = z.infer<typeof DuplicationResultSchema>;

// Quality Assessment Types
export const QualityAssessmentConfigSchema = z.object({
  readabilityWeight: z.number().min(0).max(1).default(0.3),
  structureWeight: z.number().min(0).max(1).default(0.3),
  conceptDensityWeight: z.number().min(0).max(1).default(0.2),
  originalityWeight: z.number().min(0).max(1).default(0.2),
});
export type QualityAssessmentConfig = z.infer<typeof QualityAssessmentConfigSchema>;

export const QualityScoreBreakdownSchema = z.object({
  overallScore: z.number().min(0).max(1),
  readabilityScore: z.number().min(0).max(1),
  structureScore: z.number().min(0).max(1),
  conceptDensityScore: z.number().min(0).max(1),
  originalityScore: z.number().min(0).max(1),
  metrics: z.object({
    wordCount: z.number(),
    sentenceCount: z.number(),
    paragraphCount: z.number(),
    averageWordsPerSentence: z.number(),
    structuralElements: z.array(z.string()),
    conceptCount: z.number(),
  }).optional(),
});
export type QualityScoreBreakdown = z.infer<typeof QualityScoreBreakdownSchema>;

// Tool Interfaces following ISP (Interface Segregation Principle)
export interface DuplicateDetectionToolInterface {
  detectDuplicate(content: string, existingContent: string[]): Promise<DuplicationResult>;
}

export interface QualityAssessmentToolInterface {
  assessQuality(content: string): Promise<QualityScoreBreakdown>;
}

// Performance monitoring types
export const PerformanceMetricsSchema = z.object({
  operation: z.string(),
  startTime: z.number(),
  endTime: z.number(),
  duration: z.number(),
  success: z.boolean(),
  error: z.string().optional(),
});
export type PerformanceMetrics = z.infer<typeof PerformanceMetricsSchema>;

// Configuration validation
export const DuplicateDetectionConfigSchema = z.object({
  threshold: z.number().min(0).max(1).default(0.85),
  performanceTarget: z.number().default(50), // milliseconds
  enableEarlyTermination: z.boolean().default(true),
  maxComparisons: z.number().min(1).default(1000),
});
export type DuplicateDetectionConfig = z.infer<typeof DuplicateDetectionConfigSchema>;

// Error types for proper error handling
export class QualityAssessmentError extends Error {
  constructor(message: string, public readonly operation: string, public readonly cause?: Error) {
    super(message);
    this.name = 'QualityAssessmentError';
  }
}

export class DuplicateDetectionError extends Error {
  constructor(message: string, public readonly threshold?: number, public readonly cause?: Error) {
    super(message);
    this.name = 'DuplicateDetectionError';
  }
}

// Mastra.ai Tool Integration Types
export const QualityAssessmentToolSchema = z.object({
  id: z.literal('quality-assessment-tool'),
  description: z.string(),
  inputSchema: z.object({
    content: z.string(),
    config: QualityAssessmentConfigSchema.optional(),
  }),
  outputSchema: QualityScoreBreakdownSchema,
});

export const DuplicateDetectionToolSchema = z.object({
  id: z.literal('duplicate-detection-tool'),
  description: z.string(),
  inputSchema: z.object({
    content: z.string(),
    existingContent: z.array(z.string()),
    threshold: z.number().min(0).max(1).optional(),
  }),
  outputSchema: DuplicationResultSchema,
});

// Integration with existing capture types
export interface EnhancedCaptureOutput {
  id: string;
  content: string;
  source: string;
  type: string;
  extractedMetadata: {
    qualityBreakdown?: QualityScoreBreakdown;
    duplicationStatus?: DuplicationResult;
    [key: string]: any;
  };
  qualityScore: number;
  timestamp: string;
  processed: boolean;
}