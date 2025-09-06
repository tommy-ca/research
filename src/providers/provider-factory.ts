/**
 * Enhanced ProviderFactory with intelligent Claude Sonnet/Opus model selection
 * Following SOLID principles with dependency injection and single responsibility
 */

import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';
import { ModelSelector, ModelType, TaskType, TaskContext, defaultModelSelectionRules } from './model-selector.js';

// Provider configuration schema (DRY: Centralized configuration)
export const ProviderConfigSchema = z.object({
  primary: z.enum(['claude-code', 'openai', 'anthropic']).default('claude-code'),
  fallbacks: z.array(z.enum(['claude-code', 'openai', 'anthropic'])).default(['openai', 'anthropic']),
  models: z.object({
    'claude-code': z.string().default('claude-3-5-sonnet-20241022'),
    'claude-code-opus': z.string().default('claude-3-opus-20240229'),
    'openai': z.string().default('gpt-4o-mini'),
    'anthropic': z.string().default('claude-3-haiku-20240307'),
  }).default({
    'claude-code': 'claude-3-5-sonnet-20241022',
    'claude-code-opus': 'claude-3-opus-20240229',
    'openai': 'gpt-4o-mini',
    'anthropic': 'claude-3-haiku-20240307',
  }),
  subscriptionBased: z.boolean().default(true),
  costOptimization: z.boolean().default(true),
  enableFallback: z.boolean().default(true),
});

export type ProviderConfig = z.infer<typeof ProviderConfigSchema>;

// Provider metrics for monitoring (DRY: Reusable metrics structure)
export interface ProviderMetrics {
  subscriptionUsage: {
    remaining: number;
    resetDate: Date;
    provider: 'claude-pro' | 'claude-max';
  };
  fallbackCosts: {
    openai: number;
    anthropic: number;
  };
  routingDecisions: Array<{
    timestamp: Date;
    provider: string;
    reason: 'subscription' | 'fallback' | 'error' | 'selection';
    cost: number;
    metadata?: {
      selectedModel?: ModelType;
      reasoning?: string[];
      confidence?: number;
    };
  }>;
}

// Error types for provider handling (SOLID: Single responsibility for errors)
export class ProviderError extends Error {
  constructor(
    message: string,
    public provider: string,
    public cause?: Error
  ) {
    super(message);
    this.name = 'ProviderError';
  }
}

export class SubscriptionError extends ProviderError {
  constructor(provider: string, cause?: Error) {
    super(`Subscription error for provider: ${provider}`, provider, cause);
    this.name = 'SubscriptionError';
  }
}

export class RateLimitError extends ProviderError {
  constructor(provider: string, cause?: Error) {
    super(`Rate limit exceeded for provider: ${provider}`, provider, cause);
    this.name = 'RateLimitError';
  }
}

/**
 * SOLID-compliant Provider Factory with intelligent model selection
 * Single Responsibility: Create and manage language model providers
 * Open/Closed: Extensible for new providers without modification
 * Dependency Inversion: Accepts ModelSelector via constructor injection
 */
export class ProviderFactory {
  private config: ProviderConfig;
  private metrics: ProviderMetrics;
  private modelSelector: ModelSelector;

  constructor(
    config: Partial<ProviderConfig> = {},
    modelSelector?: ModelSelector
  ) {
    // Validate and set default configuration
    this.config = ProviderConfigSchema.parse(config);
    this.validateEnhancedConfig(this.config);
    
    // Dependency injection for model selector (SOLID: Dependency Inversion)
    this.modelSelector = modelSelector || new ModelSelector(defaultModelSelectionRules);
    this.validateModelSelector(this.modelSelector);
    
    // Initialize metrics
    this.metrics = {
      subscriptionUsage: {
        remaining: 100, // Mock value
        resetDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
        provider: 'claude-pro',
      },
      fallbackCosts: {
        openai: 0,
        anthropic: 0,
      },
      routingDecisions: [],
    };
  }

  /**
   * Create model with intelligent selection based on task characteristics
   * SOLID: Open/Closed - extensible for new selection strategies
   */
  async createModelWithSelection(
    task: TaskType,
    content: string,
    context?: TaskContext
  ): Promise<any> {
    try {
      // Use model selector to determine optimal model
      const selectedModel = this.modelSelector.selectModel(task, content, context || {});
      const reasoning = this.modelSelector.getSelectionReasoning(task, content, context || {});
      
      // Create the selected model
      const model = await this.createModel('claude-code', selectedModel);
      
      // Log selection decision for metrics
      this.logRoutingDecision('claude-code', 'selection', this.estimateCost('claude-code'), {
        selectedModel,
        reasoning: reasoning.reasons,
        confidence: reasoning.confidence,
      });
      
      return model;
    } catch (error) {
      // Fallback to default behavior on selection error
      console.warn('Model selection failed, falling back to default:', error);
      return this.createModel();
    }
  }

  /**
   * Create a model instance using the configured provider strategy
   * Enhanced to support Claude model variants
   * SOLID: Single Responsibility - model creation
   */
  async createModel(providerType?: string, modelType?: ModelType): Promise<any> {
    const provider = providerType || this.config.primary;
    
    // Check if provider is supported before attempting creation
    const supportedProviders = ['claude-code', 'openai', 'anthropic'];
    if (!supportedProviders.includes(provider)) {
      throw new ProviderError(`Unsupported provider: ${provider}`, provider);
    }
    
    try {
      const model = await this.createProviderModel(provider, modelType);
      this.logRoutingDecision(provider, 'subscription', this.estimateCost(provider));
      return model;
    } catch (error) {
      if (this.config.enableFallback && provider === this.config.primary) {
        return this.createFallbackProvider(provider, error as Error, modelType);
      }
      throw new ProviderError(`Failed to create model for provider: ${provider}`, provider, error as Error);
    }
  }

  /**
   * Create a specific provider model with model variant support
   * SOLID: Single Responsibility - Model creation for specific providers
   * KISS: Simple, clear model creation logic
   */
  private async createProviderModel(provider: string, modelType?: ModelType): Promise<any> {
    switch (provider) {
      case 'claude-code':
        return this.createClaudeCodeProvider(modelType);
      case 'openai':
        return openai(this.config.models.openai);
      case 'anthropic':
        return anthropic(this.config.models.anthropic);
      default:
        throw new ProviderError(`Unsupported provider: ${provider}`, provider);
    }
  }

  /**
   * Create Claude Code provider instance with model selection support
   * SOLID: Single Responsibility - Claude Code provider creation
   * KISS: Simple model variant handling
   */
  private async createClaudeCodeProvider(modelType?: ModelType): Promise<any> {
    try {
      const { claudeCode } = await import('ai-sdk-provider-claude-code');
      
      // Determine which Claude model to use
      let claudeModel: string;
      
      if (modelType === 'opus') {
        claudeModel = this.config.models['claude-code-opus'];
      } else if (modelType === 'sonnet') {
        claudeModel = this.config.models['claude-code'];
      } else if (!modelType) {
        claudeModel = this.config.models['claude-code']; // Default to Sonnet
      } else {
        throw new ProviderError(`Unsupported Claude model variant: ${modelType}`, 'claude-code');
      }
      
      // Claude Code provider uses CLI-based authentication automatically
      return claudeCode(claudeModel);
    } catch (importError) {
      // Handle both import errors and model creation errors
      if (importError instanceof ProviderError) {
        throw importError;
      }
      
      throw new ProviderError(
        'Failed to import Claude Code provider. Ensure ai-sdk-provider-claude-code is installed.',
        'claude-code',
        importError as Error
      );
    }
  }

  /**
   * Handle provider fallback with model type preservation
   * SOLID: Single Responsibility - Fallback handling
   * DRY: Reuses model creation logic
   */
  private async createFallbackProvider(
    failedProvider: string, 
    originalError: Error, 
    modelType?: ModelType
  ): Promise<any> {
    const fallbacks = this.config.fallbacks.filter(p => p !== failedProvider);
    
    // Try Claude Code with different model first if that wasn't the original failure
    if (failedProvider === 'claude-code' && modelType) {
      const alternateModel = modelType === 'opus' ? 'sonnet' : 'opus';
      try {
        const model = await this.createClaudeCodeProvider(alternateModel);
        this.logRoutingDecision('claude-code', 'fallback', this.estimateCost('claude-code'), {
          selectedModel: alternateModel,
          reasoning: [`Fallback from ${modelType} to ${alternateModel}`],
          confidence: 0.7,
        });
        return model;
      } catch (alternateError) {
        // Continue to external provider fallbacks
        console.warn(`Claude ${alternateModel} also failed, trying external providers`);
      }
    }
    
    // Try external provider fallbacks
    for (const fallback of fallbacks) {
      try {
        const model = await this.createProviderModel(fallback);
        this.logRoutingDecision(fallback, 'fallback', this.estimateCost(fallback));
        return model;
      } catch (error) {
        continue; // Try next fallback
      }
    }
    
    throw new ProviderError(
      `All providers failed. Original error: ${originalError.message}`,
      'all-providers',
      originalError
    );
  }

  /**
   * Estimate cost for API-based providers
   * SOLID: Single Responsibility - Cost estimation
   */
  public estimateCost(provider: string): number {
    // Simple cost estimation (per 1K tokens)
    switch (provider) {
      case 'claude-code':
        return 0; // Subscription-based
      case 'openai':
        return 0.01; // Rough estimate for gpt-4o-mini
      case 'anthropic':
        return 0.008; // Rough estimate for claude-3-haiku
      default:
        return 0;
    }
  }

  /**
   * Log routing decisions for metrics and debugging
   * DRY: Centralized logging logic
   */
  private logRoutingDecision(
    provider: string, 
    reason: 'subscription' | 'fallback' | 'error' | 'selection', 
    cost: number,
    metadata?: {
      selectedModel?: ModelType;
      reasoning?: string[];
      confidence?: number;
    }
  ): void {
    this.metrics.routingDecisions.push({
      timestamp: new Date(),
      provider,
      reason,
      cost,
      metadata,
    });
    
    // Keep only last 100 decisions to prevent memory growth
    if (this.metrics.routingDecisions.length > 100) {
      this.metrics.routingDecisions = this.metrics.routingDecisions.slice(-100);
    }
  }

  /**
   * Enhanced configuration validation
   * SOLID: Single Responsibility - Configuration validation
   */
  private validateEnhancedConfig(config: ProviderConfig): void {
    // Ensure Opus model configuration exists
    if (!config.models['claude-code-opus']) {
      throw new ProviderError('Missing Claude Opus model configuration', 'configuration');
    }
    
    // Validate model configuration format
    const claudeModels = ['claude-code', 'claude-code-opus'];
    for (const modelKey of claudeModels) {
      if (!config.models[modelKey as keyof typeof config.models]) {
        throw new ProviderError(`Missing model configuration for: ${modelKey}`, 'configuration');
      }
    }
  }

  /**
   * Validate model selector interface
   * SOLID: Single Responsibility - Interface validation
   */
  private validateModelSelector(selector: ModelSelector): void {
    if (!selector || typeof selector.selectModel !== 'function') {
      throw new ProviderError('Invalid model selector: missing selectModel method', 'configuration');
    }
    
    if (typeof selector.getSelectionReasoning !== 'function') {
      throw new ProviderError('Invalid model selector: missing getSelectionReasoning method', 'configuration');
    }
  }

  /**
   * Get provider metrics for monitoring
   */
  getMetrics(): ProviderMetrics {
    return { ...this.metrics };
  }

  /**
   * Get model selector instance (for testing)
   */
  getModelSelector(): ModelSelector {
    return this.modelSelector;
  }

  /**
   * Update provider configuration
   * SOLID: Interface Segregation - Separate concerns for configuration management
   */
  updateConfig(newConfig: Partial<ProviderConfig>): void {
    this.config = ProviderConfigSchema.parse({ ...this.config, ...newConfig });
    this.validateEnhancedConfig(this.config);
  }

  /**
   * Get current configuration
   */
  getConfig(): ProviderConfig {
    return { ...this.config };
  }

  /**
   * Test provider availability with model type support
   */
  async testProvider(provider: string, modelType?: ModelType): Promise<boolean> {
    try {
      const model = await this.createProviderModel(provider, modelType);
      // Simple test - just creation success indicates availability
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Get available providers in priority order
   */
  getAvailableProviders(): string[] {
    return [this.config.primary, ...this.config.fallbacks];
  }
}

// Default configuration for easy instantiation
export const defaultProviderConfig: ProviderConfig = {
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

// Factory instance with default configuration
export const providerFactory = new ProviderFactory(defaultProviderConfig);