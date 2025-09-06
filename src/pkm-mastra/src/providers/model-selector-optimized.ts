/**
 * SOLID-Optimized ModelSelector with proper separation of concerns
 * Single Responsibility: Each class has one reason to change
 * Open/Closed: Extensible without modification
 * Interface Segregation: Focused interfaces
 * Dependency Inversion: Depends on abstractions
 */

import { 
  ModelType, 
  TaskType, 
  TaskContext, 
  ModelSelectionRules,
  ComplexityThresholds,
  PerformanceConstraints 
} from '../types/model-types.js';
import { IModelSelector, SelectionReasoning } from '../interfaces/provider-interfaces.js';

// SOLID: Single Responsibility - Only handles complexity analysis
export class ComplexityAnalyzer {
  constructor(private thresholds: ComplexityThresholds) {}

  analyzeContent(content: string): number {
    // KISS: Simple scoring algorithm
    const lengthScore = Math.min(content.length / this.thresholds.contentLength, 1);
    const complexityIndicators = this.countComplexityIndicators(content);
    const indicatorScore = Math.min(complexityIndicators / 10, 1);
    
    return (lengthScore + indicatorScore) / 2;
  }

  analyzeTask(task: TaskType): number {
    // KISS: Simple task complexity mapping
    const complexTasks: TaskType[] = [
      'research-analysis',
      'complex-synthesis', 
      'quality-assessment',
      'deep-reasoning'
    ];
    
    return complexTasks.includes(task) ? 0.8 : 0.3;
  }

  // DRY: Reusable complexity detection
  private countComplexityIndicators(content: string): number {
    const indicators = [
      /analysis|research|evaluation/gi,
      /complex|intricate|sophisticated/gi,
      /multiple|various|several/gi,
      /\b\d+%|\b\d+\.\d+/g, // Numbers and percentages
      /[;:].*[;:]/g, // Multiple colons/semicolons (lists, complex structure)
    ];
    
    return indicators.reduce((count, pattern) => 
      count + (content.match(pattern)?.length || 0), 0
    );
  }
}

// SOLID: Single Responsibility - Only handles quality requirements
export class QualityAnalyzer {
  constructor(private qualityThreshold: number) {}

  requiresHighQuality(context: TaskContext): boolean {
    return (context.qualityRequirement || 0) > this.qualityThreshold;
  }

  calculateConfidence(
    task: TaskType, 
    content: string, 
    context: TaskContext,
    selectedModel: ModelType
  ): number {
    // KISS: Simple confidence calculation
    let confidence = 0.7; // Base confidence
    
    if (this.requiresHighQuality(context) && selectedModel === 'opus') {
      confidence += 0.2;
    }
    
    if (task.includes('research') && selectedModel === 'opus') {
      confidence += 0.15;
    }
    
    if (content.length < 100 && selectedModel === 'sonnet') {
      confidence += 0.1;
    }
    
    return Math.min(confidence, 1.0);
  }
}

// SOLID: Single Responsibility - Only handles performance constraints
export class PerformanceAnalyzer {
  constructor(private constraints: PerformanceConstraints) {}

  requiresSpeed(context: TaskContext): boolean {
    if (!context.maxResponseTime) return this.constraints.prioritizeSpeed;
    
    const sonnetTime = this.constraints.maxResponseTime.sonnet;
    return context.maxResponseTime <= sonnetTime;
  }

  canMeetConstraints(modelType: ModelType, context: TaskContext): boolean {
    if (!context.maxResponseTime) return true;
    
    const modelTime = this.constraints.maxResponseTime[modelType];
    return context.maxResponseTime >= modelTime;
  }
}

// SOLID: Single Responsibility - Only generates reasoning explanations  
export class SelectionReasoningGenerator {
  generateReasons(
    task: TaskType,
    content: string, 
    context: TaskContext,
    selectedModel: ModelType,
    overrides: { quality?: boolean; length?: boolean; performance?: boolean }
  ): string[] {
    const reasons: string[] = [];
    
    // DRY: Centralized reason templates
    const reasonTemplates = {
      quality: 'High quality requirement (>{threshold}%) requires best model',
      length: 'Content length ({length} chars) exceeds threshold ({threshold} chars)',
      performance: 'Performance constraints require speed optimization',
      task: 'Task type "{task}" requires high-quality analysis',
      fallback: 'Fallback to default model due to unknown task type'
    };
    
    if (overrides.quality) {
      reasons.push(reasonTemplates.quality.replace('{threshold}', '95'));
    }
    
    if (overrides.length) {
      reasons.push(reasonTemplates.length
        .replace('{length}', content.length.toString())
        .replace('{threshold}', '5000')
      );
    }
    
    if (overrides.performance) {
      reasons.push(reasonTemplates.performance);
    }
    
    if (!overrides.quality && !overrides.length && !overrides.performance) {
      const isComplexTask = ['research-analysis', 'complex-synthesis', 'quality-assessment', 'deep-reasoning'].includes(task);
      if (isComplexTask) {
        reasons.push(reasonTemplates.task.replace('{task}', task));
      } else {
        reasons.push('Simple task optimized for speed and efficiency');
      }
    }
    
    return reasons;
  }
}

// SOLID: Main ModelSelector class with dependency injection
export class OptimizedModelSelector implements IModelSelector {
  private complexityAnalyzer: ComplexityAnalyzer;
  private qualityAnalyzer: QualityAnalyzer;  
  private performanceAnalyzer: PerformanceAnalyzer;
  private reasoningGenerator: SelectionReasoningGenerator;

  constructor(private rules: ModelSelectionRules) {
    this.validateRules(rules);
    
    // SOLID: Dependency Injection of specialized analyzers
    this.complexityAnalyzer = new ComplexityAnalyzer(rules.complexityThresholds);
    this.qualityAnalyzer = new QualityAnalyzer(rules.complexityThresholds.qualityRequirement);
    this.performanceAnalyzer = new PerformanceAnalyzer(rules.performanceConstraints);
    this.reasoningGenerator = new SelectionReasoningGenerator();
  }

  // SOLID: Single Responsibility - Only orchestrates selection decision
  selectModel(task: TaskType, content: string, context: TaskContext = {}): ModelType {
    try {
      // KISS: Simple decision tree with clear priorities
      const overrides = this.checkOverrides(task, content, context);
      
      if (overrides.quality) return 'opus';
      if (overrides.performance) return 'sonnet';
      if (overrides.length) return 'opus';
      
      // Default to task mapping
      return this.rules.taskTypeMapping[task] || 'sonnet';
    } catch (error) {
      // KISS: Simple error handling
      return 'sonnet'; // Safe fallback
    }
  }

  getSelectionReasoning(task: TaskType, content: string, context: TaskContext = {}): SelectionReasoning {
    const selectedModel = this.selectModel(task, content, context);
    const overrides = this.checkOverrides(task, content, context);
    
    const reasons = this.reasoningGenerator.generateReasons(
      task, content, context, selectedModel, overrides
    );
    
    const confidence = this.qualityAnalyzer.calculateConfidence(
      task, content, context, selectedModel
    );
    
    return {
      selectedModel,
      reasons,
      confidence,
      fallbackApplied: !this.rules.taskTypeMapping[task] && selectedModel === 'sonnet'
    };
  }

  // DRY: Centralized override logic
  private checkOverrides(task: TaskType, content: string, context: TaskContext) {
    return {
      quality: this.qualityAnalyzer.requiresHighQuality(context),
      performance: this.performanceAnalyzer.requiresSpeed(context),
      length: content.length > this.rules.complexityThresholds.contentLength
    };
  }

  // SOLID: Single Responsibility - Only validates configuration
  private validateRules(rules: ModelSelectionRules): void {
    if (!rules?.taskTypeMapping || Object.keys(rules.taskTypeMapping).length === 0) {
      throw new Error('Task type mappings required');
    }

    if (!rules.complexityThresholds) {
      throw new Error('Complexity thresholds required');
    }

    const { complexityThresholds } = rules;
    if (complexityThresholds.contentLength < 0) {
      throw new Error('Content length threshold must be non-negative');
    }

    if (complexityThresholds.processingComplexity < 0 || complexityThresholds.processingComplexity > 1) {
      throw new Error('Processing complexity must be between 0 and 1');
    }

    if (complexityThresholds.qualityRequirement <= 0 || complexityThresholds.qualityRequirement > 1) {
      throw new Error('Quality requirement must be between 0 and 1');
    }
  }

  // Configuration access (for testing/debugging)
  getRules(): ModelSelectionRules {
    return { ...this.rules };
  }
}

// DRY: Default configuration factory
export function createDefaultModelSelector(): OptimizedModelSelector {
  const defaultRules: ModelSelectionRules = {
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

  return new OptimizedModelSelector(defaultRules);
}