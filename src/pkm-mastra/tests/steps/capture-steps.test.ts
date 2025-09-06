import { describe, it, expect, beforeEach } from 'vitest';
import { z } from 'zod';
import { createStep } from '@mastra/core';
import { 
  captureStep, 
  qualityAssessmentStep,
  duplicateDetectionStep,
  complianceValidationStep 
} from '@/steps/capture-steps';

describe('Capture Steps - Mastra 2025 createStep Patterns', () => {
  describe('Capture Step Implementation', () => {
    it('should be created using createStep with proper schemas', () => {
      // This test SHOULD FAIL initially - we need to implement these steps
      expect(captureStep).toBeDefined();
      expect(captureStep.inputSchema).toBeDefined();
      expect(captureStep.outputSchema).toBeDefined();
      expect(typeof captureStep.execute).toBe('function');
    });

    it('should have proper input schema validation', () => {
      const inputSchema = captureStep.inputSchema;
      
      const validInput = {
        content: "Test content for capture",
        source: "https://example.com",
        type: "url" as const,
        metadata: { title: "Test" }
      };
      
      expect(() => inputSchema.parse(validInput)).not.toThrow();
      
      // Invalid input should fail
      expect(() => inputSchema.parse({
        content: "", // Empty content
        source: "invalid-url",
        type: "unknown" as any
      })).toThrow();
    });

    it('should have proper output schema validation', () => {
      const outputSchema = captureStep.outputSchema;
      
      const validOutput = {
        id: "capture_123456789_abc123def",
        capturedContent: "Processed content",
        extractedMetadata: { title: "Test" },
        qualityScore: 0.85,
        processed: true,
      };
      
      expect(() => outputSchema.parse(validOutput)).not.toThrow();
    });

    it('should execute capture logic correctly', async () => {
      const testInput = {
        content: "High quality test content with good structure",
        source: "https://example.com/test",
        type: "url" as const,
        metadata: { title: "Test Article" }
      };

      const mockContext = {
        agents: {
          captureAgent: {
            generate: async ({ messages }: any) => ({
              text: "Processed: " + messages[0].content
            })
          }
        }
      };

      const result = await captureStep.execute({ 
        input: testInput, 
        context: mockContext 
      });
      
      expect(result.id).toBeDefined();
      expect(result.capturedContent).toContain("Processed:");
      expect(result.qualityScore).toBeGreaterThan(0);
      expect(result.processed).toBe(true);
    });
  });

  describe('Quality Assessment Step Implementation', () => {
    it('should be created using createStep pattern', () => {
      expect(qualityAssessmentStep).toBeDefined();
      expect(qualityAssessmentStep.inputSchema).toBeDefined();
      expect(qualityAssessmentStep.outputSchema).toBeDefined();
    });

    it('should properly assess content quality', async () => {
      const testInput = {
        capturedContent: "High quality content with excellent structure and comprehensive details",
        extractedMetadata: { title: "Quality Content" },
        qualityScore: 0.8,
      };

      const result = await qualityAssessmentStep.execute({ 
        input: testInput, 
        context: {} 
      });
      
      expect(result.overallScore).toBeGreaterThan(0.7);
      expect(result.readabilityScore).toBeDefined();
      expect(result.structureScore).toBeDefined();
      expect(result.conceptDensityScore).toBeDefined();
      expect(result.passesQualityGate).toBe(true);
    });

    it('should fail quality gate for poor content', async () => {
      const testInput = {
        capturedContent: "x", // Very poor content
        extractedMetadata: {},
        qualityScore: 0.1,
      };

      const result = await qualityAssessmentStep.execute({ 
        input: testInput, 
        context: {} 
      });
      
      expect(result.overallScore).toBeLessThan(0.5);
      expect(result.passesQualityGate).toBe(false);
      expect(result.improvementSuggestions.length).toBeGreaterThan(0);
    });
  });

  describe('Duplicate Detection Step Implementation', () => {
    it('should be created using createStep pattern', () => {
      expect(duplicateDetectionStep).toBeDefined();
      expect(duplicateDetectionStep.inputSchema).toBeDefined();
      expect(duplicateDetectionStep.outputSchema).toBeDefined();
    });

    it('should detect exact duplicates', async () => {
      const testInput = {
        capturedContent: "Duplicate content for testing",
        existingContent: ["Duplicate content for testing", "Other content"],
        similarityThreshold: 0.9,
      };

      const result = await duplicateDetectionStep.execute({ 
        input: testInput, 
        context: {} 
      });
      
      expect(result.isDuplicate).toBe(true);
      expect(result.similarityScore).toBeGreaterThan(0.9);
      expect(result.duplicateIndex).toBe(0);
    });

    it('should not detect false positives', async () => {
      const testInput = {
        capturedContent: "Unique content that should not match",
        existingContent: ["Completely different content", "Another unrelated text"],
        similarityThreshold: 0.8,
      };

      const result = await duplicateDetectionStep.execute({ 
        input: testInput, 
        context: {} 
      });
      
      expect(result.isDuplicate).toBe(false);
      expect(result.similarityScore).toBeLessThan(0.8);
      expect(result.duplicateIndex).toBeUndefined();
    });
  });

  describe('Compliance Validation Step Implementation', () => {
    it('should be created using createStep pattern', () => {
      expect(complianceValidationStep).toBeDefined();
      expect(complianceValidationStep.inputSchema).toBeDefined();
      expect(complianceValidationStep.outputSchema).toBeDefined();
    });

    it('should validate GTD compliance for high-quality captures', async () => {
      const testInput = {
        capturedContent: "Comprehensive content with complete information and proper structure",
        qualityScore: 0.95,
        duplicateStatus: { isDuplicate: false },
        extractedMetadata: { 
          title: "Complete Article",
          source: "https://example.com",
          concepts: ["concept1", "concept2"]
        }
      };

      const result = await complianceValidationStep.execute({ 
        input: testInput, 
        context: {} 
      });
      
      expect(result.gtdCompliance).toBe(true);
      expect(result.captureCompleteness).toBeGreaterThan(0.9);
      expect(result.informationFidelity).toBeGreaterThan(0.9);
      expect(result.handoffReady).toBe(true);
    });

    it('should fail compliance for incomplete captures', async () => {
      const testInput = {
        capturedContent: "Incomplete content",
        qualityScore: 0.3,
        duplicateStatus: { isDuplicate: false },
        extractedMetadata: {}
      };

      const result = await complianceValidationStep.execute({ 
        input: testInput, 
        context: {} 
      });
      
      expect(result.gtdCompliance).toBe(false);
      expect(result.captureCompleteness).toBeLessThan(0.7);
      expect(result.handoffReady).toBe(false);
      expect(result.improvementRequired).toBe(true);
    });
  });

  describe('Type Safety and Error Handling', () => {
    it('should maintain strict typing across all steps', () => {
      const steps = [
        captureStep,
        qualityAssessmentStep,
        duplicateDetectionStep,
        complianceValidationStep
      ];

      steps.forEach(step => {
        expect(step.inputSchema._def.typeName).toBe('ZodObject');
        expect(step.outputSchema._def.typeName).toBe('ZodObject');
      });
    });

    it('should handle invalid inputs gracefully', async () => {
      const invalidInput = {
        content: null, // Invalid type
        source: 123, // Invalid type
        type: "invalid" // Invalid enum
      };

      // Should throw validation error, not runtime error
      await expect(async () => {
        await captureStep.execute({ 
          input: invalidInput as any, 
          context: {} 
        });
      }).rejects.toThrow();
    });

    it('should provide detailed error information', async () => {
      try {
        await captureStep.execute({ 
          input: { content: "", source: "", type: "text" } as any, 
          context: {} 
        });
      } catch (error: any) {
        expect(error.message).toBeDefined();
        expect(error.step).toBe('capture');
      }
    });
  });
});