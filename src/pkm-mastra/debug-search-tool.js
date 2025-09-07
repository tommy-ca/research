/**
 * Debug script to test search tool execution directly
 */

import { braveSearchTool } from './src/tools/search-tools.js';

console.log('Testing brave search tool...');

try {
  const result = await braveSearchTool.execute({
    input: { 
      query: 'artificial intelligence ethics', 
      count: 5,
      safeSearch: 'moderate'
    }
  });
  
  console.log('Result:', JSON.stringify(result, null, 2));
} catch (error) {
  console.error('Error:', error.message);
  console.error('Error details:', error);
}