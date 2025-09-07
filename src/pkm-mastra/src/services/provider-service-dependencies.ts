/**
 * Service Dependencies for ProviderService
 * Concrete implementations of interfaces required by ProviderService
 */

import type {
  ServiceDependencies,
  MetricsService,
  Logger,
  ProviderFactory,
  ProviderMetrics,
  ProviderContext,
  LLMProvider
} from '../provider-types.js';

// Default Metrics Service Implementation
export class DefaultMetricsService implements MetricsService {
  private metrics: ProviderMetrics = {
    selections: {
      total: 0,
      byProvider: {},
      byModel: {}
    },
    creations: {
      successful: 0,
      failed: 0,
      averageTime: 0
    },
    fallbacks: {
      triggered: 0,
      successful: 0,
      failed: 0
    },
    performance: {
      averageSelectionTime: 0,
      averageCreationTime: 0,
      p95SelectionTime: 0,
      p95CreationTime: 0
    }
  };

  private selectionTimes: number[] = [];
  private creationTimes: number[] = [];

  recordSelection(data: {
    provider: string;
    model: string;
    selectionTime: number;
    confidence: number;
    context: ProviderContext;
  }): void {
    this.metrics.selections.total++;
    this.metrics.selections.byProvider[data.provider] = 
      (this.metrics.selections.byProvider[data.provider] || 0) + 1;
    this.metrics.selections.byModel[data.model] = 
      (this.metrics.selections.byModel[data.model] || 0) + 1;
    
    // Track selection times for performance metrics
    this.selectionTimes.push(data.selectionTime);
    this.updatePerformanceMetrics();
  }

  recordCreation(data: {
    provider: string;
    model: string;
    success: boolean;
  }): void {
    if (data.success) {
      this.metrics.creations.successful++;
    } else {
      this.metrics.creations.failed++;
    }
  }

  recordFailure(data: {
    provider: string;
    error: string;
    fallbackUsed?: string;
  }): void {
    this.metrics.fallbacks.triggered++;
    if (data.fallbackUsed) {
      this.metrics.fallbacks.successful++;
    } else {
      this.metrics.fallbacks.failed++;
    }
  }

  getMetrics(): ProviderMetrics {
    return { ...this.metrics }; // Return copy
  }

  private updatePerformanceMetrics(): void {
    if (this.selectionTimes.length > 0) {
      this.metrics.performance.averageSelectionTime = 
        this.selectionTimes.reduce((a, b) => a + b, 0) / this.selectionTimes.length;
      
      // Calculate P95 (95th percentile)
      const sorted = [...this.selectionTimes].sort((a, b) => a - b);
      const p95Index = Math.floor(sorted.length * 0.95);
      this.metrics.performance.p95SelectionTime = sorted[p95Index] || 0;
    }
  }
}

// Default Logger Implementation
export class DefaultLogger implements Logger {
  info(message: string, meta?: any): void {
    console.log(`[INFO] ${message}`, meta || '');
  }

  warn(message: string, meta?: any): void {
    console.warn(`[WARN] ${message}`, meta || '');
  }

  error(message: string, error?: Error): void {
    console.error(`[ERROR] ${message}`, error || '');
  }

  debug(message: string, meta?: any): void {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`[DEBUG] ${message}`, meta || '');
    }
  }
}

// Default Provider Factory Implementation
export class DefaultProviderFactory implements ProviderFactory {
  async createClaudeCodeProvider(model: string): Promise<LLMProvider> {
    try {
      const { claudeCode } = await import('ai-sdk-provider-claude-code');
      const provider = claudeCode(model);
      
      return {
        id: `claude-code-${model}`,
        model,
        generate: async (input: any) => provider.generate?.(input),
        stream: async (input: any) => provider.stream?.(input)
      };
    } catch (error) {
      throw new Error(`Failed to create Claude Code provider: ${error}`);
    }
  }

  async createOpenAIProvider(model: string): Promise<LLMProvider> {
    try {
      const { openai } = await import('@ai-sdk/openai');
      const provider = openai(model);
      
      return {
        id: `openai-${model}`,
        model,
        generate: async (input: any) => provider.generate?.(input),
        stream: async (input: any) => provider.stream?.(input)
      };
    } catch (error) {
      throw new Error(`Failed to create OpenAI provider: ${error}`);
    }
  }

  async createAnthropicProvider(model: string): Promise<LLMProvider> {
    try {
      const { anthropic } = await import('@ai-sdk/anthropic');
      const provider = anthropic(model);
      
      return {
        id: `anthropic-${model}`,
        model,
        generate: async (input: any) => provider.generate?.(input),
        stream: async (input: any) => provider.stream?.(input)
      };
    } catch (error) {
      throw new Error(`Failed to create Anthropic provider: ${error}`);
    }
  }
}

// Factory function to create service dependencies
export function createServiceDependencies(options?: {
  metricsService?: MetricsService;
  logger?: Logger;
  providerFactory?: ProviderFactory;
}): ServiceDependencies {
  return {
    metricsService: options?.metricsService || new DefaultMetricsService(),
    logger: options?.logger || new DefaultLogger(),
    providerFactory: options?.providerFactory || new DefaultProviderFactory()
  };
}

// Export individual implementations for testing and customization
export { DefaultMetricsService, DefaultLogger, DefaultProviderFactory };