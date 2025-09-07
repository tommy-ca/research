// Debug orchestrator issue test
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('Debug Orchestrator Issue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should work in isolation like debug test', async () => {
    const { searchOrchestratorTool } = await import('../src/tools/search-orchestrator.js');
    
    console.log('Testing orchestrator in test environment...');
    
    const result = await searchOrchestratorTool.execute({
      query: 'latest AI breakthroughs January 2025',
      strategy: 'smart',
      content_type: 'current_events',
      max_results: 10
    });
    
    console.log('Result keys:', Object.keys(result));
    console.log('Combined results length:', result?.combined_results?.length || 'undefined');
    console.log('Search strategy used:', result?.search_strategy_used || 'undefined');
    
    expect(result).toBeDefined();
    expect(result.combined_results).toBeDefined();
    expect(result.combined_results.length).toBeGreaterThan(0);
  });
  
  it('should test brave search tool directly', async () => {
    const { braveSearchTool } = await import('../src/tools/search-tools.js');
    
    console.log('Testing brave search tool directly...');
    
    const result = await braveSearchTool.execute({
      query: 'latest AI breakthroughs January 2025',
      count: 10,
      safeSearch: 'moderate'
    });
    
    console.log('Brave result keys:', Object.keys(result));
    console.log('Brave results length:', result?.results?.length || 'undefined');
    
    expect(result).toBeDefined();
    expect(result.results).toBeDefined();
    expect(result.results.length).toBeGreaterThan(0);
  });
});