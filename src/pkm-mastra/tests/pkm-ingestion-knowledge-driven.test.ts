/**
 * PKM Ingestion Knowledge-Driven TDD Tests - RED Phase
 * 
 * Comprehensive test suite using realistic knowledge examples to drive
 * the development of a robust PKM ingestion pipeline.
 * 
 * THESE TESTS MUST FAIL INITIALLY - Driving implementation through real knowledge requirements
 */

import { describe, test, expect, beforeEach, vi } from 'vitest';
import { 
  pkmIngestionWorkflow,
  modelSelectionStep,
  contentProcessingStep,
  atomicNoteGenerationStep,
  qualityAssessmentStep,
  type ContentInput,
  type ProcessingResult
} from '../src/workflows/pkm-ingestion-workflow.js';

import {
  allExampleKnowledge,
  softwareEngineeringExamples,
  pkmExamples,
  scientificExamples,
  businessExamples,
  philosophicalExamples,
  quickCaptureExamples,
  datasetCategories,
  qualityBenchmarks,
  type KnowledgeExample
} from './fixtures/example-knowledge-datasets.js';

describe('PKM Ingestion Pipeline - Knowledge-Driven TDD (RED PHASE)', () => {

  describe('Model Selection Intelligence with Real Knowledge', () => {
    test('RED: should select Opus for complex quantum computing paper', async () => {
      const quantumPaper = scientificExamples[0]; // Complex scientific content
      
      const input: ContentInput = {
        content: quantumPaper.content,
        source: quantumPaper.source,
        type: quantumPaper.type,
        metadata: quantumPaper.metadata,
      };
      
      const result = await modelSelectionStep.execute({ input });
      
      expect(result.selectedModel).toBe('opus');
      expect(result.confidence).toBeGreaterThan(0.9);
      expect(result.rationale).toContain('complex');
      expect(result.rationale).toMatch(/length.*complexity|complex.*content/i);
    });

    test('RED: should select Sonnet for simple PARA method overview', async () => {
      const paraMethod = pkmExamples[1]; // Simple methodological content
      
      const input: ContentInput = {
        content: paraMethod.content,
        source: paraMethod.source,
        type: paraMethod.type,
        metadata: paraMethod.metadata,
      };
      
      const result = await modelSelectionStep.execute({ input });
      
      expect(result.selectedModel).toBe('sonnet');
      expect(result.confidence).toBeGreaterThan(0.8);
      expect(result.rationale).toContain('simple');
    });

    test('RED: should respect user preference override for complex content', async () => {
      const complexContent = scientificExamples[0];
      
      const input: ContentInput = {
        content: complexContent.content,
        source: complexContent.source,
        type: complexContent.type,
        processingOptions: {
          modelPreference: 'sonnet', // Override complex content default
        },
      };
      
      const result = await modelSelectionStep.execute({ input });
      
      expect(result.selectedModel).toBe('sonnet');
      expect(result.confidence).toBe(1.0);
      expect(result.rationale).toContain('user preference');
    });

    test('RED: should select Opus for high quality threshold requirement', async () => {
      const simpleContent = quickCaptureExamples[0]; // Simple fragment
      
      const input: ContentInput = {
        content: simpleContent.content,
        source: simpleContent.source,
        type: simpleContent.type,
        processingOptions: {
          qualityThreshold: 0.95, // High quality requirement
        },
      };
      
      const result = await modelSelectionStep.execute({ input });
      
      expect(result.selectedModel).toBe('opus');
      expect(result.rationale).toContain('high quality threshold');
    });
  });

  describe('Technical Knowledge Processing Excellence', () => {
    test('RED: should process SOLID principles with expert-level accuracy', async () => {
      const solidPrinciples = softwareEngineeringExamples[0];
      
      const input: ContentInput = {
        content: solidPrinciples.content,
        source: solidPrinciples.source,
        type: solidPrinciples.type,
        metadata: solidPrinciples.metadata,
      };
      
      const result = await pkmIngestionWorkflow.execute(input);
      
      // Expected outcomes from knowledge dataset
      expect(result.atomicNotes).toHaveLength(solidPrinciples.expectedOutcomes.atomicNotesCount);
      expect(result.validationResults.overallQuality).toBeCloseTo(
        solidPrinciples.expectedOutcomes.avgQualityScore, 1
      );
      expect(result.validationResults.atomicityCompliance).toBeCloseTo(
        solidPrinciples.expectedOutcomes.avgAtomicityScore, 1
      );
      expect(result.processingMetrics.totalTime).toBeLessThan(45000); // 45s max
      
      // Verify specific SOLID concepts are extracted
      const allContent = result.atomicNotes.map(note => note.content).join(' ');
      expect(allContent).toMatch(/single responsibility|SRP/i);
      expect(allContent).toMatch(/open.?closed|OCP/i);
      expect(allContent).toMatch(/liskov substitution|LSP/i);
      expect(allContent).toMatch(/interface segregation|ISP/i);
      expect(allContent).toMatch(/dependency inversion|DIP/i);
    });

    test('RED: should extract technical concepts from microservices overview', async () => {
      const microservices = softwareEngineeringExamples[1];
      
      const processing = await contentProcessingStep.execute({
        input: {
          content: microservices.content,
          selectedModel: microservices.expectedOutcomes.processingModel,
          processingOptions: {},
        },
        context: {},
      });
      
      const concepts = processing.extractedMetadata.concepts;
      expect(concepts).toContain('microservices');
      expect(concepts).toContain('monolithic');
      expect(concepts.some(c => c.includes('independence'))).toBe(true);
      expect(concepts.some(c => c.includes('scalability'))).toBe(true);
      expect(concepts.length).toBeGreaterThan(microservices.expectedOutcomes.keyConceptsCount - 2);
    });
  });

  describe('PKM Methodology Processing with Domain Expertise', () => {
    test('RED: should process Zettelkasten method with methodological precision', async () => {
      const zettelkasten = pkmExamples[0];
      
      const input: ContentInput = {
        content: zettelkasten.content,
        source: zettelkasten.source,
        type: zettelkasten.type,
        metadata: zettelkasten.metadata,
      };
      
      const result = await pkmIngestionWorkflow.execute(input);
      
      // Verify expected atomic note count with tolerance
      const expectedCount = zettelkasten.expectedOutcomes.atomicNotesCount;
      expect(result.atomicNotes.length).toBeGreaterThanOrEqual(expectedCount - 3);
      expect(result.atomicNotes.length).toBeLessThanOrEqual(expectedCount + 3);
      
      // High-quality methodological content expectations
      expect(result.validationResults.overallQuality).toBeGreaterThan(0.90);
      expect(result.validationResults.atomicityCompliance).toBeGreaterThan(0.88);
      
      // Should identify both areas and resources categories
      const paraCategories = result.atomicNotes.map(note => note.paraCategory);
      expect(paraCategories).toContain('areas');
      expect(paraCategories).toContain('resources');
      
      // Verify PKM-specific concepts are identified
      const allContent = result.atomicNotes.map(note => note.content).join(' ');
      expect(allContent).toMatch(/atomicity|atomic/i);
      expect(allContent).toMatch(/connectivity|connection/i);
      expect(allContent).toMatch(/identifier|linking/i);
      expect(allContent).toMatch(/zettelkasten|luhmann/i);
    });

    test('RED: should classify PARA method content appropriately', async () => {
      const paraMethod = pkmExamples[1];
      
      const input: ContentInput = {
        content: paraMethod.content,
        source: paraMethod.source,
        type: paraMethod.type,
        metadata: paraMethod.metadata,
      };
      
      const result = await pkmIngestionWorkflow.execute(input);
      
      // PARA method is reference material
      expect(result.atomicNotes.every(note => 
        note.paraCategory === 'resources'
      )).toBe(true);
      
      // Should identify the four PARA categories as concepts
      const allContent = result.atomicNotes.map(note => note.content).join(' ');
      expect(allContent).toMatch(/projects?/i);
      expect(allContent).toMatch(/areas?/i);
      expect(allContent).toMatch(/resources?/i);
      expect(allContent).toMatch(/archives?/i);
      expect(allContent).toMatch(/actionability|actionable/i);
    });
  });

  describe('Scientific Knowledge Processing with Expert Precision', () => {
    test('RED: should process quantum computing paper with scientific rigor', async () => {
      const quantumPaper = scientificExamples[0];
      
      const input: ContentInput = {
        content: quantumPaper.content,
        source: quantumPaper.source,
        type: quantumPaper.type,
        metadata: quantumPaper.metadata,
      };
      
      const result = await pkmIngestionWorkflow.execute(input);
      
      // Complex scientific content expectations
      const expectedCount = quantumPaper.expectedOutcomes.atomicNotesCount;
      expect(result.atomicNotes.length).toBeGreaterThanOrEqual(expectedCount - 4);
      expect(result.atomicNotes.length).toBeLessThanOrEqual(expectedCount + 4);
      
      // Extremely high quality for expert-level content
      expect(result.validationResults.overallQuality).toBeGreaterThan(0.92);
      expect(result.processingMetrics.modelUsage).toHaveProperty('opus');
      
      // Scientific concepts must be preserved
      const allContent = result.atomicNotes.map(note => note.content).join(' ');
      expect(allContent).toMatch(/qubit|quantum.?bit/i);
      expect(allContent).toMatch(/superposition/i);
      expect(allContent).toMatch(/entanglement/i);
      expect(allContent).toMatch(/decoherence/i);
      expect(allContent).toMatch(/shor|grover/i); // Famous algorithms
      expect(allContent).toMatch(/quantum.?gate/i);
      
      // Should process within reasonable time even for complex content
      expect(result.processingMetrics.totalTime).toBeLessThan(60000); // 60s max
    });
  });

  describe('Business Knowledge Processing with Strategic Insight', () => {
    test('RED: should process Lean Startup methodology with business acumen', async () => {
      const leanStartup = businessExamples[0];
      
      const input: ContentInput = {
        content: leanStartup.content,
        source: leanStartup.source,
        type: leanStartup.type,
        metadata: leanStartup.metadata,
      };
      
      const result = await pkmIngestionWorkflow.execute(input);
      
      // Business methodology processing expectations
      const expectedCount = leanStartup.expectedOutcomes.atomicNotesCount;
      expect(result.atomicNotes.length).toBeGreaterThanOrEqual(expectedCount - 3);
      expect(result.atomicNotes.length).toBeLessThanOrEqual(expectedCount + 3);
      
      // Should identify both resources and projects
      const paraCategories = result.atomicNotes.map(note => note.paraCategory);
      expect(paraCategories).toContain('resources'); // Methodology reference
      expect(paraCategories).toContain('projects'); // Implementation aspects
      
      // Key Lean Startup concepts
      const allContent = result.atomicNotes.map(note => note.content).join(' ');
      expect(allContent).toMatch(/build.?measure.?learn/i);
      expect(allContent).toMatch(/mvp|minimum.?viable.?product/i);
      expect(allContent).toMatch(/validated.?learning/i);
      expect(allContent).toMatch(/pivot/i);
      expect(allContent).toMatch(/dropbox|zappos|buffer/i); // Example companies
    });
  });

  describe('Quick Capture Processing with Practical Intelligence', () => {
    test('RED: should handle meeting notes with actionable intelligence', async () => {
      const meetingNotes = quickCaptureExamples[1]; // Sprint planning
      
      const input: ContentInput = {
        content: meetingNotes.content,
        source: meetingNotes.source,
        type: meetingNotes.type,
        metadata: meetingNotes.metadata,
      };
      
      const result = await pkmIngestionWorkflow.execute(input);
      
      // Meeting notes should be primarily projects
      expect(result.atomicNotes.some(note => 
        note.paraCategory === 'projects'
      )).toBe(true);
      
      // Should identify action items and timeline elements
      const allContent = result.atomicNotes.map(note => note.content).join(' ');
      expect(allContent).toMatch(/action|task|todo/i);
      expect(allContent).toMatch(/timeline|deadline|monday|wednesday|friday/i);
      expect(allContent).toMatch(/sarah|mike/i); // People involved
      expect(allContent).toMatch(/authentication|redis/i); // Technical elements
      
      // Appropriate quality for informal notes
      expect(result.validationResults.overallQuality).toBeGreaterThan(0.65);
      expect(result.validationResults.overallQuality).toBeLessThan(0.80);
    });

    test('RED: should process idea fragments with appropriate quality', async () => {
      const fragment = quickCaptureExamples[0]; // AI ethics thought
      
      const input: ContentInput = {
        content: fragment.content,
        source: fragment.source,
        type: fragment.type,
        metadata: fragment.metadata,
      };
      
      const result = await pkmIngestionWorkflow.execute(input);
      
      // Small fragment should produce few, highly atomic notes
      expect(result.atomicNotes).toHaveLength(fragment.expectedOutcomes.atomicNotesCount);
      expect(result.atomicNotes.every(note => note.atomicityScore > 0.85)).toBe(true);
      
      // Should categorize as area (ongoing concern)
      expect(result.atomicNotes.every(note => 
        note.paraCategory === 'areas'
      )).toBe(true);
      
      // Key concepts from the fragment
      const allContent = result.atomicNotes.map(note => note.content).join(' ');
      expect(allContent).toMatch(/alignment.?problem/i);
      expect(allContent).toMatch(/human.?flourishing|human.?agency/i);
      expect(allContent).toMatch(/ai.?ethics/i);
    });
  });

  describe('Cross-Domain Knowledge Validation', () => {
    test('RED: should maintain quality consistency across knowledge domains', async () => {
      const representativeExamples = [
        softwareEngineeringExamples[0], // Technical
        pkmExamples[0], // Methodological  
        scientificExamples[0], // Scientific
        businessExamples[0], // Business
        philosophicalExamples[0], // Philosophical
      ];
      
      for (const example of representativeExamples) {
        const input: ContentInput = {
          content: example.content,
          source: example.source,
          type: example.type,
          metadata: example.metadata,
        };
        
        const result = await pkmIngestionWorkflow.execute(input);
        
        // Quality should be within expected range ±15%
        const expectedQuality = example.expectedOutcomes.avgQualityScore;
        expect(result.validationResults.overallQuality).toBeGreaterThan(expectedQuality - 0.15);
        expect(result.validationResults.overallQuality).toBeLessThan(expectedQuality + 0.15);
        
        // Atomicity should be within expected range ±10%
        const expectedAtomicity = example.expectedOutcomes.avgAtomicityScore;
        expect(result.validationResults.atomicityCompliance).toBeGreaterThan(expectedAtomicity - 0.10);
        expect(result.validationResults.atomicityCompliance).toBeLessThan(expectedAtomicity + 0.10);
        
        // Model selection should match expectations
        expect(result.atomicNotes[0]?.processingModel).toBe(example.expectedOutcomes.processingModel);
      }
    });
  });

  describe('Performance Requirements with Real Knowledge', () => {
    test('RED: should process all knowledge types within time limits', async () => {
      // Test a sampling of different knowledge types for performance
      const performanceTestCases = [
        quickCaptureExamples[0], // Quick fragment
        softwareEngineeringExamples[1], // Medium technical
        pkmExamples[1], // Medium methodological
        scientificExamples[0], // Large complex scientific
      ];
      
      for (const testCase of performanceTestCases) {
        const input: ContentInput = {
          content: testCase.content,
          source: testCase.source,
          type: testCase.type,
          metadata: testCase.metadata,
        };
        
        const startTime = Date.now();
        const result = await pkmIngestionWorkflow.execute(input);
        const endTime = Date.now();
        
        const processingTime = endTime - startTime;
        const timeLimit = testCase.content.length > 1000 ? 60000 : 30000; // 60s for long, 30s for short
        
        expect(processingTime).toBeLessThan(timeLimit);
        expect(result.processingMetrics.totalTime).toBeCloseTo(processingTime, 2000); // Within 2s accuracy
      }
    });

    test('RED: should handle concurrent processing of multiple knowledge types', async () => {
      const concurrentInputs = [
        quickCaptureExamples[0],
        quickCaptureExamples[1],
        softwareEngineeringExamples[1],
      ].map(example => ({
        content: example.content,
        source: example.source,
        type: example.type,
        metadata: example.metadata,
      }));
      
      const startTime = Date.now();
      const results = await Promise.all(
        concurrentInputs.map(input => pkmIngestionWorkflow.execute(input))
      );
      const endTime = Date.now();
      
      // Concurrent processing should be faster than sequential
      const concurrentTime = endTime - startTime;
      expect(concurrentTime).toBeLessThan(90000); // Should complete within 90s
      
      // All results should be valid
      expect(results).toHaveLength(3);
      expect(results.every(result => result.atomicNotes.length > 0)).toBe(true);
      expect(results.every(result => result.validationResults.overallQuality > 0.6)).toBe(true);
    });
  });

  describe('End-to-End Pipeline Validation with Complete Knowledge', () => {
    test('RED: should process complete knowledge pipeline with scientific paper', async () => {
      const quantumPaper = scientificExamples[0];
      
      // Step-by-step validation
      
      // Step 1: Model Selection
      const modelResult = await modelSelectionStep.execute({ input: {
        content: quantumPaper.content,
        source: quantumPaper.source,
        type: quantumPaper.type,
        metadata: quantumPaper.metadata,
      }});
      expect(modelResult.selectedModel).toBe('opus');
      expect(modelResult.confidence).toBeGreaterThan(0.9);
      
      // Step 2: Content Processing  
      const processingResult = await contentProcessingStep.execute({
        input: {
          content: quantumPaper.content,
          selectedModel: modelResult.selectedModel,
          processingOptions: {},
        },
        context: {},
      });
      expect(processingResult.extractedMetadata.concepts.length).toBeGreaterThan(20);
      expect(processingResult.qualityMetrics.accuracy).toBeGreaterThan(0.85);
      
      // Step 3: Atomic Note Generation
      const atomicResult = await atomicNoteGenerationStep.execute({
        processedContent: processingResult.processedContent,
        extractedMetadata: processingResult.extractedMetadata,
        selectedModel: modelResult.selectedModel,
      });
      expect(atomicResult.atomicNotes.length).toBeGreaterThan(15);
      expect(atomicResult.atomicNotes.every(note => note.atomicityScore > 0.8)).toBe(true);
      
      // Step 4: Quality Assessment
      const qualityResult = await qualityAssessmentStep.execute({
        atomicNotes: atomicResult.atomicNotes,
      });
      expect(qualityResult.qualityResults.every(q => q.qualityScore > 0.7)).toBe(true);
      expect(qualityResult.qualityResults.every(q => q.complianceCheck.atomicity)).toBe(true);
      
      // Step 5: Full Pipeline Integration
      const fullResult = await pkmIngestionWorkflow.execute({
        content: quantumPaper.content,
        source: quantumPaper.source,
        type: quantumPaper.type,
        metadata: quantumPaper.metadata,
      });
      
      expect(fullResult.validationResults.overallQuality).toBeGreaterThan(0.90);
      expect(fullResult.atomicNotes.length).toBeGreaterThanOrEqual(quantumPaper.expectedOutcomes.atomicNotesCount - 4);
      expect(fullResult.processingMetrics.modelUsage.opus).toBe(1);
    });
  });

  describe('Knowledge Quality Benchmarks Validation', () => {
    test('RED: should meet minimum quality benchmarks across all knowledge types', async () => {
      for (const knowledge of allExampleKnowledge.slice(0, 8)) { // Test representative sample
        const input: ContentInput = {
          content: knowledge.content,
          source: knowledge.source,
          type: knowledge.type,
          metadata: knowledge.metadata,
        };
        
        const result = await pkmIngestionWorkflow.execute(input);
        
        // Apply quality benchmarks
        expect(result.validationResults.atomicityCompliance).toBeGreaterThan(qualityBenchmarks.minAtomicityScore);
        expect(result.validationResults.overallQuality).toBeGreaterThan(qualityBenchmarks.minQualityScore);
        expect(result.processingMetrics.totalTime).toBeLessThan(qualityBenchmarks.maxProcessingTime);
        
        // Concept extraction minimum
        const conceptCount = result.atomicNotes.reduce((count, note) => 
          count + (note.conceptBoundaries?.length || 1), 0
        );
        expect(conceptCount).toBeGreaterThan(qualityBenchmarks.minConceptExtraction);
      }
    });

    test('RED: should provide actionable improvement suggestions for lower quality content', async () => {
      const meetingNotes = quickCaptureExamples[1]; // Should have improvement suggestions
      
      const input: ContentInput = {
        content: meetingNotes.content,
        source: meetingNotes.source,
        type: meetingNotes.type,
        metadata: meetingNotes.metadata,
      };
      
      const result = await qualityAssessmentStep.execute({
        input: {
          atomicNotes: [
            {
              id: 'test-note',
              title: 'Test',
              content: meetingNotes.content,
              atomicityScore: 0.7,
              conceptBoundaries: ['test'],
            }
          ],
        },
        context: {},
      });
      
      expect(result.qualityResults[0].improvements.length).toBeGreaterThan(0);
      expect(result.qualityResults[0].improvements.some(imp => 
        imp.includes('structure') || imp.includes('clarity') || imp.includes('detail')
      )).toBe(true);
    });
  });
});

/**
 * Expected Test Results (RED Phase):
 * 
 * ❌ All tests should FAIL with various errors:
 * - Model selection logic not implemented for complexity analysis
 * - Content processing doesn't extract domain-specific concepts accurately
 * - Atomic note generation doesn't meet quality/atomicity requirements
 * - PARA classification logic missing or inadequate
 * - Performance requirements not met
 * - Quality assessment not calibrated to knowledge domains
 * 
 * This comprehensive failure is EXPECTED and CORRECT for TDD RED phase.
 * 
 * Next Steps:
 * 1. GREEN phase: Implement knowledge-aware processing logic
 * 2. REFACTOR phase: Optimize for performance and quality consistency
 * 3. VALIDATE phase: Verify with additional real-world knowledge examples
 */