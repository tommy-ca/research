/**
 * Provider Service Type Definitions
 * Supporting TDD Cycle 1.1: Provider System Unification
 */

// Core provider configuration
export interface ProviderConfig {
  primary: 'claude-code' | 'openai' | 'anthropic';
  fallbacks: Array<'claude-code' | 'openai' | 'anthropic'>;
  models: {
    'claude-code': string;
    'openai': string; 
    'anthropic': string;
  };
  subscriptionBased: boolean;
  costOptimization: boolean;
  enableFallback: boolean;
  qualityThresholds: {
    high: number;
    medium: number;
    low: number;
  };
}

// Provider selection context
export interface ProviderContext {
  qualityThreshold: number;
  contentLength: number;
  contentType: 'research' | 'capture' | 'synthesis' | 'processing';
  urgency: 'low' | 'normal' | 'high';
  budget?: number;
  previousFailures?: string[];
}

// Provider selection result
export interface ProviderSelection {
  provider: string;
  model: string;
  rationale: string;
  confidence: number;
  estimatedCost: number;
  estimatedTime: number;
}

// LLM provider interface
export interface LLMProvider {
  id: string;
  model: string;
  generate: (input: any) => Promise<any>;
  stream: (input: any) => Promise<any>;
}

// Provider validation result
export interface ProviderValidation {
  isHealthy: boolean;
  responseTime: number;
  errors: string[];
  lastChecked: Date;
}

// Provider metrics
export interface ProviderMetrics {
  selections: {
    total: number;
    byProvider: Record<string, number>;
    byModel: Record<string, number>;
  };
  creations: {
    successful: number;
    failed: number;
    averageTime: number;
  };
  fallbacks: {
    triggered: number;
    successful: number;
    failed: number;
  };
  performance: {
    averageSelectionTime: number;
    averageCreationTime: number;
    p95SelectionTime: number;
    p95CreationTime: number;
  };
}

// Service dependencies (Dependency Injection)
export interface ServiceDependencies {
  metricsService: MetricsService;
  logger: Logger;
  providerFactory: ProviderFactory;
}

export interface MetricsService {
  recordSelection(data: {
    provider: string;
    model: string;
    selectionTime: number;
    confidence: number;
    context: ProviderContext;
  }): void;
  
  recordCreation(data: {
    provider: string;
    model: string;
    success: boolean;
  }): void;
  
  recordFailure(data: {
    provider: string;
    error: string;
    fallbackUsed?: string;
  }): void;
  
  getMetrics(): ProviderMetrics;
}

export interface Logger {
  info(message: string, meta?: any): void;
  warn(message: string, meta?: any): void;
  error(message: string, error?: Error): void;
  debug(message: string, meta?: any): void;
}

export interface ProviderFactory {
  createClaudeCodeProvider(model: string): Promise<LLMProvider>;
  createOpenAIProvider(model: string): Promise<LLMProvider>;
  createAnthropicProvider(model: string): Promise<LLMProvider>;
}

// Provider selection strategy interface (Strategy Pattern - OCP compliance)
export interface ProviderSelectionStrategy {
  select(context: ProviderContext): ProviderSelection;
}

// Main service interface
export interface ProviderServiceInterface {
  selectOptimalProvider(context: ProviderContext): Promise<ProviderSelection>;
  createProvider(selection: ProviderSelection): Promise<LLMProvider>;
  validateProvider(provider: LLMProvider): Promise<ProviderValidation>;
  updateConfig(config: Partial<ProviderConfig>): void;
  getConfig(): ProviderConfig;
  getMetrics(): ProviderMetrics;
  getAvailableProviders(): string[];
}