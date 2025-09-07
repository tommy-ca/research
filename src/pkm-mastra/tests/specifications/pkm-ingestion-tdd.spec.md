# PKM Ingestion Pipeline TDD Specification

## Feature: Knowledge-Driven PKM Ingestion with Example Datasets
**SPEC-PKM-ING-001**: Comprehensive testing of PKM ingestion pipeline using realistic knowledge examples

### Requirements

#### Functional Requirements (FR) - PRIORITY
- **FR-001**: Process diverse knowledge types (technical, methodological, scientific, business, philosophical, quick captures)
- **FR-002**: Intelligent model selection based on content complexity and domain
- **FR-003**: Generate atomic notes following Zettelkasten principles
- **FR-004**: Quality assessment with domain-appropriate scoring
- **FR-005**: Extract concepts, entities, and metadata accurately
- **FR-006**: PARA classification based on content actionability
- **FR-007**: Performance within acceptable time bounds (<30s per input)

#### Non-Functional Requirements (NFR) - DEFERRED
- **NFR-001**: Concurrent processing of multiple knowledge inputs (Phase 2)
- **NFR-002**: Persistent storage and retrieval optimization (Phase 3)
- **NFR-003**: Advanced semantic linking and graph analysis (Phase 4)

### Test Data Strategy

#### Knowledge Complexity Levels
1. **Expert Level**: Complex scientific papers, advanced technical documentation
2. **Intermediate Level**: Business methodologies, software engineering principles
3. **Beginner Level**: Brief overviews, simple explanations, meeting notes
4. **Fragment Level**: Quick captures, fleeting thoughts, incomplete ideas

#### Domain Coverage
1. **Technical**: Software engineering, quantum computing, system architecture
2. **Methodological**: PKM systems (Zettelkasten, PARA), business frameworks (Lean Startup)
3. **Scientific**: Research papers, theoretical concepts, experimental results
4. **Business**: Strategy frameworks, case studies, organizational methods
5. **Philosophical**: Systems thinking, ethics, abstract concepts
6. **Practical**: Meeting notes, quick captures, action items

### Acceptance Criteria

#### AC-001: Model Selection Intelligence
- [ ] **Given** complex technical content (>1000 words, high technical density), **When** processing through model selection, **Then** selects Opus with >0.9 confidence
- [ ] **Given** simple overview content (<500 words, clear structure), **When** processing through model selection, **Then** selects Sonnet with >0.8 confidence
- [ ] **Given** user preference override, **When** processing with explicit model choice, **Then** respects user preference regardless of content complexity

#### AC-002: Atomic Note Generation Quality
- [ ] **Given** SOLID principles explanation, **When** generating atomic notes, **Then** produces 8±2 atomic notes with >0.85 atomicity score
- [ ] **Given** Zettelkasten methodology description, **When** generating atomic notes, **Then** produces 12±3 atomic notes with >0.90 quality score
- [ ] **Given** quick meeting capture, **When** generating atomic notes, **Then** produces 6±2 atomic notes with clear action items identified

#### AC-003: Concept Extraction Accuracy
- [ ] **Given** quantum computing paper, **When** extracting concepts, **Then** identifies 25+ key concepts including "superposition", "entanglement", "qubits"
- [ ] **Given** business strategy content, **When** extracting concepts, **Then** identifies methodology-specific terms and company examples
- [ ] **Given** philosophical content, **When** extracting concepts, **Then** identifies abstract concepts and their relationships

#### AC-004: Quality Assessment Precision
- [ ] **Given** well-structured technical documentation, **When** assessing quality, **Then** produces >0.90 quality score
- [ ] **Given** informal meeting notes, **When** assessing quality, **Then** produces 0.65-0.75 quality score with appropriate improvement suggestions
- [ ] **Given** incomplete fragment capture, **When** assessing quality, **Then** produces <0.70 score with specific enhancement recommendations

#### AC-005: PARA Classification Intelligence
- [ ] **Given** sprint planning notes with action items, **When** classifying, **Then** categorizes as "projects" with high confidence
- [ ] **Given** reference material like SOLID principles, **When** classifying, **Then** categorizes as "resources" 
- [ ] **Given** systems thinking methodology, **When** classifying, **Then** categorizes as "areas" (ongoing responsibility)

#### AC-006: Performance Requirements
- [ ] **Given** any knowledge input <5000 words, **When** processing end-to-end, **Then** completes within 30 seconds
- [ ] **Given** complex scientific paper, **When** processing with Opus, **Then** completes within 60 seconds
- [ ] **Given** simple text capture, **When** processing with Sonnet, **Then** completes within 15 seconds

### Test Cases

#### 1. Technical Knowledge Processing
```typescript
describe('Technical Knowledge Processing', () => {
  test('should process SOLID principles with expert-level accuracy', async () => {
    const input = softwareEngineeringExamples[0]; // SOLID principles
    const result = await pkmIngestionWorkflow.execute(input);
    
    expect(result.atomicNotes).toHaveLength(8); // ±2 tolerance
    expect(result.validationResults.overallQuality).toBeGreaterThan(0.90);
    expect(result.atomicNotes.every(note => note.atomicityScore > 0.85)).toBe(true);
    expect(result.processingMetrics.totalTime).toBeLessThan(45000); // 45s max
  });
  
  test('should select appropriate model for complex technical content', async () => {
    const input = scientificExamples[0]; // Quantum computing
    const modelSelection = await modelSelectionStep.execute(input);
    
    expect(modelSelection.selectedModel).toBe('opus');
    expect(modelSelection.confidence).toBeGreaterThan(0.9);
    expect(modelSelection.rationale).toContain('complex');
  });
});
```

#### 2. PKM Methodology Processing
```typescript
describe('PKM Methodology Processing', () => {
  test('should process Zettelkasten method with methodological precision', async () => {
    const input = pkmExamples[0]; // Zettelkasten method
    const result = await pkmIngestionWorkflow.execute(input);
    
    expect(result.atomicNotes).toHaveLength(12); // ±3 tolerance
    expect(result.validationResults.atomicityCompliance).toBeGreaterThan(0.88);
    expect(result.atomicNotes.some(note => note.paraCategory === 'areas')).toBe(true);
    expect(result.atomicNotes.some(note => note.paraCategory === 'resources')).toBe(true);
  });
  
  test('should identify PKM-specific concepts accurately', async () => {
    const input = pkmExamples[0]; // Zettelkasten
    const processing = await contentProcessingStep.execute({
      content: input.content,
      selectedModel: 'opus',
    });
    
    const concepts = processing.extractedMetadata.concepts;
    expect(concepts).toContain('atomicity');
    expect(concepts).toContain('connectivity');
    expect(concepts).toContain('unique identifiers');
    expect(concepts.length).toBeGreaterThan(15);
  });
});
```

#### 3. Quick Capture Processing
```typescript
describe('Quick Capture Processing', () => {
  test('should handle meeting notes with practical intelligence', async () => {
    const input = quickCaptureExamples[1]; // Sprint planning notes
    const result = await pkmIngestionWorkflow.execute(input);
    
    expect(result.atomicNotes.some(note => 
      note.paraCategory === 'projects'
    )).toBe(true);
    expect(result.atomicNotes.some(note => 
      note.content.includes('action') || note.content.includes('timeline')
    )).toBe(true);
    expect(result.validationResults.overallQuality).toBeGreaterThan(0.65);
  });
  
  test('should process fragments with appropriate quality assessment', async () => {
    const input = quickCaptureExamples[0]; // AI ethics fragment
    const result = await pkmIngestionWorkflow.execute(input);
    
    expect(result.atomicNotes).toHaveLength(2); // Small fragment
    expect(result.validationResults.overallQuality).toBeGreaterThan(0.70);
    expect(result.atomicNotes.every(note => note.atomicityScore > 0.85)).toBe(true); // Short = atomic
  });
});
```

#### 4. Cross-Domain Validation
```typescript
describe('Cross-Domain Knowledge Processing', () => {
  test('should maintain quality across diverse knowledge domains', async () => {
    const testCases = [
      softwareEngineeringExamples[0], // Technical
      pkmExamples[0], // Methodological  
      scientificExamples[0], // Scientific
      businessExamples[0], // Business
      philosophicalExamples[0], // Philosophical
    ];
    
    for (const testCase of testCases) {
      const result = await pkmIngestionWorkflow.execute(testCase);
      
      // Quality should be within expected range ±15%
      const expectedQuality = testCase.expectedOutcomes.avgQualityScore;
      expect(result.validationResults.overallQuality).toBeGreaterThan(expectedQuality - 0.15);
      expect(result.validationResults.overallQuality).toBeLessThan(expectedQuality + 0.15);
      
      // Atomicity should be within expected range ±10%
      const expectedAtomicity = testCase.expectedOutcomes.avgAtomicityScore;
      expect(result.validationResults.atomicityCompliance).toBeGreaterThan(expectedAtomicity - 0.10);
      expect(result.validationResults.atomicityCompliance).toBeLessThan(expectedAtomicity + 0.10);
    }
  });
});
```

#### 5. Performance and Scalability
```typescript
describe('Performance Requirements', () => {
  test('should process all knowledge types within time limits', async () => {
    const performanceTests = allExampleKnowledge.map(async (knowledge) => {
      const startTime = Date.now();
      const result = await pkmIngestionWorkflow.execute(knowledge);
      const endTime = Date.now();
      
      const processingTime = endTime - startTime;
      const timeLimit = knowledge.content.length > 1000 ? 60000 : 30000; // 60s for long, 30s for short
      
      expect(processingTime).toBeLessThan(timeLimit);
      return { knowledge: knowledge.id, time: processingTime, result };
    });
    
    const results = await Promise.all(performanceTests);
    
    // Verify performance metrics
    const avgTime = results.reduce((sum, r) => sum + r.time, 0) / results.length;
    expect(avgTime).toBeLessThan(25000); // Average under 25s
    
    console.log('Performance Results:', results.map(r => ({
      id: r.knowledge,
      time: `${r.time}ms`,
      notes: r.result.atomicNotes.length,
      quality: r.result.validationResults.overallQuality,
    })));
  });
});
```

### Integration Test Scenarios

#### E2E-001: Complete Pipeline Validation
```typescript
test('should process complete knowledge pipeline end-to-end', async () => {
  const complexKnowledge = scientificExamples[0]; // Quantum computing
  
  // Step 1: Model Selection
  const modelResult = await modelSelectionStep.execute(complexKnowledge);
  expect(modelResult.selectedModel).toBe('opus');
  
  // Step 2: Content Processing  
  const processingResult = await contentProcessingStep.execute({
    content: complexKnowledge.content,
    selectedModel: modelResult.selectedModel,
  });
  expect(processingResult.extractedMetadata.concepts.length).toBeGreaterThan(20);
  
  // Step 3: Atomic Note Generation
  const atomicResult = await atomicNoteGenerationStep.execute({
    processedContent: processingResult.processedContent,
    extractedMetadata: processingResult.extractedMetadata,
    selectedModel: modelResult.selectedModel,
  });
  expect(atomicResult.atomicNotes.length).toBeGreaterThan(15);
  
  // Step 4: Quality Assessment
  const qualityResult = await qualityAssessmentStep.execute({
    atomicNotes: atomicResult.atomicNotes,
  });
  expect(qualityResult.qualityResults.every(q => q.qualityScore > 0.7)).toBe(true);
  
  // Step 5: Full Pipeline
  const fullResult = await pkmIngestionWorkflow.execute(complexKnowledge);
  expect(fullResult.validationResults.overallQuality).toBeGreaterThan(0.90);
});
```

### Success Metrics

#### Quantitative Benchmarks
- **Accuracy**: >90% correct concept identification for technical content
- **Quality**: Average quality score >0.80 across all knowledge types  
- **Atomicity**: >85% of generated notes meet atomicity criteria
- **Performance**: <30s processing time for standard inputs
- **Consistency**: <15% variance from expected quality scores
- **Coverage**: 100% test coverage for all example knowledge datasets

#### Qualitative Benchmarks
- Generated notes are comprehensible and useful for PKM workflows
- Concept extraction captures domain-specific terminology accurately
- PARA categorization aligns with content actionability
- Quality assessments provide actionable improvement suggestions
- Model selection rationale is transparent and logical

### Risk Mitigation

#### Technical Risks
- **Model availability**: Mock providers for testing independence
- **API rate limits**: Use test-specific rate limiting strategies
- **Processing variability**: Allow tolerance ranges for quality metrics
- **Complex content edge cases**: Include challenging examples in dataset

#### Quality Risks
- **Subjective quality assessment**: Define objective criteria for quality scoring
- **Domain bias**: Ensure balanced representation across knowledge domains
- **Atomicity variance**: Allow reasonable tolerance for interconnected concepts
- **Processing consistency**: Test multiple runs for stability validation

---

**Implementation Priority**: Knowledge-driven TDD approach ensures the PKM ingestion pipeline works effectively with real-world knowledge examples before optimization.

**Expected Duration**: 2-3 days for complete TDD cycle (RED → GREEN → REFACTOR)

**Success Probability**: 90% (comprehensive test datasets provide clear validation criteria)