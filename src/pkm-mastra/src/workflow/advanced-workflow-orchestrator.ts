/**
 * Advanced Workflow Orchestrator
 * TDD Cycle 1.4 - Sophisticated workflow routing and decision making
 * 
 * SOLID Principles:
 * - SRP: Single responsibility for workflow decision orchestration
 * - OCP: Open for extension through rule addition
 * - DIP: Depends on rule abstractions rather than concrete implementations
 */

export interface WorkflowRule {
  name: string;
  condition: (qualityScore: number, isDuplicate: boolean, metadata: any) => boolean;
  action: 'accept' | 'review' | 'reject' | 'enhance' | 'archive';
  priority: number;
}

export interface WorkflowContext {
  contentType: 'research' | 'note' | 'task' | 'reference' | 'draft';
  source: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  userPreferences: {
    qualityThreshold: number;
    strictMode: boolean;
    autoEnhance: boolean;
  };
}

export class AdvancedWorkflowOrchestrator {
  private rules: WorkflowRule[] = [];
  
  constructor() {
    this.initializeDefaultRules();
  }

  /**
   * KISS: Simple rule initialization with clear priorities
   */
  private initializeDefaultRules(): void {
    // High priority rules (checked first)
    this.rules = [
      {
        name: 'reject-duplicates',
        condition: (_, isDuplicate) => isDuplicate,
        action: 'reject',
        priority: 100
      },
      {
        name: 'critical-content-fast-track',
        condition: (qualityScore, _, metadata) => 
          metadata.context?.urgency === 'critical' && qualityScore > 0.6,
        action: 'accept',
        priority: 90
      },
      {
        name: 'research-high-standard',
        condition: (qualityScore, _, metadata) => 
          metadata.context?.contentType === 'research' && qualityScore > 0.8,
        action: 'accept',
        priority: 80
      },
      {
        name: 'research-moderate-review',
        condition: (qualityScore, _, metadata) => 
          metadata.context?.contentType === 'research' && 
          qualityScore > 0.6 && qualityScore <= 0.8,
        action: 'review',
        priority: 75
      },
      {
        name: 'notes-drafts-standard',
        condition: (qualityScore, isDuplicate, metadata) => 
          !isDuplicate && 
          (metadata.context?.contentType === 'note' || metadata.context?.contentType === 'draft') &&
          qualityScore > 0.5,
        action: 'accept',
        priority: 72
      },
      {
        name: 'auto-enhance-enabled',
        condition: (qualityScore, isDuplicate, metadata) => 
          !isDuplicate && 
          qualityScore > 0.4 && qualityScore < 0.7 && 
          metadata.context?.userPreferences?.autoEnhance === true,
        action: 'enhance',
        priority: 70
      },
      {
        name: 'standard-accept',
        condition: (qualityScore, isDuplicate, metadata) => 
          !isDuplicate && qualityScore >= metadata.context?.userPreferences?.qualityThreshold,
        action: 'accept',
        priority: 60
      },
      {
        name: 'edge-case-review',
        condition: (qualityScore, isDuplicate, metadata) => 
          !isDuplicate && 
          qualityScore >= 0.49 && qualityScore <= 0.51,
        action: 'review',
        priority: 55
      },
      {
        name: 'moderate-review',
        condition: (qualityScore, isDuplicate, metadata) => 
          !isDuplicate && 
          qualityScore >= (metadata.context?.userPreferences?.qualityThreshold * 0.6),
        action: 'review',
        priority: 50
      },
      {
        name: 'low-quality-reject',
        condition: (qualityScore, isDuplicate, metadata) => 
          qualityScore < (metadata.context?.userPreferences?.qualityThreshold * 0.6),
        action: 'reject',
        priority: 10
      }
    ];

    // DRY: Sort by priority once during initialization
    this.rules.sort((a, b) => b.priority - a.priority);
  }

  /**
   * Main orchestration method following SOLID principles
   */
  orchestrateWorkflow(
    qualityScore: number,
    isDuplicate: boolean,
    metadata: { context?: WorkflowContext; [key: string]: any }
  ): {
    action: 'accept' | 'review' | 'reject' | 'enhance' | 'archive';
    appliedRule: string;
    reasoning: string;
    confidence: number;
  } {
    // Apply rules in priority order - KISS principle
    for (const rule of this.rules) {
      if (rule.condition(qualityScore, isDuplicate, metadata)) {
        return {
          action: rule.action,
          appliedRule: rule.name,
          reasoning: this.generateReasoning(rule, qualityScore, isDuplicate, metadata),
          confidence: this.calculateConfidence(rule, qualityScore, isDuplicate, metadata)
        };
      }
    }

    // Fallback (should never reach here with current rules)
    return {
      action: 'review',
      appliedRule: 'fallback',
      reasoning: 'No rule matched - defaulting to manual review',
      confidence: 0.1
    };
  }

  /**
   * DRY: Extracted reasoning generation
   */
  private generateReasoning(
    rule: WorkflowRule,
    qualityScore: number,
    isDuplicate: boolean,
    metadata: any
  ): string {
    const context = metadata.context;
    
    switch (rule.name) {
      case 'reject-duplicates':
        return `Content rejected due to duplicate detection (similarity score too high)`;
      case 'critical-content-fast-track':
        return `Critical urgency content fast-tracked (quality: ${qualityScore.toFixed(3)})`;
      case 'research-high-standard':
        return `Research content meets high quality standards (${qualityScore.toFixed(3)})`;
      case 'research-moderate-review':
        return `Research content requires review - good but not excellent quality (${qualityScore.toFixed(3)})`;
      case 'auto-enhance-enabled':
        return `Content quality improvable with auto-enhancement (${qualityScore.toFixed(3)})`;
      case 'standard-accept':
        return `Content meets user quality threshold (${qualityScore.toFixed(3)} ≥ ${context?.userPreferences?.qualityThreshold})`;
      case 'moderate-review':
        return `Content quality warrants human review (${qualityScore.toFixed(3)})`;
      case 'low-quality-reject':
        return `Content quality below acceptable threshold (${qualityScore.toFixed(3)})`;
      default:
        return `Applied rule: ${rule.name}`;
    }
  }

  /**
   * DRY: Extracted confidence calculation algorithm
   */
  private calculateConfidence(
    rule: WorkflowRule,
    qualityScore: number,
    isDuplicate: boolean,
    metadata: any
  ): number {
    const context = metadata.context;
    
    // Base confidence from rule priority
    let confidence = rule.priority / 100;
    
    // Adjust confidence based on quality score certainty
    if (isDuplicate) {
      confidence = Math.max(confidence, 0.95); // High confidence for duplicates
    } else if (qualityScore > 0.9 || qualityScore < 0.1) {
      confidence = Math.max(confidence, 0.9); // High confidence for extreme scores
    } else if (qualityScore > 0.8 || qualityScore < 0.2) {
      confidence = Math.max(confidence, 0.8); // Good confidence
    }
    
    // Adjust for context clarity
    if (context?.contentType && context?.urgency && context?.userPreferences) {
      confidence *= 1.1; // Boost confidence when we have full context
    }
    
    return Math.min(confidence, 1.0);
  }

  // OCP: Open for extension through rule management
  addCustomRule(rule: WorkflowRule): void {
    this.rules.push(rule);
    this.rules.sort((a, b) => b.priority - a.priority);
  }

  updateRule(ruleName: string, updates: Partial<WorkflowRule>): boolean {
    const ruleIndex = this.rules.findIndex(r => r.name === ruleName);
    if (ruleIndex !== -1) {
      this.rules[ruleIndex] = { ...this.rules[ruleIndex], ...updates };
      this.rules.sort((a, b) => b.priority - a.priority);
      return true;
    }
    return false;
  }

  getRules(): WorkflowRule[] {
    return [...this.rules]; // Return copy to maintain encapsulation
  }
}