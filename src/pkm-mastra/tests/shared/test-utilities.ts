/**
 * Shared Test Utilities
 * 
 * Common testing patterns and utilities to reduce duplication
 * and provide consistent test setup across the PKM system.
 */

import { vi } from 'vitest';

/**
 * Common mock factory for creating standardized mock objects
 */
export class MockFactory {
  /**
   * Create a mock with all methods stubbed
   */
  static createMockService<T extends Record<string, any>>(methods: (keyof T)[]): T {
    const mock = {} as T;
    for (const method of methods) {
      mock[method] = vi.fn() as any;
    }
    return mock;
  }

  /**
   * Reset all mocks - common beforeEach pattern
   */
  static resetAllMocks(): void {
    vi.clearAllMocks();
  }

  /**
   * Create standard PKM content input for testing
   */
  static createTestContentInput(overrides: Partial<{
    content: string;
    source: string;
    type: string;
    metadata: any;
  }> = {}) {
    return {
      content: 'Test content for PKM processing',
      source: 'test-source',
      type: 'text' as const,
      metadata: { testId: 'mock-test' },
      ...overrides,
    };
  }
}

/**
 * Common test data generators
 */
export class TestDataFactory {
  /**
   * Generate realistic test content for different domains
   */
  static generateContent(domain: 'technical' | 'business' | 'scientific', length: 'short' | 'medium' | 'long' = 'medium'): string {
    const templates = {
      technical: {
        short: 'Function implementation using SOLID principles',
        medium: 'Software architecture following SOLID principles includes single responsibility, open-closed design, and dependency inversion patterns for maintainable code.',
        long: 'Comprehensive software engineering approach incorporating SOLID principles, design patterns, and architectural best practices for scalable, maintainable systems with proper separation of concerns and testable interfaces.',
      },
      business: {
        short: 'Business process optimization strategy',
        medium: 'Lean startup methodology focuses on build-measure-learn cycles, minimum viable products, and validated learning to reduce market risk.',
        long: 'Strategic business development using lean startup principles, customer development, innovation accounting, and iterative product development to achieve product-market fit while minimizing resource waste.',
      },
      scientific: {
        short: 'Research methodology and analysis',
        medium: 'Scientific research methodology requires systematic observation, hypothesis formation, controlled experimentation, and peer review validation.',
        long: 'Comprehensive scientific research approach incorporating rigorous experimental design, statistical analysis, reproducible methodologies, and evidence-based conclusions with appropriate controls and validation measures.',
      },
    };
    
    return templates[domain][length];
  }
}

/**
 * Performance testing utilities
 */
export class PerformanceTestUtils {
  /**
   * Measure execution time of async operations
   */
  static async measureExecutionTime<T>(operation: () => Promise<T>): Promise<{ result: T; duration: number }> {
    const startTime = Date.now();
    const result = await operation();
    const duration = Date.now() - startTime;
    return { result, duration };
  }

  /**
   * Assert operation completes within time limit
   */
  static async assertWithinTimeLimit<T>(
    operation: () => Promise<T>, 
    timeLimitMs: number, 
    errorMessage?: string
  ): Promise<T> {
    const { result, duration } = await this.measureExecutionTime(operation);
    
    if (duration > timeLimitMs) {
      throw new Error(
        errorMessage || `Operation took ${duration}ms, expected < ${timeLimitMs}ms`
      );
    }
    
    return result;
  }
}

/**
 * Quality assertion helpers
 */
export class QualityAssertions {
  /**
   * Assert quality score within expected range
   */
  static assertQualityRange(score: number, min: number, max: number, context?: string): void {
    if (score < min || score > max) {
      throw new Error(
        `Quality score ${score} outside expected range [${min}, ${max}]${context ? ` for ${context}` : ''}`
      );
    }
  }

  /**
   * Assert PARA category is valid
   */
  static assertValidPARACategory(category: string): void {
    const validCategories = ['projects', 'areas', 'resources', 'archive'];
    if (!validCategories.includes(category)) {
      throw new Error(`Invalid PARA category: ${category}. Must be one of: ${validCategories.join(', ')}`);
    }
  }
}