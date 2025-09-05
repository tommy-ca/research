import { describe, it, expect, beforeEach } from 'vitest';
import { MultiSourceCaptureAgent } from '@/agents/capture-agent';
import { CaptureConfig } from '@/types/capture';

describe('MultiSourceCaptureAgent', () => {
  let captureAgent: MultiSourceCaptureAgent;
  let config: CaptureConfig;

  beforeEach(() => {
    config = {
      name: 'Multi-Source Capture Agent',
      model: 'gpt-4o-mini',
      provider: 'openai',
      memory: {
        type: 'context',
        maxTokens: 8000
      },
      tools: ['webContentExtractor', 'documentProcessor', 'qualityAssessment']
    };
  });

  describe('Agent Initialization', () => {
    it('should initialize with valid configuration', () => {
      captureAgent = new MultiSourceCaptureAgent(config);
      
      expect(captureAgent).toBeDefined();
      expect(captureAgent.name).toBe('Multi-Source Capture Agent');
      expect(captureAgent.model).toBe('gpt-4o-mini');
      expect(captureAgent.provider).toBe('openai');
    });

    it('should throw error with invalid configuration', () => {
      const invalidConfig = { ...config, name: '' };
      
      expect(() => new MultiSourceCaptureAgent(invalidConfig))
        .toThrow('Agent name is required');
    });

    it('should initialize with default memory configuration when not provided', () => {
      const minimalConfig = {
        name: 'Test Agent',
        model: 'gpt-4o-mini',
        provider: 'openai' as const
      };
      
      captureAgent = new MultiSourceCaptureAgent(minimalConfig);
      
      expect(captureAgent.memory.type).toBe('context');
      expect(captureAgent.memory.maxTokens).toBe(4000);
    });
  });

  describe('Tool Configuration', () => {
    beforeEach(() => {
      captureAgent = new MultiSourceCaptureAgent(config);
    });

    it('should register all required tools', () => {
      const tools = captureAgent.getTools();
      
      expect(tools).toContain('webContentExtractor');
      expect(tools).toContain('documentProcessor');
      expect(tools).toContain('qualityAssessment');
      expect(tools.length).toBe(3);
    });

    it('should validate tool availability', () => {
      expect(captureAgent.hasToolAvailable('webContentExtractor')).toBe(true);
      expect(captureAgent.hasToolAvailable('invalidTool')).toBe(false);
    });
  });

  describe('Multi-LLM Provider Support', () => {
    it('should support OpenAI provider', () => {
      const openaiConfig = { ...config, provider: 'openai' as const };
      captureAgent = new MultiSourceCaptureAgent(openaiConfig);
      
      expect(captureAgent.provider).toBe('openai');
      expect(captureAgent.isProviderSupported('openai')).toBe(true);
    });

    it('should support Anthropic provider', () => {
      const anthropicConfig = { ...config, provider: 'anthropic' as const };
      captureAgent = new MultiSourceCaptureAgent(anthropicConfig);
      
      expect(captureAgent.provider).toBe('anthropic');
      expect(captureAgent.isProviderSupported('anthropic')).toBe(true);
    });

    it('should support Google provider', () => {
      const googleConfig = { ...config, provider: 'google' as const };
      captureAgent = new MultiSourceCaptureAgent(googleConfig);
      
      expect(captureAgent.provider).toBe('google');
      expect(captureAgent.isProviderSupported('google')).toBe(true);
    });

    it('should throw error for unsupported provider', () => {
      const invalidConfig = { ...config, provider: 'unsupported' as any };
      
      expect(() => new MultiSourceCaptureAgent(invalidConfig))
        .toThrow('Unsupported provider: unsupported');
    });
  });

  describe('Content Processing', () => {
    beforeEach(() => {
      captureAgent = new MultiSourceCaptureAgent(config);
    });

    describe('Text Content Processing', () => {
      it('should process text content successfully', async () => {
        const input = {
          content: 'This is a test content for PKM system.',
          source: 'direct-input',
          type: 'text' as const
        };

        const result = await captureAgent.processContent(input);

        expect(result).toBeDefined();
        expect(result.id).toBeDefined();
        expect(result.content).toBe(input.content);
        expect(result.source).toBe(input.source);
        expect(result.type).toBe('text');
        expect(result.qualityScore).toBeGreaterThan(0);
        expect(result.qualityScore).toBeLessThanOrEqual(1);
        expect(result.timestamp).toBeDefined();
        expect(result.processed).toBe(true);
      });

      it('should extract metadata from text content', async () => {
        const input = {
          content: 'Machine Learning is a subset of Artificial Intelligence that focuses on algorithms.',
          source: 'research-notes',
          type: 'text' as const,
          metadata: { category: 'AI/ML', tags: ['machine-learning', 'AI'] }
        };

        const result = await captureAgent.processContent(input);

        expect(result.extractedMetadata).toBeDefined();
        expect(result.extractedMetadata.concepts).toContain('Machine Learning');
        expect(result.extractedMetadata.concepts).toContain('Artificial Intelligence');
        expect(result.extractedMetadata.wordCount).toBe(12);
        expect(result.extractedMetadata.originalMetadata).toEqual(input.metadata);
      });
    });

    describe('URL Content Processing', () => {
      it('should process URL content with web extraction', async () => {
        const input = {
          content: 'https://example.com/article',
          source: 'web-browser',
          type: 'url' as const
        };

        const result = await captureAgent.processContent(input);

        expect(result).toBeDefined();
        expect(result.content).not.toBe(input.content); // Should be extracted content
        expect(result.source).toBe('web-browser');
        expect(result.type).toBe('url');
        expect(result.extractedMetadata.originalUrl).toBe('https://example.com/article');
        expect(result.extractedMetadata.title).toBeDefined();
        expect(result.qualityScore).toBeGreaterThan(0);
      });

      it('should handle invalid URLs gracefully', async () => {
        const input = {
          content: 'not-a-valid-url',
          source: 'clipboard',
          type: 'url' as const
        };

        await expect(captureAgent.processContent(input))
          .rejects.toThrow('Invalid URL format');
      });
    });

    describe('File Content Processing', () => {
      it('should process file content', async () => {
        const input = {
          content: '/path/to/document.md',
          source: 'file-system',
          type: 'file' as const
        };

        const result = await captureAgent.processContent(input);

        expect(result).toBeDefined();
        expect(result.source).toBe('file-system');
        expect(result.type).toBe('file');
        expect(result.extractedMetadata.filePath).toBe('/path/to/document.md');
        expect(result.extractedMetadata.fileExtension).toBe('md');
      });

      it('should extract file metadata', async () => {
        const input = {
          content: '/path/to/research.pdf',
          source: 'file-drop',
          type: 'file' as const
        };

        const result = await captureAgent.processContent(input);

        expect(result.extractedMetadata.filePath).toBe('/path/to/research.pdf');
        expect(result.extractedMetadata.fileExtension).toBe('pdf');
        expect(result.extractedMetadata.fileName).toBe('research.pdf');
      });
    });

    describe('Quality Assessment', () => {
      it('should assign high quality score to well-structured content', async () => {
        const input = {
          content: `# Research Notes on Neural Networks
          
          Neural networks are computational models inspired by biological neural networks.
          
          ## Key Concepts:
          - Artificial neurons
          - Backpropagation
          - Deep learning
          
          ## Applications:
          - Image recognition
          - Natural language processing`,
          source: 'research-document',
          type: 'text' as const
        };

        const result = await captureAgent.processContent(input);

        expect(result.qualityScore).toBeGreaterThan(0.7);
        expect(result.extractedMetadata.hasStructure).toBe(true);
        expect(result.extractedMetadata.readabilityScore).toBeGreaterThan(0.6);
      });

      it('should assign lower quality score to poor content', async () => {
        const input = {
          content: 'asdf jkl; qwerty random text no meaning',
          source: 'quick-capture',
          type: 'text' as const
        };

        const result = await captureAgent.processContent(input);

        expect(result.qualityScore).toBeLessThan(0.5);
        expect(result.extractedMetadata.hasStructure).toBe(false);
      });
    });
  });

  describe('Batch Processing', () => {
    beforeEach(() => {
      captureAgent = new MultiSourceCaptureAgent(config);
    });

    it('should process multiple items in batch', async () => {
      const inputs = [
        { content: 'First item', source: 'batch-1', type: 'text' as const },
        { content: 'Second item', source: 'batch-1', type: 'text' as const },
        { content: 'Third item', source: 'batch-1', type: 'text' as const }
      ];

      const results = await captureAgent.processBatch(inputs);

      expect(results).toHaveLength(3);
      expect(results[0].content).toBe('First item');
      expect(results[1].content).toBe('Second item');
      expect(results[2].content).toBe('Third item');
      
      results.forEach(result => {
        expect(result.id).toBeDefined();
        expect(result.processed).toBe(true);
        expect(result.qualityScore).toBeGreaterThan(0);
      });
    });

    it('should handle batch processing errors gracefully', async () => {
      const inputs = [
        { content: 'Valid content', source: 'batch-2', type: 'text' as const },
        { content: 'invalid-url', source: 'batch-2', type: 'url' as const },
        { content: 'More valid content', source: 'batch-2', type: 'text' as const }
      ];

      const results = await captureAgent.processBatch(inputs, { continueOnError: true });

      expect(results).toHaveLength(3);
      expect(results[0].processed).toBe(true);
      expect(results[1].processed).toBe(false);
      expect(results[2].processed).toBe(true);
    });
  });
});