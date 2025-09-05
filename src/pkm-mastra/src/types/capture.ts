import { z } from 'zod';

// LLM Provider types
export const LLMProviderSchema = z.enum(['openai', 'anthropic', 'google']);
export type LLMProvider = z.infer<typeof LLMProviderSchema>;

// Memory configuration
export const MemoryConfigSchema = z.object({
  type: z.enum(['context', 'vector', 'hybrid']).default('context'),
  maxTokens: z.number().min(1000).max(32000).default(4000),
  vectorStore: z.string().optional(),
  embeddingModel: z.string().optional()
});
export type MemoryConfig = z.infer<typeof MemoryConfigSchema>;

// Capture tool types
export const CaptureToolSchema = z.enum([
  'webContentExtractor',
  'documentProcessor', 
  'qualityAssessment',
  'metadataExtractor',
  'sourceValidator',
  'contentCleaner'
]);
export type CaptureTool = z.infer<typeof CaptureToolSchema>;

// Main capture configuration
export const CaptureConfigSchema = z.object({
  name: z.string().min(1, 'Agent name is required'),
  model: z.string().min(1, 'Model is required'),
  provider: LLMProviderSchema,
  memory: MemoryConfigSchema.optional(),
  tools: z.array(CaptureToolSchema).optional().default([
    'webContentExtractor',
    'documentProcessor', 
    'qualityAssessment'
  ])
});
export type CaptureConfig = z.infer<typeof CaptureConfigSchema>;

// Capture input/output types
export const CaptureInputSchema = z.object({
  content: z.string(),
  source: z.string(),
  type: z.enum(['text', 'url', 'file', 'clipboard']),
  metadata: z.record(z.any()).optional()
});
export type CaptureInput = z.infer<typeof CaptureInputSchema>;

// Enhanced metadata schema
export const ExtractedMetadataSchema = z.object({
  // Text processing metadata
  concepts: z.array(z.string()).optional(),
  wordCount: z.number().optional(),
  hasStructure: z.boolean().optional(),
  readabilityScore: z.number().min(0).max(1).optional(),
  
  // URL processing metadata  
  originalUrl: z.string().optional(),
  title: z.string().optional(),
  
  // File processing metadata
  filePath: z.string().optional(),
  fileName: z.string().optional(),
  fileExtension: z.string().optional(),
  
  // Original metadata preservation
  originalMetadata: z.record(z.any()).optional()
}).passthrough(); // Allow additional properties

export type ExtractedMetadata = z.infer<typeof ExtractedMetadataSchema>;

export const CaptureOutputSchema = z.object({
  id: z.string(),
  content: z.string(),
  source: z.string(),
  type: z.string(),
  extractedMetadata: ExtractedMetadataSchema,
  qualityScore: z.number().min(0).max(1),
  timestamp: z.string(),
  processed: z.boolean().default(false)
});
export type CaptureOutput = z.infer<typeof CaptureOutputSchema>;

// Batch processing options
export const BatchProcessingOptionsSchema = z.object({
  continueOnError: z.boolean().default(false),
  maxConcurrency: z.number().min(1).max(10).default(3)
}).optional();
export type BatchProcessingOptions = z.infer<typeof BatchProcessingOptionsSchema>;