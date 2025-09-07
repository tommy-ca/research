/**
 * Enhanced PKM Workflow with Search Integration - TDD RED Phase
 * These tests MUST FAIL initially as enhanced workflow doesn't exist yet
 * Following TDD methodology: RED → GREEN → REFACTOR
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { enhancedPkmWorkflow } from '../src/workflows/enhanced-pkm-workflow.js';

describe('Enhanced PKM Workflow with Search - TDD RED Phase', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Backward Compatibility - Local Processing', () => {
    it('RED: should process content locally when search disabled', async () => {
      const input = {
        content: 'Context engineering is a systematic approach to designing contextual information for AI coding agents.',
        source: 'test',
        type: 'text' as const,
        metadata: { domain: 'technical' },
        processingOptions: {
          enableSearch: false,
          modelPreference: 'sonnet' as const
        }
      };

      // This will FAIL until enhancedPkmWorkflow is implemented
      const result = await enhancedPkmWorkflow.execute(input);
      
      expect(result).toBeDefined();
      expect(result.atomicNotes).toBeDefined();
      expect(result.atomicNotes.length).toBeGreaterThan(0);
      expect(result.processingMetrics).toBeDefined();
      expect(result.processingMetrics.enrichmentScore).toBe(0);
      expect(result.atomicNotes.every(note => !note.externalSources)).toBe(true);
      expect(result.processingMetrics.totalTime).toBeLessThan(200); // Fast local processing
    });

    it('RED: should maintain existing quality standards without search', async () => {
      const input = {
        content: 'Artificial intelligence alignment involves ensuring AI systems pursue beneficial goals for humanity.',
        source: 'research-paper',
        type: 'text' as const,
        processingOptions: {
          enableSearch: false,
          qualityThreshold: 0.8
        }
      };

      const result = await enhancedPkmWorkflow.execute(input);
      
      expect(result.atomicNotes).toBeDefined();
      expect(result.validationResults.overallQuality).toBeGreaterThan(0.8);
      expect(result.atomicNotes.every(note => note.qualityScore >= 0.8)).toBe(true);
      expect(result.validationResults.atomicityCompliance).toBeGreaterThan(0.7);
    });
  });

  describe('Search-Enhanced Processing', () => {
    it('RED: should enrich content with external sources when enabled', async () => {
      const input = {
        content: 'The alignment problem in AI safety requires solving value learning and robust oversight challenges.',
        source: 'research-paper',
        type: 'text' as const,
        metadata: { 
          domain: 'technical',
          complexity: 'high'
        },
        processingOptions: {
          enableSearch: true,
          searchStrategy: 'smart' as const,
          maxSearchResults: 10,
          qualityThreshold: 0.85
        }
      };

      const result = await enhancedPkmWorkflow.execute(input);
      
      expect(result.atomicNotes).toBeDefined();
      expect(result.atomicNotes.length).toBeGreaterThan(0);
      expect(result.processingMetrics.enrichmentScore).toBeGreaterThan(0);
      expect(result.atomicNotes.some(note => 
        note.externalSources && note.externalSources.length > 0
      )).toBe(true);
      expect(result.validationResults.knowledgeGaps).toBeDefined();
      expect(result.validationResults.gapScore).toBeGreaterThanOrEqual(0);
      expect(result.processingMetrics.searchMetrics).toBeDefined();
    });

    it('RED: should improve quality scores with search enrichment', async () => {
      const testContent = 'AI alignment requires value learning but current approaches are limited.';

      // Process without search
      const localResult = await enhancedPkmWorkflow.execute({
        content: testContent,
        source: 'test',
        type: 'text' as const,
        processingOptions: { enableSearch: false }
      });

      // Process with search
      const enrichedResult = await enhancedPkmWorkflow.execute({
        content: testContent,
        source: 'test',
        type: 'text' as const,
        processingOptions: { 
          enableSearch: true,
          searchStrategy: 'parallel' as const
        }
      });

      // Calculate average quality scores
      const localAvgQuality = localResult.atomicNotes.reduce((sum, note) => 
        sum + note.qualityScore, 0) / localResult.atomicNotes.length;
      
      const enrichedAvgQuality = enrichedResult.atomicNotes.reduce((sum, note) => 
        sum + note.qualityScore, 0) / enrichedResult.atomicNotes.length;

      expect(enrichedAvgQuality).toBeGreaterThanOrEqual(localAvgQuality);
      expect(enrichedResult.processingMetrics.enrichmentScore).toBeGreaterThan(0);
      expect(enrichedResult.validationResults.overallQuality).toBeGreaterThanOrEqual(
        localResult.validationResults.overallQuality
      );
    });

    it('RED: should handle different search strategies', async () => {
      const content = 'Context engineering methodologies for large language models in production systems.';
      const strategies = ['brave_only', 'exa_only', 'parallel', 'smart'] as const;

      for (const strategy of strategies) {
        const result = await enhancedPkmWorkflow.execute({
          content,
          source: 'test',
          type: 'text' as const,
          processingOptions: {
            enableSearch: true,
            searchStrategy: strategy,
            maxSearchResults: 8
          }
        });

        expect(result.atomicNotes).toBeDefined();
        expect(result.processingMetrics.enrichmentScore).toBeGreaterThanOrEqual(0);
        
        if (result.processingMetrics.searchMetrics) {
          expect(result.processingMetrics.searchMetrics.strategy_used).toContain(strategy);
        }
      }
    });
  });

  describe('Knowledge Gap Detection and Enrichment', () => {
    it('RED: should identify knowledge gaps in content', async () => {
      const complexContent = `
        Machine learning interpretability is crucial for deploying AI systems safely.
        Current methods include LIME, SHAP, and attention visualization.
        However, these approaches have significant limitations.
      `;

      const input = {
        content: complexContent,
        source: 'research',
        type: 'text' as const,
        processingOptions: { 
          enableSearch: true,
          searchStrategy: 'smart' as const
        }
      };

      const result = await enhancedPkmWorkflow.execute(input);
      
      expect(result.validationResults.knowledgeGaps).toBeDefined();
      expect(result.validationResults.knowledgeGaps.length).toBeGreaterThan(0);
      expect(result.validationResults.gapScore).toBeGreaterThan(0);
      
      // Check gap structure
      result.validationResults.knowledgeGaps.forEach(gap => {
        expect(gap.topic).toBeDefined();
        expect(gap.confidence).toBeGreaterThan(0);
        expect(gap.confidence).toBeLessThanOrEqual(1);
        expect(gap.priority).toMatch(/^(low|medium|high)$/);
        expect(gap.suggestedSearchQueries).toBeDefined();
        expect(gap.suggestedSearchQueries.length).toBeGreaterThan(0);
      });
    });

    it('RED: should find relevant sources for knowledge gaps', async () => {
      const input = {
        content: 'Quantum machine learning shows promise but has unclear practical applications.',
        source: 'research',
        type: 'text' as const,
        processingOptions: {
          enableSearch: true,
          searchStrategy: 'parallel' as const,
          maxSearchResults: 15
        }
      };

      const result = await enhancedPkmWorkflow.execute(input);
      
      expect(result.processingMetrics.searchMetrics).toBeDefined();
      expect(result.processingMetrics.searchMetrics.gaps_processed).toBeGreaterThan(0);
      
      // Check that notes with high-priority gaps got external sources
      const highGapNotes = result.atomicNotes.filter(note => {
        const relatedGaps = result.validationResults.knowledgeGaps.filter(gap => 
          note.title.toLowerCase().includes(gap.topic.toLowerCase()) ||
          note.content.toLowerCase().includes(gap.topic.toLowerCase())
        );
        return relatedGaps.some(gap => gap.priority === 'high');
      });

      expect(highGapNotes.some(note => 
        note.externalSources && note.externalSources.length > 0
      )).toBe(true);
    });

    it('RED: should prioritize gaps appropriately', async () => {
      const input = {
        content: 'Transformer architectures revolutionized NLP. Attention mechanisms are key. Self-attention enables parallelization.',
        source: 'technical-article',
        type: 'text' as const,
        processingOptions: { enableSearch: true }
      };

      const result = await enhancedPkmWorkflow.execute(input);
      
      const highPriorityGaps = result.validationResults.knowledgeGaps.filter(gap => gap.priority === 'high');
      const mediumPriorityGaps = result.validationResults.knowledgeGaps.filter(gap => gap.priority === 'medium');
      const lowPriorityGaps = result.validationResults.knowledgeGaps.filter(gap => gap.priority === 'low');
      
      // High priority gaps should have higher confidence scores
      if (highPriorityGaps.length > 0 && mediumPriorityGaps.length > 0) {
        const avgHighConfidence = highPriorityGaps.reduce((sum, gap) => sum + gap.confidence, 0) / highPriorityGaps.length;
        const avgMediumConfidence = mediumPriorityGaps.reduce((sum, gap) => sum + gap.confidence, 0) / mediumPriorityGaps.length;
        
        expect(avgHighConfidence).toBeGreaterThanOrEqual(avgMediumConfidence);
      }
    });
  });

  describe('Performance and Reliability', () => {
    it('RED: should maintain performance targets with search', async () => {
      const testCases = [
        { 
          content: 'Brief AI ethics overview.', 
          expectedTime: 2000,
          label: 'short content'
        },
        { 
          content: 'Medium length discussion about machine learning interpretability methods including LIME, SHAP, attention mechanisms, and their trade-offs in different application domains.',
          expectedTime: 3000,
          label: 'medium content'
        },
        { 
          content: generateLongContent(),
          expectedTime: 4000,
          label: 'long content'
        }
      ];

      for (const { content, expectedTime, label } of testCases) {
        const startTime = Date.now();
        const result = await enhancedPkmWorkflow.execute({
          content,
          source: 'performance-test',
          type: 'text' as const,
          processingOptions: { enableSearch: true }
        });
        const duration = Date.now() - startTime;
        
        expect(duration).toBeLessThan(expectedTime);
        expect(result.atomicNotes).toBeDefined();
        expect(result.processingMetrics.totalTime).toBeLessThan(expectedTime);
        
        console.log(`✓ ${label}: ${duration}ms (limit: ${expectedTime}ms)`);
      }
    });

    it('RED: should gracefully degrade when search fails', async () => {
      // Mock search failure
      vi.mock('../src/tools/search-orchestrator.js', () => ({
        searchOrchestratorTool: {
          execute: vi.fn().mockRejectedValue(new Error('All search providers unavailable'))
        }
      }));

      const input = {
        content: 'Test content for search failure graceful degradation.',
        source: 'test',
        type: 'text' as const,
        processingOptions: {
          enableSearch: true,
          searchStrategy: 'parallel' as const
        }
      };

      const result = await enhancedPkmWorkflow.execute(input);
      
      // Should still return valid results even if search fails
      expect(result.atomicNotes).toBeDefined();
      expect(result.atomicNotes.length).toBeGreaterThan(0);
      expect(result.processingMetrics.enrichmentScore).toBe(0); // No enrichment due to failure
      expect(result.validationResults.overallQuality).toBeGreaterThan(0.6); // Still decent quality
    });

    it('RED: should handle partial search failures', async () => {
      // Mock partial failure (one provider works, one fails)
      vi.mock('../src/tools/search-tools.js', () => ({
        braveSearchTool: {
          execute: vi.fn().mockRejectedValue(new Error('Brave API down'))
        },
        exaSearchTool: {
          execute: vi.fn().mockResolvedValue({
            results: [
              { title: 'Test Result', url: 'https://example.com', description: 'Test', relevance_score: 0.8, quality_score: 0.9 }
            ],
            search_metadata: { provider: 'exa', search_time: 500 }
          })
        }
      }));

      const result = await enhancedPkmWorkflow.execute({
        content: 'Context engineering best practices for AI systems.',
        source: 'test',
        type: 'text' as const,
        processingOptions: {
          enableSearch: true,
          searchStrategy: 'parallel' as const
        }
      });
      
      // Should work with partial results
      expect(result.atomicNotes).toBeDefined();
      expect(result.processingMetrics.enrichmentScore).toBeGreaterThan(0); // Some enrichment
      expect(result.processingMetrics.searchMetrics.exa_results).toBeGreaterThan(0);
      expect(result.processingMetrics.searchMetrics.brave_results).toBe(0);
    });
  });

  describe('Integration and Compatibility', () => {
    it('RED: should maintain compatibility with existing workflow interface', async () => {
      const input = {
        content: 'SOLID principles include single responsibility and open-closed principles.',
        source: 'educational',
        type: 'text' as const,
        metadata: { author: 'Robert Martin' },
        processingOptions: {
          modelPreference: 'opus' as const,
          qualityThreshold: 0.9
        }
      };

      const result = await enhancedPkmWorkflow.execute(input);
      
      // Should have all expected fields from original workflow
      expect(result.atomicNotes).toBeDefined();
      expect(result.processingMetrics).toBeDefined();
      expect(result.validationResults).toBeDefined();
      
      // Each atomic note should have required fields
      result.atomicNotes.forEach(note => {
        expect(note.id).toBeDefined();
        expect(note.title).toBeDefined();
        expect(note.content).toBeDefined();
        expect(note.atomicityScore).toBeGreaterThan(0);
        expect(note.qualityScore).toBeGreaterThan(0);
        expect(note.paraCategory).toMatch(/^(projects|areas|resources|archive)$/);
        expect(note.processingModel).toMatch(/^(sonnet|opus)$/);
      });
    });

    it('RED: should validate enhanced input schema', () => {
      const validInput = {
        content: 'Test content',
        source: 'test',
        type: 'text',
        processingOptions: {
          enableSearch: true,
          searchStrategy: 'smart',
          maxSearchResults: 10
        }
      };

      expect(() => enhancedPkmWorkflow.validateInput(validInput)).not.toThrow();

      const invalidInput = {
        content: '',
        source: '',
        type: 'invalid',
        processingOptions: {
          enableSearch: 'invalid',
          searchStrategy: 'invalid',
          maxSearchResults: -1
        }
      };

      expect(() => enhancedPkmWorkflow.validateInput(invalidInput)).toThrow();
    });

    it('RED: should validate enhanced output schema', async () => {
      const result = await enhancedPkmWorkflow.execute({
        content: 'Schema validation test content.',
        source: 'test',
        type: 'text' as const,
        processingOptions: { enableSearch: true }
      });

      expect(() => enhancedPkmWorkflow.validateOutput(result)).not.toThrow();
    });
  });
});

function generateLongContent(): string {
  return Array.from({ length: 8 }, (_, i) => 
    `Section ${i + 1}: This discusses advanced concepts in context engineering including prompt optimization, memory management, semantic understanding, and their applications in various AI domains such as natural language processing, computer vision, and reasoning systems.`
  ).join('\n\n');
}

/**
 * Expected Test Results (RED Phase):
 * 
 * ❌ All tests should FAIL with "Cannot find module '../src/workflows/enhanced-pkm-workflow.js'"
 * ❌ enhancedPkmWorkflow not defined
 * ❌ Search-enhanced content processing not implemented
 * ❌ Knowledge gap detection not implemented  
 * ❌ Search enrichment workflow not implemented
 * ❌ Performance targets with search not met
 * ❌ Graceful degradation not implemented
 * 
 * This is EXPECTED and CORRECT for TDD RED phase.
 * Next step: GREEN phase - implement minimal enhanced workflow to pass tests.
 */