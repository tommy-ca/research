import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { DuplicateDetectionTool } from '@/tools/duplicate-detection-tool';
import { QualityAssessmentTool } from '@/tools/quality-assessment-tool';
import { MockSimilarityCalculator } from '@/tools/mock-similarity-calculator';
import { EnhancedCaptureWorkflow } from '@/workflow/enhanced-capture-workflow';
import { 
  QualityScoreBreakdown, 
  DuplicationResult, 
  EnhancedCaptureOutput,
  SimilarityCalculatorInterface 
} from '@/types/quality-assessment';

// Import the actual workflow interfaces  
import { CaptureWorkflowConfig, WorkflowMetrics } from '@/workflow/enhanced-capture-workflow';

describe('TDD Cycle 1.4 - Enhanced Capture Workflow Integration', () => {
  let mockSimilarityCalculator: SimilarityCalculatorInterface;
  let captureWorkflow: EnhancedCaptureWorkflow;

  beforeEach(() => {
    mockSimilarityCalculator = {
      calculateSimilarity: vi.fn(),
      calculateBatch: vi.fn(),
      calculateWithEarlyTermination: vi.fn()
    };
    
    captureWorkflow = new EnhancedCaptureWorkflow(mockSimilarityCalculator);
  });

  afterEach(() => {
    captureWorkflow.clearExistingContent();
  });

  describe('Automated Quality Gates Integration', () => {
    it('should automatically trigger quality assessment during capture', async () => {
      const content = 'High quality content with excellent structure, clear concepts, and comprehensive coverage of the topic at hand.';
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1]);

      const result = await captureWorkflow.processCapture(content);

      expect(result.output.qualityScore).toBeGreaterThan(0.7);
      expect(result.metrics.qualityGateTriggered).toBe(true);
      expect(result.output.extractedMetadata.qualityGatePassed).toBe(true);
      
      console.log(`✅ Quality assessment triggered: Score ${result.output.qualityScore.toFixed(3)}`);
    });

    it('should integrate duplicate detection seamlessly', async () => {
      const content = 'Content for duplicate detection testing';
      
      // Add some existing content to test against
      captureWorkflow.addExistingContent(['Similar content that already exists']);
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.3]);

      const result = await captureWorkflow.processCapture(content);

      expect(result.output.extractedMetadata.duplicationStatus).toBeDefined();
      expect(result.output.extractedMetadata.duplicationStatus.isDuplicate).toBe(false);
      expect(result.output.extractedMetadata.duplicationStatus.similarityScore).toBe(0.3);
      
      console.log(`✅ Duplicate detection integrated: Similarity ${result.output.extractedMetadata.duplicationStatus.similarityScore}`);
    });

    it('should provide performance monitoring during capture', async () => {
      const content = 'Content for performance monitoring';
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.2]);

      const result = await captureWorkflow.processCapture(content);

      expect(result.metrics.processingTimeMs).toBeDefined();
      expect(result.metrics.performanceWithinThreshold).toBeDefined();
      expect(result.metrics.processingTimeMs).toBeLessThan(100); // <100ms requirement
      
      console.log(`✅ Performance monitored: ${result.metrics.processingTimeMs.toFixed(2)}ms`);
    });

    it('should handle performance degradation gracefully', async () => {
      const content = 'Performance degradation test';
      
      // Add existing content to ensure similarity calculation is triggered
      captureWorkflow.addExistingContent(['Some existing content to trigger similarity check']);
      
      // Simulate slow similarity calculation
      mockSimilarityCalculator.calculateBatch.mockImplementation(async () => {
        await new Promise(resolve => setTimeout(resolve, 50)); // 50ms delay
        return [0.1];
      });

      const result = await captureWorkflow.processCapture(content);

      // Should still complete successfully even if slower
      expect(result.output).toBeDefined();
      expect(result.metrics.processingTimeMs).toBeGreaterThan(50);
      
      // Performance flag should reflect slower processing
      if (result.metrics.processingTimeMs > 100) {
        expect(result.metrics.performanceWithinThreshold).toBe(false);
      }
      
      console.log(`✅ Performance degradation handled: ${result.metrics.processingTimeMs.toFixed(2)}ms`);
    });
  });

  describe('Workflow Orchestration Based on Quality Thresholds', () => {
    it('should route high-quality content to accept', async () => {
      const highQualityContent = 'Exceptional quality content with perfect structure, comprehensive analysis, and detailed exploration of complex concepts.';
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.05]);

      const result = await captureWorkflow.processCapture(highQualityContent);

      expect(result.output.qualityScore).toBeGreaterThan(0.7); // Above threshold
      expect(result.metrics.routingDecision).toBe('accept');
      expect(result.output.extractedMetadata.qualityGatePassed).toBe(true);
      
      console.log(`✅ High quality routed to accept: Score ${result.output.qualityScore.toFixed(3)}`);
    });

    it('should route medium-quality content to review', async () => {
      const mediumQualityContent = 'Moderate quality content that needs some review.';
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1]);

      const result = await captureWorkflow.processCapture(mediumQualityContent);

      expect(result.output.qualityScore).toBeLessThan(0.7); // Below accept threshold
      expect(result.output.qualityScore).toBeGreaterThan(0.35); // Above reject threshold
      expect(result.metrics.routingDecision).toBe('review');
      
      console.log(`✅ Medium quality routed to review: Score ${result.output.qualityScore.toFixed(3)}`);
    });

    it('should route low-quality content to reject', async () => {
      const lowQualityContent = 'bad content no structure unclear';
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.05]);

      const result = await captureWorkflow.processCapture(lowQualityContent);

      expect(result.output.qualityScore).toBeLessThan(0.42); // Below review threshold
      expect(result.metrics.routingDecision).toBe('reject');
      expect(result.output.extractedMetadata.qualityGatePassed).toBe(false);
      
      console.log(`✅ Low quality routed to reject: Score ${result.output.qualityScore.toFixed(3)}`);
    });

    it('should support configurable quality thresholds', async () => {
      const content = 'Medium quality content for threshold testing';
      
      // Test with strict threshold (0.9)
      captureWorkflow.updateConfig({ qualityThreshold: 0.9 });
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1]);

      const strictResult = await captureWorkflow.processCapture(content);
      
      // Same content should be rejected with higher threshold
      expect(strictResult.metrics.routingDecision).toBe('review');
      
      // Test with lenient threshold (0.3)
      captureWorkflow.updateConfig({ qualityThreshold: 0.3 });
      const lenientResult = await captureWorkflow.processCapture(content);
      
      expect(lenientResult.metrics.routingDecision).toBe('accept');
      
      console.log(`✅ Configurable thresholds: Strict=review, Lenient=accept`);
    });
  });

  describe('Enhanced Metadata Capture', () => {
    it('should include comprehensive quality breakdown in metadata', async () => {
      const content = 'Content for quality breakdown metadata testing';
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.15]);

      const result = await captureWorkflow.processCapture(content);

      expect(result.output.extractedMetadata.qualityBreakdown).toBeDefined();
      expect(result.output.extractedMetadata.qualityBreakdown.overallScore).toBeDefined();
      expect(result.output.extractedMetadata.qualityBreakdown.readabilityScore).toBeDefined();
      expect(result.output.extractedMetadata.qualityBreakdown.structureScore).toBeDefined();
      expect(result.output.extractedMetadata.qualityBreakdown.conceptDensityScore).toBeDefined();
      expect(result.output.extractedMetadata.qualityBreakdown.originalityScore).toBeDefined();
      
      console.log(`✅ Enhanced metadata includes complete quality breakdown`);
    });

    it('should include duplication status in metadata', async () => {
      const content = 'Content for duplication metadata testing';
      
      // Add some existing content to enable similarity calculation
      captureWorkflow.addExistingContent(['Some existing content for comparison']);
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.2]);

      const result = await captureWorkflow.processCapture(content);

      expect(result.output.extractedMetadata.duplicationStatus).toBeDefined();
      expect(result.output.extractedMetadata.duplicationStatus.isDuplicate).toBe(false);
      expect(result.output.extractedMetadata.duplicationStatus.similarityScore).toBe(0.2);
      
      console.log(`✅ Duplication status included in metadata`);
    });

    it('should include workflow processing metadata', async () => {
      const content = 'Content for workflow metadata testing';
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.1]);

      const result = await captureWorkflow.processCapture(content);

      expect(result.output.extractedMetadata.workflowProcessed).toBe(true);
      expect(result.output.extractedMetadata.processingTimestamp).toBeDefined();
      expect(result.output.extractedMetadata.routingMetadata).toBeDefined();
      expect(result.output.extractedMetadata.routingMetadata.qualityThreshold).toBe(0.7);
      expect(result.output.extractedMetadata.routingMetadata.duplicateThreshold).toBe(0.85);
      
      console.log(`✅ Workflow processing metadata included`);
    });
  });

  describe('Performance Monitoring Integration', () => {
    it('should track processing time for all operations', async () => {
      const content = 'Content for performance tracking';
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.2]);

      const result = await captureWorkflow.processCapture(content);

      expect(result.metrics.processingTimeMs).toBeDefined();
      expect(result.metrics.processingTimeMs).toBeGreaterThan(0);
      expect(result.metrics.processingTimeMs).toBeLessThan(100); // Within performance requirement
      
      console.log(`✅ Performance tracked: ${result.metrics.processingTimeMs.toFixed(2)}ms`);
    });
  });

  describe('Error Handling and Recovery', () => {
    it('should handle quality assessment errors gracefully', async () => {
      const invalidContent = null as any;
      
      await expect(captureWorkflow.processCapture(invalidContent)).rejects.toThrow('Enhanced capture workflow failed: Invalid content provided');
      
      console.log(`✅ Quality assessment errors handled with appropriate error message`);
    });

    it('should handle duplicate detection failures gracefully', async () => {
      const content = 'Content for error handling testing';
      
      // Mock similarity calculator to throw error
      mockSimilarityCalculator.calculateBatch.mockRejectedValue(new Error('Similarity calculation failed'));
      
      await expect(captureWorkflow.processCapture(content)).rejects.toThrow('Enhanced capture workflow failed');
      
      console.log(`✅ Duplicate detection errors handled gracefully`);
    });
  });

  describe('End-to-End Integration Validation', () => {
    it('should process complex content through complete pipeline', async () => {
      const complexContent = `
        # Research Study: Advanced Machine Learning Applications
        
        This comprehensive study explores the intersection of artificial intelligence and 
        quantum computing, providing detailed analysis of emerging trends and future implications.
        
        ## Key Findings
        - Novel quantum-ML algorithms show 50x performance improvement
        - Hybrid approaches demonstrate superior accuracy in complex pattern recognition
        - Implementation challenges include quantum decoherence and error correction
        
        ## Methodology
        Our research methodology employed rigorous experimental design with statistical
        validation across multiple quantum computing platforms and classical baselines.
        
        ## Conclusions
        The convergence of quantum computing and machine learning represents a paradigm 
        shift that will revolutionize computational approaches across multiple domains.
      `;
      
      mockSimilarityCalculator.calculateBatch.mockResolvedValue([0.15]);

      const result = await captureWorkflow.processCapture(complexContent, {
        source: 'research-database',
        type: 'academic-paper',
        author: 'Research Team'
      });

      // Validate complete pipeline processing
      expect(result.output).toBeDefined();
      expect(result.output.qualityScore).toBeGreaterThan(0.8); // High quality expected
      expect(result.metrics.routingDecision).toBe('accept');
      expect(result.output.extractedMetadata.qualityBreakdown).toBeDefined();
      expect(result.output.extractedMetadata.duplicationStatus).toBeDefined();
      expect(result.output.extractedMetadata.workflowProcessed).toBe(true);
      expect(result.metrics.performanceWithinThreshold).toBe(true);
      
      console.log(`✅ Complete pipeline: Score ${result.output.qualityScore.toFixed(3)}, Decision: ${result.metrics.routingDecision}`);
    });
  });
});