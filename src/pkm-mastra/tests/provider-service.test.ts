/**
 * ProviderService TDD Tests - RED Phase
 * These tests MUST FAIL initially as ProviderService doesn't exist yet
 * Following TDD methodology: SPECS → RED → GREEN → REFACTOR
 */

import { describe, test, expect, beforeEach, vi } from 'vitest';
import { ProviderService } from '../src/services/provider-service.js';
import type { 
  ProviderContext, 
  ProviderSelection, 
  ProviderConfig, 
  ServiceDependencies,
  LLMProvider,
  ProviderMetrics
} from '../src/provider-types.js';

// Mock dependencies for isolated unit testing
const mockMetricsService = {
  recordSelection: vi.fn(),
  recordCreation: vi.fn(),
  recordFailure: vi.fn(),
  getMetrics: vi.fn().mockReturnValue({
    selections: 0,
    creations: 0,
    failures: 0,
    averageResponseTime: 0
  })
};

const mockLogger = {
  info: vi.fn(),
  warn: vi.fn(),
  error: vi.fn(),
  debug: vi.fn()
};

const mockProviderFactory = {
  createClaudeCodeProvider: vi.fn(),
  createOpenAIProvider: vi.fn(),
  createAnthropicProvider: vi.fn()
};

const mockDependencies: ServiceDependencies = {
  metricsService: mockMetricsService,
  logger: mockLogger,
  providerFactory: mockProviderFactory
};

const defaultConfig: ProviderConfig = {
  primary: 'claude-code',
  fallbacks: ['openai', 'anthropic'],
  models: {
    'claude-code': 'claude-3-5-sonnet-20241022',
    'openai': 'gpt-4o-mini',
    'anthropic': 'claude-3-haiku-20240307'
  },
  subscriptionBased: true,
  costOptimization: true,
  enableFallback: true,
  qualityThresholds: {
    high: 0.95,
    medium: 0.7,
    low: 0.5
  }
};

describe('ProviderService - TDD Cycle 1.1', () => {
  let service: ProviderService;

  beforeEach(() => {
    vi.clearAllMocks();
    // This constructor call WILL FAIL until we implement ProviderService
    service = new ProviderService(defaultConfig, mockDependencies);
  });

  describe('Provider Selection (FR-001, FR-002)', () => {
    test('RED: should select Opus for high quality requirements', async () => {
      // This test MUST FAIL initially - no ProviderService exists
      const context: ProviderContext = {
        qualityThreshold: 0.95,
        contentLength: 1000,
        contentType: 'research',
        urgency: 'normal'
      };

      const selection = await service.selectOptimalProvider(context);

      expect(selection.provider).toBe('claude-code');
      expect(selection.model).toBe('opus');
      expect(selection.rationale).toContain('High quality requirement');
      expect(selection.confidence).toBeGreaterThan(0.9);
      expect(selection.estimatedCost).toBeGreaterThan(0);
      expect(selection.estimatedTime).toBeGreaterThan(0);
    });

    test('RED: should select Sonnet for standard quality requirements', async () => {
      const context: ProviderContext = {
        qualityThreshold: 0.7,
        contentLength: 500,
        contentType: 'capture',
        urgency: 'normal'
      };

      const selection = await service.selectOptimalProvider(context);

      expect(selection.provider).toBe('claude-code');
      expect(selection.model).toBe('sonnet');
      expect(selection.rationale).toContain('Standard quality sufficient');
      expect(selection.confidence).toBeGreaterThan(0.7);
    });

    test('RED: should throw validation error for invalid context', async () => {
      const invalidContext = {
        qualityThreshold: -1, // Invalid
        contentLength: 0,     // Invalid
        contentType: 'invalid' as any, // Invalid
        urgency: 'extreme' as any      // Invalid
      };

      await expect(service.selectOptimalProvider(invalidContext))
        .rejects
        .toThrow('Invalid provider context');
    });

    test('RED: should consider urgency in selection', async () => {
      const urgentContext: ProviderContext = {
        qualityThreshold: 0.8,
        contentLength: 1000,
        contentType: 'processing',
        urgency: 'high'
      };

      const selection = await service.selectOptimalProvider(urgentContext);

      expect(selection.estimatedTime).toBeLessThan(5000); // Fast response required
      expect(selection.rationale).toContain('urgent');
    });
  });

  describe('Provider Creation (FR-003)', () => {
    test('RED: should create provider from selection', async () => {
      const selection: ProviderSelection = {
        provider: 'claude-code',
        model: 'sonnet',
        rationale: 'Standard quality',
        confidence: 0.85,
        estimatedCost: 0.01,
        estimatedTime: 2000
      };

      const mockProvider = { id: 'claude-sonnet', model: 'claude-3-5-sonnet-20241022' };
      mockProviderFactory.createClaudeCodeProvider.mockResolvedValueOnce(mockProvider);

      const provider = await service.createProvider(selection);

      expect(provider).toBe(mockProvider);
      expect(mockProviderFactory.createClaudeCodeProvider).toHaveBeenCalledWith('claude-3-5-sonnet-20241022');
      expect(mockMetricsService.recordCreation).toHaveBeenCalledWith({
        provider: 'claude-code',
        model: 'sonnet',
        success: true
      });
    });

    test('RED: should handle provider creation failure with fallback', async () => {
      const selection: ProviderSelection = {
        provider: 'claude-code',
        model: 'opus',
        rationale: 'High quality',
        confidence: 0.95,
        estimatedCost: 0.05,
        estimatedTime: 3000
      };

      // Primary provider fails
      mockProviderFactory.createClaudeCodeProvider.mockRejectedValueOnce(new Error('Rate limit'));
      
      // Fallback succeeds
      const fallbackProvider = { id: 'openai', model: 'gpt-4o-mini' };
      mockProviderFactory.createOpenAIProvider.mockResolvedValueOnce(fallbackProvider);

      const provider = await service.createProvider(selection);

      expect(provider).toBe(fallbackProvider);
      expect(mockMetricsService.recordFailure).toHaveBeenCalledWith({
        provider: 'claude-code',
        error: 'Rate limit',
        fallbackUsed: 'openai'
      });
    });

    test('RED: should throw error when all providers fail', async () => {
      const selection: ProviderSelection = {
        provider: 'claude-code',
        model: 'sonnet',
        rationale: 'Standard quality',
        confidence: 0.8,
        estimatedCost: 0.02,
        estimatedTime: 2500
      };

      // All providers fail
      mockProviderFactory.createClaudeCodeProvider.mockRejectedValueOnce(new Error('Claude failed'));
      mockProviderFactory.createOpenAIProvider.mockRejectedValueOnce(new Error('OpenAI failed'));
      mockProviderFactory.createAnthropicProvider.mockRejectedValueOnce(new Error('Anthropic failed'));

      await expect(service.createProvider(selection))
        .rejects
        .toThrow('All providers failed');
    });
  });

  describe('Configuration Management (FR-005)', () => {
    test('RED: should update configuration successfully', () => {
      const newConfig: Partial<ProviderConfig> = {
        primary: 'openai',
        enableFallback: false,
        qualityThresholds: {
          high: 0.98,
          medium: 0.8,
          low: 0.6
        }
      };

      service.updateConfig(newConfig);

      const updatedConfig = service.getConfig();
      expect(updatedConfig.primary).toBe('openai');
      expect(updatedConfig.enableFallback).toBe(false);
      expect(updatedConfig.qualityThresholds.high).toBe(0.98);
    });

    test('RED: should validate configuration on update', () => {
      const invalidConfig: Partial<ProviderConfig> = {
        primary: 'invalid-provider' as any,
        qualityThresholds: {
          high: 1.5, // Invalid: > 1.0
          medium: -0.1, // Invalid: < 0
          low: 0.8 // Invalid: > medium
        }
      };

      expect(() => service.updateConfig(invalidConfig))
        .toThrow('Invalid provider configuration');
    });

    test('RED: should get current configuration', () => {
      const config = service.getConfig();

      expect(config).toEqual(defaultConfig);
      expect(config).not.toBe(defaultConfig); // Should be a copy
    });
  });

  describe('Provider Metrics (FR-004)', () => {
    test('RED: should return provider metrics', () => {
      const expectedMetrics: ProviderMetrics = {
        selections: {
          total: 100,
          byProvider: { 'claude-code': 80, 'openai': 15, 'anthropic': 5 },
          byModel: { 'opus': 30, 'sonnet': 50, 'gpt-4o-mini': 15, 'haiku': 5 }
        },
        creations: {
          successful: 95,
          failed: 5,
          averageTime: 1500
        },
        fallbacks: {
          triggered: 8,
          successful: 7,
          failed: 1
        },
        performance: {
          averageSelectionTime: 50,
          averageCreationTime: 1500,
          p95SelectionTime: 100,
          p95CreationTime: 3000
        }
      };

      mockMetricsService.getMetrics.mockReturnValueOnce(expectedMetrics);

      const metrics = service.getMetrics();

      expect(metrics).toEqual(expectedMetrics);
      expect(mockMetricsService.getMetrics).toHaveBeenCalled();
    });

    test('RED: should record provider selection metrics', async () => {
      const context: ProviderContext = {
        qualityThreshold: 0.8,
        contentLength: 750,
        contentType: 'synthesis',
        urgency: 'normal'
      };

      await service.selectOptimalProvider(context);

      expect(mockMetricsService.recordSelection).toHaveBeenCalledWith({
        provider: expect.any(String),
        model: expect.any(String),
        selectionTime: expect.any(Number),
        confidence: expect.any(Number),
        context: context
      });
    });
  });

  describe('Provider Validation', () => {
    test('RED: should validate provider health', async () => {
      const mockProvider: LLMProvider = {
        id: 'claude-sonnet',
        model: 'claude-3-5-sonnet-20241022',
        generate: vi.fn(),
        stream: vi.fn()
      };

      const validation = await service.validateProvider(mockProvider);

      expect(validation.isHealthy).toBe(true);
      expect(validation.responseTime).toBeGreaterThan(0);
      expect(validation.errors).toHaveLength(0);
    });

    test('RED: should detect unhealthy provider', async () => {
      const mockProvider: LLMProvider = {
        id: 'failed-provider',
        model: 'failing-model',
        generate: vi.fn().mockRejectedValue(new Error('Provider unavailable')),
        stream: vi.fn()
      };

      const validation = await service.validateProvider(mockProvider);

      expect(validation.isHealthy).toBe(false);
      expect(validation.errors).toContain('Provider unavailable');
    });
  });

  describe('Available Providers', () => {
    test('RED: should return available providers in priority order', () => {
      const providers = service.getAvailableProviders();

      expect(providers).toEqual(['claude-code', 'openai', 'anthropic']);
      expect(providers[0]).toBe(defaultConfig.primary);
    });

    test('RED: should reflect configuration changes', () => {
      service.updateConfig({ 
        primary: 'openai', 
        fallbacks: ['anthropic', 'claude-code'] 
      });

      const providers = service.getAvailableProviders();

      expect(providers).toEqual(['openai', 'anthropic', 'claude-code']);
    });
  });
});

// Integration tests to verify SOLID principles compliance
describe('ProviderService - SOLID Principles Compliance', () => {
  test('RED: should allow strategy pattern for provider selection (OCP)', () => {
    // This tests Open/Closed Principle - extensible without modification
    const customStrategy = {
      select: vi.fn().mockReturnValue({
        provider: 'custom-provider',
        model: 'custom-model',
        rationale: 'Custom selection logic',
        confidence: 0.9,
        estimatedCost: 0.03,
        estimatedTime: 2000
      })
    };

    const serviceWithCustomStrategy = new ProviderService(
      defaultConfig, 
      mockDependencies,
      customStrategy
    );

    const context: ProviderContext = {
      qualityThreshold: 0.8,
      contentLength: 1000,
      contentType: 'research',
      urgency: 'normal'
    };

    // This should use the custom strategy
    const selection = serviceWithCustomStrategy.selectOptimalProvider(context);

    expect(customStrategy.select).toHaveBeenCalledWith(context);
  });

  test('RED: should maintain single responsibility (SRP)', () => {
    // ProviderService should only handle provider management
    // Metrics, logging, and factory concerns are injected dependencies
    
    const service = new ProviderService(defaultConfig, mockDependencies);

    // Service should not have methods for concerns outside provider management
    expect(service.logMessage).toBeUndefined();
    expect(service.calculateMetrics).toBeUndefined();
    expect(service.createDatabase).toBeUndefined();
    
    // Should only have provider-related methods
    expect(service.selectOptimalProvider).toBeDefined();
    expect(service.createProvider).toBeDefined();
    expect(service.updateConfig).toBeDefined();
    expect(service.getMetrics).toBeDefined();
    expect(service.validateProvider).toBeDefined();
  });
});

/**
 * Expected Test Results (RED Phase):
 * 
 * ❌ All tests should FAIL with "Cannot find module './provider-service.js'"
 * ❌ ProviderService constructor not found
 * ❌ selectOptimalProvider method not implemented  
 * ❌ createProvider method not implemented
 * ❌ updateConfig method not implemented
 * ❌ getMetrics method not implemented
 * ❌ validateProvider method not implemented
 * ❌ getAvailableProviders method not implemented
 * 
 * This is EXPECTED and CORRECT for TDD RED phase.
 * Next step: GREEN phase - implement minimal code to pass tests.
 */