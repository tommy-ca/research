# PKM Claude Code SDK Ingestion Pipeline Specification

## Document Information
- **Document Type**: PKM Ingestion Pipeline System Specification
- **Version**: 1.0.0 - Claude Code SDK Integration
- **Created**: 2025-09-06
- **Framework**: Claude Code SDK + Mastra.ai v0.16.0+
- **Engineering Standards**: TDD, SOLID, KISS, DRY, Specs-Driven Development
- **Focus**: Production-ready PKM ingestion with intelligent Claude model selection

## Executive Summary

This specification defines a comprehensive PKM (Personal Knowledge Management) ingestion pipeline system built specifically for Claude Code SDK integration. The system leverages Claude Code's subscription-based access (Claude Pro/Max) with intelligent model selection between Claude 3.5 Sonnet and Claude 3 Opus based on content complexity and processing requirements.

## Ultra-Strategic Analysis Results

### Current State Assessment
- **PKM Agents**: Well-specified but not implemented with Claude Code SDK
- **Claude Integration**: Basic model selection exists, lacks PKM-specific pipelines
- **TDD Status**: Corrected methodology established with 100% test success rate
- **Architecture**: Solid SOLID/KISS/DRY foundation with Mastra.ai framework

### Strategic Requirements
1. **Claude Code SDK-First**: Leverage subscription model with intelligent fallbacks
2. **Ingestion Pipeline Focus**: Transform diverse content into atomic PKM notes
3. **Specs-Driven TDD**: Apply proven RED-GREEN-REFACTOR methodology
4. **Production Readiness**: >95% test coverage with performance targets

## Claude Code SDK Integration Architecture

### Model Selection Strategy for PKM Ingestion

**Claude 3.5 Sonnet (Fast Processing)**:
```typescript
interface SonnetOptimizedTasks {
  contentCapture: [
    'text-extraction',
    'basic-metadata',
    'format-conversion',
    'quick-categorization'
  ];
  
  lightProcessing: [
    'tagging-generation',
    'basic-linking',
    'simple-summarization',
    'inbox-processing'
  ];
  
  criteria: {
    contentLength: '<5000 chars';
    processingTime: '<2s required';
    complexity: '<0.6 score';
    accuracy: '>90% sufficient';
  };
}
```

**Claude 3 Opus (Quality Processing)**:
```typescript
interface OpusOptimizedTasks {
  deepAnalysis: [
    'concept-extraction',
    'semantic-analysis',
    'quality-assessment',
    'research-synthesis'
  ];
  
  complexProcessing: [
    'atomicity-validation',
    'relationship-mapping',
    'pattern-recognition',
    'insight-extraction'
  ];
  
  criteria: {
    contentLength: '>5000 chars OR complex';
    processingTime: 'quality over speed';
    complexity: '>0.6 score';
    accuracy: '>95% required';
  };
}
```

## PKM Ingestion Pipeline Requirements

### FR-PKM-INGEST-001: Content Ingestion Engine
**Priority**: Critical  
**Claude Model**: Sonnet (primary), Opus (complex content)

#### Requirements
- **FR-PKM-INGEST-001.1**: Multi-format content ingestion (text, PDF, web, etc.)
- **FR-PKM-INGEST-001.2**: Intelligent model selection based on content complexity
- **FR-PKM-INGEST-001.3**: Claude Code subscription-first with API fallbacks
- **FR-PKM-INGEST-001.4**: Real-time processing with queue management
- **FR-PKM-INGEST-001.5**: Quality validation and error handling

#### Implementation Architecture
```typescript
interface ContentIngestEngine {
  // Claude Code SDK Integration
  claudeProvider: ClaudeCodeProvider;
  modelSelector: (content: string, type: ContentType) => 'sonnet' | 'opus';
  
  // Ingestion Pipeline
  ingest(source: ContentSource): Promise<IngestionResult>;
  process(content: RawContent): Promise<ProcessedContent>;
  validate(result: ProcessedContent): Promise<ValidationResult>;
  store(content: ValidatedContent): Promise<StorageResult>;
}
```

#### Success Metrics
- **Processing Speed**: <3s for text, <10s for complex documents
- **Accuracy**: >95% content extraction fidelity
- **Model Selection**: Optimal cost/quality balance >85% of time
- **Error Rate**: <2% processing failures

### FR-PKM-INGEST-002: Atomic Note Generation
**Priority**: Critical  
**Claude Model**: Opus (primary), Sonnet (simple content)

#### Requirements
- **FR-PKM-INGEST-002.1**: One-concept-per-note atomicity validation
- **FR-PKM-INGEST-002.2**: Intelligent content chunking and splitting
- **FR-PKM-INGEST-002.3**: Metadata generation and enrichment
- **FR-PKM-INGEST-002.4**: Relationship and link suggestion
- **FR-PKM-INGEST-002.5**: Quality scoring and validation

#### Implementation Architecture
```typescript
interface AtomicNoteGenerator {
  // Content Analysis
  analyzeComplexity(content: string): ComplexityScore;
  identifyAtomicConcepts(content: string): ConceptBoundary[];
  
  // Note Generation
  generateAtomicNotes(concepts: ConceptBoundary[]): AtomicNote[];
  enrichMetadata(note: AtomicNote): EnrichedNote;
  suggestLinks(note: EnrichedNote): LinkSuggestion[];
  
  // Quality Validation
  validateAtomicity(note: AtomicNote): AtomicityScore;
  scoreQuality(note: EnrichedNote): QualityMetrics;
}
```

#### Success Metrics
- **Atomicity Score**: >90% single-concept compliance
- **Link Relevance**: >80% user acceptance of suggestions
- **Processing Quality**: >95% notes pass quality threshold
- **Metadata Accuracy**: >90% automatic metadata correctness

### FR-PKM-INGEST-003: Intelligent Metadata Extraction
**Priority**: High  
**Claude Model**: Sonnet (basic), Opus (complex analysis)

#### Requirements
- **FR-PKM-INGEST-003.1**: Automatic frontmatter generation
- **FR-PKM-INGEST-003.2**: Entity and concept extraction
- **FR-PKM-INGEST-003.3**: Tag hierarchy generation
- **FR-PKM-INGEST-003.4**: Source attribution and provenance
- **FR-PKM-INGEST-003.5**: PARA method classification

#### Implementation Architecture
```typescript
interface MetadataExtractor {
  // Basic Metadata (Sonnet)
  extractBasicMetadata(content: string): BasicMetadata;
  generateTags(content: string): TagHierarchy;
  classifyPARA(content: string): PARACategory;
  
  // Advanced Analysis (Opus)
  extractEntities(content: string): EntityMap;
  identifyConcepts(content: string): ConceptGraph;
  analyzeSentiment(content: string): SentimentAnalysis;
  assessQuality(content: string): QualityMetrics;
}
```

#### Success Metrics
- **Classification Accuracy**: >85% PARA categorization correctness
- **Tag Relevance**: >80% user acceptance of generated tags
- **Entity Extraction**: >90% precision, >85% recall
- **Processing Speed**: <2s for basic, <5s for complex analysis

### FR-PKM-INGEST-004: Quality Assessment Pipeline
**Priority**: High  
**Claude Model**: Opus (quality analysis)

#### Requirements
- **FR-PKM-INGEST-004.1**: Multi-dimensional quality scoring
- **FR-PKM-INGEST-004.2**: Content completeness validation
- **FR-PKM-INGEST-004.3**: Source credibility assessment
- **FR-PKM-INGEST-004.4**: Atomicity compliance checking
- **FR-PKM-INGEST-004.5**: Improvement recommendation generation

#### Implementation Architecture
```typescript
interface QualityAssessmentPipeline {
  // Quality Scoring
  scoreContent(content: ProcessedContent): QualityScore;
  validateCompleteness(content: ProcessedContent): CompletenessReport;
  assessCredibility(source: ContentSource): CredibilityScore;
  
  // Compliance Checking
  validateAtomicity(note: AtomicNote): AtomicityCompliance;
  checkPKMStandards(note: EnrichedNote): StandardsCompliance;
  
  // Improvement Suggestions
  generateImprovements(note: EnrichedNote): ImprovementSuggestions;
  identifyGaps(content: ProcessedContent): ContentGap[];
}
```

#### Success Metrics
- **Quality Prediction**: >90% correlation with human assessment
- **Improvement Accuracy**: >80% user acceptance of suggestions
- **Compliance Detection**: >95% accuracy in standard violations
- **Processing Efficiency**: <3s quality assessment per note

## Technical Implementation Specifications

### PKM Ingestion Workflow Architecture

```typescript
// Claude Code SDK-based PKM Ingestion System
import { claudeCode } from 'ai-sdk-provider-claude-code';
import { createStep, createWorkflow } from '@mastra/core';
import { z } from 'zod';

// Content Input Schema
const ContentInputSchema = z.object({
  content: z.string(),
  source: z.string(),
  type: z.enum(['text', 'url', 'file', 'clipboard', 'email']),
  metadata: z.record(z.any()).optional(),
  processingOptions: z.object({
    modelPreference: z.enum(['auto', 'sonnet', 'opus']).optional(),
    qualityThreshold: z.number().min(0).max(1).optional(),
    atomicityStrict: z.boolean().optional(),
  }).optional(),
});

// Processing Result Schema
const ProcessingResultSchema = z.object({
  atomicNotes: z.array(z.object({
    id: z.string(),
    title: z.string(),
    content: z.string(),
    frontmatter: z.record(z.any()),
    atomicityScore: z.number().min(0).max(1),
    qualityScore: z.number().min(0).max(1),
    suggestedLinks: z.array(z.string()),
    parakCategory: z.enum(['projects', 'areas', 'resources', 'archive']),
    processingModel: z.enum(['sonnet', 'opus']),
  })),
  processingMetrics: z.object({
    totalTime: z.number(),
    modelUsage: z.record(z.number()),
    qualityDistribution: z.record(z.number()),
  }),
  validationResults: z.object({
    atomicityCompliance: z.number().min(0).max(1),
    standardsCompliance: z.number().min(0).max(1),
    overallQuality: z.number().min(0).max(1),
  }),
});

// Model Selection Step
const modelSelectionStep = createStep({
  id: 'model-selection',
  inputSchema: ContentInputSchema,
  outputSchema: z.object({
    selectedModel: z.enum(['sonnet', 'opus']),
    rationale: z.string(),
    confidence: z.number().min(0).max(1),
  }),
  execute: async ({ input, context }) => {
    const complexity = await analyzeContentComplexity(input.content);
    const selectedModel = selectOptimalModel(input, complexity);
    
    return {
      selectedModel,
      rationale: `Selected ${selectedModel} based on complexity ${complexity.score}`,
      confidence: complexity.confidence,
    };
  },
});

// Content Processing Step
const contentProcessingStep = createStep({
  id: 'content-processing',
  inputSchema: z.object({
    content: z.string(),
    selectedModel: z.enum(['sonnet', 'opus']),
    processingOptions: z.object({}).optional(),
  }),
  outputSchema: z.object({
    processedContent: z.string(),
    extractedMetadata: z.record(z.any()),
    entityMap: z.record(z.any()),
    qualityMetrics: z.object({
      clarity: z.number(),
      completeness: z.number(),
      accuracy: z.number(),
    }),
  }),
  execute: async ({ input, context }) => {
    const model = await createClaudeCodeProvider(input.selectedModel);
    const agent = new Agent({
      name: `PKM Content Processor (${input.selectedModel})`,
      model,
      instructions: getPKMProcessingInstructions(input.selectedModel),
      tools: [contentAnalysisTool, metadataExtractorTool],
    });

    const result = await agent.generate({
      messages: [{
        role: 'user',
        content: `Process this content for PKM ingestion: ${input.content}`,
      }],
    });

    return parseProcessingResult(result.text);
  },
});

// Atomic Note Generation Step
const atomicNoteGenerationStep = createStep({
  id: 'atomic-note-generation',
  inputSchema: z.object({
    processedContent: z.string(),
    extractedMetadata: z.record(z.any()),
    selectedModel: z.enum(['sonnet', 'opus']),
  }),
  outputSchema: z.object({
    atomicNotes: z.array(z.object({
      id: z.string(),
      title: z.string(),
      content: z.string(),
      atomicityScore: z.number(),
      conceptBoundaries: z.array(z.string()),
    })),
  }),
  execute: async ({ input, context }) => {
    // Use Opus for complex atomicity analysis, Sonnet for simple content
    const model = input.selectedModel === 'opus' ? 'opus' : 
                   await shouldUseOpusForAtomicity(input.processedContent) ? 'opus' : 'sonnet';
    
    const atomicityAgent = await createAtomicityAgent(model);
    const notes = await atomicityAgent.generateAtomicNotes(input.processedContent);
    
    return { atomicNotes: notes };
  },
});

// Quality Assessment Step
const qualityAssessmentStep = createStep({
  id: 'quality-assessment',
  inputSchema: z.object({
    atomicNotes: z.array(z.object({
      id: z.string(),
      content: z.string(),
      atomicityScore: z.number(),
    })),
  }),
  outputSchema: z.object({
    qualityResults: z.array(z.object({
      noteId: z.string(),
      qualityScore: z.number(),
      improvements: z.array(z.string()),
      complianceCheck: z.object({
        atomicity: z.boolean(),
        standards: z.boolean(),
        pkm: z.boolean(),
      }),
    })),
  }),
  execute: async ({ input, context }) => {
    // Always use Opus for quality assessment
    const qualityAgent = await createQualityAgent('opus');
    const results = await Promise.all(
      input.atomicNotes.map(note => qualityAgent.assessQuality(note))
    );
    
    return { qualityResults: results };
  },
});

// PKM Ingestion Workflow
const pkmIngestionWorkflow = createWorkflow({
  name: 'pkm-ingestion-pipeline',
  triggerSchema: ContentInputSchema,
  outputSchema: ProcessingResultSchema,
})
.then(modelSelectionStep)
.then(contentProcessingStep)
.then(atomicNoteGenerationStep)
.then(qualityAssessmentStep)
.commit();

// Helper Functions
async function analyzeContentComplexity(content: string): Promise<ComplexityScore> {
  // Lightweight analysis for model selection
  const length = content.length;
  const sentences = content.split(/[.!?]+/).length;
  const avgSentenceLength = length / sentences;
  const technicalTerms = countTechnicalTerms(content);
  
  const complexityScore = calculateComplexityScore({
    length,
    avgSentenceLength,
    technicalTerms,
    structuralComplexity: analyzeStructuralComplexity(content),
  });
  
  return {
    score: complexityScore,
    confidence: Math.min(0.9, 0.6 + (length / 10000) * 0.3),
    factors: { length, avgSentenceLength, technicalTerms },
  };
}

function selectOptimalModel(
  input: ContentInput, 
  complexity: ComplexityScore
): 'sonnet' | 'opus' {
  // User preference override
  if (input.processingOptions?.modelPreference && 
      input.processingOptions.modelPreference !== 'auto') {
    return input.processingOptions.modelPreference;
  }
  
  // Quality threshold override
  if (input.processingOptions?.qualityThreshold && 
      input.processingOptions.qualityThreshold >= 0.95) {
    return 'opus';
  }
  
  // Content-based selection
  if (complexity.score > 0.7) return 'opus';
  if (input.content.length > 5000) return 'opus';
  if (input.type === 'file' && isComplexDocument(input.source)) return 'opus';
  
  return 'sonnet';
}

async function createClaudeCodeProvider(model: 'sonnet' | 'opus') {
  return claudeCode(
    model === 'opus' ? 'claude-3-opus-20240229' : 'claude-3-5-sonnet-20241022',
    {
      // Subscription-based configuration
      useSubscription: true,
      fallbackOnError: true,
      temperature: model === 'opus' ? 0.1 : 0.3,
      maxTokens: model === 'opus' ? 4000 : 2000,
    }
  );
}

function getPKMProcessingInstructions(model: 'sonnet' | 'opus'): string {
  const baseInstructions = `
    You are a PKM (Personal Knowledge Management) content processing specialist.
    Your goal is to transform raw content into atomic, well-structured knowledge notes.
    
    ALWAYS follow these PKM principles:
    - One concept per note (atomicity)
    - Self-contained understanding
    - Rich metadata generation
    - Intelligent linking suggestions
    - PARA method classification
  `;
  
  if (model === 'opus') {
    return baseInstructions + `
    OPUS-SPECIFIC REQUIREMENTS:
    - Deep semantic analysis and concept extraction
    - Complex relationship identification
    - Advanced quality validation
    - Sophisticated pattern recognition
    - Research-grade accuracy standards
    `;
  }
  
  return baseInstructions + `
    SONNET-SPECIFIC REQUIREMENTS:
    - Fast, efficient processing
    - Clear, straightforward analysis
    - Essential metadata extraction
    - Basic relationship identification
    - Standard quality validation
  `;
}
```

## TDD Implementation Requirements

### Test-Driven Development Specifications

#### Test Categories and Coverage Requirements

**Unit Tests (>95% Coverage)**:
```typescript
describe('PKM Ingestion Pipeline - TDD Implementation', () => {
  describe('Model Selection Logic', () => {
    test('selects Sonnet for simple text content < 1000 chars', () => {
      const input = createTestInput('Simple content', 500);
      expect(selectOptimalModel(input, analyzeComplexity(input.content))).toBe('sonnet');
    });
    
    test('selects Opus for complex research content > 5000 chars', () => {
      const input = createTestInput('Complex research with multiple concepts...', 6000);
      expect(selectOptimalModel(input, analyzeComplexity(input.content))).toBe('opus');
    });
    
    test('selects Opus when quality threshold >= 0.95', () => {
      const input = createTestInput('Any content', 1000, { qualityThreshold: 0.95 });
      expect(selectOptimalModel(input, analyzeComplexity(input.content))).toBe('opus');
    });
  });
  
  describe('Content Processing', () => {
    test('processes simple text content successfully with Sonnet', async () => {
      const result = await processContent('Simple PKM content', 'sonnet');
      expect(result.processedContent).toBeDefined();
      expect(result.qualityMetrics.completeness).toBeGreaterThan(0.8);
    });
    
    test('extracts complex metadata with Opus', async () => {
      const result = await processContent(complexResearchContent, 'opus');
      expect(result.entityMap).toHaveProperty('concepts');
      expect(result.entityMap).toHaveProperty('entities');
    });
  });
  
  describe('Atomic Note Generation', () => {
    test('generates atomic notes with single concepts', async () => {
      const notes = await generateAtomicNotes(testContent);
      notes.forEach(note => {
        expect(note.atomicityScore).toBeGreaterThan(0.8);
        expect(note.conceptBoundaries).toHaveLength(1);
      });
    });
  });
  
  describe('Quality Assessment', () => {
    test('validates PKM standards compliance', async () => {
      const assessment = await assessQuality(testNote);
      expect(assessment.complianceCheck.atomicity).toBe(true);
      expect(assessment.complianceCheck.standards).toBe(true);
      expect(assessment.qualityScore).toBeGreaterThan(0.7);
    });
  });
});
```

**Integration Tests**:
```typescript
describe('PKM Ingestion Integration Tests', () => {
  test('complete workflow processes web article successfully', async () => {
    const input = {
      content: await fetchWebContent('https://example.com/article'),
      source: 'web',
      type: 'url' as const,
    };
    
    const result = await pkmIngestionWorkflow.execute(input);
    
    expect(result.status).toBe('success');
    expect(result.output.atomicNotes.length).toBeGreaterThan(0);
    expect(result.output.validationResults.overallQuality).toBeGreaterThan(0.8);
  });
  
  test('handles Claude Code provider failures with graceful degradation', async () => {
    // Mock provider failure
    mockClaudeCodeFailure();
    
    const result = await pkmIngestionWorkflow.execute(testInput);
    
    expect(result.status).not.toBe('failed');
    // Should fallback to alternative provider or retry logic
  });
});
```

#### Performance Tests
```typescript
describe('PKM Ingestion Performance Requirements', () => {
  test('processes simple content within 3 seconds', async () => {
    const startTime = Date.now();
    await processSimpleContent(testContent);
    const duration = Date.now() - startTime;
    
    expect(duration).toBeLessThan(3000);
  });
  
  test('handles batch processing of 100 notes efficiently', async () => {
    const startTime = Date.now();
    const results = await processBatch(create100TestNotes());
    const duration = Date.now() - startTime;
    
    expect(duration).toBeLessThan(60000); // 1 minute for 100 notes
    expect(results.filter(r => r.success).length).toBeGreaterThan(95); // >95% success
  });
});
```

## Implementation Roadmap and Task Scheduling

### Phase 1: Foundation (Week 1-2)
```yaml
tasks:
  - task: "Implement basic Claude Code SDK provider integration"
    priority: critical
    tdd_phase: RED
    duration: 3 days
    
  - task: "Create model selection logic with comprehensive tests"
    priority: critical
    tdd_phase: GREEN
    duration: 2 days
    
  - task: "Implement content complexity analysis"
    priority: high
    tdd_phase: REFACTOR
    duration: 2 days
```

### Phase 2: Core Pipeline (Week 3-4)
```yaml
tasks:
  - task: "Implement content processing step with Mastra.ai workflow"
    priority: critical
    tdd_phase: RED
    duration: 4 days
    
  - task: "Create atomic note generation with atomicity validation"
    priority: critical
    tdd_phase: GREEN
    duration: 3 days
    
  - task: "Implement metadata extraction and PARA classification"
    priority: high
    tdd_phase: REFACTOR
    duration: 3 days
```

### Phase 3: Quality and Validation (Week 5-6)
```yaml
tasks:
  - task: "Implement quality assessment pipeline"
    priority: critical
    tdd_phase: RED
    duration: 3 days
    
  - task: "Create comprehensive validation and error handling"
    priority: high
    tdd_phase: GREEN
    duration: 2 days
    
  - task: "Performance optimization and monitoring"
    priority: medium
    tdd_phase: REFACTOR
    duration: 3 days
```

### Phase 4: Integration and Production (Week 7-8)
```yaml
tasks:
  - task: "End-to-end integration testing with real PKM vault"
    priority: critical
    tdd_phase: VALIDATE
    duration: 3 days
    
  - task: "Production deployment with monitoring and alerting"
    priority: high
    tdd_phase: EVALUATE
    duration: 2 days
    
  - task: "Documentation and user training materials"
    priority: medium
    duration: 2 days
```

## Success Metrics and Validation

### Technical Metrics
- **Test Coverage**: >95% unit test coverage, >90% integration coverage
- **Performance**: <3s simple content, <10s complex content processing
- **Quality**: >90% atomicity compliance, >85% user acceptance
- **Reliability**: <2% error rate, >99% uptime

### Business Metrics
- **Processing Throughput**: >100 notes processed per hour
- **Cost Efficiency**: Optimal Sonnet/Opus selection saving >30% costs
- **User Satisfaction**: >85% user rating for processing quality
- **Knowledge Quality**: >90% notes meet PKM standards

### PKM Methodology Compliance
- **Atomicity**: >95% single-concept compliance
- **PARA Classification**: >85% correct categorization
- **Link Quality**: >80% relevant link suggestions
- **Metadata Completeness**: >90% essential metadata present

---

**Next Phase**: Update steering document and execute TDD implementation cycle with comprehensive test-first development.

**Document Status**: Ready for TDD implementation with complete specifications and requirements defined.