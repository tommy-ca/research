import { createStep } from '@mastra/core';
import { z } from 'zod';
import { QualityAssessmentTool } from '@/tools/quality-assessment-tool';
import { DuplicateDetectionTool } from '@/tools/duplicate-detection-tool';

// Input/Output Schemas for typed steps
const captureInputSchema = z.object({
  content: z.string().min(1),
  source: z.string().min(1),
  type: z.enum(['text', 'url', 'file', 'clipboard']),
  metadata: z.record(z.any()).optional(),
});

const captureOutputSchema = z.object({
  id: z.string(),
  capturedContent: z.string(),
  extractedMetadata: z.record(z.any()),
  qualityScore: z.number().min(0).max(1),
  processed: z.boolean(),
});

const qualityAssessmentInputSchema = z.object({
  capturedContent: z.string(),
  extractedMetadata: z.record(z.any()),
  qualityScore: z.number(),
});

const qualityAssessmentOutputSchema = z.object({
  overallScore: z.number().min(0).max(1),
  readabilityScore: z.number().min(0).max(1),
  structureScore: z.number().min(0).max(1),
  conceptDensityScore: z.number().min(0).max(1),
  passesQualityGate: z.boolean(),
  improvementSuggestions: z.array(z.string()),
  metrics: z.record(z.any()),
});

const duplicateDetectionInputSchema = z.object({
  capturedContent: z.string(),
  existingContent: z.array(z.string()),
  similarityThreshold: z.number().min(0).max(1).default(0.8),
});

const duplicateDetectionOutputSchema = z.object({
  isDuplicate: z.boolean(),
  similarityScore: z.number().min(0).max(1),
  duplicateIndex: z.number().optional(),
  consolidationRecommendation: z.string().optional(),
});

const complianceValidationInputSchema = z.object({
  capturedContent: z.string(),
  qualityScore: z.number(),
  duplicateStatus: z.object({
    isDuplicate: z.boolean(),
    similarityScore: z.number().optional(),
  }),
  extractedMetadata: z.record(z.any()),
});

const complianceValidationOutputSchema = z.object({
  gtdCompliance: z.boolean(),
  captureCompleteness: z.number().min(0).max(1),
  informationFidelity: z.number().min(0).max(1),
  handoffReady: z.boolean(),
  improvementRequired: z.boolean(),
  complianceScore: z.number().min(0).max(1),
});

// Capture Step Implementation
export const captureStep = createStep({
  id: 'capture',
  inputSchema: captureInputSchema,
  outputSchema: captureOutputSchema,
  execute: async ({ input, context }) => {
    try {
      // Generate unique ID
      const id = `capture_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      // Use agent for content processing if available
      let processedContent = input.content;
      if (context.agents?.captureAgent) {
        const result = await context.agents.captureAgent.generate({
          messages: [{
            role: 'user',
            content: `Process this ${input.type} content from ${input.source}: ${input.content}`
          }]
        });
        processedContent = result.text || input.content;
      }
      
      // Extract basic metadata
      const extractedMetadata = {
        originalSource: input.source,
        contentType: input.type,
        captureTimestamp: new Date().toISOString(),
        wordCount: input.content.split(/\s+/).length,
        ...input.metadata,
      };
      
      // Calculate basic quality score
      const qualityScore = calculateBasicQualityScore(input.content);
      
      return {
        id,
        capturedContent: processedContent,
        extractedMetadata,
        qualityScore,
        processed: true,
      };
      
    } catch (error) {
      const captureError = new Error(`Capture step failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      (captureError as any).step = 'capture';
      throw captureError;
    }
  },
});

// Quality Assessment Step Implementation
export const qualityAssessmentStep = createStep({
  id: 'quality-assessment',
  inputSchema: qualityAssessmentInputSchema,
  outputSchema: qualityAssessmentOutputSchema,
  execute: async ({ input, context }) => {
    try {
      const qualityTool = new QualityAssessmentTool();
      const assessment = await qualityTool.assessQuality(input.capturedContent);
      
      const passesQualityGate = assessment.overallScore >= 0.7; // Quality gate threshold
      
      const improvementSuggestions = [];
      if (assessment.readabilityScore < 0.6) {
        improvementSuggestions.push('Improve sentence structure and readability');
      }
      if (assessment.structureScore < 0.6) {
        improvementSuggestions.push('Add better structure with headers and lists');
      }
      if (assessment.conceptDensityScore < 0.6) {
        improvementSuggestions.push('Increase concept density with more specific terminology');
      }
      
      return {
        overallScore: assessment.overallScore,
        readabilityScore: assessment.readabilityScore,
        structureScore: assessment.structureScore,
        conceptDensityScore: assessment.conceptDensityScore,
        passesQualityGate,
        improvementSuggestions,
        metrics: assessment.metrics,
      };
      
    } catch (error) {
      throw new Error(`Quality assessment step failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  },
});

// Duplicate Detection Step Implementation
export const duplicateDetectionStep = createStep({
  id: 'duplicate-detection',
  inputSchema: duplicateDetectionInputSchema,
  outputSchema: duplicateDetectionOutputSchema,
  execute: async ({ input, context }) => {
    try {
      const duplicateTool = new DuplicateDetectionTool();
      const result = await duplicateTool.detectDuplicates({
        content: input.capturedContent,
        existingContent: input.existingContent,
        similarityThreshold: input.similarityThreshold,
      });
      
      return {
        isDuplicate: result.isDuplicate,
        similarityScore: result.similarityScore,
        duplicateIndex: result.duplicateIndex,
        consolidationRecommendation: result.consolidationRecommendation,
      };
      
    } catch (error) {
      throw new Error(`Duplicate detection step failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  },
});

// Compliance Validation Step Implementation
export const complianceValidationStep = createStep({
  id: 'compliance-validation',
  inputSchema: complianceValidationInputSchema,
  outputSchema: complianceValidationOutputSchema,
  execute: async ({ input, context }) => {
    try {
      // GTD Compliance Assessment
      const captureCompleteness = assessCaptureCompleteness(input.capturedContent);
      const informationFidelity = assessInformationFidelity(
        input.capturedContent, 
        input.extractedMetadata
      );
      
      // Overall compliance score
      const complianceScore = (
        (captureCompleteness * 0.4) +
        (informationFidelity * 0.3) +
        (input.qualityScore * 0.2) +
        ((input.duplicateStatus.isDuplicate ? 0.5 : 1.0) * 0.1)
      );
      
      const gtdCompliance = complianceScore >= 0.8; // GTD requires high fidelity
      const handoffReady = gtdCompliance && !input.duplicateStatus.isDuplicate;
      const improvementRequired = complianceScore < 0.7;
      
      return {
        gtdCompliance,
        captureCompleteness,
        informationFidelity,
        handoffReady,
        improvementRequired,
        complianceScore,
      };
      
    } catch (error) {
      throw new Error(`Compliance validation step failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  },
});

// Helper Functions
function calculateBasicQualityScore(content: string): number {
  const words = content.trim().split(/\s+/);
  const wordCount = words.length;
  
  let score = 0.3; // Base score
  
  // Word count factor
  if (wordCount >= 10) score += 0.2;
  if (wordCount >= 50) score += 0.2;
  
  // Structure factor
  if (/^#|\*\s|-\s|\d+\.\s/m.test(content)) {
    score += 0.2;
  }
  
  // Sentence structure factor
  if (/[.!?]/.test(content)) {
    score += 0.1;
  }
  
  return Math.max(0, Math.min(1, score));
}

function assessCaptureCompleteness(content: string): number {
  const words = content.trim().split(/\s+/);
  const wordCount = words.length;
  
  // Completeness based on content richness
  if (wordCount < 5) return 0.2;
  if (wordCount < 20) return 0.5;
  if (wordCount < 100) return 0.8;
  return 0.95;
}

function assessInformationFidelity(content: string, metadata: Record<string, any>): number {
  let fidelity = 0.5; // Base fidelity
  
  // Metadata completeness contributes to fidelity
  const metadataFields = Object.keys(metadata);
  if (metadataFields.length > 3) fidelity += 0.2;
  
  // Content richness contributes to fidelity
  const hasStructure = /^#|\*\s|-\s|\d+\.\s/m.test(content);
  if (hasStructure) fidelity += 0.2;
  
  // Source attribution contributes to fidelity
  if (metadata.originalSource) fidelity += 0.1;
  
  return Math.max(0, Math.min(1, fidelity));
}