import { describe, it, expect, beforeEach } from 'vitest';
import { Agent } from '@mastra/core';
import { openai } from '@ai-sdk/openai';
import { enhancedCaptureAgent } from '@/agents/enhanced-capture-agent';

describe('Enhanced Capture Agent - Mastra 2025 Integration', () => {
  describe('Agent Configuration Compliance', () => {
    it('should be properly configured with Mastra Agent pattern', () => {
      // This test SHOULD FAIL initially - we need to create enhanced agent
      expect(enhancedCaptureAgent).toBeDefined();
      expect(enhancedCaptureAgent).toBeInstanceOf(Agent);
    });

    it('should have proper instructions for PKM capture', () => {
      const agent = enhancedCaptureAgent;
      
      // Should have comprehensive instructions for GTD compliance
      expect(agent.instructions).toBeDefined();
      expect(typeof agent.instructions).toBe('string');
      expect(agent.instructions.length).toBeGreaterThan(100);
      
      // Should mention key PKM concepts
      expect(agent.instructions.toLowerCase()).toMatch(/(gtd|capture|fidelity|quality)/);
    });

    it('should have proper model configuration', () => {
      const agent = enhancedCaptureAgent;
      
      // Should use appropriate model for capture tasks
      expect(agent.model).toBeDefined();
      // For capture, we want speed over capability, so gpt-4o-mini is appropriate
    });

    it('should have proper memory configuration', () => {
      const agent = enhancedCaptureAgent;
      
      // Should have memory for context awareness
      expect(agent.memory).toBeDefined();
      expect(Array.isArray(agent.memory)).toBe(true);
      
      // Should include relevant memory types for PKM
      const memoryTypes = agent.memory.map((m: any) => m.type || m.name);
      expect(memoryTypes).toContain('captureContext');
      expect(memoryTypes).toContain('gtdCompliance');
    });

    it('should have proper tool integration', () => {
      const agent = enhancedCaptureAgent;
      
      // Should have tools for comprehensive capture
      expect(agent.tools).toBeDefined();
      expect(Array.isArray(agent.tools)).toBe(true);
      expect(agent.tools.length).toBeGreaterThan(0);
      
      // Should include essential capture tools
      const toolIds = agent.tools.map((t: any) => t.id);
      expect(toolIds).toContain('webContentExtractor');
      expect(toolIds).toContain('qualityAssessment');
      expect(toolIds).toContain('duplicateDetection');
    });
  });

  describe('Agent Execution and Response Generation', () => {
    it('should generate appropriate responses for content capture', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Process this content: "Comprehensive guide to personal knowledge management systems with practical implementation strategies"'
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result).toBeDefined();
      expect(result.text).toBeDefined();
      expect(typeof result.text).toBe('string');
      expect(result.text.length).toBeGreaterThan(0);
    });

    it('should handle structured output with Zod schemas', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Analyze this content for capture: "Personal knowledge management best practices"'
      }];

      // Should support structured output for consistent data extraction
      const result = await enhancedCaptureAgent.generate({
        messages: testMessages,
        schema: {
          capturedContent: 'string',
          qualityScore: 'number',
          extractedMetadata: 'object'
        }
      });

      expect(result.object).toBeDefined();
      if (result.object) {
        expect(result.object.capturedContent).toBeDefined();
        expect(typeof result.object.qualityScore).toBe('number');
        expect(result.object.extractedMetadata).toBeDefined();
      }
    });

    it('should support streaming responses for long content', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Process this lengthy content: ' + 'Content '.repeat(1000)
      }];

      let streamChunks: string[] = [];
      
      const stream = await enhancedCaptureAgent.stream({
        messages: testMessages
      });

      for await (const chunk of stream) {
        if (chunk.text) {
          streamChunks.push(chunk.text);
        }
      }

      expect(streamChunks.length).toBeGreaterThan(0);
      expect(streamChunks.join('')).toBeTruthy();
    });

    it('should handle image analysis for multimodal content', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: [
          { type: 'text', text: 'Analyze this image for content capture' },
          { 
            type: 'image', 
            image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==' // 1x1 test image
          }
        ]
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result.text).toBeDefined();
      expect(result.text.length).toBeGreaterThan(0);
      // Should acknowledge the image content
      expect(result.text.toLowerCase()).toMatch(/(image|visual|picture|diagram)/);
    });
  });

  describe('Tool Integration and Execution', () => {
    it('should properly execute web content extraction tool', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Extract content from this URL: https://example.com/article'
      }];

      // Agent should choose appropriate tool for URL content
      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result.text).toBeDefined();
      // Should include extracted content or indicate tool usage
      expect(result.text.toLowerCase()).toMatch(/(extract|content|url|article)/);
    });

    it('should execute quality assessment tool for content validation', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Assess the quality of this content: "Comprehensive analysis of machine learning algorithms with practical implementation examples and detailed performance comparisons"'
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result.text).toBeDefined();
      // Should include quality assessment results
      expect(result.text.toLowerCase()).toMatch(/(quality|score|assessment|analysis)/);
    });

    it('should execute duplicate detection when needed', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Check for duplicates of this content: "Machine learning fundamentals and applications"'
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result.text).toBeDefined();
      // Should include duplicate detection results
      expect(result.text.toLowerCase()).toMatch(/(duplicate|similar|match|unique)/);
    });
  });

  describe('Memory Utilization and Context Awareness', () => {
    it('should maintain capture context across conversations', async () => {
      // First capture
      const firstMessages = [{
        role: 'user' as const,
        content: 'Capture this content about PKM: "Personal knowledge management systems"'
      }];

      await enhancedCaptureAgent.generate({
        messages: firstMessages
      });

      // Second capture should be aware of first
      const secondMessages = [{
        role: 'user' as const,
        content: 'Now capture related content: "Knowledge graphs and connections"'
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: secondMessages
      });

      expect(result.text).toBeDefined();
      // Should show awareness of previous context
      expect(result.text.toLowerCase()).toMatch(/(previous|related|connection|pkm|knowledge)/);
    });

    it('should apply GTD compliance patterns from memory', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Capture this incomplete information: "Meeting tomorrow"'
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result.text).toBeDefined();
      // Should recognize incomplete capture and suggest improvements
      expect(result.text.toLowerCase()).toMatch(/(incomplete|missing|context|details|gtd)/);
    });

    it('should remember user preferences and patterns', async () => {
      // Simulate user preference for detailed metadata
      const preferencesMessages = [{
        role: 'user' as const,
        content: 'I always need comprehensive metadata extraction for all captures'
      }];

      await enhancedCaptureAgent.generate({
        messages: preferencesMessages
      });

      // Next capture should apply this preference
      const captureMessages = [{
        role: 'user' as const,
        content: 'Capture this article: "Advanced TypeScript patterns for AI applications"'
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: captureMessages
      });

      expect(result.text).toBeDefined();
      // Should include comprehensive metadata based on remembered preference
      expect(result.text.toLowerCase()).toMatch(/(metadata|comprehensive|detailed|extract)/);
    });
  });

  describe('Error Handling and Edge Cases', () => {
    it('should handle malformed inputs gracefully', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: '' // Empty content
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result.text).toBeDefined();
      // Should provide helpful guidance for empty input
      expect(result.text.toLowerCase()).toMatch(/(empty|provide|content|help)/);
    });

    it('should handle network errors during tool execution', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Extract content from this unreachable URL: https://nonexistent-domain-12345.com'
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result.text).toBeDefined();
      // Should gracefully handle network errors
      expect(result.text.toLowerCase()).toMatch(/(error|unable|unreachable|failed)/);
    });

    it('should validate tool outputs before proceeding', async () => {
      const testMessages = [{
        role: 'user' as const,
        content: 'Process this content with potential tool failures'
      }];

      // Should continue gracefully even if some tools fail
      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });

      expect(result.text).toBeDefined();
      expect(result.text.length).toBeGreaterThan(0);
    });
  });

  describe('Performance and Production Requirements', () => {
    it('should respond within acceptable time limits', async () => {
      const startTime = Date.now();
      
      const testMessages = [{
        role: 'user' as const,
        content: 'Quick capture: "Test content for performance validation"'
      }];

      const result = await enhancedCaptureAgent.generate({
        messages: testMessages
      });
      
      const responseTime = Date.now() - startTime;
      
      expect(result.text).toBeDefined();
      // Should respond within 2 seconds for production use
      expect(responseTime).toBeLessThan(2000);
    });

    it('should handle concurrent requests efficiently', async () => {
      const concurrentRequests = Array.from({ length: 5 }, (_, i) => 
        enhancedCaptureAgent.generate({
          messages: [{
            role: 'user' as const,
            content: `Concurrent capture test ${i}: "Content for testing concurrent processing"`
          }]
        })
      );

      const results = await Promise.all(concurrentRequests);
      
      results.forEach((result, index) => {
        expect(result.text).toBeDefined();
        expect(result.text).toContain(index.toString());
      });
    });
  });
});