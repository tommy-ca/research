import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { createEnhancedCaptureAgent, EnhancedCaptureAgentService } from '../../src/agents/enhanced-capture-agent.js';
import { ProviderConfig } from '../../src/providers/provider-factory.js';

// Mock Mastra Agent
const mockAgent = {
  generateVNext: vi.fn(),
  generate: vi.fn(),
  streamVNext: vi.fn(),
  stream: vi.fn(),
  tools: [
    { id: 'webContentExtractor', execute: vi.fn() },
    { id: 'qualityAssessment', execute: vi.fn() },
    { id: 'duplicateDetection', execute: vi.fn() },
  ],
};

vi.mock('@mastra/core', () => ({
  Agent: vi.fn().mockImplementation(() => mockAgent),
}));

// Mock the provider factory
vi.mock('../../src/providers/provider-factory.js', async () => {
  const actual = await vi.importActual('@/providers/provider-factory');
  return {
    ...actual,
    ProviderFactory: vi.fn().mockImplementation(() => ({
      createModel: vi.fn().mockResolvedValue({ model: 'test-model', provider: 'test' }),
      getMetrics: vi.fn().mockReturnValue({
        subscriptionUsage: { remaining: 100, resetDate: new Date(), provider: 'claude-pro' },
        fallbackCosts: { openai: 0, anthropic: 0 },
        routingDecisions: [],
      }),
      updateConfig: vi.fn(),
      getConfig: vi.fn().mockReturnValue({
        primary: 'claude-code',
        fallbacks: ['openai', 'anthropic'],
        models: {
          'claude-code': 'claude-3-5-sonnet-20241022',
          'openai': 'gpt-4o-mini',
          'anthropic': 'claude-3-haiku-20240307',
        },
        subscriptionBased: true,
        costOptimization: true,
        enableFallback: true,
      }),
      testProvider: vi.fn().mockResolvedValue(true),
      getAvailableProviders: vi.fn().mockReturnValue(['claude-code', 'openai', 'anthropic']),
    })),
  };
});

describe('Enhanced Capture Agent with Provider Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Agent Creation', () => {
    test('should create agent with default provider configuration', async () => {
      const agent = await createEnhancedCaptureAgent();
      
      expect(agent).toBeDefined();
      expect(vi.mocked(vi.importActual).mock.calls).toHaveLength(0);
    });

    test('should create agent with custom provider configuration', async () => {
      const customConfig: Partial<ProviderConfig> = {
        primary: 'openai',
        fallbacks: ['anthropic'],
        costOptimization: false,
      };

      const agent = await createEnhancedCaptureAgent(customConfig);
      
      expect(agent).toBeDefined();
    });

    test('should handle agent creation failure gracefully', async () => {
      // Mock provider factory to fail
      const { ProviderFactory } = await import('../../src/providers/provider-factory.js');
      const mockFactory = vi.mocked(ProviderFactory);
      mockFactory.mockImplementation(() => ({
        createModel: vi.fn().mockRejectedValue(new Error('Provider creation failed')),
      } as any));

      await expect(createEnhancedCaptureAgent()).rejects.toThrow('Provider creation failed');
    });
  });

  describe('EnhancedCaptureAgentService', () => {
    let service: EnhancedCaptureAgentService;

    beforeEach(() => {
      service = new EnhancedCaptureAgentService();
    });

    describe('Constructor and Initialization', () => {
      test('should initialize with default provider configuration', () => {
        expect(service).toBeInstanceOf(EnhancedCaptureAgentService);
      });

      test('should initialize with custom provider configuration', () => {
        const customConfig: Partial<ProviderConfig> = {
          primary: 'openai',
          enableFallback: false,
        };

        const customService = new EnhancedCaptureAgentService(customConfig);
        expect(customService).toBeInstanceOf(EnhancedCaptureAgentService);
      });
    });

    describe('Response Generation', () => {
      const testMessages = [
        { role: 'user', content: 'Capture this content for PKM system' }
      ];

      test('should generate response using generateVNext', async () => {
        const mockResponse = { text: 'Generated response', usage: { tokens: 100 } };
        mockAgent.generateVNext.mockResolvedValueOnce(mockResponse);

        const result = await service.generateResponse(testMessages);

        expect(mockAgent.generateVNext).toHaveBeenCalledWith({ messages: testMessages });
        expect(result).toEqual(mockResponse);
      });

      test('should fallback to generate when generateVNext fails', async () => {
        const mockResponse = { text: 'Fallback response', usage: { tokens: 100 } };
        mockAgent.generateVNext.mockRejectedValueOnce(new Error('generateVNext failed'));
        mockAgent.generate.mockResolvedValueOnce(mockResponse);

        const result = await service.generateResponse(testMessages);

        expect(mockAgent.generateVNext).toHaveBeenCalled();
        expect(mockAgent.generate).toHaveBeenCalledWith({ messages: testMessages });
        expect(result).toEqual(mockResponse);
      });

      test('should throw error when both generateVNext and generate fail', async () => {
        mockAgent.generateVNext.mockRejectedValueOnce(new Error('generateVNext failed'));
        mockAgent.generate.mockRejectedValueOnce(new Error('generate failed'));

        await expect(service.generateResponse(testMessages)).rejects.toThrow('Enhanced capture agent failed');
      });
    });

    describe('Structured Output Generation', () => {
      const testMessages = [
        { role: 'user', content: 'Extract structured data from this content' }
      ];
      const testSchema = {
        title: 'string',
        summary: 'string',
        tags: 'array',
      };

      test('should generate structured output using generateVNext', async () => {
        const mockResponse = {
          object: { title: 'Test Title', summary: 'Test Summary', tags: ['tag1', 'tag2'] }
        };
        mockAgent.generateVNext.mockResolvedValueOnce(mockResponse);

        const result = await service.generateStructuredOutput(testMessages, testSchema);

        expect(mockAgent.generateVNext).toHaveBeenCalledWith({
          messages: testMessages,
          schema: expect.any(Object), // Zod schema
        });
        expect(result).toEqual(mockResponse);
      });

      test('should fallback to generate for structured output', async () => {
        const mockResponse = {
          object: { title: 'Fallback Title', summary: 'Fallback Summary', tags: ['fallback'] }
        };
        mockAgent.generateVNext.mockRejectedValueOnce(new Error('generateVNext failed'));
        mockAgent.generate.mockResolvedValueOnce(mockResponse);

        const result = await service.generateStructuredOutput(testMessages, testSchema);

        expect(mockAgent.generate).toHaveBeenCalled();
        expect(result).toEqual(mockResponse);
      });

      test('should handle schema conversion correctly', async () => {
        const complexSchema = {
          title: 'string',
          count: 'number',
          isActive: 'boolean',
          metadata: 'object',
          items: 'array',
        };

        mockAgent.generateVNext.mockResolvedValueOnce({ object: {} });

        await service.generateStructuredOutput(testMessages, complexSchema);

        const callArgs = mockAgent.generateVNext.mock.calls[0][0];
        expect(callArgs.schema).toBeDefined();
        expect(typeof callArgs.schema.parse).toBe('function'); // Should be Zod schema
      });
    });

    describe('Streaming Responses', () => {
      const testMessages = [
        { role: 'user', content: 'Stream this long content processing' }
      ];

      test('should stream response using streamVNext', async () => {
        const mockStream = { stream: 'data' };
        mockAgent.streamVNext.mockResolvedValueOnce(mockStream);

        const result = await service.streamResponse(testMessages);

        expect(mockAgent.streamVNext).toHaveBeenCalledWith({ messages: testMessages });
        expect(result).toEqual(mockStream);
      });

      test('should fallback to stream when streamVNext fails', async () => {
        const mockStream = { stream: 'fallback data' };
        mockAgent.streamVNext.mockRejectedValueOnce(new Error('streamVNext failed'));
        mockAgent.stream.mockResolvedValueOnce(mockStream);

        const result = await service.streamResponse(testMessages);

        expect(mockAgent.stream).toHaveBeenCalledWith({ messages: testMessages });
        expect(result).toEqual(mockStream);
      });
    });

    describe('Multimodal Content Processing', () => {
      test('should process text-only messages', async () => {
        const textMessages = [
          { role: 'user', content: 'Analyze this text content' }
        ];
        
        mockAgent.generateVNext.mockResolvedValueOnce({ text: 'Analysis complete' });

        const result = await service.processMultimodalContent(textMessages);

        expect(mockAgent.generateVNext).toHaveBeenCalledWith({ messages: textMessages });
        expect(result.text).toBe('Analysis complete');
      });

      test('should process multimodal messages with images', async () => {
        const multimodalMessages = [
          {
            role: 'user',
            content: [
              { type: 'text', text: 'Analyze this image' },
              { type: 'image', image: 'base64-image-data' },
            ]
          }
        ];

        mockAgent.generateVNext.mockResolvedValueOnce({ text: 'Image analysis complete' });

        const result = await service.processMultimodalContent(multimodalMessages);

        expect(mockAgent.generateVNext).toHaveBeenCalled();
        const callArgs = mockAgent.generateVNext.mock.calls[0][0];
        
        // Should process image content
        const processedContent = callArgs.messages[0].content;
        expect(Array.isArray(processedContent)).toBe(true);
        expect(processedContent[1].type).toBe('image');
      });

      test('should add default text to images without text', async () => {
        const imageMessages = [
          {
            role: 'user',
            content: [
              { type: 'image', image: 'base64-image-data' }
            ]
          }
        ];

        mockAgent.generateVNext.mockResolvedValueOnce({ text: 'Default image analysis' });

        await service.processMultimodalContent(imageMessages);

        const callArgs = mockAgent.generateVNext.mock.calls[0][0];
        const imageItem = callArgs.messages[0].content[0];
        
        expect(imageItem.text).toBe('Analyze this image for content capture');
      });
    });

    describe('Tool Execution', () => {
      test('should execute available tools', async () => {
        const mockResult = { qualityScore: 0.8, assessment: 'High quality' };
        mockAgent.tools[1].execute.mockResolvedValueOnce(mockResult);

        const result = await service.executeTool('qualityAssessment', { content: 'test content' });

        expect(mockAgent.tools[1].execute).toHaveBeenCalledWith({ content: 'test content' });
        expect(result).toEqual(mockResult);
      });

      test('should throw error for non-existent tools', async () => {
        await expect(service.executeTool('nonExistentTool', {}))
          .rejects.toThrow('Tool nonExistentTool not found');
      });

      test('should throw error for non-executable tools', async () => {
        // Mock a tool without execute method
        const nonExecutableTool = { id: 'readOnlyTool' };
        mockAgent.tools.push(nonExecutableTool as any);

        await expect(service.executeTool('readOnlyTool', {}))
          .rejects.toThrow('Tool readOnlyTool is not executable');
      });
    });

    describe('Concurrent Request Processing', () => {
      test('should process multiple requests concurrently', async () => {
        const requests = [
          { messages: [{ role: 'user', content: 'Request 1' }] },
          { messages: [{ role: 'user', content: 'Request 2' }] },
          { messages: [{ role: 'user', content: 'Request 3' }] },
        ];

        const mockResponses = [
          { text: 'Response 1' },
          { text: 'Response 2' },
          { text: 'Response 3' },
        ];

        mockAgent.generateVNext
          .mockResolvedValueOnce(mockResponses[0])
          .mockResolvedValueOnce(mockResponses[1])
          .mockResolvedValueOnce(mockResponses[2]);

        const results = await service.processConcurrentRequests(requests);

        expect(results).toHaveLength(3);
        expect(results).toEqual(mockResponses);
        expect(mockAgent.generateVNext).toHaveBeenCalledTimes(3);
      });

      test('should handle mixed success/failure in concurrent requests', async () => {
        const requests = [
          { messages: [{ role: 'user', content: 'Success request' }] },
          { messages: [{ role: 'user', content: 'Failure request' }] },
        ];

        mockAgent.generateVNext
          .mockResolvedValueOnce({ text: 'Success' })
          .mockRejectedValueOnce(new Error('generateVNext failed'));
        
        mockAgent.generate
          .mockResolvedValueOnce({ text: 'Fallback success' });

        const results = await service.processConcurrentRequests(requests);

        expect(results).toHaveLength(2);
        expect(results[0].text).toBe('Success');
        expect(results[1].text).toBe('Fallback success');
      });
    });

    describe('Provider Management', () => {
      test('should get provider metrics', () => {
        const metrics = service.getProviderMetrics();

        expect(metrics).toBeDefined();
        expect(metrics.subscriptionUsage).toBeDefined();
        expect(metrics.fallbackCosts).toBeDefined();
        expect(metrics.routingDecisions).toBeDefined();
      });

      test('should update provider configuration', () => {
        const newConfig: Partial<ProviderConfig> = {
          primary: 'anthropic',
          costOptimization: false,
        };

        service.updateProviderConfig(newConfig);

        // Should recreate agent with new configuration
        expect(service).toBeDefined(); // Agent promise should be updated
      });

      test('should get current provider configuration', () => {
        const config = service.getProviderConfig();

        expect(config).toBeDefined();
        expect(config.primary).toBe('claude-code');
        expect(config.fallbacks).toContain('openai');
      });

      test('should test provider availability', async () => {
        const isAvailable = await service.testProvider('openai');
        expect(isAvailable).toBe(true);
      });

      test('should get available providers', () => {
        const providers = service.getAvailableProviders();
        expect(providers).toEqual(['claude-code', 'openai', 'anthropic']);
      });

      test('should get agent instance', async () => {
        const agent = await service.getAgent();
        expect(agent).toBeDefined();
        expect(agent).toBe(mockAgent);
      });
    });

    describe('Error Handling', () => {
      test('should handle agent creation errors', async () => {
        const { ProviderFactory } = await import('../../src/providers/provider-factory.js');
        const mockFactory = vi.mocked(ProviderFactory);
        
        // Mock factory to fail on model creation
        mockFactory.mockImplementation(() => ({
          createModel: vi.fn().mockRejectedValue(new Error('Model creation failed')),
          getMetrics: vi.fn(),
          updateConfig: vi.fn(),
          getConfig: vi.fn(),
          testProvider: vi.fn(),
          getAvailableProviders: vi.fn(),
        } as any));

        const service = new EnhancedCaptureAgentService();

        await expect(service.generateResponse([{ role: 'user', content: 'test' }]))
          .rejects.toThrow('Model creation failed');
      });

      test('should provide meaningful error messages', async () => {
        mockAgent.generateVNext.mockRejectedValueOnce(new Error('Network timeout'));
        mockAgent.generate.mockRejectedValueOnce(new Error('API limit exceeded'));

        await expect(service.generateResponse([{ role: 'user', content: 'test' }]))
          .rejects.toThrow('Enhanced capture agent failed: Network timeout');
      });
    });

    describe('Provider Integration Compliance', () => {
      test('should maintain API compatibility with existing tests', async () => {
        // Verify that existing agent API still works
        const messages = [{ role: 'user', content: 'test' }];
        mockAgent.generateVNext.mockResolvedValueOnce({ text: 'response' });

        const result = await service.generateResponse(messages);

        expect(result.text).toBe('response');
      });

      test('should support provider-specific configurations', () => {
        const claudeConfig: Partial<ProviderConfig> = {
          primary: 'claude-code',
          subscriptionBased: true,
        };

        const claudeService = new EnhancedCaptureAgentService(claudeConfig);
        expect(claudeService).toBeInstanceOf(EnhancedCaptureAgentService);

        const openaiConfig: Partial<ProviderConfig> = {
          primary: 'openai',
          subscriptionBased: false,
        };

        const openaiService = new EnhancedCaptureAgentService(openaiConfig);
        expect(openaiService).toBeInstanceOf(EnhancedCaptureAgentService);
      });
    });
  });
});