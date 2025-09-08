import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

// Provider configuration schema
export const ProviderConfigSchema = z.object({
  primary: z.enum(['claude-code', 'openai', 'anthropic']).default('claude-code'),
  fallbacks: z.array(z.enum(['claude-code', 'openai', 'anthropic'])).default(['openai', 'anthropic']),
  models: z.object({
    'claude-code': z.string().default('sonnet'),
    'openai': z.string().default('gpt-4o-mini'),
    'anthropic': z.string().default('claude-3-haiku-20240307'),
  }).default({
    'claude-code': 'sonnet',
    'openai': 'gpt-4o-mini',
    'anthropic': 'claude-3-haiku-20240307',
  }),
  subscriptionBased: z.boolean().default(true),
  costOptimization: z.boolean().default(true),
  enableFallback: z.boolean().default(true),
});

export type ProviderConfig = z.infer<typeof ProviderConfigSchema>;

// Provider metrics for monitoring
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
    reason: 'subscription' | 'fallback' | 'error';
    cost: number;
  }>;
}

// Error types for provider handling
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

// SOLID-compliant Provider Factory
export class ProviderFactory {
  private config: ProviderConfig;
  private metrics: ProviderMetrics;

  constructor(config: Partial<ProviderConfig> = {}) {
    // Validate and set default configuration
    this.config = ProviderConfigSchema.parse(config);
    
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
   * Create a model instance using the configured provider strategy
   * Implements Open/Closed Principle - extensible for new providers
   */
  async createModel(providerType?: string): Promise<any> {
    const provider = providerType || this.config.primary;
    
    // Check if provider is supported before attempting creation
    const supportedProviders = ['claude-code', 'openai', 'anthropic'];
    if (!supportedProviders.includes(provider)) {
      throw new ProviderError(`Unsupported provider: ${provider}`, provider);
    }
    
    try {
      const model = await this.createProviderModel(provider);
      this.logRoutingDecision(provider, 'subscription', this.estimateCost(provider));
      return model;
    } catch (error) {
      if (this.config.enableFallback && provider === this.config.primary) {
        return this.createFallbackProvider(provider, error as Error);
      }
      throw new ProviderError(`Failed to create model for provider: ${provider}`, provider, error as Error);
    }
  }

  /**
   * Create a specific provider model
   * Single Responsibility: Model creation for specific providers
   */
  private async createProviderModel(provider: string): Promise<any> {
    switch (provider) {
      case 'claude-code':
        return this.createClaudeCodeProvider();
      case 'openai':
        return openai(this.config.models.openai);
      case 'anthropic':
        return anthropic(this.config.models.anthropic);
      default:
        throw new ProviderError(`Unsupported provider: ${provider}`, provider);
    }
  }

  /**
   * Create Claude Code provider instance
   * Handles subscription-based authentication
   */
  private async createClaudeCodeProvider(): Promise<any> {
    try {
      const { claudeCode } = await import('ai-sdk-provider-claude-code');
      
      // Claude Code provider uses CLI-based authentication automatically
      // No API key or additional configuration needed
      return claudeCode(this.config.models['claude-code']);
    } catch (importError) {
      throw new ProviderError(
        'Failed to import Claude Code provider. Ensure ai-sdk-provider-claude-code is installed.',
        'claude-code',
        importError as Error
      );
    }
  }

  /**
   * Handle provider fallback with graceful degradation
   * Dependency Inversion: Depends on abstractions, not concretions
   */
  private async createFallbackProvider(failedProvider: string, originalError: Error): Promise<any> {
    const fallbacks = this.config.fallbacks.filter(p => p !== failedProvider);
    
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
   */
  private logRoutingDecision(provider: string, reason: 'subscription' | 'fallback' | 'error', cost: number): void {
    this.metrics.routingDecisions.push({
      timestamp: new Date(),
      provider,
      reason,
      cost,
    });
    
    // Keep only last 100 decisions to prevent memory growth
    if (this.metrics.routingDecisions.length > 100) {
      this.metrics.routingDecisions = this.metrics.routingDecisions.slice(-100);
    }
  }

  /**
   * Get provider metrics for monitoring
   */
  getMetrics(): ProviderMetrics {
    return { ...this.metrics };
  }

  /**
   * Update provider configuration
   * Interface Segregation: Separate concerns for configuration management
   */
  updateConfig(newConfig: Partial<ProviderConfig>): void {
    this.config = ProviderConfigSchema.parse({ ...this.config, ...newConfig });
  }

  /**
   * Get current configuration
   */
  getConfig(): ProviderConfig {
    return { ...this.config };
  }

  /**
   * Test provider availability
   */
  async testProvider(provider: string): Promise<boolean> {
    try {
      const model = await this.createProviderModel(provider);
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
    'claude-code': 'sonnet',
    'openai': 'gpt-4o-mini',
    'anthropic': 'claude-3-haiku-20240307',
  },
  subscriptionBased: true,
  costOptimization: true,
  enableFallback: true,
};

// Factory instance with default configuration
export const providerFactory = new ProviderFactory(defaultProviderConfig);