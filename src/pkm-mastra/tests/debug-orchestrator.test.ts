// Debug orchestrator execution
import { describe, it, expect } from 'vitest';

describe('Debug Orchestrator', () => {
  it('should debug orchestrator execution', async () => {
    try {
      const { searchOrchestratorTool } = await import('./src/tools/search-orchestrator.js');
      
      console.log('Testing orchestrator...');
      
      const result = await searchOrchestratorTool.execute({
        query: 'latest AI breakthroughs January 2025',
        strategy: 'smart',
        content_type: 'current_events',
        max_results: 10
      });
      
      console.log('Orchestrator result:', JSON.stringify(result, null, 2));
      
      expect(true).toBe(true);
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  });
});