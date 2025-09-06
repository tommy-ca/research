import { describe, it, expect, beforeEach } from 'vitest';
import { z } from 'zod';
import { createWorkflow, createStep } from '@mastra/core';
import { enhancedCaptureWorkflow } from '@/workflow/enhanced-capture-workflow';
import { captureAgent } from '@/agents/capture-agent';

describe('Enhanced Capture Workflow - Mastra 2025 Patterns', () => {
  describe('createWorkflow Pattern Compliance', () => {
    it('should be created using createWorkflow with proper schemas', () => {
      // This test SHOULD FAIL initially as we need to convert existing implementation
      expect(enhancedCaptureWorkflow).toBeDefined();
      expect(typeof enhancedCaptureWorkflow.execute).toBe('function');
      expect(typeof enhancedCaptureWorkflow.stream).toBe('function');
      expect(typeof enhancedCaptureWorkflow.watch).toBe('function');
    });

    it('should have proper trigger schema validation', () => {
      const triggerSchema = enhancedCaptureWorkflow.triggerSchema;
      
      // Valid input should pass
      const validInput = {
        content: "Test content for processing",
        source: "https://example.com",
        type: "url" as const,
        metadata: { title: "Test Article" }
      };
      
      expect(() => triggerSchema.parse(validInput)).not.toThrow();
      
      // Invalid input should fail
      const invalidInput = {
        content: "", // Empty content should fail
        source: "invalid-url", 
        type: "unknown" as any
      };
      
      expect(() => triggerSchema.parse(invalidInput)).toThrow();
    });

    it('should have proper output schema validation', () => {
      const outputSchema = enhancedCaptureWorkflow.outputSchema;
      
      const validOutput = {
        captureId: "capture_123456789_abc123def",
        processedContent: "Processed test content",
        qualityScore: 0.85,
        duplicateStatus: {
          isDuplicate: false,
        },
        gtdCompliance: true,
        handoffReady: true,
      };
      
      expect(() => outputSchema.parse(validOutput)).not.toThrow();
    });
  });

  describe('createStep Integration', () => {
    it('should use typed createStep pattern for capture step', async () => {
      // This should fail initially - we need to implement createStep patterns
      const mockInput = {
        content: "Test content",
        source: "test-source",
        type: "text" as const,
      };

      // The workflow should be composed of createStep instances
      // This test validates that our workflow uses the modern pattern
      const result = await enhancedCaptureWorkflow.execute(mockInput);
      
      expect(result).toBeDefined();
      expect(result.status).toBe('success');
      if (result.status === 'success') {
        expect(result.output.captureId).toBeDefined();
        expect(result.output.processedContent).toBeDefined();
        expect(typeof result.output.qualityScore).toBe('number');
        expect(result.output.qualityScore).toBeGreaterThanOrEqual(0);
        expect(result.output.qualityScore).toBeLessThanOrEqual(1);
      }
    });

    it('should handle workflow suspension for human input', async () => {
      // Test that workflow can suspend when quality is too low
      const lowQualityInput = {
        content: "x", // Very low quality content
        source: "unknown",
        type: "text" as const,
      };

      const result = await enhancedCaptureWorkflow.execute(lowQualityInput);
      
      // Should suspend for human review when quality is insufficient
      expect(result.status).toBe('suspended');
    });

    it('should handle workflow failure gracefully', async () => {
      const invalidInput = {
        content: "Test content",
        source: "", // Empty source should cause failure
        type: "url" as const,
      };

      const result = await enhancedCaptureWorkflow.execute(invalidInput);
      
      expect(result.status).toBe('failed');
      expect(result.error).toBeDefined();
    });
  });

  describe('Agent Integration within Workflow', () => {
    it('should properly integrate capture agent within workflow steps', async () => {
      // This tests that our workflow properly uses agents within createStep execution
      const testInput = {
        content: "High quality test content with good structure and comprehensive details",
        source: "https://example.com/article",
        type: "url" as const,
        metadata: { title: "Test Article", author: "Test Author" }
      };

      const result = await enhancedCaptureWorkflow.execute(testInput);
      
      expect(result.status).toBe('success');
      if (result.status === 'success') {
        // Validate that the agent processed the content
        expect(result.output.processedContent).toBeDefined();
        expect(result.output.processedContent.length).toBeGreaterThan(0);
        
        // Quality score should be reasonable for good content
        expect(result.output.qualityScore).toBeGreaterThan(0.5);
        
        // GTD compliance for well-structured content
        expect(result.output.gtdCompliance).toBe(true);
      }
    });
  });

  describe('Type Safety and Schema Validation', () => {
    it('should maintain strict TypeScript typing throughout workflow', () => {
      // This test validates that our workflow maintains type safety
      const triggerSchema = enhancedCaptureWorkflow.triggerSchema;
      const outputSchema = enhancedCaptureWorkflow.outputSchema;
      
      // Schemas should be proper Zod schemas
      expect(triggerSchema).toHaveProperty('_def');
      expect(outputSchema).toHaveProperty('_def');
      
      // Should validate types correctly
      expect(triggerSchema._def.typeName).toBe('ZodObject');
      expect(outputSchema._def.typeName).toBe('ZodObject');
    });

    it('should provide clear error messages for invalid inputs', () => {
      const triggerSchema = enhancedCaptureWorkflow.triggerSchema;
      
      try {
        triggerSchema.parse({
          content: 123, // Wrong type
          source: null, // Wrong type
          type: "invalid", // Invalid enum value
        });
        expect.fail('Should have thrown validation error');
      } catch (error: any) {
        expect(error.message).toContain('Invalid input');
        expect(Array.isArray(error.errors)).toBe(true);
      }
    });
  });

  describe('Performance and Production Requirements', () => {
    it('should execute within acceptable time limits', async () => {
      const startTime = Date.now();
      
      const testInput = {
        content: "Test content for performance validation",
        source: "performance-test",
        type: "text" as const,
      };

      await enhancedCaptureWorkflow.execute(testInput);
      
      const executionTime = Date.now() - startTime;
      
      // Should complete within 2 seconds as per production requirements
      expect(executionTime).toBeLessThan(2000);
    });

    it('should support streaming workflow results', async () => {
      const testInput = {
        content: "Streaming test content",
        source: "stream-test",
        type: "text" as const,
      };

      // Test streaming capability
      let streamResults: any[] = [];
      
      await enhancedCaptureWorkflow.stream(testInput, {
        onStepComplete: (stepResult) => {
          streamResults.push(stepResult);
        }
      });

      // Should have received step-by-step results
      expect(streamResults.length).toBeGreaterThan(0);
    });
  });
});