import { describe, test, expect, vi, beforeEach, afterEach } from 'vitest';
import { ProviderFactory, ProviderConfig, ProviderError } from '../../src/providers/provider-factory.js';
import { ModelSelector, TaskType, TaskContext } from '../../src/providers/model-selector.js';

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

describe('ProviderFactory Enhanced Claude Integration', () => {
  let factory: ProviderFactory;
  let mockConfig: ProviderConfig;
  let mockModelSelector: ModelSelector;

  beforeEach(() => {
    mockConfig = {
      primary: 'claude-code',
      fallbacks: ['openai', 'anthropic'],
      models: {
        'claude-code': 'claude-3-5-sonnet-20241022',
        'claude-code-opus': 'claude-3-opus-20240229',
        'openai': 'gpt-4o-mini',
        'anthropic': 'claude-3-haiku-20240307',
      },
      subscriptionBased: true,
      costOptimization: true,
      enableFallback: true,
    };
    
    mockModelSelector = {
      selectModel: vi.fn(),
      getSelectionReasoning: vi.fn(),
    } as any;
    
    factory = new ProviderFactory(mockConfig, mockModelSelector);
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Model Selection Integration', () => {
    // TS-005: Sonnet Model Creation
    test('should create sonnet model when selector chooses sonnet', async () => {
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('sonnet');
      
      const model = await factory.createModelWithSelection(
        'content-capture',
        'Simple note content'
      );
      
      expect(mockModelSelector.selectModel).toHaveBeenCalledWith(
        'content-capture',
        'Simple note content',
        expect.any(Object)
      );
      expect(model).toEqual({
        model: 'claude-3-5-sonnet-20241022',
        provider: 'claude-code'
      });
    });

    // TS-006: Opus Model Creation
    test('should create opus model when selector chooses opus', async () => {
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('opus');
      
      const model = await factory.createModelWithSelection(
        'research-analysis',
        'Complex research data to analyze'
      );
      
      expect(mockModelSelector.selectModel).toHaveBeenCalledWith(
        'research-analysis',
        'Complex research data to analyze',
        expect.any(Object)
      );
      expect(model).toEqual({
        model: 'claude-3-opus-20240229',
        provider: 'claude-code'
      });
    });

    test('should pass context to model selector', async () => {
      const context: TaskContext = {
        qualityRequirement: 0.98,
        maxResponseTime: 5000,
      };
      
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('opus');
      
      await factory.createModelWithSelection(
        'quality-assessment',
        'Assess quality of research',
        context
      );
      
      expect(mockModelSelector.selectModel).toHaveBeenCalledWith(
        'quality-assessment',
        'Assess quality of research',
        context
      );
    });

    test('should handle direct model specification override', async () => {
      // When model is explicitly specified, skip selector
      const model = await factory.createModel('claude-code', 'opus');
      
      expect(mockModelSelector.selectModel).not.toHaveBeenCalled();
      expect(model).toEqual({
        model: 'claude-3-opus-20240229',
        provider: 'claude-code'
      });
    });
  });

  describe('Claude Code Provider Model Variants', () => {
    test('should support explicit sonnet model creation', async () => {
      const model = await factory.createModel('claude-code', 'sonnet');
      
      expect(model).toEqual({
        model: 'claude-3-5-sonnet-20241022',
        provider: 'claude-code'
      });
    });

    test('should support explicit opus model creation', async () => {
      const model = await factory.createModel('claude-code', 'opus');
      
      expect(model).toEqual({
        model: 'claude-3-opus-20240229',
        provider: 'claude-code'
      });
    });

    test('should default to sonnet when no model specified', async () => {
      const model = await factory.createModel('claude-code');
      
      expect(model).toEqual({
        model: 'claude-3-5-sonnet-20241022',
        provider: 'claude-code'
      });
    });

    test('should throw error for unsupported model variant', async () => {
      await expect(factory.createModel('claude-code', 'invalid-model')).rejects.toThrow(
        'Unsupported Claude model variant: invalid-model'
      );
    });
  });

  describe('Fallback with Model Selection', () => {
    // TS-007: Opus to Sonnet Fallback
    test('should fallback from opus to sonnet when opus unavailable', async () => {
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('opus');
      
      // Mock Opus model creation failure
      vi.doMock('ai-sdk-provider-claude-code', () => {
        const claudeCode = vi.fn((model: string) => {
          if (model.includes('opus')) {
            throw new Error('Opus model not available');
          }
          return { model, provider: 'claude-code' };
        });
        return { claudeCode };
      });
      
      const model = await factory.createModelWithSelection(
        'research-analysis',
        'Research content'
      );
      
      // Should fallback to Sonnet
      expect(model).toEqual({
        model: 'claude-3-5-sonnet-20241022',
        provider: 'claude-code'
      });
      
      // Should log fallback decision
      const metrics = factory.getMetrics();
      const fallbackDecision = metrics.routingDecisions.find(
        d => d.reason === 'fallback'
      );
      expect(fallbackDecision).toBeDefined();
      expect(fallbackDecision?.provider).toBe('claude-code');
    });

    test('should fallback from sonnet to opus when sonnet unavailable', async () => {
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('sonnet');
      
      // Mock Sonnet model creation failure
      vi.doMock('ai-sdk-provider-claude-code', () => {
        const claudeCode = vi.fn((model: string) => {
          if (model.includes('sonnet')) {
            throw new Error('Sonnet model not available');
          }
          return { model, provider: 'claude-code' };
        });
        return { claudeCode };
      });
      
      const model = await factory.createModelWithSelection(
        'content-capture',
        'Simple content'
      );
      
      // Should fallback to Opus
      expect(model).toEqual({
        model: 'claude-3-opus-20240229',
        provider: 'claude-code'
      });
    });

    // TS-008: Complete Fallback Chain
    test('should fallback to external providers when both claude models fail', async () => {
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('opus');
      
      // Mock all Claude Code models to fail
      vi.doMock('ai-sdk-provider-claude-code', () => {
        throw new Error('Claude Code provider not available');
      });
      
      const model = await factory.createModelWithSelection(
        'research-analysis',
        'Research content'
      );
      
      // Should fallback to first external provider (OpenAI)
      expect(model).toEqual({
        model: 'gpt-4o-mini',
        provider: 'openai'
      });
      
      // Should log fallback decision
      const metrics = factory.getMetrics();
      const fallbackDecision = metrics.routingDecisions.find(
        d => d.reason === 'fallback'
      );
      expect(fallbackDecision?.provider).toBe('openai');
    });
  });

  describe('Configuration Validation', () => {
    // TS-009: Custom Selection Rules
    test('should accept custom model selector in configuration', () => {
      const customSelector = {
        selectModel: vi.fn().mockReturnValue('sonnet'),
        getSelectionReasoning: vi.fn(),
      } as any;
      
      const customFactory = new ProviderFactory(mockConfig, customSelector);
      
      expect(customFactory.getModelSelector()).toBe(customSelector);
    });

    // TS-010: Invalid Configuration Handling  
    test('should throw validation error for missing opus model configuration', () => {
      const invalidConfig = {
        ...mockConfig,
        models: {
          'claude-code': 'claude-3-5-sonnet-20241022',
          // Missing claude-code-opus configuration
        },
      };
      
      expect(() => {
        new ProviderFactory(invalidConfig, mockModelSelector);
      }).toThrow('Missing Claude Opus model configuration');
    });

    test('should validate model selector interface', () => {
      const invalidSelector = {
        // Missing required methods
        selectModel: undefined,
        getSelectionReasoning: vi.fn(),
      };
      
      expect(() => {
        new ProviderFactory(mockConfig, invalidSelector as any);
      }).toThrow('Invalid model selector: missing selectModel method');
    });
  });

  describe('Metrics and Logging', () => {
    test('should log model selection decisions', async () => {
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('opus');
      vi.mocked(mockModelSelector.getSelectionReasoning).mockReturnValue({
        selectedModel: 'opus',
        reasons: ['High quality analysis required'],
        confidence: 0.95,
        fallbackApplied: false,
      });
      
      await factory.createModelWithSelection(
        'research-analysis',
        'Complex research data'
      );
      
      const metrics = factory.getMetrics();
      const decision = metrics.routingDecisions[metrics.routingDecisions.length - 1];
      
      expect(decision.provider).toBe('claude-code');
      expect(decision.reason).toBe('selection');
      expect(decision.metadata).toEqual({
        selectedModel: 'opus',
        reasoning: ['High quality analysis required'],
        confidence: 0.95,
      });
    });

    test('should track selection confidence over time', async () => {
      const selections = [
        { model: 'sonnet', confidence: 0.8 },
        { model: 'opus', confidence: 0.95 },
        { model: 'sonnet', confidence: 0.9 },
      ];
      
      for (const selection of selections) {
        vi.mocked(mockModelSelector.selectModel).mockReturnValue(selection.model as any);
        vi.mocked(mockModelSelector.getSelectionReasoning).mockReturnValue({
          selectedModel: selection.model as any,
          reasons: ['Test reason'],
          confidence: selection.confidence,
          fallbackApplied: false,
        });
        
        await factory.createModelWithSelection('test-task' as TaskType, 'test content');
      }
      
      const metrics = factory.getMetrics();
      const avgConfidence = metrics.routingDecisions
        .map(d => d.metadata?.confidence || 0)
        .reduce((sum, conf) => sum + conf, 0) / metrics.routingDecisions.length;
        
      expect(avgConfidence).toBeCloseTo(0.88, 1);
    });
  });

  describe('Error Scenarios', () => {
    test('should handle model selector errors gracefully', async () => {
      vi.mocked(mockModelSelector.selectModel).mockImplementation(() => {
        throw new Error('Model selection failed');
      });
      
      // Should fallback to default behavior (primary provider)
      const model = await factory.createModelWithSelection(
        'content-capture',
        'Simple content'
      );
      
      expect(model).toEqual({
        model: 'claude-3-5-sonnet-20241022',
        provider: 'claude-code'
      });
    });

    test('should handle empty content gracefully', async () => {
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('sonnet');
      
      const model = await factory.createModelWithSelection(
        'content-capture',
        ''
      );
      
      expect(mockModelSelector.selectModel).toHaveBeenCalledWith(
        'content-capture',
        '',
        expect.any(Object)
      );
      expect(model).toBeDefined();
    });

    test('should handle invalid task type with default selection', async () => {
      vi.mocked(mockModelSelector.selectModel).mockReturnValue('sonnet');
      
      const model = await factory.createModelWithSelection(
        'invalid-task' as TaskType,
        'Some content'
      );
      
      expect(model).toEqual({
        model: 'claude-3-5-sonnet-20241022',
        provider: 'claude-code'
      });
    });
  });
});