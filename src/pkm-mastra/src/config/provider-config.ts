import { z } from 'zod';
import { ProviderConfig, ProviderConfigSchema } from '../providers/provider-factory.js';

// Environment-based provider configuration
export interface ProviderEnvironmentConfig {
  development: ProviderConfig;
  test: ProviderConfig;
  production: ProviderConfig;
}

// Environment configuration schema
export const ProviderEnvironmentConfigSchema = z.object({
  development: ProviderConfigSchema,
  test: ProviderConfigSchema,
  production: ProviderConfigSchema,
});

// Default environment configurations
export const defaultProviderEnvironmentConfig: ProviderEnvironmentConfig = {
  development: {
    primary: 'claude-code',
    fallbacks: ['openai'],
    models: {
      'claude-code': 'claude-3-5-sonnet-20241022',
      'openai': 'gpt-4o-mini',
      'anthropic': 'claude-3-haiku-20240307',
    },
    subscriptionBased: true,
    costOptimization: true,
    enableFallback: true,
  },
  test: {
    primary: 'openai', // Use faster/cheaper model for tests
    fallbacks: ['anthropic'],
    models: {
      'claude-code': 'claude-3-5-sonnet-20241022',
      'openai': 'gpt-4o-mini',
      'anthropic': 'claude-3-haiku-20240307',
    },
    subscriptionBased: false, // API keys more predictable for testing
    costOptimization: false,
    enableFallback: true,
  },
  production: {
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
  },
};

// Environment variable mapping
export interface ProviderEnvVars {
  CLAUDE_CODE_ENABLED?: string;
  CLAUDE_CODE_MODEL?: string;
  OPENAI_FALLBACK_ENABLED?: string;
  ANTHROPIC_FALLBACK_ENABLED?: string;
  PROVIDER_METRICS_ENABLED?: string;
  PRIMARY_PROVIDER?: 'claude-code' | 'openai' | 'anthropic';
  ENABLE_PROVIDER_FALLBACK?: string;
  COST_OPTIMIZATION_ENABLED?: string;
}

/**
 * Load provider configuration from environment variables
 */
export function loadProviderConfigFromEnv(env: ProviderEnvVars = {}): ProviderConfig {
  const config: Partial<ProviderConfig> = {};

  // Set primary provider
  if (env.PRIMARY_PROVIDER) {
    config.primary = env.PRIMARY_PROVIDER as 'claude-code' | 'openai' | 'anthropic';
  }

  // Configure fallbacks based on enabled providers
  const fallbacks: Array<'claude-code' | 'openai' | 'anthropic'> = [];
  
  if (env.CLAUDE_CODE_ENABLED !== 'false' && config.primary !== 'claude-code') {
    fallbacks.push('claude-code');
  }
  if (env.OPENAI_FALLBACK_ENABLED !== 'false' && config.primary !== 'openai') {
    fallbacks.push('openai');
  }
  if (env.ANTHROPIC_FALLBACK_ENABLED !== 'false' && config.primary !== 'anthropic') {
    fallbacks.push('anthropic');
  }
  
  if (fallbacks.length > 0) {
    config.fallbacks = fallbacks;
  }

  // Configure models
  config.models = {};
  if (env.CLAUDE_CODE_MODEL) {
    config.models['claude-code'] = env.CLAUDE_CODE_MODEL;
  }

  // Configure boolean options
  if (env.ENABLE_PROVIDER_FALLBACK !== undefined) {
    config.enableFallback = env.ENABLE_PROVIDER_FALLBACK === 'true';
  }
  
  if (env.COST_OPTIMIZATION_ENABLED !== undefined) {
    config.costOptimization = env.COST_OPTIMIZATION_ENABLED === 'true';
  }

  // Always prefer subscription-based for Claude Code
  config.subscriptionBased = config.primary === 'claude-code';

  return ProviderConfigSchema.parse(config);
}

/**
 * Get provider configuration for current environment
 */
export function getProviderConfigForEnvironment(
  environment: 'development' | 'test' | 'production' = 'development',
  envOverrides?: ProviderEnvVars
): ProviderConfig {
  // Start with environment default
  let config = defaultProviderEnvironmentConfig[environment];

  // Apply environment variable overrides if provided
  if (envOverrides || process.env.PRIMARY_PROVIDER) {
    const envConfig = loadProviderConfigFromEnv(envOverrides || {
      PRIMARY_PROVIDER: process.env.PRIMARY_PROVIDER as any,
      CLAUDE_CODE_ENABLED: process.env.CLAUDE_CODE_ENABLED,
      CLAUDE_CODE_MODEL: process.env.CLAUDE_CODE_MODEL,
      OPENAI_FALLBACK_ENABLED: process.env.OPENAI_FALLBACK_ENABLED,
      ANTHROPIC_FALLBACK_ENABLED: process.env.ANTHROPIC_FALLBACK_ENABLED,
      PROVIDER_METRICS_ENABLED: process.env.PROVIDER_METRICS_ENABLED,
      ENABLE_PROVIDER_FALLBACK: process.env.ENABLE_PROVIDER_FALLBACK,
      COST_OPTIMIZATION_ENABLED: process.env.COST_OPTIMIZATION_ENABLED,
    });
    config = ProviderConfigSchema.parse({ ...config, ...envConfig });
  }

  return config;
}

/**
 * Validate provider configuration
 */
export function validateProviderConfig(config: unknown): ProviderConfig {
  return ProviderConfigSchema.parse(config);
}

/**
 * Create provider configuration with intelligent defaults
 */
export function createProviderConfig(overrides: Partial<ProviderConfig> = {}): ProviderConfig {
  const environment = (process.env.NODE_ENV as 'development' | 'test' | 'production') || 'development';
  const baseConfig = getProviderConfigForEnvironment(environment);
  
  return ProviderConfigSchema.parse({ ...baseConfig, ...overrides });
}

// Export current environment configuration
export const currentProviderConfig = getProviderConfigForEnvironment(
  (process.env.NODE_ENV as 'development' | 'test' | 'production') || 'development'
);