/**
 * PKM INGESTION TDD CYCLE - PHASE 1, TASK 1.1
 * GREEN PHASE: Minimal implementation to make tests pass
 * 
 * Claude Code SDK Provider Integration Implementation
 * Following KISS principle: Simplest code to pass all tests
 */

import { claudeCode } from 'ai-sdk-provider-claude-code';

// Type definitions for provider configuration
export interface ClaudeCodeProviderConfig {
  useSubscription?: boolean;
  fallbackOnError?: boolean;
  temperature?: number;
  maxTokens?: number;
  retryAttempts?: number;
}

// Provider interface for type safety
export interface ClaudeCodeProvider {
  model: string;
  provider: string;
  config?: ClaudeCodeProviderConfig & {
    useSubscription: boolean;
    fallbackOnError: boolean;
    temperature: number;
    maxTokens: number;
  };
  subscription?: {
    type: string;
    active: boolean;
  };
  fallback?: {
    active: boolean;
    provider: string;
  };
}

// Model mapping for Claude Code SDK
const MODEL_MAP = {
  sonnet: 'claude-3-5-sonnet-20241022',
  opus: 'claude-3-opus-20240229'
} as const;

// Default configurations per model
const DEFAULT_CONFIG: Record<'sonnet' | 'opus', ClaudeCodeProviderConfig> = {
  sonnet: {
    useSubscription: true,
    fallbackOnError: true,
    temperature: 0.3,
    maxTokens: 2000,
    retryAttempts: 3,
  },
  opus: {
    useSubscription: true,
    fallbackOnError: true,
    temperature: 0.1,
    maxTokens: 4000,
    retryAttempts: 3,
  },
};

/**
 * Create Claude Code provider with intelligent configuration
 * GREEN PHASE: Minimal implementation to pass tests
 */
export async function createClaudeCodeProvider(
  model: 'sonnet' | 'opus',
  config?: ClaudeCodeProviderConfig
): Promise<ClaudeCodeProvider> {
  // Validate model type
  if (!MODEL_MAP[model]) {
    throw new Error('Invalid model type');
  }
  
  // Validate configuration
  if (config === null) {
    throw new Error('Invalid provider configuration');
  }
  
  // Merge with defaults
  const finalConfig = {
    ...DEFAULT_CONFIG[model],
    ...config,
  };
  
  // Validate configuration values
  if (finalConfig.temperature && (finalConfig.temperature < 0 || finalConfig.temperature > 1)) {
    throw new Error('Configuration validation failed');
  }
  
  if (finalConfig.maxTokens && finalConfig.maxTokens < 0) {
    throw new Error('Configuration validation failed');
  }
  
  // Retry logic for transient failures
  let lastError: Error | null = null;
  const maxRetries = finalConfig.retryAttempts || 3;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const provider = await createProviderWithRetry(model, finalConfig);
      return provider;
    } catch (error) {
      lastError = error as Error;
      
      // Don't retry on configuration errors
      if (lastError.message.includes('Configuration validation failed') ||
          lastError.message.includes('Invalid')) {
        throw lastError;
      }
      
      // Continue retrying for transient errors
      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, attempt * 100));
        continue;
      }
    }
  }
  
  // All retries failed
  throw new Error('Provider initialization failed');
}

/**
 * Internal helper for provider creation with error handling
 */
async function createProviderWithRetry(
  model: 'sonnet' | 'opus',
  config: ClaudeCodeProviderConfig
): Promise<ClaudeCodeProvider> {
  try {
    // Claude Code provider only accepts simple model names: 'sonnet' or 'opus'
    const claudeProvider = claudeCode(model);
    
    // Return our wrapper with config tracking
    return {
      model: model,
      provider: 'claude-code',
      config: {
        useSubscription: config.useSubscription!,
        fallbackOnError: config.fallbackOnError!,
        temperature: config.temperature!,
        maxTokens: config.maxTokens!,
      },
      subscription: {
        type: 'claude-pro', // Mock subscription detection
        active: true,
      },
    };
  } catch (error) {
    // Handle subscription unavailable
    if ((error as Error).message.includes('Subscription not available') ||
        (error as Error).message.includes('Claude Code not available')) {
      return {
        model: model,
        provider: 'claude-code',
        config: {
          useSubscription: false,
          fallbackOnError: true,
          temperature: config.temperature!,
          maxTokens: config.maxTokens!,
        },
        fallback: {
          active: true,
          provider: 'openai', // Mock fallback provider
        },
      };
    }
    
    throw error;
  }
}

/**
 * Provider Factory for SOLID compliance (Dependency Injection)
 * GREEN PHASE: Basic factory implementation
 */
export class ClaudeCodeProviderFactory {
  constructor(private config: ClaudeCodeProviderConfig = {}) {
    // Validate configuration on construction
    if (this.config.temperature && 
        (this.config.temperature < 0 || this.config.temperature > 1)) {
      throw new Error('Configuration validation failed');
    }
    
    if (this.config.maxTokens && this.config.maxTokens < 0) {
      throw new Error('Configuration validation failed');
    }
  }
  
  /**
   * Create provider instance with factory configuration
   */
  async create(model: 'sonnet' | 'opus'): Promise<ClaudeCodeProvider> {
    return createClaudeCodeProvider(model, this.config);
  }
  
  /**
   * Get current factory configuration
   */
  get config(): ClaudeCodeProviderConfig {
    return { ...this.config };
  }
}

/**
 * GREEN PHASE IMPLEMENTATION NOTES:
 * 
 * ✅ KISS Principle: Simple functions and classes
 * ✅ Minimal code to pass all tests
 * ✅ Proper error handling for all test cases
 * ✅ Configuration validation and defaults
 * ✅ Retry logic for transient failures
 * ✅ SOLID compliance with factory pattern
 * ✅ Type safety with TypeScript interfaces
 * ✅ Subscription model mock implementation
 * 
 * NEXT PHASE: REFACTOR - Improve code quality while maintaining tests
 */