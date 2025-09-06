/**
 * Model and Task Type Definitions
 * DRY: Centralized type definitions to avoid duplication
 * KISS: Simple, clear type definitions
 */

// Core model types
export type ModelType = 'sonnet' | 'opus';

export type TaskType = 
  | 'content-capture'
  | 'metadata-generation'
  | 'basic-organization'
  | 'research-analysis'
  | 'complex-synthesis'
  | 'quality-assessment'
  | 'deep-reasoning';

export type ProviderType = 'claude-code' | 'openai' | 'anthropic';

// Task context for model selection
export interface TaskContext {
  qualityRequirement?: number;
  maxResponseTime?: number;
  processingComplexity?: number;
  priority?: 'speed' | 'quality' | 'balanced';
}

// Model selection configuration
export interface ModelSelectionRules {
  taskTypeMapping: Record<TaskType, ModelType>;
  complexityThresholds: ComplexityThresholds;
  performanceConstraints: PerformanceConstraints;
}

export interface ComplexityThresholds {
  contentLength: number;
  processingComplexity: number;
  qualityRequirement: number;
}

export interface PerformanceConstraints {
  maxResponseTime: Record<ModelType, number>;
  prioritizeSpeed: boolean;
}

// Provider configuration schema
export interface ProviderConfig {
  primary: ProviderType;
  fallbacks: ProviderType[];
  models: ModelConfiguration;
  subscriptionBased: boolean;
  costOptimization: boolean;
  enableFallback: boolean;
}

export interface ModelConfiguration {
  'claude-code': string;
  'claude-code-opus': string;
  'openai': string;
  'anthropic': string;
}

// Metrics and monitoring types
export interface ProviderMetrics {
  subscriptionUsage: SubscriptionUsage;
  fallbackCosts: FallbackCosts;
  routingDecisions: RoutingDecision[];
}

export interface SubscriptionUsage {
  remaining: number;
  resetDate: Date;
  provider: 'claude-pro' | 'claude-max';
}

export interface FallbackCosts {
  openai: number;
  anthropic: number;
}

export interface RoutingDecision {
  timestamp: Date;
  provider: string;
  reason: 'subscription' | 'fallback' | 'error' | 'selection';
  cost: number;
  metadata?: DecisionMetadata;
}

export interface DecisionMetadata {
  selectedModel?: ModelType;
  reasoning?: string[];
  confidence?: number;
}