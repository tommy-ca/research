/**
 * Model Selector for intelligent Claude 3.5 Sonnet + Claude 3 Opus selection
 * Following SOLID principles with Single Responsibility for model selection logic
 */

// Core Types (KISS: Simple, clear type definitions)
export type ModelType = 'sonnet' | 'opus';

export type TaskType = 
  | 'content-capture'
  | 'metadata-generation'
  | 'basic-organization'
  | 'research-analysis'
  | 'complex-synthesis'
  | 'quality-assessment'
  | 'deep-reasoning';

export interface TaskContext {
  qualityRequirement?: number;
  maxResponseTime?: number;
  processingComplexity?: number;
  priority?: 'speed' | 'quality' | 'balanced';
}

export interface SelectionReasoning {
  selectedModel: ModelType;
  reasons: string[];
  confidence: number;
  fallbackApplied: boolean;
}

// Configuration Schema (DRY: Centralized configuration)
export interface ModelSelectionRules {
  taskTypeMapping: Record<TaskType, ModelType>;
  complexityThresholds: {
    contentLength: number;
    processingComplexity: number;
    qualityRequirement: number;
  };
  performanceConstraints: {
    maxResponseTime: Record<ModelType, number>;
    prioritizeSpeed: boolean;
  };
}

// Default configuration (DRY: Reusable defaults)
export const defaultModelSelectionRules: ModelSelectionRules = {
  taskTypeMapping: {
    'content-capture': 'sonnet',
    'metadata-generation': 'sonnet',
    'basic-organization': 'sonnet',
    'research-analysis': 'opus',
    'complex-synthesis': 'opus',
    'quality-assessment': 'opus',
    'deep-reasoning': 'opus',
  },
  complexityThresholds: {
    contentLength: 5000,
    processingComplexity: 0.7,
    qualityRequirement: 0.95,
  },
  performanceConstraints: {
    maxResponseTime: {
      'sonnet': 2000,
      'opus': 10000,
    },
    prioritizeSpeed: false,
  },
};

/**
 * ModelSelector - SOLID Single Responsibility for model selection
 * KISS - Simple, clear logic for making selection decisions
 * DRY - Reuses configuration and validation logic
 */
export class ModelSelector {
  private rules: ModelSelectionRules;

  constructor(rules: ModelSelectionRules = defaultModelSelectionRules) {
    this.validateRules(rules);
    this.rules = rules;
  }

  /**
   * Select optimal model based on task, content, and context
   * KISS: Simple decision tree logic
   */
  selectModel(task: TaskType, content: string, context: TaskContext = {}): ModelType {
    try {
      // Quality requirement override (highest priority)
      if (context.qualityRequirement && context.qualityRequirement > this.rules.complexityThresholds.qualityRequirement) {
        return 'opus';
      }

      // Performance constraint override
      if (this.rules.performanceConstraints.prioritizeSpeed && context.maxResponseTime) {
        const sonnetTime = this.rules.performanceConstraints.maxResponseTime.sonnet;
        if (context.maxResponseTime <= sonnetTime) {
          return 'sonnet';
        }
      }

      // Content length override
      if (content.length > this.rules.complexityThresholds.contentLength) {
        return 'opus';
      }

      // Processing complexity override
      if (context.processingComplexity && context.processingComplexity > this.rules.complexityThresholds.processingComplexity) {
        return 'opus';
      }

      // Default to task type mapping
      return this.rules.taskTypeMapping[task] || 'sonnet';
    } catch (error) {
      // Graceful fallback on any selection error
      return 'sonnet';
    }
  }

  /**
   * Provide detailed reasoning for selection decision
   * SOLID: Single responsibility for generating explanations
   */
  getSelectionReasoning(task: TaskType, content: string, context: TaskContext = {}): SelectionReasoning {
    const selectedModel = this.selectModel(task, content, context);
    const reasons: string[] = [];
    let confidence = 0.8; // Base confidence

    // Build reasoning chain
    if (context.qualityRequirement && context.qualityRequirement > this.rules.complexityThresholds.qualityRequirement) {
      reasons.push('High quality requirement');
      confidence = 0.95;
    } else if (content.length > this.rules.complexityThresholds.contentLength) {
      reasons.push('Content length exceeds threshold');
      confidence = 0.9;
    } else if (context.processingComplexity && context.processingComplexity > this.rules.complexityThresholds.processingComplexity) {
      reasons.push('High processing complexity');
      confidence = 0.85;
    } else {
      reasons.push('Task type requires high-quality analysis');
      if (this.rules.taskTypeMapping[task]) {
        confidence = 0.85;
      } else {
        reasons.push('Fallback to default model');
        confidence = 0.6;
      }
    }

    // Performance considerations
    if (this.rules.performanceConstraints.prioritizeSpeed && selectedModel === 'sonnet') {
      reasons.push('Speed optimization enabled');
      confidence += 0.1;
    }

    return {
      selectedModel,
      reasons,
      confidence: Math.min(confidence, 1.0),
      fallbackApplied: !this.rules.taskTypeMapping[task] && selectedModel === 'sonnet',
    };
  }

  /**
   * Validate configuration rules
   * SOLID: Single responsibility for validation
   * KISS: Simple validation checks
   */
  private validateRules(rules: ModelSelectionRules): void {
    if (!rules) {
      throw new Error('Invalid model selection rules: rules cannot be null or undefined');
    }

    if (!rules.taskTypeMapping || Object.keys(rules.taskTypeMapping).length === 0) {
      throw new Error('Task type mappings required');
    }

    if (!rules.complexityThresholds) {
      throw new Error('Complexity thresholds required');
    }

    const { complexityThresholds } = rules;
    
    if (complexityThresholds.contentLength < 0) {
      throw new Error('Invalid model selection rules: contentLength must be non-negative');
    }

    if (complexityThresholds.processingComplexity < 0 || complexityThresholds.processingComplexity > 1) {
      throw new Error('Invalid model selection rules: processingComplexity must be between 0 and 1');
    }

    if (complexityThresholds.qualityRequirement <= 0 || complexityThresholds.qualityRequirement > 1) {
      throw new Error('Invalid model selection rules: qualityRequirement must be between 0 and 1');
    }

    if (!rules.performanceConstraints) {
      throw new Error('Performance constraints required');
    }
  }

  /**
   * Get current configuration (for testing/debugging)
   */
  getRules(): ModelSelectionRules {
    return { ...this.rules }; // Return copy to prevent mutation
  }
}