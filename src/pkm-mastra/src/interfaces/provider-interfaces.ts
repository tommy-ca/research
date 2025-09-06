/**
 * Provider Interfaces following SOLID Interface Segregation Principle
 * Each interface has a single, focused responsibility
 */

import { ModelType, TaskType, TaskContext } from '../types/model-types.js';

// SOLID: Interface Segregation - Separate concerns into focused interfaces

/**
 * Core model selection interface
 * Single responsibility: Model selection logic
 */
export interface IModelSelector {
  selectModel(task: TaskType, content: string, context?: TaskContext): ModelType;
  getSelectionReasoning(task: TaskType, content: string, context?: TaskContext): SelectionReasoning;
}

/**
 * Model creation interface
 * Single responsibility: Model instance creation
 */
export interface IModelFactory {
  createModel(providerType?: string, modelType?: ModelType): Promise<LanguageModel>;
  testProvider(provider: string, modelType?: ModelType): Promise<boolean>;
}

/**
 * Configuration management interface
 * Single responsibility: Configuration handling
 */
export interface IConfigurable<T> {
  getConfig(): T;
  updateConfig(newConfig: Partial<T>): void;
  validateConfig(config: T): void;
}

/**
 * Metrics collection interface
 * Single responsibility: Metrics and monitoring
 */
export interface IMetricsCollector<T> {
  getMetrics(): T;
  logDecision(decision: any): void;
  clearMetrics(): void;
}

/**
 * Fallback handling interface
 * Single responsibility: Error recovery and fallback logic
 */
export interface IFallbackHandler {
  createFallbackProvider(failedProvider: string, error: Error): Promise<LanguageModel>;
  getAvailableProviders(): string[];
  estimateCost(provider: string): number;
}

// Supporting types (DRY: Centralized type definitions)
export interface LanguageModel {
  model: string;
  provider: string;
}

export interface SelectionReasoning {
  selectedModel: ModelType;
  reasons: string[];
  confidence: number;
  fallbackApplied: boolean;
}

export interface RoutingDecision {
  timestamp: Date;
  provider: string;
  reason: 'subscription' | 'fallback' | 'error' | 'selection';
  cost: number;
  metadata?: {
    selectedModel?: ModelType;
    reasoning?: string[];
    confidence?: number;
  };
}

// SOLID: Dependency Inversion - Depend on abstractions
export interface IProviderFactory extends 
  IModelFactory, 
  IConfigurable<any>, 
  IMetricsCollector<any>,
  IFallbackHandler {
  
  // Enhanced interface combining focused interfaces
  createModelWithSelection(task: TaskType, content: string, context?: TaskContext): Promise<LanguageModel>;
}