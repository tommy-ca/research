import { describe, it, expect, beforeEach, vi } from 'vitest';
import { SimilarityCalculatorInterface } from '@/types/quality-assessment';

/**
 * Workflow Orchestration Test Scenarios
 * TDD Cycle 1.4 - Advanced workflow routing and decision making
 */

interface WorkflowRule {
  name: string;
  condition: (qualityScore: number, isDuplicate: boolean, metadata: any) => boolean;
  action: 'accept' | 'review' | 'reject' | 'enhance' | 'archive';
  priority: number;
}

interface WorkflowContext {
  contentType: 'research' | 'note' | 'task' | 'reference' | 'draft';
  source: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  userPreferences: {
    qualityThreshold: number;
    strictMode: boolean;
    autoEnhance: boolean;
  };
}

class AdvancedWorkflowOrchestrator {
  private rules: WorkflowRule[] = [];
  
  constructor() {
    this.initializeDefaultRules();
  }

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

    // Sort by priority (highest first)
    this.rules.sort((a, b) => b.priority - a.priority);
  }

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
    // Apply rules in priority order
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
    return [...this.rules]; // Return copy
  }
}

describe('TDD Cycle 1.4 - Workflow Orchestration Test Scenarios', () => {
  let orchestrator: AdvancedWorkflowOrchestrator;

  beforeEach(() => {
    orchestrator = new AdvancedWorkflowOrchestrator();
  });

  describe('Content Type-Based Routing', () => {
    it('should apply higher standards to research content', () => {
      const researchContext: WorkflowContext = {
        contentType: 'research',
        source: 'academic-paper',
        urgency: 'medium',
        userPreferences: {
          qualityThreshold: 0.7,
          strictMode: true,
          autoEnhance: false
        }
      };

      // High quality research content
      const highQualityResult = orchestrator.orchestrateWorkflow(
        0.85, false, { context: researchContext }
      );
      expect(highQualityResult.action).toBe('accept');
      expect(highQualityResult.appliedRule).toBe('research-high-standard');
      expect(highQualityResult.confidence).toBeGreaterThan(0.8);

      // Moderate quality research content
      const moderateQualityResult = orchestrator.orchestrateWorkflow(
        0.75, false, { context: researchContext }
      );
      expect(moderateQualityResult.action).toBe('review');
      expect(moderateQualityResult.appliedRule).toBe('research-moderate-review');

      console.log(`✅ Research routing: High=${highQualityResult.action}, Moderate=${moderateQualityResult.action}`);
    });

    it('should handle notes and drafts with standard criteria', () => {
      const noteContext: WorkflowContext = {
        contentType: 'note',
        source: 'user-input',
        urgency: 'low',
        userPreferences: {
          qualityThreshold: 0.6,
          strictMode: false,
          autoEnhance: true
        }
      };

      const result = orchestrator.orchestrateWorkflow(
        0.65, false, { context: noteContext }
      );

      expect(result.action).toBe('accept');
      expect(result.appliedRule).toBe('standard-accept');
      
      console.log(`✅ Note routing: ${result.action} (${result.reasoning})`);
    });

    it('should prioritize tasks based on urgency', () => {
      const criticalTaskContext: WorkflowContext = {
        contentType: 'task',
        source: 'project-management',
        urgency: 'critical',
        userPreferences: {
          qualityThreshold: 0.7,
          strictMode: true,
          autoEnhance: false
        }
      };

      const result = orchestrator.orchestrateWorkflow(
        0.65, false, { context: criticalTaskContext }
      );

      // Should fast-track critical content even if slightly below research standards
      expect(result.action).toBe('accept');
      expect(result.appliedRule).toBe('critical-content-fast-track');
      expect(result.confidence).toBeGreaterThan(0.85);
      
      console.log(`✅ Critical task fast-tracked: ${result.confidence.toFixed(3)} confidence`);
    });
  });

  describe('User Preference Integration', () => {
    it('should respect custom quality thresholds', () => {
      const strictUserContext: WorkflowContext = {
        contentType: 'note',
        source: 'user-input',
        urgency: 'medium',
        userPreferences: {
          qualityThreshold: 0.9, // Very strict
          strictMode: true,
          autoEnhance: false
        }
      };

      const result = orchestrator.orchestrateWorkflow(
        0.85, false, { context: strictUserContext }
      );

      // Should require review because 0.85 < 0.9 threshold
      expect(result.action).toBe('review');
      expect(result.appliedRule).toBe('moderate-review');
      
      console.log(`✅ Strict threshold respected: 0.85 quality → ${result.action}`);
    });

    it('should enable auto-enhancement when user prefers it', () => {
      const autoEnhanceContext: WorkflowContext = {
        contentType: 'draft',
        source: 'document-editor',
        urgency: 'low',
        userPreferences: {
          qualityThreshold: 0.7,
          strictMode: false,
          autoEnhance: true
        }
      };

      const result = orchestrator.orchestrateWorkflow(
        0.55, false, { context: autoEnhanceContext }
      );

      // Should route to enhancement instead of review
      expect(result.action).toBe('enhance');
      expect(result.appliedRule).toBe('auto-enhance-enabled');
      
      console.log(`✅ Auto-enhancement triggered: ${result.reasoning}`);
    });
  });

  describe('Duplicate Detection Priority', () => {
    it('should always reject duplicates regardless of quality', () => {
      const perfectQualityDuplicate = orchestrator.orchestrateWorkflow(
        1.0, true, { 
          context: {
            contentType: 'research',
            source: 'academic-paper',
            urgency: 'critical',
            userPreferences: { qualityThreshold: 0.5, strictMode: false, autoEnhance: true }
          }
        }
      );

      expect(perfectQualityDuplicate.action).toBe('reject');
      expect(perfectQualityDuplicate.appliedRule).toBe('reject-duplicates');
      expect(perfectQualityDuplicate.confidence).toBeGreaterThan(0.9);
      
      console.log(`✅ Perfect quality duplicate rejected: ${perfectQualityDuplicate.confidence.toFixed(3)} confidence`);
    });
  });

  describe('Complex Decision Scenarios', () => {
    it('should handle edge case quality scores appropriately', () => {
      const edgeCaseContext: WorkflowContext = {
        contentType: 'reference',
        source: 'external-link',
        urgency: 'low',
        userPreferences: {
          qualityThreshold: 0.7,
          strictMode: false,
          autoEnhance: true
        }
      };

      // Test boundary conditions
      const scenarios = [
        { quality: 0.699, expected: 'review', description: 'just below threshold' },
        { quality: 0.700, expected: 'accept', description: 'exactly at threshold' },
        { quality: 0.701, expected: 'accept', description: 'just above threshold' },
        { quality: 0.419, expected: 'review', description: 'at 60% of threshold' },
        { quality: 0.418, expected: 'reject', description: 'just below 60% threshold' }
      ];

      scenarios.forEach(scenario => {
        const result = orchestrator.orchestrateWorkflow(
          scenario.quality, false, { context: edgeCaseContext }
        );
        
        expect(result.action).toBe(scenario.expected);
        console.log(`✅ Edge case ${scenario.description}: ${scenario.quality} → ${result.action}`);
      });
    });

    it('should provide appropriate confidence levels for decisions', () => {
      const testContext: WorkflowContext = {
        contentType: 'note',
        source: 'user-input',
        urgency: 'medium',
        userPreferences: {
          qualityThreshold: 0.6,
          strictMode: false,
          autoEnhance: false
        }
      };

      const scenarios = [
        { quality: 0.95, isDuplicate: false, expectedMinConfidence: 0.8 },
        { quality: 0.75, isDuplicate: false, expectedMinConfidence: 0.6 },
        { quality: 0.45, isDuplicate: false, expectedMinConfidence: 0.5 },
        { quality: 0.05, isDuplicate: false, expectedMinConfidence: 0.8 }, // Extreme low score
        { quality: 0.50, isDuplicate: true, expectedMinConfidence: 0.9 }   // Duplicate
      ];

      scenarios.forEach(scenario => {
        const result = orchestrator.orchestrateWorkflow(
          scenario.quality, scenario.isDuplicate, { context: testContext }
        );
        
        expect(result.confidence).toBeGreaterThanOrEqual(scenario.expectedMinConfidence);
        console.log(`✅ Confidence validation: Q=${scenario.quality}, D=${scenario.isDuplicate} → ${result.confidence.toFixed(3)}`);
      });
    });
  });

  describe('Custom Rule Management', () => {
    it('should allow adding custom rules with proper priority handling', () => {
      const customRule: WorkflowRule = {
        name: 'vip-user-bypass',
        condition: (_, __, metadata) => metadata.userType === 'vip',
        action: 'accept',
        priority: 95
      };

      orchestrator.addCustomRule(customRule);

      const result = orchestrator.orchestrateWorkflow(
        0.3, false, { 
          userType: 'vip',
          context: {
            contentType: 'note',
            source: 'user-input',
            urgency: 'low',
            userPreferences: { qualityThreshold: 0.7, strictMode: true, autoEnhance: false }
          }
        }
      );

      expect(result.action).toBe('accept');
      expect(result.appliedRule).toBe('vip-user-bypass');
      
      console.log(`✅ Custom VIP rule applied despite low quality (0.3)`);
    });

    it('should allow updating existing rules', () => {
      const updateSuccess = orchestrator.updateRule('standard-accept', {
        priority: 85 // Increase priority
      });

      expect(updateSuccess).toBe(true);
      
      const rules = orchestrator.getRules();
      const updatedRule = rules.find(r => r.name === 'standard-accept');
      expect(updatedRule?.priority).toBe(85);
      
      console.log(`✅ Rule update successful: standard-accept priority now 85`);
    });
  });

  describe('Workflow Performance and Scalability', () => {
    it('should perform rule evaluation efficiently', () => {
      const testContext: WorkflowContext = {
        contentType: 'note',
        source: 'batch-import',
        urgency: 'low',
        userPreferences: {
          qualityThreshold: 0.6,
          strictMode: false,
          autoEnhance: true
        }
      };

      const startTime = performance.now();
      
      // Process 1000 orchestration decisions
      for (let i = 0; i < 1000; i++) {
        const quality = Math.random();
        const isDuplicate = Math.random() < 0.1; // 10% duplicate rate
        orchestrator.orchestrateWorkflow(quality, isDuplicate, { context: testContext });
      }
      
      const duration = performance.now() - startTime;
      const avgPerDecision = duration / 1000;
      
      expect(avgPerDecision).toBeLessThan(1); // Should be very fast
      
      console.log(`✅ Orchestration performance: ${avgPerDecision.toFixed(3)}ms per decision`);
    });

    it('should handle missing context gracefully', () => {
      // Test with minimal context
      const result = orchestrator.orchestrateWorkflow(0.65, false, {});
      
      expect(result.action).toBeDefined();
      expect(result.appliedRule).toBeDefined();
      expect(result.confidence).toBeGreaterThan(0);
      
      console.log(`✅ Graceful handling of missing context: ${result.appliedRule}`);
    });
  });
});