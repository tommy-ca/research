/**
 * Example Knowledge Datasets for TDD PKM Ingestion Pipeline Testing
 * 
 * Comprehensive, realistic knowledge examples across domains and complexity levels
 * to drive systematic test-driven development of the PKM ingestion system.
 */

export interface KnowledgeExample {
  id: string;
  title: string;
  content: string;
  source: string;
  type: 'text' | 'url' | 'file' | 'clipboard' | 'document' | 'email';
  metadata?: Record<string, any>;
  expectedOutcomes: {
    atomicNotesCount: number;
    avgQualityScore: number;
    avgAtomicityScore: number;
    paraCategories: Array<'projects' | 'areas' | 'resources' | 'archive'>;
    keyConceptsCount: number;
    suggestedLinksCount: number;
    processingModel: 'sonnet' | 'opus';
  };
  testingNotes?: string;
}

// DATASET 1: SOFTWARE ENGINEERING KNOWLEDGE
export const softwareEngineeringExamples: KnowledgeExample[] = [
  {
    id: 'se-001-solid-principles',
    title: 'SOLID Principles in Software Design',
    content: `
The SOLID principles are five design principles intended to make software designs more understandable, flexible, and maintainable. These principles were introduced by Robert Martin and are fundamental to object-oriented programming and design.

1. Single Responsibility Principle (SRP): A class should have only one reason to change. This means that a class should have only one job or responsibility. When a class has multiple responsibilities, it becomes coupled, making it more difficult to change and maintain.

2. Open/Closed Principle (OCP): Software entities should be open for extension but closed for modification. This means you should be able to extend a class's behavior without modifying the existing code. This is typically achieved through inheritance and polymorphism.

3. Liskov Substitution Principle (LSP): Objects of a superclass should be replaceable with objects of its subclasses without breaking the application. This principle ensures that inheritance is used correctly and that subclasses truly represent specialized versions of their parent class.

4. Interface Segregation Principle (ISP): No client should be forced to depend on methods it does not use. This principle advocates for creating specific interfaces rather than one general-purpose interface. It helps in keeping the system decoupled and easier to refactor.

5. Dependency Inversion Principle (DIP): High-level modules should not depend on low-level modules. Both should depend on abstractions. This principle promotes loose coupling by ensuring that classes depend on interfaces or abstract classes rather than concrete implementations.

Implementation Example:
// Violating SRP
class UserManager {
  validateUser(user: User): boolean { /* validation logic */ }
  saveUser(user: User): void { /* database logic */ }
  sendEmail(user: User): void { /* email logic */ }
}

// Following SRP
class UserValidator {
  validate(user: User): boolean { /* validation logic */ }
}

class UserRepository {
  save(user: User): void { /* database logic */ }
}

class EmailService {
  sendWelcomeEmail(user: User): void { /* email logic */ }
}

Benefits of following SOLID principles include improved code maintainability, better testability, reduced code coupling, increased code reusability, and easier debugging and refactoring.
    `,
    source: 'software-engineering-course',
    type: 'document',
    metadata: {
      author: 'Robert Martin',
      domain: 'software-engineering',
      difficulty: 'intermediate',
      lastUpdated: '2024-01-15',
      tags: ['design-patterns', 'oop', 'architecture'],
    },
    expectedOutcomes: {
      atomicNotesCount: 8, // 5 principles + definition + benefits + example
      avgQualityScore: 0.92,
      avgAtomicityScore: 0.88,
      paraCategories: ['resources'],
      keyConceptsCount: 12,
      suggestedLinksCount: 15,
      processingModel: 'opus', // Complex technical content
    },
    testingNotes: 'High-quality, well-structured technical content with clear concepts'
  },
  
  {
    id: 'se-002-microservices-brief',
    title: 'Microservices Architecture Overview',
    content: `
Microservices architecture is a design approach where applications are built as a collection of loosely coupled services. Each service is independently deployable and maintains its own data. This contrasts with monolithic architectures where all components are tightly integrated.

Key characteristics include service independence, technology diversity, fault isolation, and scalability. Popular companies like Netflix and Amazon have successfully implemented microservices to handle massive scale.

Challenges include distributed system complexity, network latency, data consistency issues, and increased operational overhead. Teams need strong DevOps practices and monitoring tools to manage microservices effectively.
    `,
    source: 'tech-blog',
    type: 'text',
    metadata: {
      domain: 'software-architecture',
      difficulty: 'beginner',
      readingTime: '2 minutes',
    },
    expectedOutcomes: {
      atomicNotesCount: 4, // Definition + characteristics + examples + challenges
      avgQualityScore: 0.75,
      avgAtomicityScore: 0.82,
      paraCategories: ['resources'],
      keyConceptsCount: 6,
      suggestedLinksCount: 8,
      processingModel: 'sonnet', // Simpler content
    },
  }
];

// DATASET 2: PERSONAL KNOWLEDGE MANAGEMENT
export const pkmExamples: KnowledgeExample[] = [
  {
    id: 'pkm-001-zettelkasten-method',
    title: 'The Zettelkasten Method for Knowledge Management',
    content: `
The Zettelkasten method, developed by sociologist Niklas Luhmann, is a systematic approach to taking and organizing notes that emphasizes connecting ideas rather than hierarchical categorization. Luhmann used this method to write over 70 books and 400+ articles, attributing much of his productivity to this system.

Core Principles:

Atomicity: Each note should contain exactly one idea or concept. This makes notes reusable and allows for better connections between different concepts. Atomic notes are easier to link and reference in multiple contexts.

Connectivity: Notes gain value through their connections to other notes. The system emphasizes creating links between related concepts, building a web of knowledge rather than isolated information silos. These connections often reveal unexpected relationships and insights.

Unique Identifiers: Each note receives a unique identifier that allows for precise referencing and linking. Traditional numbering systems work, but modern digital implementations often use timestamps or generated IDs.

Personal Language: Notes should be written in your own words to ensure understanding and facilitate future retrieval. Paraphrasing forces deeper processing and makes the content more accessible to your future self.

Continuous Development: The Zettelkasten grows organically through regular addition of new notes and creation of new connections. This iterative process builds a personal knowledge network that becomes more valuable over time.

Digital Implementation:
Modern tools like Obsidian, Roam Research, and Logseq have made Zettelkasten methods more accessible through features like backlinks, graph visualization, and full-text search. However, the core principles remain the same regardless of the medium.

Benefits include enhanced creativity through serendipitous connections, improved retention through active processing, better writing through organized thoughts, and long-term knowledge accumulation that compounds over time.

Challenges include initial setup complexity, maintaining consistency in note-taking habits, avoiding over-optimization of the system, and balancing structure with flexibility as the system grows.
    `,
    source: 'pkm-research-paper',
    type: 'document',
    metadata: {
      author: 'Niklas Luhmann',
      domain: 'personal-knowledge-management',
      year: '1981',
      methodology: 'zettelkasten',
      complexity: 'high',
    },
    expectedOutcomes: {
      atomicNotesCount: 12, // Principles + implementation + benefits + challenges + examples
      avgQualityScore: 0.95,
      avgAtomicityScore: 0.91,
      paraCategories: ['resources', 'areas'],
      keyConceptsCount: 18,
      suggestedLinksCount: 25,
      processingModel: 'opus', // Complex methodological content
    },
  },

  {
    id: 'pkm-002-para-method',
    title: 'PARA Method for Digital Organization',
    content: `
PARA is an organizational method created by Tiago Forte for managing digital information. It stands for Projects, Areas, Resources, and Archives. The method focuses on actionability rather than subject matter.

Projects are specific outcomes with deadlines. Areas are ongoing responsibilities to maintain. Resources are future reference topics. Archives are inactive items from the other categories.

The system works by organizing information based on how actionable it is right now, making it easier to find relevant information when you need to act on it.
    `,
    source: 'productivity-blog',
    type: 'text',
    metadata: {
      author: 'Tiago Forte',
      method: 'PARA',
      focus: 'actionability',
    },
    expectedOutcomes: {
      atomicNotesCount: 5, // Definition + 4 categories + principle
      avgQualityScore: 0.78,
      avgAtomicityScore: 0.85,
      paraCategories: ['resources'],
      keyConceptsCount: 8,
      suggestedLinksCount: 6,
      processingModel: 'sonnet', // Clear, structured content
    },
  }
];

// DATASET 3: SCIENTIFIC RESEARCH
export const scientificExamples: KnowledgeExample[] = [
  {
    id: 'sci-001-quantum-computing',
    title: 'Quantum Computing Fundamentals and Applications',
    content: `
Quantum computing represents a paradigm shift in computational capability, leveraging quantum mechanical phenomena like superposition and entanglement to process information in fundamentally different ways than classical computers.

Fundamental Concepts:

Quantum Bits (Qubits): Unlike classical bits that exist in definite states of 0 or 1, qubits can exist in superposition states, simultaneously representing both 0 and 1 with specific probability amplitudes. This superposition is described mathematically as |ψ⟩ = α|0⟩ + β|1⟩, where α and β are complex probability amplitudes.

Superposition allows quantum systems to explore multiple computational paths simultaneously. An n-qubit system can represent 2^n states simultaneously, providing exponential scaling advantages for certain problem types. This property is what gives quantum computers their potential for massive parallelism.

Entanglement creates strong correlations between qubits such that measuring one qubit instantaneously affects others, regardless of physical separation. Einstein famously called this "spooky action at a distance," but it's now understood as a fundamental feature of quantum mechanics that quantum computers exploit for enhanced computational power.

Quantum Gates and Circuits: Quantum computation operates through quantum gates that manipulate qubit states through unitary transformations. Common gates include the Hadamard gate (creates superposition), CNOT gate (creates entanglement), and Pauli gates (single-qubit rotations). These gates are combined into quantum circuits to implement algorithms.

Current Applications and Algorithms:

Shor's Algorithm demonstrates exponential speedup for integer factorization, threatening current RSA cryptography. The algorithm uses quantum Fourier transform and period-finding to factor large numbers efficiently, with profound implications for cybersecurity.

Grover's Algorithm provides quadratic speedup for unstructured search problems, effectively searching unsorted databases in O(√N) time compared to classical O(N). This has applications in optimization and cryptography.

Quantum Simulation allows modeling of quantum systems that are intractable for classical computers. Applications include drug discovery (molecular interactions), materials science (superconductor behavior), and fundamental physics research.

Quantum Machine Learning explores how quantum computing might accelerate certain machine learning algorithms, particularly those involving high-dimensional vector spaces and pattern recognition tasks.

Technical Challenges:

Quantum Decoherence: Quantum states are extremely fragile and lose their quantum properties through interaction with the environment. Current quantum computers operate for microseconds before decoherence destroys quantum information, limiting algorithm complexity.

Error Rates: Current quantum computers have error rates of 0.1-1% per operation, much higher than classical computers. Quantum error correction requires hundreds or thousands of physical qubits to create one logical qubit, making current systems "noisy intermediate-scale quantum" (NISQ) devices.

Scaling Challenges: Building larger quantum systems requires maintaining quantum coherence across more qubits while reducing cross-talk and improving gate fidelities. Different approaches include superconducting circuits, trapped ions, photonic systems, and topological qubits.

Current quantum computers from IBM, Google, and others demonstrate quantum supremacy for specific tasks but lack practical advantages for most real-world problems. The field is progressing toward fault-tolerant quantum computers that could revolutionize cryptography, simulation, and optimization within the next decade.
    `,
    source: 'quantum-physics-journal',
    type: 'document',
    metadata: {
      domain: 'quantum-physics',
      subfield: 'quantum-computing',
      complexity: 'expert',
      equations: true,
      figures: 3,
      references: 45,
      impactFactor: 8.2,
    },
    expectedOutcomes: {
      atomicNotesCount: 18, // Concepts + algorithms + applications + challenges + examples
      avgQualityScore: 0.96,
      avgAtomicityScore: 0.87, // High quality but some concepts naturally interconnected
      paraCategories: ['resources'],
      keyConceptsCount: 28,
      suggestedLinksCount: 35,
      processingModel: 'opus', // Highly complex scientific content
    },
    testingNotes: 'Extremely complex scientific content requiring deep analysis'
  }
];

// DATASET 4: BUSINESS AND STRATEGY
export const businessExamples: KnowledgeExample[] = [
  {
    id: 'biz-001-lean-startup',
    title: 'Lean Startup Methodology Implementation',
    content: `
The Lean Startup methodology, popularized by Eric Ries, emphasizes rapid experimentation and iterative development to build sustainable businesses. The core philosophy centers on learning what customers actually want through validated learning rather than assumptions.

Build-Measure-Learn Cycle forms the heart of the methodology. Teams build minimum viable products (MVPs), measure customer responses through metrics and feedback, then learn from the data to make informed decisions about pivoting or persevering with the current approach.

Key Principles:

Validated Learning prioritizes learning over traditional business plan execution. Instead of spending months developing features customers might not want, teams test hypotheses quickly and cheaply through experiments.

Innovation Accounting tracks progress through actionable metrics rather than vanity metrics. Teams focus on cohort analysis, conversion rates, and customer lifetime value rather than total users or page views.

Minimum Viable Product (MVP) represents the smallest version of a product that enables a full turn of the Build-Measure-Learn loop with minimum effort and development time. MVPs aren't about building less – they're about learning more.

Pivot or Persevere decisions are made based on validated learning. A pivot involves changing fundamental hypotheses about the product, strategy, or engine of growth while staying grounded in what has been learned.

Success Stories:
Dropbox used a simple video demonstrating file syncing as their MVP, validating demand before building the complex backend infrastructure. This approach saved months of development time and proved product-market fit existed.

Zappos started by photographing shoes from local stores and posting them online. When customers ordered, they'd buy the shoes retail and ship them, proving the online shoe market existed before building inventory systems.

Buffer used a landing page with an email signup to validate demand for their social media scheduling tool, gathering thousands of interested users before writing any code.

Implementation Challenges include organizational resistance to experimentation, difficulty measuring learning progress, maintaining team morale during pivots, and balancing speed with quality.

Modern applications extend beyond startups to established companies implementing innovation programs, government agencies testing policy changes, and non-profits validating social interventions.
    `,
    source: 'business-strategy-book',
    type: 'document',
    metadata: {
      author: 'Eric Ries',
      domain: 'business-strategy',
      methodology: 'lean-startup',
      examples: ['Dropbox', 'Zappos', 'Buffer'],
    },
    expectedOutcomes: {
      atomicNotesCount: 14, // Methodology + principles + examples + challenges + applications
      avgQualityScore: 0.89,
      avgAtomicityScore: 0.86,
      paraCategories: ['resources', 'projects'],
      keyConceptsCount: 20,
      suggestedLinksCount: 18,
      processingModel: 'opus', // Complex business methodology
    },
  }
];

// DATASET 5: CREATIVE AND PHILOSOPHICAL
export const philosophicalExamples: KnowledgeExample[] = [
  {
    id: 'phil-001-systems-thinking',
    title: 'Systems Thinking and Complexity Theory',
    content: `
Systems thinking is a disciplinary framework that sees the world as a series of interconnected systems rather than individual, isolated events. This perspective emphasizes relationships, patterns, and contexts over linear cause-and-effect thinking.

A system is more than the sum of its parts. The behavior of a system emerges from the relationships and interactions between its components, not from the components themselves. Understanding these emergent properties requires holistic thinking rather than reductionist analysis.

Key characteristics of systems include purpose (why the system exists), structure (how parts are arranged), and function (what the system does). These elements interact dynamically, with changes in one affecting the others through feedback loops and interconnections.

Feedback loops are critical in systems thinking. Reinforcing loops amplify or accelerate change, while balancing loops seek equilibrium. Most complex systems contain multiple feedback loops operating simultaneously, creating the complex behaviors we observe in organizations, ecosystems, and societies.

Systems archetypes represent common problematic patterns of behavior in systems. Examples include "limits to growth" where rapid expansion hits constraints, "shifting the burden" where quick fixes prevent addressing root causes, and "tragedy of the commons" where individual rational behavior leads to collective irrationality.

Applications span from personal development (understanding habit formation and behavior change) to organizational development (designing culture and processes) to global challenges (climate change, poverty, conflict resolution).

The systems perspective reveals that many problems we face are not really problems but symptoms of larger systemic issues. Effective solutions require understanding and working with the system's structure and dynamics rather than just treating symptoms.
    `,
    source: 'systems-theory-workshop',
    type: 'text',
    metadata: {
      domain: 'systems-theory',
      author: 'Peter Senge',
      applications: ['personal-development', 'organizational-development', 'global-issues'],
    },
    expectedOutcomes: {
      atomicNotesCount: 9, // Definition + characteristics + feedback loops + archetypes + applications
      avgQualityScore: 0.84,
      avgAtomicityScore: 0.81,
      paraCategories: ['resources', 'areas'],
      keyConceptsCount: 15,
      suggestedLinksCount: 12,
      processingModel: 'opus', // Abstract, interconnected concepts
    },
  }
];

// DATASET 6: QUICK CAPTURES AND FRAGMENTS
export const quickCaptureExamples: KnowledgeExample[] = [
  {
    id: 'quick-001-idea-fragment',
    title: 'Fleeting Thought on AI Ethics',
    content: `
The alignment problem in AI isn't just about preventing catastrophic outcomes - it's about ensuring AI systems optimize for human flourishing rather than narrow metrics. We need to think beyond "don't do harm" to "actively promote human agency and dignity."
    `,
    source: 'mobile-capture',
    type: 'clipboard',
    metadata: {
      capturedAt: '2024-01-20T14:30:00Z',
      device: 'mobile',
      context: 'walking',
    },
    expectedOutcomes: {
      atomicNotesCount: 2, // Main idea + implication
      avgQualityScore: 0.72,
      avgAtomicityScore: 0.88, // Short, focused thoughts
      paraCategories: ['areas'],
      keyConceptsCount: 4,
      suggestedLinksCount: 3,
      processingModel: 'sonnet', // Simple capture
    },
  },

  {
    id: 'quick-002-meeting-notes',
    title: 'Sprint Planning Meeting Notes',
    content: `
Sprint 23 Planning - Team decided to focus on user authentication refactor. 
Key points:
- Move from JWT to session-based auth for better security
- Timeline: 2 weeks
- Dependencies: Need new Redis cluster setup
- Risk: Migration strategy for existing users needs careful planning
- Sarah will lead the backend changes, Mike handles frontend integration
- Review scheduled for Thursday to assess progress

Action items: Set up Redis by Monday, Create migration plan by Wednesday, Begin user testing on Friday.
    `,
    source: 'meeting-notes',
    type: 'text',
    metadata: {
      meetingType: 'sprint-planning',
      attendees: ['Sarah', 'Mike'],
      project: 'authentication-refactor',
      sprint: 23,
    },
    expectedOutcomes: {
      atomicNotesCount: 6, // Decision + timeline + dependencies + risks + responsibilities + actions
      avgQualityScore: 0.68, // Informal meeting notes format
      avgAtomicityScore: 0.79, // Some interconnected items
      paraCategories: ['projects'],
      keyConceptsCount: 8,
      suggestedLinksCount: 5,
      processingModel: 'sonnet', // Structured but simple content
    },
  }
];

// COMPREHENSIVE DATASET COLLECTION
export const allExampleKnowledge: KnowledgeExample[] = [
  ...softwareEngineeringExamples,
  ...pkmExamples,
  ...scientificExamples,
  ...businessExamples,
  ...philosophicalExamples,
  ...quickCaptureExamples,
];

// DATASET CATEGORIES FOR TESTING
export const datasetCategories = {
  highComplexity: allExampleKnowledge.filter(ex => ex.expectedOutcomes.processingModel === 'opus'),
  lowComplexity: allExampleKnowledge.filter(ex => ex.expectedOutcomes.processingModel === 'sonnet'),
  longForm: allExampleKnowledge.filter(ex => ex.content.length > 1000),
  shortForm: allExampleKnowledge.filter(ex => ex.content.length <= 1000),
  technical: allExampleKnowledge.filter(ex => 
    ex.metadata?.domain?.includes('software') || 
    ex.metadata?.domain?.includes('quantum') ||
    ex.metadata?.domain?.includes('engineering')
  ),
  methodological: allExampleKnowledge.filter(ex => 
    ex.metadata?.methodology || 
    ex.metadata?.method ||
    ex.id.includes('pkm') ||
    ex.id.includes('lean')
  ),
  quickCaptures: quickCaptureExamples,
};

// QUALITY BENCHMARKS FOR VALIDATION
export const qualityBenchmarks = {
  minAtomicityScore: 0.75,
  minQualityScore: 0.65,
  maxProcessingTime: 30000, // 30 seconds
  minConceptExtraction: 3,
  expectedAtomicityVariance: 0.1, // ±10% from expected
  expectedQualityVariance: 0.15, // ±15% from expected
};

/**
 * TESTING STRATEGY NOTES:
 * 
 * 1. COMPLEXITY TESTING: Use high/low complexity datasets to validate model selection
 * 2. DOMAIN TESTING: Ensure consistent processing across different knowledge domains
 * 3. FORMAT TESTING: Validate handling of different input types and sources
 * 4. QUALITY TESTING: Verify output quality meets expected benchmarks
 * 5. PERFORMANCE TESTING: Ensure processing times are within acceptable limits
 * 6. EDGE CASE TESTING: Test with fragment captures and incomplete information
 * 7. INTEGRATION TESTING: Validate end-to-end pipeline with realistic knowledge
 * 
 * These datasets provide comprehensive coverage for TDD development of the
 * PKM ingestion pipeline with real-world knowledge examples.
 */