/**
 * Search Tools - TDD GREEN Phase Implementation
 * Minimal implementation to make RED tests pass
 * Following TDD methodology: Make tests pass with simplest possible code
 */

import { createTool } from '@mastra/core';
import { z } from 'zod';

// Mock API clients - GREEN phase uses mocks
const braveApiClient = {
  async search(params: any) {
    // Minimal mock response to pass tests
    return {
      web: {
        results: Array.from({ length: params.count || 10 }, (_, i) => ({
          title: `Mock Brave Result ${i + 1}: ${params.q}`,
          url: `https://example.com/brave-result-${i + 1}`,
          description: `Mock description for ${params.q} result ${i + 1}`,
          date_published: new Date().toISOString(),
          page_age: '2024-01-01'
        }))
      },
      query: params.q
    };
  }
};

const exaApiClient = {
  async search(params: any) {
    // Minimal mock response to pass tests
    return {
      results: Array.from({ length: params.numResults || 10 }, (_, i) => ({
        title: `Mock Exa Result ${i + 1}: ${params.query}`,
        url: `https://example.com/exa-result-${i + 1}`,
        snippet: `High-quality content about ${params.query} from academic source ${i + 1}`,
        published_date: new Date().toISOString(),
        score: 0.9 - (i * 0.05), // Decreasing relevance scores
        text: params.contents?.text ? `Full text content for ${params.query}` : undefined
      }))
    };
  }
};

// Transform functions - minimal implementation
function transformBraveResults(response: any) {
  return {
    results: response.web.results.map((result: any, index: number) => ({
      title: result.title,
      url: result.url,
      description: result.description,
      published_date: result.date_published,
      relevance_score: Math.max(0.1, 1 - (index * 0.1)) // Simple relevance scoring
    })),
    total_results: response.web.results.length,
    search_metadata: {
      query: response.query,
      provider: 'brave' as const,
      search_time: 100 + Math.random() * 200 // Mock search time
    }
  };
}

function transformExaResults(response: any) {
  return {
    results: response.results.map((result: any) => ({
      title: result.title,
      url: result.url,
      description: result.snippet,
      content: result.text,
      published_date: result.published_date,
      relevance_score: Math.max(0.1, result.score),
      quality_score: Math.min(1.0, result.score + 0.1) // Exa has slightly higher quality scores
    })),
    total_results: response.results.length,
    search_metadata: {
      query: response.results[0] ? 'query from response' : 'no results',
      provider: 'exa' as const,
      search_time: 150 + Math.random() * 250
    }
  };
}

// Brave Search Tool
export const braveSearchTool = createTool({
  id: "brave-search",
  description: "Search the web using Brave Search API for privacy-focused results",
  inputSchema: z.object({
    query: z.string().min(1, 'Query cannot be empty'),
    count: z.number().min(1).max(20).default(10),
    freshness: z.enum(['24h', '7d', '30d', '1y']).optional(),
    safeSearch: z.enum(['off', 'moderate', 'strict']).default('moderate')
  }),
  outputSchema: z.object({
    results: z.array(z.object({
      title: z.string(),
      url: z.string().url(),
      description: z.string(),
      published_date: z.string().optional(),
      relevance_score: z.number().min(0).max(1)
    })),
    total_results: z.number(),
    search_metadata: z.object({
      query: z.string(),
      provider: z.literal('brave'),
      search_time: z.number()
    })
  }),
  execute: async (params) => {
    try {
      const response = await braveApiClient.search({
        q: params.query,
        count: params.count,
        freshness: params.freshness,
        safesearch: params.safeSearch
      });
      
      return transformBraveResults(response);
    } catch (error) {
      throw new Error(`Brave search failed: ${error.message}`);
    }
  }
});

// Exa Search Tool
export const exaSearchTool = createTool({
  id: "exa-search",
  description: "Search using Exa AI for high-quality, semantic search results",
  inputSchema: z.object({
    query: z.string().min(1, 'Query cannot be empty'),
    num_results: z.number().min(1).max(20).default(10),
    type: z.enum(['neural', 'keyword', 'auto']).default('auto'),
    contents: z.object({
      text: z.boolean().default(true),
      highlights: z.boolean().default(false),
      summary: z.boolean().default(false)
    }).optional(),
    include_domains: z.array(z.string()).optional(),
    exclude_domains: z.array(z.string()).optional()
  }),
  outputSchema: z.object({
    results: z.array(z.object({
      title: z.string(),
      url: z.string().url(),
      description: z.string(),
      content: z.string().optional(),
      published_date: z.string().optional(),
      relevance_score: z.number().min(0).max(1),
      quality_score: z.number().min(0).max(1)
    })),
    total_results: z.number(),
    search_metadata: z.object({
      query: z.string(),
      provider: z.literal('exa'),
      search_time: z.number()
    })
  }),
  execute: async (params) => {
    try {
      // Apply domain filtering to mock results
      let mockResults = await exaApiClient.search({
        query: params.query,
        numResults: params.num_results,
        type: params.type,
        contents: params.contents
      });

      // Filter by domains if specified
      if (params.include_domains || params.exclude_domains) {
        mockResults.results = mockResults.results.filter((result: any) => {
          const url = result.url.toLowerCase();
          
          if (params.include_domains) {
            return params.include_domains.some(domain => url.includes(domain.toLowerCase()));
          }
          
          if (params.exclude_domains) {
            return !params.exclude_domains.some(domain => url.includes(domain.toLowerCase()));
          }
          
          return true;
        });
      }
      
      return transformExaResults(mockResults);
    } catch (error) {
      throw new Error(`Exa search failed: ${error.message}`);
    }
  }
});