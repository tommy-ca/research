// Simple debug test to see what the tool returns
import { describe, it, expect } from 'vitest';

console.log('Starting debug test...');

describe('Debug Test', () => {
  it('should log what happens', async () => {
    try {
      console.log('Attempting to import search tools...');
      
      // Try to import the tool
      const { braveSearchTool } = await import('./src/tools/search-tools.js');
      console.log('braveSearchTool imported:', typeof braveSearchTool);
      
      // Try to execute it
      console.log('Attempting to execute tool...');
      const result = await braveSearchTool.execute({
        query: 'test',
        count: 5,
        safeSearch: 'moderate'
      });
      
      console.log('Result type:', typeof result);
      console.log('Result:', result);
      
      expect(true).toBe(true); // Just pass the test
    } catch (error) {
      console.error('Error in debug test:', error);
      throw error;
    }
  });
});