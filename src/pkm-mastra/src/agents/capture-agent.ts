import { 
  CaptureConfig, 
  CaptureConfigSchema, 
  CaptureInput,
  CaptureOutput,
  LLMProvider, 
  MemoryConfig, 
  CaptureTool,
  ExtractedMetadata,
  BatchProcessingOptions
} from '@/types/capture';

/**
 * Multi-Source Capture Agent for PKM system
 * 
 * Handles content ingestion from various sources with quality assessment
 * and supports multiple LLM providers (OpenAI, Anthropic, Google).
 */
export class MultiSourceCaptureAgent {
  public readonly name: string;
  public readonly model: string;
  public readonly provider: LLMProvider;
  public readonly memory: MemoryConfig;
  private readonly tools: CaptureTool[];

  /** Supported LLM providers */
  private static readonly SUPPORTED_PROVIDERS: readonly LLMProvider[] = [
    'openai', 
    'anthropic', 
    'google'
  ] as const;

  /** Default tools for capture operations */
  private static readonly DEFAULT_TOOLS: readonly CaptureTool[] = [
    'webContentExtractor',
    'documentProcessor',
    'qualityAssessment'
  ] as const;

  /** Default memory configuration */
  private static readonly DEFAULT_MEMORY: MemoryConfig = {
    type: 'context',
    maxTokens: 4000
  } as const;

  constructor(config: CaptureConfig | Partial<CaptureConfig>) {
    // Early validation for better error messages
    this.validateProviderSupport(config);

    // Validate and parse full configuration
    const validatedConfig = CaptureConfigSchema.parse(config);

    // Initialize properties
    this.name = validatedConfig.name;
    this.model = validatedConfig.model;
    this.provider = validatedConfig.provider;
    this.memory = validatedConfig.memory ?? MultiSourceCaptureAgent.DEFAULT_MEMORY;
    this.tools = validatedConfig.tools ?? [...MultiSourceCaptureAgent.DEFAULT_TOOLS];
  }

  /**
   * Get a copy of available tools
   */
  public getTools(): CaptureTool[] {
    return [...this.tools];
  }

  /**
   * Check if a specific tool is available
   */
  public hasToolAvailable(tool: string): boolean {
    return this.tools.includes(tool as CaptureTool);
  }

  /**
   * Check if a provider is supported
   */
  public isProviderSupported(provider: string): boolean {
    return MultiSourceCaptureAgent.SUPPORTED_PROVIDERS.includes(provider as LLMProvider);
  }

  /**
   * Process content from various sources
   */
  public async processContent(input: CaptureInput): Promise<CaptureOutput> {
    // Generate unique ID
    const id = `capture_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const timestamp = new Date().toISOString();
    
    let processedContent = input.content;
    let extractedMetadata: ExtractedMetadata = {};
    let qualityScore = 0.5; // Default score

    try {
      // Process based on input type
      switch (input.type) {
        case 'text':
          ({ content: processedContent, metadata: extractedMetadata, qualityScore } = 
            await this.processTextContent(input));
          break;
        case 'url':
          ({ content: processedContent, metadata: extractedMetadata, qualityScore } = 
            await this.processUrlContent(input));
          break;
        case 'file':
          ({ content: processedContent, metadata: extractedMetadata, qualityScore } = 
            await this.processFileContent(input));
          break;
        case 'clipboard':
          ({ content: processedContent, metadata: extractedMetadata, qualityScore } = 
            await this.processTextContent(input));
          break;
        default:
          throw new Error(`Unsupported content type: ${input.type}`);
      }

      return {
        id,
        content: processedContent,
        source: input.source,
        type: input.type,
        extractedMetadata,
        qualityScore,
        timestamp,
        processed: true
      };

    } catch (error) {
      // Re-throw validation errors (like invalid URLs)
      if (error instanceof Error && error.message.includes('Invalid URL format')) {
        throw error;
      }
      
      // Return failed result for other errors
      return {
        id,
        content: input.content,
        source: input.source,
        type: input.type,
        extractedMetadata: { originalMetadata: input.metadata },
        qualityScore: 0,
        timestamp,
        processed: false
      };
    }
  }

  /**
   * Process multiple items in batch
   */
  public async processBatch(
    inputs: CaptureInput[], 
    options?: BatchProcessingOptions
  ): Promise<CaptureOutput[]> {
    const { continueOnError = false } = options || {};
    const results: CaptureOutput[] = [];

    for (const input of inputs) {
      try {
        const result = await this.processContent(input);
        results.push(result);
      } catch (error) {
        if (continueOnError) {
          // Create failed result
          const failedResult: CaptureOutput = {
            id: `failed_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            content: input.content,
            source: input.source,
            type: input.type,
            extractedMetadata: { originalMetadata: input.metadata },
            qualityScore: 0,
            timestamp: new Date().toISOString(),
            processed: false
          };
          results.push(failedResult);
        } else {
          throw error;
        }
      }
    }

    return results;
  }

  /**
   * Process text content and extract metadata
   */
  private async processTextContent(input: CaptureInput): Promise<{
    content: string;
    metadata: ExtractedMetadata;
    qualityScore: number;
  }> {
    const content = input.content;
    const words = content.trim().split(/\s+/);
    const wordCount = words.length;
    
    // Extract concepts (simple keyword extraction)
    const concepts = this.extractConcepts(content);
    
    // Assess structure
    const hasStructure = /^#|\*\s|-\s|\d+\.\s/m.test(content);
    
    // Calculate readability (simplified)
    const readabilityScore = this.calculateReadabilityScore(content);
    
    // Calculate quality score
    const qualityScore = this.calculateQualityScore({
      wordCount,
      hasStructure,
      readabilityScore,
      concepts: concepts.length
    });

    return {
      content,
      metadata: {
        concepts,
        wordCount,
        hasStructure,
        readabilityScore,
        originalMetadata: input.metadata
      },
      qualityScore
    };
  }

  /**
   * Process URL content with web extraction
   */
  private async processUrlContent(input: CaptureInput): Promise<{
    content: string;
    metadata: ExtractedMetadata;
    qualityScore: number;
  }> {
    const url = input.content;
    
    // Validate URL format
    if (!this.isValidUrl(url)) {
      throw new Error('Invalid URL format');
    }

    // Mock web extraction (in real implementation, would use web scraping)
    const extractedContent = `Extracted content from ${url}`;
    const title = `Article from ${new URL(url).hostname}`;
    
    const qualityScore = 0.8; // Mock good quality for valid URLs

    return {
      content: extractedContent,
      metadata: {
        originalUrl: url,
        title,
        originalMetadata: input.metadata
      },
      qualityScore
    };
  }

  /**
   * Process file content
   */
  private async processFileContent(input: CaptureInput): Promise<{
    content: string;
    metadata: ExtractedMetadata;
    qualityScore: number;
  }> {
    const filePath = input.content;
    const fileName = filePath.split('/').pop() || '';
    const fileExtension = fileName.includes('.') ? fileName.split('.').pop() || '' : '';
    
    // Mock file reading (in real implementation, would read actual file)
    const content = `Content from file: ${fileName}`;
    const qualityScore = 0.7; // Mock quality for files

    return {
      content,
      metadata: {
        filePath,
        fileName,
        fileExtension,
        originalMetadata: input.metadata
      },
      qualityScore
    };
  }

  /**
   * Extract concepts from text (simplified keyword extraction)
   */
  private extractConcepts(text: string): string[] {
    const concepts: string[] = [];
    
    // First, extract proper nouns and capitalized phrases
    const capitalizedPhrases = text.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*/g) || [];
    concepts.push(...capitalizedPhrases);
    
    // Then extract individual keywords
    const commonWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'this', 'that', 'these', 'those']);
    
    const words = text.toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 3 && !commonWords.has(word));
    
    concepts.push(...words);
    
    // Return unique concepts, prioritizing capitalized phrases
    return [...new Set(concepts)].slice(0, 10);
  }

  /**
   * Calculate readability score (simplified)
   */
  private calculateReadabilityScore(text: string): number {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const words = text.trim().split(/\s+/);
    const avgWordsPerSentence = words.length / Math.max(sentences.length, 1);
    
    // Readability factors
    let score = 0.5; // Base score
    
    // Optimal sentence length (10-20 words)
    if (avgWordsPerSentence >= 8 && avgWordsPerSentence <= 25) {
      score += 0.3;
    }
    
    // Structure indicators improve readability
    const hasStructuralElements = /^#|\*\s|-\s|\d+\.\s/m.test(text);
    if (hasStructuralElements) {
      score += 0.2;
    }
    
    // Proper punctuation
    if (/[.!?]/.test(text)) {
      score += 0.1;
    }
    
    return Math.max(0, Math.min(1, score));
  }

  /**
   * Calculate overall quality score
   */
  private calculateQualityScore(factors: {
    wordCount: number;
    hasStructure: boolean;
    readabilityScore: number;
    concepts: number;
  }): number {
    let score = 0;
    
    // Word count factor (sweet spot around 50-200 words)
    if (factors.wordCount >= 10) {
      score += 0.2;
    }
    if (factors.wordCount >= 50) {
      score += 0.2;
    }
    if (factors.wordCount >= 100) {
      score += 0.1;
    }
    
    // Structure bonus (major factor for well-structured content)
    if (factors.hasStructure) {
      score += 0.3; // Increased from 0.2
    }
    
    // Readability factor
    score += factors.readabilityScore * 0.2;
    
    // Concepts factor (good concepts indicate quality)
    if (factors.concepts > 2) {
      score += 0.1;
    }
    if (factors.concepts > 5) {
      score += 0.1; // Additional bonus for rich content
    }
    
    // Check for low-quality indicators only for very short content
    if (factors.wordCount < 10 && factors.concepts < 2) {
      score = Math.min(score, 0.4);
    }
    
    return Math.max(0, Math.min(1, score));
  }

  /**
   * Validate URL format
   */
  private isValidUrl(string: string): boolean {
    try {
      new URL(string);
      return true;
    } catch (_) {
      return false;
    }
  }

  /**
   * Validate provider support before schema validation
   */
  private validateProviderSupport(config: CaptureConfig | Partial<CaptureConfig>): void {
    const rawProvider = (config as any).provider;
    if (rawProvider && !this.isProviderSupported(rawProvider)) {
      throw new Error(`Unsupported provider: ${rawProvider}`);
    }
  }
}