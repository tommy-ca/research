# PKM-Mastra Search Integration Architecture

**Date**: 2025-09-07  
**Framework**: Mastra.ai + Brave Search + Exa Search  
**Pattern**: External API Integration with Type-Safe Tools  

## Architecture Overview

Following Mastra.ai patterns for external API integration, this architecture creates modular, type-safe search tools that integrate seamlessly with existing PKM workflows.

## 1. Core Search Tool Architecture

### Search Provider Tools (Mastra.ai Pattern)

```typescript
// Brave Search Tool
export const braveSearchTool = createTool({
  id: "brave-search",
  inputSchema: z.object({
    query: z.string().min(1),
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
  execute: async ({ input, context }) => {
    try {
      const response = await braveApiClient.search({
        q: input.query,
        count: input.count,
        freshness: input.freshness,
        safesearch: input.safeSearch
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
  inputSchema: z.object({
    query: z.string().min(1),
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
  execute: async ({ input, context }) => {
    try {
      const response = await exaApiClient.search({
        query: input.query,
        numResults: input.num_results,
        type: input.type,
        contents: input.contents,
        includeDomains: input.include_domains,
        excludeDomains: input.exclude_domains
      });
      
      return transformExaResults(response);
    } catch (error) {
      throw new Error(`Exa search failed: ${error.message}`);
    }
  }
});
```

## 2. Search Orchestration Tool

```typescript
// Smart Search Orchestrator Tool
export const searchOrchestratorTool = createTool({
  id: "search-orchestrator", 
  inputSchema: z.object({
    query: z.string().min(1),
    strategy: z.enum(['brave_only', 'exa_only', 'parallel', 'smart']).default('smart'),
    content_type: z.enum(['current_events', 'academic', 'general', 'technical']).optional(),
    max_results: z.number().min(1).max(50).default(20)
  }),
  outputSchema: z.object({
    combined_results: z.array(z.object({
      title: z.string(),
      url: z.string().url(),
      description: z.string(),
      content: z.string().optional(),
      source_provider: z.enum(['brave', 'exa']),
      relevance_score: z.number().min(0).max(1),
      quality_score: z.number().min(0).max(1),
      confidence_score: z.number().min(0).max(1)
    })),
    search_strategy_used: z.string(),
    total_sources: z.number(),
    processing_metrics: z.object({
      brave_results: z.number(),
      exa_results: z.number(),
      total_time: z.number(),
      deduplication_removed: z.number()
    })
  }),
  execute: async ({ input, context }) => {
    const strategy = determineSearchStrategy(input.strategy, input.content_type, input.query);
    
    let searchPromises: Promise<SearchResult[]>[] = [];
    
    switch (strategy) {
      case 'brave_only':
        searchPromises = [braveSearchTool.execute({ 
          input: { query: input.query, count: input.max_results } 
        })];
        break;
        
      case 'exa_only':
        searchPromises = [exaSearchTool.execute({ 
          input: { query: input.query, num_results: input.max_results } 
        })];
        break;
        
      case 'parallel':
        searchPromises = [
          braveSearchTool.execute({ 
            input: { query: input.query, count: Math.ceil(input.max_results / 2) } 
          }),
          exaSearchTool.execute({ 
            input: { query: input.query, num_results: Math.ceil(input.max_results / 2) } 
          })
        ];
        break;
        
      case 'smart':
      default:
        searchPromises = await smartOrchestration(input);
    }
    
    const results = await Promise.allSettled(searchPromises);
    const successfulResults = results
      .filter(result => result.status === 'fulfilled')
      .flatMap(result => result.value.results);
    
    // Deduplicate, rank, and score results
    const processedResults = await processSearchResults(successfulResults, input.query);
    
    return {
      combined_results: processedResults,
      search_strategy_used: strategy,
      total_sources: processedResults.length,
      processing_metrics: calculateMetrics(results, processedResults)
    };
  }
});
```

## 3. Enhanced PKM Workflow Integration

### Updated Workflow Steps

```typescript
// Enhanced Content Processing with Search Integration
export const contentProcessingWithSearchStep = createStep({
  id: 'content-processing-with-search',
  inputSchema: z.object({
    content: z.string().min(1),
    selectedModel: z.enum(['sonnet', 'opus']),
    processingOptions: z.object({
      enableSearch: z.boolean().default(false),
      searchStrategy: z.enum(['brave_only', 'exa_only', 'parallel', 'smart']).default('smart'),
      maxSearchResults: z.number().min(1).max(20).default(10)
    }).optional()
  }),
  outputSchema: z.object({
    processedContent: z.string(),
    extractedMetadata: z.record(z.any()),
    searchResults: z.array(z.object({
      title: z.string(),
      url: z.string(),
      relevance_score: z.number()
    })).optional(),
    enrichmentScore: z.number().min(0).max(1).optional()
  }),
  execute: async ({ input, context }) => {
    // Process content locally first
    const localProcessing = await processContentLocally(input.content, input.selectedModel);
    
    // If search enabled, enrich with external sources
    if (input.processingOptions?.enableSearch) {
      try {
        // Extract key concepts for search
        const searchQueries = extractSearchQueries(localProcessing.extractedMetadata);
        
        // Orchestrate search across providers
        const searchResults = await Promise.all(
          searchQueries.map(query => 
            searchOrchestratorTool.execute({
              input: {
                query,
                strategy: input.processingOptions.searchStrategy,
                max_results: input.processingOptions.maxSearchResults
              }
            })
          )
        );
        
        // Combine and rank all search results
        const combinedResults = combineSearchResults(searchResults);
        const enrichmentScore = calculateEnrichmentScore(localProcessing, combinedResults);
        
        return {
          ...localProcessing,
          searchResults: combinedResults.slice(0, 10), // Top 10 most relevant
          enrichmentScore
        };
        
      } catch (searchError) {
        // Graceful degradation - return local processing with warning
        console.warn('Search enrichment failed, returning local results:', searchError);
        return {
          ...localProcessing,
          enrichmentScore: 0
        };
      }
    }
    
    return localProcessing;
  }
});

// Gap Detection Step
export const gapDetectionStep = createStep({
  id: 'gap-detection',
  inputSchema: z.object({
    processedContent: z.string(),
    extractedMetadata: z.record(z.any()),
    atomicNotes: z.array(z.object({
      content: z.string(),
      concepts: z.array(z.string())
    }))
  }),
  outputSchema: z.object({
    knowledgeGaps: z.array(z.object({
      topic: z.string(),
      confidence: z.number().min(0).max(1),
      suggestedSearchQueries: z.array(z.string()),
      priority: z.enum(['low', 'medium', 'high'])
    })),
    gapScore: z.number().min(0).max(1)
  }),
  execute: async ({ input, context }) => {
    // Analyze content for missing context or incomplete explanations
    const gaps = await analyzeKnowledgeGaps(input);
    
    return {
      knowledgeGaps: gaps,
      gapScore: calculateOverallGapScore(gaps)
    };
  }
});

// Search Enrichment Step
export const searchEnrichmentStep = createStep({
  id: 'search-enrichment',
  inputSchema: z.object({
    knowledgeGaps: z.array(z.object({
      topic: z.string(),
      suggestedSearchQueries: z.array(z.string()),
      priority: z.enum(['low', 'medium', 'high'])
    })),
    processingOptions: z.object({
      searchStrategy: z.enum(['brave_only', 'exa_only', 'parallel', 'smart']).default('smart'),
      maxResultsPerGap: z.number().default(5)
    }).optional()
  }),
  outputSchema: z.object({
    enrichmentSources: z.array(z.object({
      gap_topic: z.string(),
      sources: z.array(z.object({
        title: z.string(),
        url: z.string(),
        relevance_score: z.number(),
        content_preview: z.string()
      }))
    })),
    totalSourcesFound: z.number(),
    searchMetrics: z.record(z.any())
  }),
  execute: async ({ input, context }) => {
    const enrichmentPromises = input.knowledgeGaps
      .filter(gap => gap.priority === 'high' || gap.priority === 'medium')
      .map(async (gap) => {
        const searchResults = await Promise.all(
          gap.suggestedSearchQueries.map(query => 
            searchOrchestratorTool.execute({
              input: {
                query,
                strategy: input.processingOptions?.searchStrategy || 'smart',
                max_results: input.processingOptions?.maxResultsPerGap || 5
              }
            })
          )
        );
        
        const combinedSources = combineAndRankSources(searchResults);
        
        return {
          gap_topic: gap.topic,
          sources: combinedSources
        };
      });
    
    const enrichmentSources = await Promise.all(enrichmentPromises);
    const totalSources = enrichmentSources.reduce((sum, item) => sum + item.sources.length, 0);
    
    return {
      enrichmentSources,
      totalSourcesFound: totalSources,
      searchMetrics: {
        gaps_processed: enrichmentSources.length,
        avg_sources_per_gap: totalSources / Math.max(1, enrichmentSources.length)
      }
    };
  }
});
```

## 4. Enhanced Workflow Definition

```typescript
// Enhanced PKM Workflow with Search Integration
export const enhancedPkmWorkflow = {
  name: 'pkm-ingestion-with-search',
  
  async execute(input: EnhancedContentInput): Promise<EnhancedProcessingResult> {
    const startTime = Date.now();
    
    try {
      // Phase 1: Model Selection (existing)
      const modelResult = await modelSelectionStep.execute({ input, context: {} });
      
      // Phase 2: Enhanced Content Processing with Optional Search
      const processingResult = await contentProcessingWithSearchStep.execute({
        input: {
          content: input.content,
          selectedModel: modelResult.selectedModel,
          processingOptions: input.processingOptions
        },
        context: { modelSelection: modelResult }
      });
      
      // Phase 3: Atomic Note Generation (existing)
      const atomicResult = await atomicNoteGenerationStep.execute({
        input: {
          processedContent: processingResult.processedContent,
          extractedMetadata: processingResult.extractedMetadata,
          selectedModel: modelResult.selectedModel
        },
        context: { processing: processingResult }
      });
      
      // Phase 4: Gap Detection (new)
      const gapResult = await gapDetectionStep.execute({
        input: {
          processedContent: processingResult.processedContent,
          extractedMetadata: processingResult.extractedMetadata,
          atomicNotes: atomicResult.atomicNotes
        },
        context: {}
      });
      
      // Phase 5: Search Enrichment (new - conditional)
      let enrichmentResult = null;
      if (input.processingOptions?.enableSearch && gapResult.gapScore > 0.3) {
        enrichmentResult = await searchEnrichmentStep.execute({
          input: {
            knowledgeGaps: gapResult.knowledgeGaps,
            processingOptions: input.processingOptions
          },
          context: {}
        });
      }
      
      // Phase 6: Quality Assessment (enhanced with search data)
      const qualityResult = await enhancedQualityAssessmentStep.execute({
        input: {
          atomicNotes: atomicResult.atomicNotes,
          originalContent: input.content,
          metadata: input.metadata,
          searchResults: processingResult.searchResults,
          enrichmentSources: enrichmentResult?.enrichmentSources
        },
        context: {}
      });
      
      const endTime = Date.now();
      
      return {
        atomicNotes: atomicResult.atomicNotes.map((note, index) => ({
          ...note,
          qualityScore: qualityResult.qualityResults[index]?.qualityScore || 0.8,
          suggestedLinks: generateSuggestedLinks(note.content),
          paraCategory: classifyPARA(note.content, input.content, input.metadata),
          processingModel: modelResult.selectedModel,
          externalSources: enrichmentResult?.enrichmentSources
            ?.find(item => item.gap_topic === note.title)?.sources
        })),
        processingMetrics: {
          totalTime: endTime - startTime,
          modelUsage: { [modelResult.selectedModel]: 1, total: 1 },
          searchMetrics: enrichmentResult?.searchMetrics,
          enrichmentScore: processingResult.enrichmentScore || 0
        },
        validationResults: {
          ...qualityResult,
          knowledgeGaps: gapResult.knowledgeGaps,
          gapScore: gapResult.gapScore
        }
      };
      
    } catch (error) {
      return {
        status: 'failed',
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  },
  
  // Validate input and output schemas
  validateInput(input: any): ContentInput {
    return EnhancedContentInputSchema.parse(input);
  },
  
  validateOutput(output: any): ProcessingResult {
    return EnhancedProcessingResultSchema.parse(output);
  }
};
```

## 5. Type Definitions

```typescript
// Enhanced Input Schema
const EnhancedContentInputSchema = z.object({
  content: z.string().min(1, 'Content cannot be empty'),
  source: z.string(),
  type: z.enum(['text', 'url', 'file', 'clipboard', 'document', 'email']),
  metadata: z.record(z.any()).optional(),
  processingOptions: z.object({
    modelPreference: z.enum(['auto', 'sonnet', 'opus']).optional(),
    qualityThreshold: z.number().min(0).max(1).optional(),
    enableSearch: z.boolean().default(false),
    searchStrategy: z.enum(['brave_only', 'exa_only', 'parallel', 'smart']).default('smart'),
    maxSearchResults: z.number().min(1).max(50).default(10),
    requireHumanReview: z.boolean().optional()
  }).optional()
});

// Search Provider Configuration
interface SearchProviderConfig {
  brave: {
    apiKey: string;
    baseUrl: string;
    rateLimits: {
      requestsPerMinute: number;
      requestsPerDay: number;
    };
  };
  exa: {
    apiKey: string;
    baseUrl: string; 
    rateLimits: {
      requestsPerMinute: number;
      requestsPerMonth: number;
    };
  };
}
```

## 6. Implementation Strategy

### Phase 1: Basic Search Integration (TDD RED/GREEN)
1. Implement `braveSearchTool` with minimal functionality
2. Create basic search result processing
3. Add simple workflow integration
4. Implement graceful degradation for API failures

### Phase 2: Intelligent Orchestration (TDD REFACTOR)
1. Add `exaSearchTool` implementation
2. Implement `searchOrchestratorTool` with strategy selection
3. Add gap detection and enrichment steps
4. Enhance quality assessment with search data

### Phase 3: Advanced Features
1. Implement caching and rate limiting
2. Add predictive search and prefetching
3. Implement search result ranking optimization
4. Add comprehensive monitoring and metrics

This architecture maintains the existing PKM workflow patterns while adding powerful search capabilities through modular, testable tools following Mastra.ai conventions.

---

*Architecture designed following Mastra.ai patterns for type-safe external API integration with progressive enhancement capabilities.*