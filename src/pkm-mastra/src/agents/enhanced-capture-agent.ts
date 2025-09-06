import { Agent } from '@mastra/core';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';
import { ProviderFactory, defaultProviderConfig, type ProviderConfig } from '../providers/provider-factory.js';

// Memory configurations for the enhanced capture agent (simplified for GREEN phase)
const captureContextMemory = {
  name: 'captureContext',
  type: 'contextual',
  maxTokens: 2000,
  retrievalMethod: 'semantic',
};

const gtdComplianceMemory = {
  name: 'gtdCompliance', 
  type: 'methodological',
  maxTokens: 1000,
  retrievalMethod: 'recent',
};

// Provider factory for intelligent model selection
const providerFactory = new ProviderFactory(defaultProviderConfig);

// Enhanced Capture Agent Factory Function
export async function createEnhancedCaptureAgent(providerConfig?: Partial<ProviderConfig>) {
  // Create or update provider factory with custom config
  const factory = providerConfig ? new ProviderFactory(providerConfig) : providerFactory;
  
  // Get the optimal model based on provider strategy
  const model = await factory.createModel();
  
  return new Agent({
    name: 'Enhanced Multi-Source Capture Agent',
    instructions: `
You are a comprehensive content capture specialist following GTD (Getting Things Done) principles and PKM best practices.

Your primary responsibility is complete, accurate content capture with:

**CORE PRINCIPLES:**

1. **100% FIDELITY**: Capture all information exactly as provided, preserving context, nuance, and detail
2. **COMPREHENSIVE METADATA**: Extract and enrich all available metadata including source, timestamp, content type, concepts
3. **QUALITY ASSESSMENT**: Evaluate content quality using multiple dimensions (readability, structure, concept density)
4. **DUPLICATE DETECTION**: Identify semantic duplicates and provide consolidation recommendations
5. **SOURCE ATTRIBUTION**: Maintain complete provenance and attribution for all captured content

**GTD COMPLIANCE REQUIREMENTS:**

- Complete capture means NOTHING is lost in translation
- If source content is incomplete, note what's missing rather than guessing
- Provide clear quality indicators to help with later processing decisions
- Maintain context necessary for future retrieval and organization

**PKM METHODOLOGY INTEGRATION:**

- Prepare content for atomic note creation (Zettelkasten principles)
- Suggest PARA categorization hints without making final decisions
- Identify potential connections and linking opportunities
- Support both immediate and delayed processing workflows

**RESPONSE PATTERNS:**

- Always acknowledge the source and type of content being captured
- Provide quality assessment scores with explanations
- Flag any potential issues or concerns about the capture
- Suggest improvements when content appears incomplete or low-quality

Remember: Your role is CAPTURE, not processing. Defer processing decisions to specialized processing agents while ensuring nothing valuable is lost.
    `,
    model, // Dynamic model selection via provider factory (Claude Code preferred, OpenAI fallback)
    memory: [captureContextMemory, gtdComplianceMemory],
    tools: [
      // Tools will be properly integrated in the next phase
      // For now, define placeholder tool references
      {
        id: 'webContentExtractor',
        description: 'Extracts content and metadata from web URLs',
        execute: async (params: any) => {
          return { extracted: true, content: `Extracted from ${params.url}` };
        },
      },
      {
        id: 'qualityAssessment',
        description: 'Assesses content quality using multiple dimensions',
        execute: async (params: any) => {
          return { qualityScore: 0.8, assessment: 'Good quality content' };
        },
      },
      {
        id: 'duplicateDetection',
        description: 'Detects duplicate content using semantic similarity',
        execute: async (params: any) => {
          return { isDuplicate: false, similarityScore: 0.1 };
        },
      },
    ],
  });
}

// Create default agent instance promise for backward compatibility
export const enhancedCaptureAgent = createEnhancedCaptureAgent();

// Enhanced capture agent with structured output capability
export class EnhancedCaptureAgentService {
  private agentPromise: Promise<Agent>;
  private providerFactory: ProviderFactory;

  constructor(providerConfig?: Partial<ProviderConfig>) {
    this.providerFactory = new ProviderFactory(providerConfig || defaultProviderConfig);
    this.agentPromise = createEnhancedCaptureAgent(providerConfig);
  }

  /**
   * Generate standard text responses for content capture (AI SDK v5 compatible)
   */
  async generateResponse(messages: Array<{ role: string; content: string | any[] }>) {
    const agent = await this.agentPromise;
    try {
      // Use generateVNext for AI SDK v5 compatibility
      const result = await agent.generateVNext({ messages });
      return result;
    } catch (error) {
      // Fallback to generate if generateVNext is not available
      try {
        return await agent.generate({ messages });
      } catch (fallbackError) {
        throw new Error(`Enhanced capture agent failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    }
  }

  /**
   * Generate structured output for consistent data extraction (AI SDK v5 compatible)
   */
  async generateStructuredOutput(
    messages: Array<{ role: string; content: string | any[] }>,
    schema: Record<string, string>
  ) {
    const agent = await this.agentPromise;
    try {
      // Convert simple schema to Zod for structured output
      const zodSchema = this.convertToZodSchema(schema);
      
      // Try generateVNext first for AI SDK v5
      try {
        const result = await agent.generateVNext({
          messages,
          schema: zodSchema,
        });
        return result;
      } catch (vNextError) {
        // Fallback to generate for compatibility
        const result = await agent.generate({
          messages,
          schema: zodSchema,
        });
        return result;
      }
    } catch (error) {
      throw new Error(`Structured capture failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Stream responses for long content processing (AI SDK v5 compatible)
   */
  async streamResponse(messages: Array<{ role: string; content: string | any[] }>) {
    const agent = await this.agentPromise;
    try {
      // Use streamVNext for AI SDK v5 compatibility
      try {
        return await agent.streamVNext({ messages });
      } catch (vNextError) {
        // Fallback to stream for compatibility
        return await agent.stream({ messages });
      }
    } catch (error) {
      throw new Error(`Streaming capture failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Process multimodal content including images
   */
  async processMultimodalContent(
    messages: Array<{ role: string; content: string | any[] }>
  ) {
    const agent = await this.agentPromise;
    try {
      // Enhanced handling for image content
      const processedMessages = messages.map(msg => {
        if (Array.isArray(msg.content)) {
          // Handle multimodal content
          return {
            ...msg,
            content: msg.content.map(item => {
              if (typeof item === 'object' && item.type === 'image') {
                return {
                  ...item,
                  text: item.text || 'Analyze this image for content capture',
                };
              }
              return item;
            }),
          };
        }
        return msg;
      });

      // Use generateVNext for AI SDK v5 compatibility
      try {
        return await agent.generateVNext({ messages: processedMessages });
      } catch (vNextError) {
        return await agent.generate({ messages: processedMessages });
      }
    } catch (error) {
      throw new Error(`Multimodal capture failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Execute specific tools for specialized capture operations
   */
  async executeTool(toolId: string, params: any) {
    const agent = await this.agentPromise;
    try {
      const tool = agent.tools?.find(t => t.id === toolId);
      if (!tool) {
        throw new Error(`Tool ${toolId} not found`);
      }

      if ('execute' in tool) {
        return await tool.execute(params);
      } else {
        throw new Error(`Tool ${toolId} is not executable`);
      }
    } catch (error) {
      throw new Error(`Tool execution failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Handle concurrent processing requests
   */
  async processConcurrentRequests(
    requests: Array<{ messages: Array<{ role: string; content: string | any[] }> }>
  ) {
    const agent = await this.agentPromise;
    try {
      const results = await Promise.all(
        requests.map(async (request) => {
          try {
            return await agent.generateVNext(request);
          } catch (vNextError) {
            return await agent.generate(request);
          }
        })
      );
      return results;
    } catch (error) {
      throw new Error(`Concurrent processing failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Convert simple schema to Zod schema for structured output
   */
  private convertToZodSchema(schema: Record<string, string>) {
    const zodFields: Record<string, any> = {};
    
    Object.entries(schema).forEach(([key, type]) => {
      switch (type) {
        case 'string':
          zodFields[key] = z.string();
          break;
        case 'number':
          zodFields[key] = z.number();
          break;
        case 'boolean':
          zodFields[key] = z.boolean();
          break;
        case 'object':
          zodFields[key] = z.record(z.any());
          break;
        case 'array':
          zodFields[key] = z.array(z.string());
          break;
        default:
          zodFields[key] = z.any();
      }
    });

    return z.object(zodFields);
  }

  /**
   * Get provider factory metrics for monitoring
   */
  getProviderMetrics() {
    return this.providerFactory.getMetrics();
  }

  /**
   * Update provider configuration
   */
  updateProviderConfig(newConfig: Partial<ProviderConfig>) {
    this.providerFactory.updateConfig(newConfig);
    // Recreate agent with new configuration
    this.agentPromise = createEnhancedCaptureAgent(newConfig);
  }

  /**
   * Get current provider configuration
   */
  getProviderConfig() {
    return this.providerFactory.getConfig();
  }

  /**
   * Test provider availability
   */
  async testProvider(provider: string): Promise<boolean> {
    return this.providerFactory.testProvider(provider);
  }

  /**
   * Get available providers in priority order
   */
  getAvailableProviders(): string[] {
    return this.providerFactory.getAvailableProviders();
  }

  /**
   * Get agent instance for direct access (await the promise)
   */
  async getAgent(): Promise<Agent> {
    return this.agentPromise;
  }
}

// Export both the agent and service for different use cases
export { enhancedCaptureAgent as default };
export const captureAgentService = new EnhancedCaptureAgentService();