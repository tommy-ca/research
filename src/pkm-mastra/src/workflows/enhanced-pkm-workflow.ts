/**
 * Enhanced PKM Workflow with Search Integration - TDD GREEN Phase Implementation
 * Minimal implementation to make RED tests pass
 * Following TDD methodology: Make tests pass with simplest possible code
 */

// No Mastra imports needed for GREEN phase - using simple object pattern
import { pkmIngestionWorkflow } from './pkm-ingestion-workflow.js';
import { searchOrchestratorTool } from '../tools/search-orchestrator.js';

// Mock gap detection - GREEN phase uses simple heuristics
function detectKnowledgeGaps(content: string): Array<{
  topic: string;
  confidence: number;
  priority: 'low' | 'medium' | 'high';
  suggestedSearchQueries: string[];
}> {
  const gaps = [];
  
  // Simple heuristic: look for incomplete statements
  if (content.includes('but') || content.includes('however') || content.includes('limited')) {
    gaps.push({
      topic: 'Limitations and challenges',
      confidence: 0.7,
      priority: 'high' as const,
      suggestedSearchQueries: ['limitations challenges', 'current approaches']
    });
  }
  
  // Look for mentions of methods without explanation
  if (content.includes('methods') || content.includes('approaches') || content.includes('techniques')) {
    gaps.push({
      topic: 'Methodological details',
      confidence: 0.6,
      priority: 'medium' as const,
      suggestedSearchQueries: ['methods approaches', 'implementation details']
    });
  }
  
  // Look for emerging or recent topics
  if (content.includes('recent') || content.includes('emerging') || content.includes('new')) {
    gaps.push({
      topic: 'Recent developments',
      confidence: 0.8,
      priority: 'high' as const,
      suggestedSearchQueries: ['recent developments', 'latest research']
    });
  }
  
  return gaps;
}

// Mock search enrichment - GREEN phase uses simple matching
async function enrichWithSearchResults(atomicNotes: any[], gaps: any[], processingOptions: any) {
  if (!processingOptions.enableSearch) {
    return { enrichedNotes: atomicNotes, searchMetrics: null };
  }
  
  let totalSearchResults = 0;
  let gapsProcessed = 0;
  const searchStartTime = Date.now();
  
  // Process high-priority gaps
  const highPriorityGaps = gaps.filter(gap => gap.priority === 'high');
  
  for (const gap of highPriorityGaps.slice(0, 3)) { // Limit to 3 gaps in GREEN phase
    try {
      const searchResults = await searchOrchestratorTool.execute({
        input: {
          query: gap.suggestedSearchQueries[0] || gap.topic,
          strategy: processingOptions.searchStrategy || 'smart',
          max_results: processingOptions.maxSearchResults || 5
        }
      });
      
      totalSearchResults += searchResults.total_sources;
      gapsProcessed++;
      
      // Add sources to relevant notes (simple matching)
      const relevantNotes = atomicNotes.filter(note => 
        note.content.toLowerCase().includes(gap.topic.toLowerCase()) ||
        note.title.toLowerCase().includes(gap.topic.toLowerCase())
      );
      
      for (const note of relevantNotes.slice(0, 2)) { // Limit to 2 notes per gap
        if (!note.externalSources) {
          note.externalSources = [];
        }
        
        // Add top search results as sources
        const topResults = searchResults.combined_results.slice(0, 2);
        note.externalSources.push(...topResults.map(result => ({
          url: result.url,
          title: result.title,
          description: result.description,
          relevanceScore: result.relevance_score,
          sourceProvider: result.source_provider
        })));
      }
      
    } catch (error) {
      console.warn(`Search enrichment failed for gap: ${gap.topic}`, error.message);
    }
  }
  
  const searchTime = Date.now() - searchStartTime;
  
  return {
    enrichedNotes: atomicNotes,
    searchMetrics: {
      strategy_used: processingOptions.searchStrategy || 'smart',
      gaps_processed: gapsProcessed,
      total_results: totalSearchResults,
      search_time: searchTime,
      brave_results: Math.floor(totalSearchResults * 0.6), // Mock distribution
      exa_results: Math.floor(totalSearchResults * 0.4)
    }
  };
}

// Enhanced PKM Workflow - Simple execution for GREEN phase
export const enhancedPkmWorkflow = {
  name: 'enhanced-pkm-workflow',
  async execute(input: {
    content: string;
    source: string;
    type: 'text' | 'code' | 'link' | 'image';
    metadata?: any;
    processingOptions?: {
      enableSearch?: boolean;
      searchStrategy?: 'brave_only' | 'exa_only' | 'parallel' | 'smart';
      maxSearchResults?: number;
      qualityThreshold?: number;
      modelPreference?: 'sonnet' | 'opus';
    };
  }) {
    const startTime = Date.now();
    
    try {
      // Step 1: Process content with existing workflow (backward compatibility)
      const baseResult = await pkmIngestionWorkflow.execute({
        content: input.content,
        source: input.source,
        type: input.type,
        metadata: input.metadata
      });
      
      // Step 2: Detect knowledge gaps if search is enabled
      let knowledgeGaps: any[] = [];
      let gapScore = 0;
      
      if (input.processingOptions?.enableSearch) {
        knowledgeGaps = detectKnowledgeGaps(input.content);
        gapScore = knowledgeGaps.length > 0 ? 
          knowledgeGaps.reduce((sum, gap) => sum + gap.confidence, 0) / knowledgeGaps.length : 0;
      }
      
      // Step 3: Enrich with search results
      const { enrichedNotes, searchMetrics } = await enrichWithSearchResults(
        baseResult.atomicNotes,
        knowledgeGaps,
        input.processingOptions || {}
      );
      
      // Step 4: Calculate enrichment score
      const enrichmentScore = input.processingOptions?.enableSearch ? 
        (searchMetrics?.total_results || 0) / Math.max(1, enrichedNotes.length) * 0.1 : 0;
      
      // Step 5: Update quality scores based on enrichment
      const updatedNotes = enrichedNotes.map(note => ({
        ...note,
        qualityScore: note.qualityScore + (note.externalSources?.length || 0) * 0.05
      }));
      
      const totalTime = Date.now() - startTime;
      
      return {
        atomicNotes: updatedNotes,
        processingMetrics: {
          ...baseResult.processingMetrics,
          totalTime,
          enrichmentScore,
          searchMetrics
        },
        validationResults: {
          ...baseResult.validationResults,
          knowledgeGaps,
          gapScore
        }
      };
      
    } catch (error) {
      // Graceful degradation - return local processing results
      console.warn('Enhanced workflow failed, falling back to local processing:', error.message);
      
      const fallbackResult = await pkmIngestionWorkflow.execute({
        content: input.content,
        source: input.source,
        type: input.type,
        metadata: input.metadata
      });
      
      return {
        ...fallbackResult,
        processingMetrics: {
          ...fallbackResult.processingMetrics,
          totalTime: Date.now() - startTime,
          enrichmentScore: 0,
          searchMetrics: null
        },
        validationResults: {
          ...fallbackResult.validationResults,
          knowledgeGaps: [],
          gapScore: 0
        }
      };
    }
  },
  
  // Input validation helper
  validateInput: (input: any) => {
    if (!input.content || input.content.length === 0) {
      throw new Error('Content cannot be empty');
    }
    if (!input.source) {
      throw new Error('Source cannot be empty');
    }
    return input;
  },
  
  // Output validation helper  
  validateOutput: (output: any) => {
    // Simple validation - just check required fields exist
    if (!output.atomicNotes || !output.processingMetrics || !output.validationResults) {
      throw new Error('Invalid output schema');
    }
    return output;
  }
};