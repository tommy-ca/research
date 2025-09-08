import { describe, it, expect, beforeEach } from 'vitest';
import { 
  createCaptureAgent, 
  createDefaultCaptureAgent,
  CaptureAgentService,
  createCaptureAgentService
} from '../../src/agents/capture-agent.js';
import { ProviderFactory, defaultProviderConfig } from '../../src/providers/provider-factory.js';

describe('CaptureAgent', () => {
  let providerFactory: ProviderFactory;
  let captureAgentService: CaptureAgentService;

  beforeEach(() => {
    providerFactory = new ProviderFactory(defaultProviderConfig);
    captureAgentService = createCaptureAgentService(providerFactory);
  });

  describe('Agent Creation', () => {
    it('should create capture agent with provider factory', async () => {
      const agent = await createCaptureAgent(providerFactory);
      
      expect(agent).toBeDefined();
      expect(agent.name).toBe('Multi-Source Capture Agent');
    });

    it('should create default capture agent', async () => {
      const agent = await createDefaultCaptureAgent();
      
      expect(agent).toBeDefined();
      expect(agent.name).toBe('Multi-Source Capture Agent');
    });

    it('should create capture agent service', () => {
      const service = createCaptureAgentService();
      
      expect(service).toBeDefined();
      expect(service).toBeInstanceOf(CaptureAgentService);
    });
  });

  describe('Service Operations', () => {
    it('should generate text responses', async () => {
      const messages = [
        { role: 'user', content: 'Test content for capture' }
      ];

      const result = await captureAgentService.generateResponse(messages);
      
      expect(result).toBeDefined();
    });

    it('should handle structured output generation', async () => {
      const messages = [
        { role: 'user', content: 'Extract metadata from this content' }
      ];
      const schema = {
        title: 'string',
        summary: 'string',
        quality: 'number'
      };

      const result = await captureAgentService.generateStructuredOutput(messages, schema);
      
      expect(result).toBeDefined();
    });

    it('should process multimodal content', async () => {
      const messages = [
        { 
          role: 'user', 
          content: [
            { type: 'text', text: 'Analyze this content' },
            { type: 'image', image: 'mock-image-data' }
          ]
        }
      ];

      const result = await captureAgentService.processMultimodalContent(messages);
      
      expect(result).toBeDefined();
    });

    it('should execute tools', async () => {
      const result = await captureAgentService.executeTool('qualityAssessment', {
        content: 'Test content'
      });
      
      expect(result).toBeDefined();
      expect(result.qualityScore).toBeGreaterThan(0);
    });

    it('should handle concurrent requests', async () => {
      const requests = [
        { messages: [{ role: 'user', content: 'First request' }] },
        { messages: [{ role: 'user', content: 'Second request' }] },
        { messages: [{ role: 'user', content: 'Third request' }] }
      ];

      const results = await captureAgentService.processConcurrentRequests(requests);
      
      expect(results).toBeDefined();
      expect(results).toHaveLength(3);
    });
  });

  describe('Provider Management', () => {
    it('should get provider metrics', () => {
      const metrics = captureAgentService.getProviderMetrics();
      
      expect(metrics).toBeDefined();
      expect(metrics.routingDecisions).toBeDefined();
    });

    it('should get provider configuration', () => {
      const config = captureAgentService.getProviderConfig();
      
      expect(config).toBeDefined();
      expect(config.primary).toBe('claude-code');
    });

    it('should test provider availability', async () => {
      const isAvailable = await captureAgentService.testProvider('claude-code');
      
      expect(typeof isAvailable).toBe('boolean');
    });

    it('should get available providers', () => {
      const providers = captureAgentService.getAvailableProviders();
      
      expect(providers).toBeDefined();
      expect(providers).toContain('claude-code');
    });

    it('should update provider configuration', () => {
      const newConfig = {
        enableFallback: false,
        costOptimization: false
      };

      captureAgentService.updateProviderConfig(newConfig);
      
      const updatedConfig = captureAgentService.getProviderConfig();
      expect(updatedConfig.enableFallback).toBe(false);
      expect(updatedConfig.costOptimization).toBe(false);
    });
  });

  describe('Error Handling', () => {
    it('should handle invalid tool execution', async () => {
      await expect(captureAgentService.executeTool('nonexistent-tool', {}))
        .rejects.toThrow('Tool nonexistent-tool not found');
    });

    it('should handle generation failures gracefully', async () => {
      // Test with empty messages array which might cause issues
      const messages: any[] = [];

      await expect(captureAgentService.generateResponse(messages))
        .rejects.toThrow();
    });
  });

  describe('Performance Requirements', () => {
    it('should process requests within reasonable time', async () => {
      const startTime = Date.now();
      
      const messages = [
        { role: 'user', content: 'Quick processing test' }
      ];
      
      await captureAgentService.generateResponse(messages);
      
      const duration = Date.now() - startTime;
      expect(duration).toBeLessThan(5000); // 5 second timeout
    });
  });

  describe('Integration with Provider Factory', () => {
    it('should work with custom provider factory', async () => {
      const customConfig = {
        ...defaultProviderConfig,
        primary: 'openai' as const
      };
      const customFactory = new ProviderFactory(customConfig);
      const customService = createCaptureAgentService(customFactory);
      
      const config = customService.getProviderConfig();
      expect(config.primary).toBe('openai');
    });
  });
});