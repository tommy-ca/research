# PKM Mastra.ai System Specification

## Document Information
- **Document Type**: Mastra.ai-Based PKM Pipeline System Specification
- **Version**: 6.0.0 - Claude Code SDK Ingestion Pipeline Integration
- **Created**: 2024-09-05
- **Updated**: 2025-09-06 (Claude Code SDK + PKM Ingestion Pipelines + TDD Implementation)
- **Framework**: Mastra.ai 2025 TypeScript AI Agent Framework (v0.16.0+)
- **API Compatibility**: AI SDK v5 Support, Claude Code Provider, Workflow Orchestration
- **LLM Integration**: Claude Code with Sonnet/Opus Model Selection + Multi-Provider Fallbacks
- **Engineering Standards**: SOLID, KISS, DRY, Specs-Driven TDD Methodology
- **Naming Convention**: Consistent naming without Enhanced/Advanced prefixes
- **Focus**: Production-ready PKM ingestion automation with intelligent Claude model selection
- **Ingestion Spec**: PKM_CLAUDE_CODE_SDK_INGESTION_SPEC.md

## Executive Summary

This specification defines a PKM (Personal Knowledge Management) system built on mastra.ai framework, leveraging its agent orchestration, workflow management, memory systems, and evaluation capabilities to create intelligent PKM pipeline automation. **Built with systematic engineering principles integration**, this system maintains strict compliance with established methodologies (PARA, Zettelkasten, GTD) while enforcing SOLID architecture, KISS simplicity, DRY maintainability, and comprehensive specs-driven TDD methodology.

**v6.0.0 Updates**: This version integrates comprehensive PKM ingestion pipeline architecture with Claude Code SDK-first implementation. See `specs/PKM_CLAUDE_CODE_SDK_INGESTION_SPEC.md` for detailed ingestion pipeline requirements, TDD specifications, and implementation architecture.

## PKM Ingestion Pipeline Integration (v6.0.0)

### Claude Code SDK-First Ingestion Architecture

**Comprehensive Ingestion System**:
- **Multi-Format Processing**: Text, PDF, web content, documents with intelligent model selection
- **Atomic Note Generation**: One-concept-per-note with quality validation
- **Intelligent Metadata**: Automatic PARA classification, entity extraction, link suggestions
- **Quality Assessment**: Multi-dimensional scoring with improvement recommendations

**Model Selection for Ingestion**:
```typescript
interface PKMIngestionModelSelection {
  // Fast processing for standard content
  sonnet: {
    tasks: ['text-extraction', 'basic-metadata', 'format-conversion', 'quick-categorization'];
    criteria: 'content <5000 chars, processing <2s, accuracy >90%';
  };
  
  // Quality processing for complex content
  opus: {
    tasks: ['concept-extraction', 'semantic-analysis', 'quality-assessment', 'research-synthesis'];
    criteria: 'content >5000 chars OR complex, quality >95%, deep analysis';
  };
}
```

**Implementation Requirements**:
- **FR-PKM-INGEST-001**: Content Ingestion Engine with multi-format support
- **FR-PKM-INGEST-002**: Atomic Note Generation with atomicity validation
- **FR-PKM-INGEST-003**: Intelligent Metadata Extraction with PARA classification
- **FR-PKM-INGEST-004**: Quality Assessment Pipeline with improvement suggestions

**Success Metrics**:
- Processing Speed: <3s simple, <10s complex content
- Quality: >95% extraction fidelity, >90% atomicity compliance
- Model Selection: >85% optimal cost/quality balance
- User Acceptance: >85% satisfaction with processing results

## Engineering Principles Foundation

### Core Engineering Standards
- **Specs-Driven TDD**: Specification-first RED-GREEN-REFACTOR-VALIDATE-EVALUATE methodology
- **SOLID Architecture**: Systematic application across all agents and components  
- **KISS Principle**: Simplicity-first design with complexity metrics enforcement
- **DRY Compliance**: Zero duplication tolerance with automated detection
- **Performance Engineering**: <100ms response time requirements with continuous monitoring
- **Quality Gates**: Automated engineering compliance validation at every stage
- **Consistent Naming**: No Enhanced/Advanced prefixes, clear descriptive names

## Claude Model Selection Strategy

### Intelligent Model Selection Architecture

**Sonnet vs Opus Selection Criteria**:
```typescript
interface ModelSelectionStrategy {
  // High-performance tasks: Research, complex analysis, synthesis
  opus: ['research-analysis', 'complex-synthesis', 'deep-reasoning'];
  
  // Standard tasks: Capture, organization, basic processing
  sonnet: ['content-capture', 'organization', 'basic-processing'];
  
  // Automatic selection based on task complexity and content length
  autoSelect: (task: TaskType, contentLength: number) => 'opus' | 'sonnet';
}
```

**Model Configuration**:
- **Claude 3.5 Sonnet**: Fast, efficient for standard PKM operations
- **Claude 3 Opus**: High-quality for complex research and analysis tasks
- **Automatic Selection**: Based on task complexity, content length, and performance requirements
- **Cost Optimization**: Intelligent routing to minimize subscription usage

### Specs-Driven TDD Methodology Integration

```typescript
interface SpecsDrivenTDDCycle {
  SPECS: {
    writeSpecifications: SpecificationDocument[];
    defineAcceptanceCriteria: AcceptanceCriteria[];
    establishSuccessMetrics: SuccessMetrics;
  };
  RED: {
    writeFailingTests: Test[];
    validateTestQuality: QualityMetrics;
    ensureSOLIDCompliance: SOLIDValidation;
  };
  GREEN: {
    implementMinimalCode: Implementation;
    validateKISSPrinciple: ComplexityMetrics;
    enforceDRYPrinciple: DuplicationAnalysis;
  };
  REFACTOR: {
    improveCodeQuality: RefactorActions[];
    validateSOLIDPrinciples: ArchitectureValidation;
    optimizePerformance: PerformanceMetrics;
  };
  VALIDATE: {
    functionalCorrectness: ValidationResults;
    nonFunctionalRequirements: NFRValidation;
    integrationTesting: IntegrationResults;
  };
  EVALUATE: {
    qualityAssessment: QualityScore;
    performanceBaseline: PerformanceBenchmarks;
    maintainabilityIndex: MaintainabilityMetrics;
  };
}
```

## Naming Convention Standards

### Consistent Naming Architecture

**File Naming Convention**:
- `capture-agent.ts` (not `enhanced-capture-agent.ts`)
- `capture-workflow.ts` (not `enhanced-capture-workflow.ts`)
- `metadata-generator.ts` (not `enhanced-metadata-generator.ts`)

**Class Naming Convention**:
```typescript
// ✅ Correct: Clear, descriptive names
class CaptureAgent { }
class CaptureWorkflow { }
class MetadataGenerator { }

// ❌ Incorrect: Unnecessary prefixes
class EnhancedCaptureAgent { }
class AdvancedCaptureWorkflow { }
class SuperMetadataGenerator { }
```

**Function Naming Convention**:
```typescript
// ✅ Correct: Action-based naming
function captureContent(content: string): CaptureResult;
function processWorkflow(workflow: Workflow): ProcessResult;
function generateMetadata(input: Input): Metadata;

// ❌ Incorrect: Enhanced/Advanced prefixes
function enhancedCaptureContent(content: string): CaptureResult;
function advancedProcessWorkflow(workflow: Workflow): ProcessResult;
```

### SOLID Principles Application

**Single Responsibility Principle (SRP)**
```typescript
// Each agent has a single, well-defined responsibility
interface CaptureAgent {
  capture(input: CaptureInput): Promise<CaptureOutput>;
}

interface ProcessingAgent {
  process(input: ProcessingInput): Promise<ProcessingOutput>;
}

interface OrganizationAgent {
  organize(input: OrganizationInput): Promise<OrganizationOutput>;
}
```

**Open/Closed Principle (OCP)**
```typescript
// Extensible LLM provider system without modification
interface LLMProvider {
  process(content: string): Promise<ProcessedContent>;
}

class ClaudeCodeProvider implements LLMProvider { } // Subscription-based, no API keys
class OpenAIProvider implements LLMProvider { }     // API key fallback
class AnthropicProvider implements LLMProvider { }  // API key fallback  
class GoogleProvider implements LLMProvider { }     // API key fallback
// New providers can be added without modifying existing code
```

**Liskov Substitution Principle (LSP)**
```typescript
// All processing agents must be substitutable
interface ProcessingAgent {
  process(input: ProcessingInput): Promise<ProcessingOutput>;
}
// Any implementation must work with the same interface contract
```

**Interface Segregation Principle (ISP)**  
```typescript
// Separate interfaces for different capabilities
interface Capturable { capture(): CaptureResult; }
interface Processable { process(): ProcessingResult; }
interface Storable { store(): StorageResult; }
interface Retrievable { retrieve(): RetrievalResult; }
```

**Dependency Inversion Principle (DIP)**
```typescript
// Depend on abstractions, not concretions
class PKMSystem {
  constructor(
    private captureService: CaptureInterface,
    private processingService: ProcessingInterface,
    private storageService: StorageInterface
  ) {}
}
```

### Quality Gates Framework

```typescript
interface QualityGate {
  name: string;
  validator: (code: string, tests: Test[]) => Promise<QualityResult>;
  threshold: number; // Minimum score to pass (0.0-1.0)
  blocking: boolean; // Whether failure blocks progression
}

const engineeringQualityGates: QualityGate[] = [
  {
    name: 'SOLID Compliance',
    validator: validateSOLIDPrinciples,
    threshold: 0.85,
    blocking: true
  },
  {
    name: 'KISS Principle',
    validator: validateComplexity,
    threshold: 0.8,
    blocking: true
  },
  {
    name: 'DRY Principle',
    validator: validateDuplication,
    threshold: 0.9,
    blocking: true
  },
  {
    name: 'Test Coverage',
    validator: validateTestCoverage,
    threshold: 1.0, // 100% coverage required
    blocking: true
  },
  {
    name: 'Performance Compliance',
    validator: validatePerformance,
    threshold: 0.95,
    blocking: false // Warning initially, blocking in production
  },
  {
    name: 'Type Safety',
    validator: validateTypeScript,
    threshold: 1.0, // Zero TypeScript errors
    blocking: true
  }
];
```

### Performance Engineering Standards

```typescript
interface PerformanceRequirements {
  responseTime: {
    capture: number;      // <50ms
    processing: number;   // <100ms  
    organization: number; // <75ms
    retrieval: number;    // <25ms
    synthesis: number;    // <200ms
  };
  throughput: {
    minOperationsPerSecond: 100;
    maxConcurrentUsers: 50;
  };
  resources: {
    maxMemoryUsage: 50; // MB
    maxCPUUsage: 70;    // %
  };
}
```

## 1. Mastra.ai Architecture Integration

### 1.1 Core Framework Capabilities

**Mastra.ai Foundation**:
- **Agent Orchestration**: Production-ready agent lifecycle management
- **Multi-LLM Support**: Priority-based provider system with Claude Code (subscription), OpenAI, Anthropic, Gemini fallbacks
- **Subscription Model**: Claude Code provider leverages Claude Pro/Max subscriptions without API keys
- **Cost Optimization**: Automatic provider selection based on availability and subscription status
- **Workflow Graphs**: State machines for complex PKM pipeline transitions
- **Memory Management**: Long-term and short-term context with vault awareness
- **Built-in Evaluation**: Automated quality assessment and compliance validation
- **OpenTelemetry Tracing**: Complete observability for debugging and optimization

### 1.2 PKM System Architecture on Mastra.ai 2025

```typescript
// PKM System Architecture - Updated for Mastra 2025
export interface PkmMastraSystem {
  agents: {
    captureAgent: Agent;     // C1: Multi-source content ingestion
    processingAgent: Agent;  // P1: Atomic note creation and structuring
    organizationAgent: Agent; // O1: PARA classification and hierarchy
    retrievalAgent: Agent;   // R1: Semantic search and discovery
    reviewAgent: Agent;      // V1: Knowledge maintenance and freshness
    synthesisAgent: Agent;   // S1: Pattern recognition and insights
  };
  workflows: {
    pkmPipeline: ReturnType<typeof createWorkflow>;   // Master PKM pipeline
    captureWorkflow: ReturnType<typeof createWorkflow>; // Capture → Processing
    organizationWorkflow: ReturnType<typeof createWorkflow>; // Processing → Organization
    maintenanceWorkflow: ReturnType<typeof createWorkflow>; // Scheduled maintenance
  };
  steps: {
    captureStep: ReturnType<typeof createStep>;      // Typed capture step
    processStep: ReturnType<typeof createStep>;      // Atomic processing step
    organizationStep: ReturnType<typeof createStep>; // PARA classification step
    validationStep: ReturnType<typeof createStep>;   // Quality validation step
  };
  memory: {
    vaultContext: Memory;    // Dynamic vault context with semantic retrieval
    userPreferences: Memory; // Adaptive PKM preferences learning
    conversationHistory: Memory; // Thread-aware conversation context
    methodologyPatterns: Memory; // PARA/Zettelkasten pattern recognition
  };
  tools: {
    vaultOperations: Tool[];  // Enhanced file operations with type safety
    qualityAssessment: Tool[]; // Comprehensive content quality scoring
    duplicateDetection: Tool[]; // Vector-based semantic duplicate detection
    linkSuggestion: Tool[];   // Intelligent bi-directional link discovery
    metadataExtraction: Tool[]; // Advanced metadata enrichment
  };
  evaluations: {
    atomicityEval: Evaluation;    // Zettelkasten atomicity compliance
    paraClassificationEval: Evaluation; // PARA method accuracy assessment
    captureCompletenessEval: Evaluation; // GTD capture fidelity validation
    linkQualityEval: Evaluation;  // Connection relevance and quality
    overallSystemEval: Evaluation; // Comprehensive system performance
  };
}
```

### 1.3 Enhanced Workflow Integration Pattern (2025)

```typescript
// Modern Mastra 2025 Workflow Pattern with createStep and createWorkflow
import { createStep, createWorkflow } from '@mastra/core';
import { z } from 'zod';

// Define typed steps for better composition
const captureStep = createStep({
  id: 'capture',
  inputSchema: z.object({
    content: z.string(),
    source: z.string(),
    metadata: z.record(z.any()).optional(),
  }),
  outputSchema: z.object({
    id: z.string(),
    capturedContent: z.string(),
    extractedMetadata: z.record(z.any()),
    qualityScore: z.number().min(0).max(1),
    processed: z.boolean(),
  }),
  execute: async ({ input, context }) => {
    // Use agent within step execution
    const result = await context.agents.captureAgent.generate({
      messages: [{ 
        role: 'user', 
        content: `Process this content: ${input.content} from source: ${input.source}` 
      }],
    });
    
    return {
      id: `capture_${Date.now()}`,
      capturedContent: result.text,
      extractedMetadata: input.metadata || {},
      qualityScore: 0.8, // From quality assessment tool
      processed: true,
    };
  },
});

const processingStep = createStep({
  id: 'processing',
  inputSchema: z.object({
    capturedContent: z.string(),
    extractedMetadata: z.record(z.any()),
    qualityScore: z.number(),
  }),
  outputSchema: z.object({
    atomicNotes: z.array(z.object({
      id: z.string(),
      title: z.string(),
      content: z.string(),
      atomicityScore: z.number(),
      suggestedLinks: z.array(z.string()),
    })),
    atomicityValidated: z.boolean(),
  }),
  execute: async ({ input, context }) => {
    // Advanced processing with atomicity validation
    const result = await context.agents.processingAgent.generate({
      messages: [{
        role: 'user',
        content: `Create atomic notes from: ${input.capturedContent}`
      }],
    });
    
    return {
      atomicNotes: [
        {
          id: `note_${Date.now()}`,
          title: "Generated Note",
          content: result.text,
          atomicityScore: 0.9,
          suggestedLinks: [],
        }
      ],
      atomicityValidated: true,
    };
  },
});

// Enhanced PKM Pipeline with modern Mastra patterns
const pkmPipelineWorkflow = createWorkflow({
  name: 'pkm-pipeline-2025',
  triggerSchema: z.object({
    content: z.string(),
    source: z.string(),
    metadata: z.record(z.any()).optional(),
  }),
  outputSchema: z.object({
    success: z.boolean(),
    capturedId: z.string(),
    processedNotes: z.array(z.string()),
    organizationResult: z.object({
      paraCategory: z.string(),
      confidence: z.number(),
    }),
  }),
})
.then(captureStep) 
.then(processingStep)
.then(organizationStep)  // To be defined
.commit(); // Complete workflow definition

// Execution with full type safety and streaming support
async function executePkmPipeline(input: { content: string; source: string; metadata?: any }) {
  const result = await pkmPipelineWorkflow.execute(input);
  
  // Full type safety and error handling
  if (result.status === 'success') {
    return result.output;
  } else if (result.status === 'suspended') {
    // Handle suspension for human input
    console.log('Workflow suspended for human review');
  } else {
    // Handle failure with detailed error information
    console.error('Workflow failed:', result.error);
  }
}
```

## 1.4 Claude Code Provider Integration Architecture

### 1.4.1 Provider Integration Strategy

**Subscription-First Architecture**: The system prioritizes Claude Code provider to leverage Claude Pro/Max subscriptions, reducing API costs while providing intelligent model selection between Claude 3.5 Sonnet and Claude 3 Opus based on task complexity.

**Intelligent Multi-Model System**:
```typescript
interface ProviderConfig {
  primary: 'claude-code';
  fallbacks: ['openai', 'anthropic'];
  models: {
    'claude-code-sonnet': 'claude-3-5-sonnet-20241022';
    'claude-code-opus': 'claude-3-opus-20240229';
    'openai': 'gpt-4o-mini';
    'anthropic': 'claude-3-haiku-20240307';
  };
  modelSelection: {
    default: 'claude-code-sonnet';
    complexTasks: 'claude-code-opus';
    selectionStrategy: ModelSelectionStrategy;
  };
  subscriptionBased: boolean;
  costOptimization: boolean;
}
```

**Model Selection Strategy**:
```typescript
interface ModelSelectionStrategy {
  selectModel(task: TaskType, content: string, context: TaskContext): 'sonnet' | 'opus';
  
  // Sonnet: Fast, efficient for standard operations
  sonnetTasks: [
    'content-capture',
    'basic-organization', 
    'metadata-generation',
    'simple-processing'
  ];
  
  // Opus: High-quality for complex operations  
  opusTasks: [
    'research-analysis',
    'complex-synthesis',
    'deep-reasoning',
    'quality-assessment'
  ];
  
  // Auto-selection criteria
  criteria: {
    contentLength: number;    // >5000 chars → Opus
    complexity: number;       // >0.7 score → Opus  
    processingTime: number;   // <100ms required → Sonnet
    qualityRequired: number;  // >0.9 required → Opus
  };
}
```

### 1.4.2 Provider Factory Implementation

**SOLID-Compliant Provider Factory with Intelligent Model Selection**:
```typescript
// Single Responsibility: Provider creation and management
class ProviderFactory {
  private config: ProviderConfig;
  private modelSelector: ModelSelectionStrategy;
  
  constructor(config: ProviderConfig) {
    this.config = config;
    this.modelSelector = new ModelSelectionStrategy(config);
  }
  
  // Open/Closed: Extensible for new providers and models
  async createModel(
    task?: TaskType, 
    content?: string, 
    context?: TaskContext
  ): Promise<MastraCompatibleModel> {
    
    // Intelligent model selection for Claude Code
    if (this.config.primary === 'claude-code') {
      const selectedModel = this.modelSelector.selectModel(task, content, context);
      return await this.createClaudeCodeProvider(selectedModel);
    }
    
    // Fallback providers
    return await this.createFallbackProvider();
  }
  
  private async createClaudeCodeProvider(model: 'sonnet' | 'opus'): Promise<MastraCompatibleModel> {
    const { claudeCode } = await import('ai-sdk-provider-claude-code');
    
    const modelId = model === 'opus' 
      ? this.config.models['claude-code-opus']
      : this.config.models['claude-code-sonnet'];
    
    return claudeCode(modelId, {
      // Subscription-based configuration - no API key required
      useSubscription: true,
      fallbackOnError: true,
      // Performance optimization based on model
      temperature: model === 'opus' ? 0.1 : 0.3,
      maxTokens: model === 'opus' ? 4000 : 2000,
    });
  }
  
  // KISS: Simple fallback mechanism
  private async createFallbackProvider(): Promise<MastraCompatibleModel> {
    for (const fallback of this.config.fallbacks) {
      try {
        switch (fallback) {
          case 'openai':
            return openai(this.config.models.openai);
          case 'anthropic':
            return anthropic(this.config.models.anthropic);
        }
      } catch (error) {
        continue; // Try next fallback
      }
    }
    throw new Error('All providers failed');
  }
  
  private async createFallbackProvider(failedProvider: string): Promise<MastraCompatibleModel> {
    const fallbacks = this.config.fallbacks.filter(p => p !== failedProvider);
    for (const fallback of fallbacks) {
      try {
        return await this.createModel(fallback);
      } catch (error) {
        continue; // Try next fallback
      }
    }
    throw new Error('All providers failed');
  }
}
```

### 1.4.3 Enhanced Agent Integration

**Updated Enhanced Capture Agent**:
```typescript
import { claudeCode } from 'ai-sdk-provider-claude-code';
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';

export class EnhancedCaptureAgent {
  private providerFactory: ProviderFactory;
  private agent: Agent;
  
  constructor(config: ProviderConfig) {
    this.providerFactory = new ProviderFactory(config);
    this.initializeAgent();
  }
  
  private async initializeAgent() {
    const model = await this.providerFactory.createModel();
    
    this.agent = new Agent({
      name: 'Enhanced Multi-Source Capture Agent',
      instructions: `/* PKM-specialized instructions */`,
      model, // Claude Code provider with fallbacks
      memory: [captureContextMemory, gtdComplianceMemory],
      tools: [/* existing tools */],
    });
  }
  
  // Maintain existing API compatibility
  async generateResponse(messages: MessageArray) {
    try {
      return await this.agent.generateVNext({ messages });
    } catch (error) {
      // Provider fallback handled internally by factory
      throw new Error(`Enhanced capture failed: ${error.message}`);
    }
  }
}
```

### 1.4.4 Cost Optimization Strategy

**Subscription vs API Key Economics**:
- **Claude Pro ($20/month)**: Unlimited usage for standard PKM operations
- **Claude Max ($100-200/month)**: High-volume research and synthesis workflows  
- **API Fallbacks**: Pay-per-token only when subscriptions unavailable
- **Intelligent Routing**: Automatic provider selection based on cost and availability

**Usage Optimization**:
```typescript
interface ProviderMetrics {
  subscriptionUsage: {
    remaining: number;
    resetDate: Date;
    provider: 'claude-pro' | 'claude-max';
  };
  fallbackCosts: {
    openai: number;
    anthropic: number;
  };
  routingDecisions: Array<{
    timestamp: Date;
    provider: string;
    reason: 'subscription' | 'fallback' | 'error';
    cost: number;
  }>;
}
```

### 1.4.5 Error Handling and Resilience

**Graceful Degradation**:
1. **Primary**: Claude Code (subscription-based)
2. **Secondary**: OpenAI API (pay-per-token)
3. **Tertiary**: Anthropic API (pay-per-token)
4. **Emergency**: Local processing with reduced features

**Error Recovery Patterns**:
```typescript
interface ProviderErrorHandler {
  handleSubscriptionError(error: SubscriptionError): Promise<MastraModel>;
  handleRateLimitError(error: RateLimitError): Promise<MastraModel>;
  handleNetworkError(error: NetworkError): Promise<MastraModel>;
  logProviderMetrics(metrics: ProviderMetrics): void;
}
```

### 1.4.6 Configuration Management

**Environment-Based Provider Selection**:
```typescript
// .env configuration
CLAUDE_CODE_ENABLED=true
CLAUDE_CODE_MODEL=claude-3-5-sonnet-20241022
OPENAI_FALLBACK_ENABLED=true
ANTHROPIC_FALLBACK_ENABLED=true
PROVIDER_METRICS_ENABLED=true

// Dynamic configuration
interface ProviderEnvironment {
  development: {
    primary: 'claude-code',
    fallbacks: ['openai'],
    metricsEnabled: true,
  },
  production: {
    primary: 'claude-code',
    fallbacks: ['openai', 'anthropic'],
    metricsEnabled: true,
    costMonitoring: true,
  }
}
```

## 2. PKM Methodology Compliance Framework

### 2.1 PARA Method Integration

**Mastra.ai Implementation**:
- **Classification Agent**: Specialized agent with PARA methodology instructions
- **Evaluation Tools**: Built-in assessment of classification accuracy
- **Memory Integration**: Persistent learning of user PARA preferences
- **Workflow Validation**: Automated compliance checking in organization workflow

```typescript
const organizationAgent = new Agent({
  name: 'PARA Organization Agent',
  instructions: `
    You are a PARA methodology expert specializing in accurate classification.
    
    PARA Categories:
    - Projects: Outcomes with deadlines requiring specific results
    - Areas: Ongoing responsibilities requiring maintenance
    - Resources: Topics of ongoing interest for future reference  
    - Archives: Inactive items from other categories
    
    Always provide classification reasoning and confidence scores.
  `,
  model: openai('gpt-4o'),
  memory: vaultContextMemory,
  tools: [paraValidationTool, hierarchyOptimizationTool],
});
```

### 2.2 Zettelkasten Principles Integration

**Mastra.ai Implementation**:
- **Processing Agent**: Enforces atomic note principles during creation
- **Linking Workflow**: Automated connection discovery and validation
- **Memory System**: Tracks note relationships and emergent patterns
- **Evaluation Framework**: Validates atomicity and connection quality

```typescript
const processingAgent = new Agent({
  name: 'Zettelkasten Processing Agent',
  instructions: `
    You are a Zettelkasten methodology expert ensuring atomic note creation.
    
    Atomic Note Principles:
    - One concept per note with clear boundaries
    - Self-contained and independently meaningful
    - Linked to related concepts through semantic connections
    - Structured for long-term value and reusability
    
    Validate conceptual atomicity and suggest connections.
  `,
  model: claude('claude-3.5-sonnet'),
  memory: zettelkastenMemory,
  tools: [atomicityValidationTool, linkDiscoveryTool],
});
```

### 2.3 Getting Things Done (GTD) Integration

**Mastra.ai Implementation**:
- **Capture Agent**: Ensures complete information capture (Mind Like Water)
- **Processing Workflow**: Clarifies captured items to actionable next steps
- **Review System**: Automated review cycle management and optimization
- **Memory Persistence**: Maintains trusted system state across sessions

## 3. Functional Requirements (Mastra.ai Implementation)

### FR-PKM-MASTRA-001: Capture Pipeline Agent (C1)
**Priority**: Critical
**Mastra.ai Components**: Agent + Tools + Workflow + Memory

#### Implementation Architecture (Mastra 2025):
```typescript
import { Agent } from '@mastra/core';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

// Enhanced Capture Agent with 2025 Features
const captureAgent = new Agent({
  name: 'Multi-Source Capture Agent',
  instructions: `
    You are a comprehensive content capture specialist following GTD principles and PKM best practices.
    
    Your primary responsibility is complete, accurate content capture with:
    - 100% fidelity to source material
    - Comprehensive metadata extraction
    - Quality assessment and scoring
    - Semantic duplicate detection
    - Source attribution and provenance tracking
    
    Always prioritize capture completeness over processing decisions.
  `,
  model: openai('gpt-4o-mini'),
  memory: [captureContextMemory, gtdComplianceMemory],
  tools: [
    webContentExtractorTool,
    documentProcessorTool,
    duplicateDetectionTool,
    qualityAssessmentTool,
    metadataEnrichmentTool,
  ],
});

// Modern Workflow with createStep pattern
const captureWorkflow = createWorkflow({
  name: 'enhanced-capture-pipeline',
  triggerSchema: z.object({
    content: z.string(),
    source: z.string(),
    type: z.enum(['text', 'url', 'file', 'clipboard']),
    metadata: z.record(z.any()).optional(),
  }),
  outputSchema: z.object({
    captureId: z.string(),
    processedContent: z.string(),
    qualityScore: z.number(),
    duplicateStatus: z.object({
      isDuplicate: z.boolean(),
      similarityScore: z.number().optional(),
    }),
    gtdCompliance: z.boolean(),
    handoffReady: z.boolean(),
  }),
})
.then(captureStep)
.then(qualityAssessmentStep)
.then(duplicateDetectionStep)
.then(complianceValidationStep)
.commit();

// Enhanced evaluation with Mastra's evaluation system
const captureCompletenessEval = {
  name: 'gtd-capture-completeness',
  evaluator: async ({ input, output }) => {
    const completeness = await assessCaptureCompleteness(
      input.content, 
      output.processedContent
    );
    
    return {
      score: completeness.fidelityScore,
      gtdCompliant: completeness.fidelityScore >= 0.995, // GTD standard
      informationLoss: 1 - completeness.fidelityScore,
      improvementSuggestions: completeness.suggestions,
    };
  },
};
```

#### Requirements:
- **FR-PKM-MASTRA-001.1**: Multi-source content ingestion via mastra.ai tools
- **FR-PKM-MASTRA-001.2**: Quality assessment using built-in evaluation system
- **FR-PKM-MASTRA-001.3**: Duplicate detection with vector similarity matching
- **FR-PKM-MASTRA-001.4**: Source attribution tracking in memory system
- **FR-PKM-MASTRA-001.5**: Workflow transition to processing pipeline

#### Success Metrics:
- **Capture Completeness**: 99.5% success rate via workflow monitoring
- **Quality Assessment Accuracy**: 90% agreement with human evaluation
- **Processing Handoff**: 100% successful workflow transitions
- **Source Attribution**: Complete provenance tracking in memory

### FR-PKM-MASTRA-002: Processing Pipeline Agent (P1) 
**Priority**: Critical
**Mastra.ai Components**: Agent + Workflow + Memory + Evaluation

#### Implementation Architecture:
```typescript
const processingAgent = new Agent({
  name: 'Atomic Note Processing Agent',
  instructions: 'Zettelkasten-compliant note creation and structuring',
  model: claude('claude-3.5-sonnet'),
  memory: processingMemory,
  tools: [
    atomicityValidatorTool,
    entityExtractionTool,
    templateApplicationTool,
    linkSuggestionTool,
  ],
});

const processingWorkflow = {
  name: 'processing-pipeline',
  steps: {
    analyze: { agent: 'processingAgent' },
    validate_atomicity: { tool: 'atomicityValidatorTool' },
    extract_entities: { tool: 'entityExtractionTool' },
    suggest_links: { tool: 'linkSuggestionTool' },
    quality_gate: { evaluation: 'atomicityEvaluation' },
  },
};
```

#### Requirements:
- **FR-PKM-MASTRA-002.1**: Atomic note creation with built-in validation
- **FR-PKM-MASTRA-002.2**: Entity extraction using mastra.ai memory integration
- **FR-PKM-MASTRA-002.3**: Link suggestion via vector similarity tools
- **FR-PKM-MASTRA-002.4**: Template application through workflow steps
- **FR-PKM-MASTRA-002.5**: Quality gates using mastra.ai evaluation system

#### Success Metrics:
- **Atomicity Compliance**: 95% pass rate on built-in evaluations
- **Entity Extraction**: 90% precision, 85% recall via evaluation tools
- **Link Quality**: 80% acceptance rate for suggested connections
- **Processing Speed**: <5 seconds via workflow performance monitoring

### FR-PKM-MASTRA-003: Organization Pipeline Agent (O1)
**Priority**: High
**Mastra.ai Components**: Agent + Memory + Tools + Evaluation

#### Implementation Architecture:
```typescript
const organizationAgent = new Agent({
  name: 'PARA Classification Agent', 
  instructions: 'Expert PARA method classification and hierarchy optimization',
  model: gemini('gemini-pro'),
  memory: paraMethodologyMemory,
  tools: [
    paraClassificationTool,
    hierarchyOptimizationTool,
    metadataEnrichmentTool,
    tagConsistencyTool,
  ],
});

const organizationEvaluation = {
  name: 'para-classification-accuracy',
  evaluator: (input, output) => {
    // Mastra.ai evaluation logic for PARA compliance
    return validateParaClassification(input.content, output.classification);
  },
};
```

#### Requirements:
- **FR-PKM-MASTRA-003.1**: PARA classification with confidence scoring
- **FR-PKM-MASTRA-003.2**: Hierarchical optimization using memory patterns
- **FR-PKM-MASTRA-003.3**: Metadata standardization via tools
- **FR-PKM-MASTRA-003.4**: Tag consistency enforcement with validation
- **FR-PKM-MASTRA-003.5**: Archive recommendations based on activity analysis

#### Success Metrics:
- **PARA Accuracy**: 85% correct classification via evaluation system
- **User Acceptance**: 80% approval rate for classifications
- **Consistency Score**: 90% metadata standardization compliance
- **Hierarchy Utility**: 75% user satisfaction with organization structure

### FR-PKM-MASTRA-004: Retrieval Pipeline Agent (R1)
**Priority**: High  
**Mastra.ai Components**: Agent + RAG + Memory + Tools

#### Implementation Architecture:
```typescript
const retrievalAgent = new Agent({
  name: 'Semantic Search Agent',
  instructions: 'Context-aware knowledge discovery and retrieval',
  model: openai('gpt-4o'),
  memory: searchContextMemory,
  tools: [
    semanticSearchTool,
    contextAnalysisTool, 
    recommendationTool,
    queryExpansionTool,
  ],
});

// Leverage Mastra.ai's built-in RAG capabilities
const knowledgeBase = new VectorStore({
  provider: 'pinecone',
  dimensions: 1536,
  metadata: ['category', 'tags', 'created_date', 'para_classification'],
});
```

#### Requirements:
- **FR-PKM-MASTRA-004.1**: Semantic search using mastra.ai RAG system
- **FR-PKM-MASTRA-004.2**: Context-aware recommendations via memory integration
- **FR-PKM-MASTRA-004.3**: Natural language query processing with agent intelligence
- **FR-PKM-MASTRA-004.4**: Proactive knowledge surfacing based on activity patterns
- **FR-PKM-MASTRA-004.5**: Search result explanation via agent reasoning

#### Success Metrics:
- **Search Relevance**: 90% user satisfaction with results
- **Intent Recognition**: 85% accuracy in query understanding
- **Context Awareness**: 70% improvement over keyword search
- **Response Time**: <2 seconds for 95% of queries

### FR-PKM-MASTRA-005: Review Pipeline Agent (V1)
**Priority**: Medium
**Mastra.ai Components**: Agent + Workflow + Memory + Evaluation

#### Implementation Architecture:
```typescript
const reviewAgent = new Agent({
  name: 'Knowledge Maintenance Agent',
  instructions: 'Automated knowledge freshness and maintenance optimization',
  model: claude('claude-3-haiku'),
  memory: maintenanceMemory,
  tools: [
    freshnessAssessmentTool,
    linkValidationTool,
    archiveRecommendationTool,
    priorityOptimizationTool,
  ],
});

const reviewWorkflow = {
  name: 'maintenance-cycle',
  triggerType: 'schedule',
  schedule: '0 9 * * SUN', // Weekly Sunday reviews
  steps: {
    assess_freshness: { agent: 'reviewAgent' },
    validate_links: { tool: 'linkValidationTool' },
    recommend_archives: { tool: 'archiveRecommendationTool' },
    optimize_priorities: { tool: 'priorityOptimizationTool' },
  },
};
```

#### Requirements:
- **FR-PKM-MASTRA-005.1**: Automated freshness assessment via scheduled workflows
- **FR-PKM-MASTRA-005.2**: Link validation using mastra.ai tools
- **FR-PKM-MASTRA-005.3**: Archive recommendations with evaluation validation
- **FR-PKM-MASTRA-005.4**: Review priority optimization through memory analysis
- **FR-PKM-MASTRA-005.5**: Maintenance workflow orchestration

#### Success Metrics:
- **Review Efficiency**: 50% reduction in manual review time
- **Link Health**: 99% accuracy in broken link detection
- **Archive Precision**: 85% user acceptance for archive recommendations
- **Cognitive Load**: 40% reduction in maintenance overhead

### FR-PKM-MASTRA-006: Synthesis Pipeline Agent (S1)
**Priority**: Medium
**Mastra.ai Components**: Agent + Memory + Evaluation + Advanced Reasoning

#### Implementation Architecture:
```typescript
const synthesisAgent = new Agent({
  name: 'Pattern Recognition & Synthesis Agent',
  instructions: 'Advanced pattern recognition and insight generation across knowledge domains',
  model: claude('claude-3.5-sonnet'),
  memory: synthesisMemory,
  tools: [
    patternRecognitionTool,
    insightGenerationTool,
    connectionDiscoveryTool,
    trendAnalysisTool,
  ],
});

const synthesisEvaluation = {
  name: 'insight-quality-assessment',
  evaluator: async (input, output) => {
    return await evaluateInsightQuality(output.insights, {
      novelty: true,
      actionability: true,
      evidence: true,
    });
  },
};
```

#### Requirements:
- **FR-PKM-MASTRA-006.1**: Pattern recognition across vault content via memory analysis
- **FR-PKM-MASTRA-006.2**: Insight generation with quality evaluation
- **FR-PKM-MASTRA-006.3**: Creative connection discovery using advanced reasoning
- **FR-PKM-MASTRA-006.4**: Trend analysis with predictive capabilities
- **FR-PKM-MASTRA-006.5**: Knowledge gap identification and research suggestions

#### Success Metrics:
- **Pattern Accuracy**: Statistical significance validation for all identified patterns
- **Insight Quality**: 70% actionability rate via evaluation system
- **Connection Novelty**: 60% user validation for discovered connections
- **Trend Prediction**: 2-3 week early trend identification

## 4. Mastra.ai Technical Implementation

### 4.1 Project Structure

```
pkm-mastra-system/
├── src/
│   ├── agents/
│   │   ├── capture.agent.ts
│   │   ├── processing.agent.ts
│   │   ├── organization.agent.ts
│   │   ├── retrieval.agent.ts
│   │   ├── review.agent.ts
│   │   └── synthesis.agent.ts
│   ├── workflows/
│   │   ├── pkm-pipeline.workflow.ts
│   │   ├── capture-to-processing.workflow.ts
│   │   └── organization-maintenance.workflow.ts
│   ├── tools/
│   │   ├── vault-operations.tool.ts
│   │   ├── para-validation.tool.ts
│   │   └── zettelkasten-compliance.tool.ts
│   ├── memory/
│   │   ├── vault-context.memory.ts
│   │   ├── user-preferences.memory.ts
│   │   └── methodology-patterns.memory.ts
│   ├── evaluations/
│   │   ├── atomicity.eval.ts
│   │   ├── para-classification.eval.ts
│   │   └── insight-quality.eval.ts
│   └── integrations/
│       ├── vault-filesystem.integration.ts
│       └── knowledge-graph.integration.ts
├── mastra.config.ts
├── package.json
└── tsconfig.json
```

### 4.2 Core Configuration

```typescript
// mastra.config.ts
import { Mastra, createLogger } from '@mastra/core';
import { z } from 'zod';

export const mastraConfig = {
  name: 'pkm-mastra-system',
  agents: {
    captureAgent,
    processingAgent, 
    organizationAgent,
    retrievalAgent,
    reviewAgent,
    synthesisAgent,
  },
  workflows: {
    pkmPipelineWorkflow,
    captureToProcessingWorkflow,
    organizationMaintenanceWorkflow,
  },
  memory: {
    provider: 'upstash-redis',
    config: {
      connectionString: process.env.UPSTASH_REDIS_URL,
    },
  },
  vectorStore: {
    provider: 'pinecone',
    config: {
      apiKey: process.env.PINECONE_API_KEY,
      environment: process.env.PINECONE_ENVIRONMENT,
    },
  },
  telemetry: {
    instructionId: process.env.MASTRA_INSTRUCTION_ID,
  },
  logger: createLogger({
    type: 'CONSOLE',
    level: 'INFO',
  }),
};
```

### 4.3 Development Workflow Integration

```typescript
// Development and testing integration
import { Mastra } from '@mastra/core';
import { PkmMastraSystem } from './types';

const pkmSystem = new Mastra(mastraConfig) as PkmMastraSystem;

// TDD Integration
export const testPkmSystem = {
  async testCaptureAgent(content: string) {
    return await pkmSystem.agent('captureAgent').generate({
      messages: [{ role: 'user', content }],
    });
  },
  
  async testPkmPipeline(triggerData: any) {
    return await pkmSystem.workflow('pkmPipelineWorkflow').execute({
      triggerData,
    });
  },
  
  async evaluateAgentPerformance(agentName: string, testCases: any[]) {
    const results = await Promise.all(
      testCases.map(testCase => 
        pkmSystem.evaluate(`${agentName}-performance`, testCase)
      )
    );
    return results;
  },
};
```

## 5. Quality Assurance and Evaluation

### 5.1 Built-in Evaluation System

**Mastra.ai Evaluation Integration**:
- **Model-Graded Evaluations**: LLM-based quality assessment for content and insights
- **Rule-Based Evaluations**: Methodology compliance checking (PARA, Zettelkasten, GTD)  
- **Statistical Evaluations**: Performance metrics and accuracy measurements
- **Custom Evaluations**: Domain-specific PKM quality criteria

```typescript
const pkmEvaluations = {
  atomicityCompliance: {
    evaluator: async (input, output) => {
      return await evaluateAtomicity(output.note);
    },
    schema: z.object({
      atomicity_score: z.number().min(0).max(1),
      conceptual_unity: z.boolean(),
      improvement_suggestions: z.array(z.string()),
    }),
  },
  
  paraClassificationAccuracy: {
    evaluator: async (input, output) => {
      return await validateParaClassification(input.content, output.classification);
    },
    schema: z.object({
      accuracy_score: z.number().min(0).max(1),
      classification_confidence: z.number().min(0).max(1),
      reasoning_quality: z.number().min(0).max(1),
    }),
  },
};
```

### 5.2 Observability and Monitoring

**OpenTelemetry Integration**:
- **Agent Performance Tracking**: Response times, token usage, success rates
- **Workflow Execution Monitoring**: Step completion, failure points, bottlenecks
- **Memory System Analytics**: Context utilization, retrieval accuracy, storage efficiency  
- **User Interaction Metrics**: Feature adoption, satisfaction scores, usage patterns

## 6. Deployment and Scaling

### 6.1 Development Environment

```json
{
  "name": "pkm-mastra-system",
  "scripts": {
    "dev": "mastra dev",
    "build": "mastra build", 
    "test": "mastra test",
    "eval": "mastra eval",
    "deploy": "mastra deploy"
  },
  "dependencies": {
    "@mastra/core": "^0.1.43",
    "@ai-sdk/openai": "^0.0.66",
    "@ai-sdk/anthropic": "^0.0.54",
    "ai-sdk-provider-claude-code": "^1.0.0",
    "@ai-sdk/google": "^0.0.52",
    "zod": "^3.23.8",
    "typescript": "^5.6.3"
  }
}
```

### 6.2 Production Deployment

**Deployment Options**:
- **Local Development**: Full mastra.ai environment with hot reloading
- **Node.js Server**: Production deployment with Hono integration
- **Serverless**: Cloud deployment with automatic scaling
- **Edge Runtime**: Distributed deployment for low-latency responses

## 7. Migration and Integration Strategy

### 7.1 Existing PKM System Integration

**Migration Path**:
1. **Phase 1**: Implement Capture Agent (C1) with mastra.ai while preserving existing workflows
2. **Phase 2**: Add Processing Agent (P1) with gradual workflow migration
3. **Phase 3**: Complete pipeline migration with full mastra.ai orchestration
4. **Phase 4**: Advanced features (Review and Synthesis agents) with optimization

### 7.2 Backward Compatibility

**Compatibility Strategy**:
- **API Preservation**: Maintain existing PKM command interfaces
- **Data Migration**: Seamless transition of existing vault content
- **Workflow Coexistence**: Gradual migration without workflow disruption
- **Rollback Capability**: Complete rollback to pre-mastra.ai system if needed

## 8. Success Metrics and Validation

### 8.1 Mastra.ai-Specific Metrics

**Framework Performance**:
- **Agent Response Time**: <2 seconds for 95% of operations
- **Workflow Completion Rate**: >99% successful pipeline executions  
- **Memory System Efficiency**: <100ms context retrieval
- **Evaluation Accuracy**: >90% agreement with human assessment

**Development Productivity**:
- **TypeScript Safety**: Zero runtime type errors
- **Testing Coverage**: >95% automated test coverage
- **Deployment Speed**: <5 minutes from commit to production
- **Debugging Efficiency**: 50% reduction in bug resolution time

### 8.2 PKM Methodology Compliance

**PARA Method Validation**:
- **Classification Accuracy**: 85% correct PARA categorization
- **User Acceptance**: 80% approval rate for automated classifications  
- **Maintenance Efficiency**: 70% reduction in manual organization time

**Zettelkasten Principle Validation**:
- **Atomicity Compliance**: 95% of notes pass atomicity evaluation
- **Link Quality**: 80% acceptance rate for suggested connections
- **Knowledge Emergence**: 5+ emergent themes identified monthly

**GTD Workflow Validation**:
- **Capture Completeness**: 99.5% information capture success rate
- **Processing Clarity**: 90% of items clarified to actionable next steps
- **Review Efficiency**: 50% reduction in review overhead time

---

**Next Steps**: Update steering document and TDD task breakdown for mastra.ai implementation approach.

**Document Status**: Ready for mastra.ai-based development with comprehensive PKM methodology integration.**