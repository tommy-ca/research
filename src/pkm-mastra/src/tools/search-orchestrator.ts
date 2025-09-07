/**
 * Search Orchestrator Tool - TDD GREEN Phase Implementation
 * Minimal implementation to make RED tests pass
 * Following TDD methodology: Make tests pass with simplest possible code
 */

import { createTool } from '@mastra/core';
import { z } from 'zod';
import { braveSearchTool, exaSearchTool } from './search-tools.js';

// Mock strategy selection - GREEN phase uses simple rules
function selectSearchStrategy(query: string, contentType?: string, strategy?: string) {
  if (strategy && strategy !== 'smart') {
    return strategy;
  }
  
  // Simple heuristic for smart strategy selection
  if (contentType === 'current_events' || query.includes('latest') || query.includes('2025')) {
    return 'brave';
  }
  
  if (contentType === 'academic' || query.includes('research') || query.includes('methodology')) {
    return 'exa';
  }
  
  // Default to parallel for comprehensive coverage
  return 'parallel';
}

// Mock result ranking - GREEN phase uses simple scoring
function rankResults(results: any[], query: string) {
  return results.map((result, index) => ({
    ...result,
    confidence_score: Math.max(0.1, result.relevance_score * 0.9 + 0.1),
    // Simple ranking based on position and existing scores
    relevance_score: Math.max(0.1, result.relevance_score - (index * 0.05))
  })).sort((a, b) => b.relevance_score - a.relevance_score);
}

// Mock deduplication - GREEN phase uses simple URL comparison
function deduplicateResults(results: any[]) {
  const seen = new Set<string>();
  const deduplicated = [];
  let removed = 0;
  
  for (const result of results) {
    if (!seen.has(result.url)) {
      seen.add(result.url);
      deduplicated.push(result);
    } else {
      removed++;
    }
  }
  
  return { results: deduplicated, removed };
}

// Search Orchestrator Tool
export const searchOrchestratorTool = createTool({
  id: "search-orchestrator",
  description: "Orchestrate multiple search providers with intelligent strategy selection",
  inputSchema: z.object({
    query: z.string().min(1, 'Query cannot be empty'),
    strategy: z.enum(['brave_only', 'exa_only', 'parallel', 'smart']).default('smart'),
    content_type: z.enum(['current_events', 'academic', 'technical', 'general']).optional(),
    max_results: z.number().min(1).max(50).default(10),
    include_domains: z.array(z.string()).optional(),
    exclude_domains: z.array(z.string()).optional()
  }),
  outputSchema: z.object({
    combined_results: z.array(z.object({
      title: z.string(),
      url: z.string().url(),
      description: z.string(),
      content: z.string().optional(),
      published_date: z.string().optional(),
      relevance_score: z.number().min(0).max(1),
      quality_score: z.number().min(0).max(1),
      confidence_score: z.number().min(0).max(1),
      source_provider: z.enum(['brave', 'exa'])
    })),
    total_sources: z.number(),
    search_strategy_used: z.string(),
    processing_metrics: z.object({
      brave_results: z.number(),
      exa_results: z.number(),
      deduplication_removed: z.number(),
      total_search_time: z.number()
    })
  }),
  execute: async (params) => {
    const startTime = Date.now();
    
    try {
      // Strategy selection
      const actualStrategy = selectSearchStrategy(params.query, params.content_type, params.strategy);
      
      let braveResults: any[] = [];
      let exaResults: any[] = [];
      let braveCount = 0;
      let exaCount = 0;
      
      // Execute searches based on strategy
      if (actualStrategy === 'brave_only' || actualStrategy === 'brave' || actualStrategy === 'parallel') {
        try {
          const braveResponse = await braveSearchTool.execute({
            query: params.query,
            count: Math.ceil(params.max_results / (actualStrategy === 'parallel' ? 2 : 1)),
            safeSearch: 'moderate'
          });
          
          braveResults = braveResponse.results.map(r => ({
            ...r,
            quality_score: Math.min(1.0, r.relevance_score + 0.1),
            confidence_score: Math.max(0.1, r.relevance_score * 0.8),
            source_provider: 'brave' as const
          }));
          braveCount = braveResults.length;
        } catch (error) {
          console.warn('Brave search failed:', error.message);
        }
      }
      
      if (actualStrategy === 'exa_only' || actualStrategy === 'exa' || actualStrategy === 'parallel') {
        try {
          const exaResponse = await exaSearchTool.execute({
            query: params.query,
            num_results: Math.ceil(params.max_results / (actualStrategy === 'parallel' ? 2 : 1)),
            type: 'auto',
            contents: { text: true },
            include_domains: params.include_domains,
            exclude_domains: params.exclude_domains
          });
          
          exaResults = exaResponse.results.map(r => ({
            ...r,
            confidence_score: Math.max(0.1, r.quality_score * 0.9),
            source_provider: 'exa' as const
          }));
          exaCount = exaResults.length;
        } catch (error) {
          console.warn('Exa search failed:', error.message);
        }
      }
      
      // Combine results
      let allResults = [...braveResults, ...exaResults];
      
      // Apply domain filtering if not already done by individual tools
      if (params.include_domains && actualStrategy !== 'exa_only') {
        allResults = allResults.filter(result => 
          params.include_domains!.some(domain => result.url.toLowerCase().includes(domain.toLowerCase()))
        );
      }
      
      if (params.exclude_domains && actualStrategy !== 'exa_only') {
        allResults = allResults.filter(result => 
          !params.exclude_domains!.some(domain => result.url.toLowerCase().includes(domain.toLowerCase()))
        );
      }
      
      // Deduplicate
      const { results: deduplicatedResults, removed } = deduplicateResults(allResults);
      
      // Rank results
      const rankedResults = rankResults(deduplicatedResults, params.query);
      
      // Limit to max_results
      const finalResults = rankedResults.slice(0, params.max_results);
      
      const totalTime = Date.now() - startTime;
      
      return {
        combined_results: finalResults,
        total_sources: finalResults.length,
        search_strategy_used: actualStrategy,
        processing_metrics: {
          brave_results: braveCount,
          exa_results: exaCount,
          deduplication_removed: removed,
          total_search_time: totalTime
        }
      };
      
    } catch (error) {
      // Graceful degradation - return empty results instead of crashing
      return {
        combined_results: [],
        total_sources: 0,
        search_strategy_used: params.strategy,
        processing_metrics: {
          brave_results: 0,
          exa_results: 0,
          deduplication_removed: 0,
          total_search_time: Date.now() - startTime
        }
      };
    }
  }
});