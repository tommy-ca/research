import { describe, test, expect, beforeEach, vi } from 'vitest';
import {
  loadProviderConfigFromEnv,
  getProviderConfigForEnvironment,
  createProviderConfig,
  validateProviderConfig,
  defaultProviderEnvironmentConfig,
  currentProviderConfig,
  type ProviderEnvVars
} from '../../src/config/provider-config.js';

describe('Provider Configuration Management', () => {
  describe('Environment Variable Loading', () => {
    test('should load configuration from environment variables', () => {
      const envVars: ProviderEnvVars = {
        PRIMARY_PROVIDER: 'openai',
        CLAUDE_CODE_ENABLED: 'true',
        CLAUDE_CODE_MODEL: 'claude-3-5-sonnet-20241022',
        OPENAI_FALLBACK_ENABLED: 'true',
        ANTHROPIC_FALLBACK_ENABLED: 'false',
        ENABLE_PROVIDER_FALLBACK: 'true',
        COST_OPTIMIZATION_ENABLED: 'true',
      };

      const config = loadProviderConfigFromEnv(envVars);

      expect(config.primary).toBe('openai');
      expect(config.fallbacks).toContain('claude-code');
      expect(config.fallbacks).not.toContain('anthropic');
      expect(config.enableFallback).toBe(true);
      expect(config.costOptimization).toBe(true);
    });

    test('should handle disabled providers', () => {
      const envVars: ProviderEnvVars = {
        PRIMARY_PROVIDER: 'claude-code',
        CLAUDE_CODE_ENABLED: 'false',
        OPENAI_FALLBACK_ENABLED: 'true',
        ANTHROPIC_FALLBACK_ENABLED: 'true',
      };

      const config = loadProviderConfigFromEnv(envVars);

      expect(config.primary).toBe('claude-code');
      expect(config.fallbacks).toContain('openai');
      expect(config.fallbacks).toContain('anthropic');
    });

    test('should set subscription based on primary provider', () => {
      const claudeConfig = loadProviderConfigFromEnv({ PRIMARY_PROVIDER: 'claude-code' });
      expect(claudeConfig.subscriptionBased).toBe(true);

      const openaiConfig = loadProviderConfigFromEnv({ PRIMARY_PROVIDER: 'openai' });
      expect(openaiConfig.subscriptionBased).toBe(false);

      const anthropicConfig = loadProviderConfigFromEnv({ PRIMARY_PROVIDER: 'anthropic' });
      expect(anthropicConfig.subscriptionBased).toBe(false);
    });

    test('should handle custom model configuration', () => {
      const envVars: ProviderEnvVars = {
        CLAUDE_CODE_MODEL: 'claude-3-opus-20240229',
      };

      const config = loadProviderConfigFromEnv(envVars);
      expect(config.models?.['claude-code']).toBe('claude-3-opus-20240229');
    });

    test('should load empty configuration gracefully', () => {
      const config = loadProviderConfigFromEnv({});

      // Should use schema defaults
      expect(config.primary).toBe('claude-code');
      expect(config.fallbacks).toEqual(['openai', 'anthropic']);
      expect(config.subscriptionBased).toBe(true);
    });
  });

  describe('Environment-Based Configuration', () => {
    test('should provide development configuration', () => {
      const config = getProviderConfigForEnvironment('development');

      expect(config.primary).toBe('claude-code');
      expect(config.fallbacks).toContain('openai');
      expect(config.subscriptionBased).toBe(true);
      expect(config.costOptimization).toBe(true);
    });

    test('should provide test configuration', () => {
      const config = getProviderConfigForEnvironment('test');

      expect(config.primary).toBe('openai'); // Faster/cheaper for tests
      expect(config.subscriptionBased).toBe(false); // API keys more predictable
      expect(config.costOptimization).toBe(false);
    });

    test('should provide production configuration', () => {
      const config = getProviderConfigForEnvironment('production');

      expect(config.primary).toBe('claude-code');
      expect(config.fallbacks).toEqual(['openai', 'anthropic']);
      expect(config.subscriptionBased).toBe(true);
      expect(config.costOptimization).toBe(true);
    });

    test('should apply environment variable overrides', () => {
      const envOverrides: ProviderEnvVars = {
        PRIMARY_PROVIDER: 'anthropic',
        COST_OPTIMIZATION_ENABLED: 'false',
      };

      const config = getProviderConfigForEnvironment('production', envOverrides);

      expect(config.primary).toBe('anthropic');
      expect(config.costOptimization).toBe(false);
      // Other production defaults should remain
      expect(config.fallbacks).toEqual(['openai', 'anthropic']);
    });
  });

  describe('Configuration Creation and Validation', () => {
    test('should create configuration with intelligent defaults', () => {
      // Mock NODE_ENV
      const originalEnv = process.env.NODE_ENV;
      process.env.NODE_ENV = 'development';

      const config = createProviderConfig();

      expect(config.primary).toBe('claude-code');
      expect(config.subscriptionBased).toBe(true);

      process.env.NODE_ENV = originalEnv;
    });

    test('should create configuration with overrides', () => {
      const overrides = {
        primary: 'openai' as const,
        costOptimization: false,
      };

      const config = createProviderConfig(overrides);

      expect(config.primary).toBe('openai');
      expect(config.costOptimization).toBe(false);
    });

    test('should validate valid configuration', () => {
      const validConfig = {
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
      };

      const result = validateProviderConfig(validConfig);
      expect(result).toEqual(validConfig);
    });

    test('should reject invalid configuration', () => {
      const invalidConfig = {
        primary: 'invalid-provider',
        fallbacks: ['also-invalid'],
      };

      expect(() => validateProviderConfig(invalidConfig)).toThrow();
    });

    test('should fill in missing required fields', () => {
      const partialConfig = {
        primary: 'openai',
      };

      const result = validateProviderConfig(partialConfig);

      expect(result.primary).toBe('openai');
      expect(result.fallbacks).toEqual(['openai', 'anthropic']); // Default
      expect(result.models).toBeDefined();
      expect(result.subscriptionBased).toBe(true); // Default
    });
  });

  describe('Default Environment Configuration', () => {
    test('should have valid development configuration', () => {
      const devConfig = defaultProviderEnvironmentConfig.development;

      expect(devConfig.primary).toBe('claude-code');
      expect(devConfig.fallbacks).toEqual(['openai']);
      expect(devConfig.subscriptionBased).toBe(true);
      expect(devConfig.enableFallback).toBe(true);
    });

    test('should have valid test configuration', () => {
      const testConfig = defaultProviderEnvironmentConfig.test;

      expect(testConfig.primary).toBe('openai');
      expect(testConfig.subscriptionBased).toBe(false);
      expect(testConfig.costOptimization).toBe(false);
    });

    test('should have valid production configuration', () => {
      const prodConfig = defaultProviderEnvironmentConfig.production;

      expect(prodConfig.primary).toBe('claude-code');
      expect(prodConfig.fallbacks).toEqual(['openai', 'anthropic']);
      expect(prodConfig.subscriptionBased).toBe(true);
      expect(prodConfig.costOptimization).toBe(true);
    });

    test('should use consistent model configurations', () => {
      const { development, test, production } = defaultProviderEnvironmentConfig;

      expect(development.models['claude-code']).toBe(test.models['claude-code']);
      expect(test.models['claude-code']).toBe(production.models['claude-code']);
      expect(development.models.openai).toBe(test.models.openai);
      expect(test.models.openai).toBe(production.models.openai);
    });
  });

  describe('Current Provider Configuration', () => {
    test('should export valid current configuration', () => {
      expect(currentProviderConfig).toBeDefined();
      expect(currentProviderConfig.primary).toBeDefined();
      expect(currentProviderConfig.fallbacks).toBeDefined();
      expect(Array.isArray(currentProviderConfig.fallbacks)).toBe(true);
      expect(currentProviderConfig.models).toBeDefined();
    });

    test('should be based on NODE_ENV', () => {
      // The current config should match the NODE_ENV or default to development
      const environment = (process.env.NODE_ENV as 'development' | 'test' | 'production') || 'development';
      const expectedConfig = defaultProviderEnvironmentConfig[environment];

      expect(currentProviderConfig.primary).toBe(expectedConfig.primary);
    });
  });

  describe('Configuration Schema Compliance', () => {
    test('should enforce provider enum values', () => {
      expect(() => {
        validateProviderConfig({
          primary: 'gpt-4', // Invalid provider
        });
      }).toThrow();
    });

    test('should enforce fallback provider enum values', () => {
      expect(() => {
        validateProviderConfig({
          primary: 'claude-code',
          fallbacks: ['gpt-4'], // Invalid fallback
        });
      }).toThrow();
    });

    test('should require string model names', () => {
      expect(() => {
        validateProviderConfig({
          primary: 'claude-code',
          models: {
            'claude-code': 123, // Invalid model name type
          },
        });
      }).toThrow();
    });

    test('should enforce boolean flags', () => {
      expect(() => {
        validateProviderConfig({
          primary: 'claude-code',
          subscriptionBased: 'yes', // Invalid boolean value
        });
      }).toThrow();
    });
  });

  describe('Provider Priority Logic', () => {
    test('should exclude primary provider from fallbacks', () => {
      const config = loadProviderConfigFromEnv({
        PRIMARY_PROVIDER: 'claude-code',
        OPENAI_FALLBACK_ENABLED: 'true',
        ANTHROPIC_FALLBACK_ENABLED: 'true',
      });

      expect(config.primary).toBe('claude-code');
      expect(config.fallbacks).not.toContain('claude-code');
      expect(config.fallbacks).toContain('openai');
      expect(config.fallbacks).toContain('anthropic');
    });

    test('should handle fallback ordering', () => {
      const config = loadProviderConfigFromEnv({
        PRIMARY_PROVIDER: 'anthropic',
        CLAUDE_CODE_ENABLED: 'true',
        OPENAI_FALLBACK_ENABLED: 'true',
      });

      expect(config.primary).toBe('anthropic');
      expect(config.fallbacks).toEqual(['claude-code', 'openai']);
    });
  });

  describe('Environment Integration', () => {
    test('should handle undefined environment variables gracefully', () => {
      const config = loadProviderConfigFromEnv({
        PRIMARY_PROVIDER: undefined,
        CLAUDE_CODE_ENABLED: undefined,
        COST_OPTIMIZATION_ENABLED: undefined,
      });

      // Should use schema defaults
      expect(config.primary).toBe('claude-code');
      expect(config.costOptimization).toBe(true);
    });

    test('should handle string boolean conversion', () => {
      const config = loadProviderConfigFromEnv({
        ENABLE_PROVIDER_FALLBACK: 'false',
        COST_OPTIMIZATION_ENABLED: 'true',
      });

      expect(config.enableFallback).toBe(false);
      expect(config.costOptimization).toBe(true);
    });
  });
});