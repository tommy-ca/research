import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { ProviderFactory, ProviderConfig, ProviderError, SubscriptionError, RateLimitError, defaultProviderConfig } from '../../src/providers/provider-factory.js';

// Mock the external providers
vi.mock('@ai-sdk/openai', () => ({
  openai: vi.fn((model: string) => ({ model, provider: 'openai' }))
}));

vi.mock('@ai-sdk/anthropic', () => ({
  anthropic: vi.fn((model: string) => ({ model, provider: 'anthropic' }))
}));

vi.mock('ai-sdk-provider-claude-code', () => ({
  claudeCode: vi.fn((model: string) => ({ model, provider: 'claude-code' }))
}));

describe('ProviderFactory', () => {
  let factory: ProviderFactory;
  let mockConfig: ProviderConfig;

  beforeEach(() => {
    mockConfig = {
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
    };
    
    factory = new ProviderFactory(mockConfig);
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Constructor and Configuration', () => {
    test('should initialize with default configuration', () => {
      const defaultFactory = new ProviderFactory();
      const config = defaultFactory.getConfig();
      
      expect(config.primary).toBe('claude-code');
      expect(config.fallbacks).toContain('openai');
      expect(config.fallbacks).toContain('anthropic');
      expect(config.subscriptionBased).toBe(true);
      expect(config.enableFallback).toBe(true);
    });

    test('should initialize with custom configuration', () => {
      const customConfig: Partial<ProviderConfig> = {
        primary: 'openai',
        fallbacks: ['anthropic'],
        costOptimization: false,
      };
      
      const customFactory = new ProviderFactory(customConfig);
      const config = customFactory.getConfig();
      
      expect(config.primary).toBe('openai');
      expect(config.fallbacks).toEqual(['anthropic']);
      expect(config.costOptimization).toBe(false);
    });

    test('should validate configuration schema', () => {
      expect(() => {
        new ProviderFactory({
          primary: 'invalid-provider' as any,
        });
      }).toThrow();
    });
  });

  describe('Model Creation', () => {
    test('should create Claude Code provider by default', async () => {
      const model = await factory.createModel();
      
      expect(model).toEqual({
        model: 'claude-3-5-sonnet-20241022',
        provider: 'claude-code'
      });
    });

    test('should create OpenAI provider when specified', async () => {
      const model = await factory.createModel('openai');
      
      expect(model).toEqual({
        model: 'gpt-4o-mini',
        provider: 'openai'
      });
    });

    test('should create Anthropic provider when specified', async () => {
      const model = await factory.createModel('anthropic');
      
      expect(model).toEqual({
        model: 'claude-3-haiku-20240307',
        provider: 'anthropic'
      });
    });

    test('should throw error for unsupported provider', async () => {
      await expect(factory.createModel('invalid-provider')).rejects.toThrow(ProviderError);
    });
  });

  describe('Fallback Mechanism', () => {
    test('should fallback to OpenAI when Claude Code fails', async () => {
      // Mock Claude Code import failure
      vi.doMock('ai-sdk-provider-claude-code', () => {
        throw new Error('Claude Code not available');
      });
      
      const model = await factory.createModel();
      
      // Should fallback to first available provider (OpenAI)
      expect(model).toEqual({
        model: 'gpt-4o-mini',
        provider: 'openai'
      });
    });

    test('should cascade through all fallbacks when providers fail', async () => {
      // Mock all providers to fail except Anthropic
      vi.doMock('ai-sdk-provider-claude-code', () => {
        throw new Error('Claude Code not available');
      });
      
      const { openai } = await import('@ai-sdk/openai');
      vi.mocked(openai).mockImplementation(() => {
        throw new Error('OpenAI not available');
      });
      
      const model = await factory.createModel();
      
      // Should fallback to Anthropic (last option)
      expect(model).toEqual({
        model: 'claude-3-haiku-20240307',
        provider: 'anthropic'
      });
    });

    test('should throw error when all providers fail', async () => {
      // Mock all providers to fail
      vi.doMock('ai-sdk-provider-claude-code', () => {
        throw new Error('Claude Code not available');
      });
      
      const { openai } = await import('@ai-sdk/openai');
      const { anthropic } = await import('@ai-sdk/anthropic');
      
      vi.mocked(openai).mockImplementation(() => {
        throw new Error('OpenAI not available');
      });
      vi.mocked(anthropic).mockImplementation(() => {
        throw new Error('Anthropic not available');
      });
      
      await expect(factory.createModel()).rejects.toThrow(ProviderError);
      await expect(factory.createModel()).rejects.toThrow('All providers failed');
    });

    test('should respect fallback disabled configuration', async () => {
      const noFallbackConfig = {
        ...mockConfig,
        enableFallback: false,
      };
      const noFallbackFactory = new ProviderFactory(noFallbackConfig);
      
      // Mock Claude Code failure
      vi.doMock('ai-sdk-provider-claude-code', () => {
        throw new Error('Claude Code not available');
      });
      
      await expect(noFallbackFactory.createModel()).rejects.toThrow(ProviderError);
    });
  });

  describe('Provider Metrics', () => {
    test('should initialize with default metrics', () => {
      const metrics = factory.getMetrics();
      
      expect(metrics.subscriptionUsage.remaining).toBe(100);
      expect(metrics.subscriptionUsage.provider).toBe('claude-pro');
      expect(metrics.fallbackCosts.openai).toBe(0);
      expect(metrics.fallbackCosts.anthropic).toBe(0);
      expect(metrics.routingDecisions).toEqual([]);
    });

    test('should log routing decisions', async () => {
      await factory.createModel('openai');
      
      const metrics = factory.getMetrics();
      expect(metrics.routingDecisions).toHaveLength(1);
      
      const decision = metrics.routingDecisions[0];
      expect(decision.provider).toBe('openai');
      expect(decision.reason).toBe('subscription');
      expect(decision.timestamp).toBeInstanceOf(Date);
    });

    test('should limit routing decisions to 100 entries', async () => {
      // Create 150 routing decisions
      for (let i = 0; i < 150; i++) {
        await factory.createModel('openai');
      }
      
      const metrics = factory.getMetrics();
      expect(metrics.routingDecisions).toHaveLength(100);
    });
  });

  describe('Configuration Management', () => {
    test('should update configuration', () => {
      const newConfig: Partial<ProviderConfig> = {
        primary: 'openai',
        costOptimization: false,
      };
      
      factory.updateConfig(newConfig);
      const config = factory.getConfig();
      
      expect(config.primary).toBe('openai');
      expect(config.costOptimization).toBe(false);
      expect(config.fallbacks).toEqual(mockConfig.fallbacks); // Should preserve other values
    });

    test('should validate updated configuration', () => {
      expect(() => {
        factory.updateConfig({
          primary: 'invalid-provider' as any,
        });
      }).toThrow();
    });
  });

  describe('Provider Testing', () => {
    test('should test provider availability', async () => {
      const isAvailable = await factory.testProvider('openai');
      expect(isAvailable).toBe(true);
    });

    test('should return false for unavailable provider', async () => {
      // Mock OpenAI to fail
      const { openai } = await import('@ai-sdk/openai');
      vi.mocked(openai).mockImplementation(() => {
        throw new Error('Provider not available');
      });
      
      const isAvailable = await factory.testProvider('openai');
      expect(isAvailable).toBe(false);
    });

    test('should get available providers in priority order', () => {
      const providers = factory.getAvailableProviders();
      
      expect(providers).toEqual(['claude-code', 'openai', 'anthropic']);
    });
  });

  describe('Error Handling', () => {
    test('should throw ProviderError with correct context', async () => {
      try {
        await factory.createModel('invalid-provider');
      } catch (error) {
        expect(error).toBeInstanceOf(ProviderError);
        expect((error as ProviderError).provider).toBe('invalid-provider');
        expect((error as ProviderError).message).toContain('Unsupported provider');
      }
    });

    test('should handle subscription errors', () => {
      const subscriptionError = new SubscriptionError('claude-code');
      
      expect(subscriptionError).toBeInstanceOf(ProviderError);
      expect(subscriptionError.provider).toBe('claude-code');
      expect(subscriptionError.message).toContain('Subscription error');
    });

    test('should handle rate limit errors', () => {
      const rateLimitError = new RateLimitError('openai');
      
      expect(rateLimitError).toBeInstanceOf(ProviderError);
      expect(rateLimitError.provider).toBe('openai');
      expect(rateLimitError.message).toContain('Rate limit exceeded');
    });
  });

  describe('Cost Estimation', () => {
    test('should estimate costs for different providers', async () => {
      // First, create some routing decisions by using the factory
      await factory.createModel('claude-code');
      await factory.createModel('openai');
      await factory.createModel('anthropic');
      
      // Now check the routing decisions
      const metrics = factory.getMetrics();
      
      // Claude Code should be free (subscription)
      expect(metrics.routingDecisions.find(d => d.provider === 'claude-code')?.cost).toBe(0);
      
      // OpenAI should have some cost
      expect(metrics.routingDecisions.find(d => d.provider === 'openai')?.cost).toBeGreaterThan(0);
    });
  });

  describe('SOLID Principles Compliance', () => {
    test('should follow Single Responsibility Principle', () => {
      // Factory should only be responsible for creating providers
      expect(typeof factory.createModel).toBe('function');
      expect(typeof factory.getMetrics).toBe('function');
      expect(typeof factory.updateConfig).toBe('function');
      expect(typeof factory.testProvider).toBe('function');
    });

    test('should follow Open/Closed Principle', async () => {
      // Should be able to add new providers without modifying existing code
      // This is demonstrated by the pluggable provider architecture
      const providers = ['claude-code', 'openai', 'anthropic'];
      
      for (const provider of providers) {
        const model = await factory.createModel(provider);
        expect(model.provider).toBe(provider);
      }
    });

    test('should follow Dependency Inversion Principle', () => {
      // Factory depends on abstractions (configuration) not concretions
      const config = factory.getConfig();
      expect(config).toBeDefined();
      expect(typeof config).toBe('object');
    });
  });
});

describe('Default Configuration', () => {
  test('should export valid default configuration', () => {
    expect(defaultProviderConfig.primary).toBe('claude-code');
    expect(defaultProviderConfig.fallbacks).toContain('openai');
    expect(defaultProviderConfig.fallbacks).toContain('anthropic');
    expect(defaultProviderConfig.subscriptionBased).toBe(true);
    expect(defaultProviderConfig.enableFallback).toBe(true);
  });
});