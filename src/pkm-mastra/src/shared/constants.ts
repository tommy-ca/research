/**
 * PKM System Shared Constants
 * 
 * Centralized constants to eliminate DRY violations and ensure consistency
 * across the PKM ingestion pipeline and related components.
 */

// PARA Method Categories (Tiago Forte's PARA organizational system)
export const PARA_CATEGORIES = ['projects', 'areas', 'resources', 'archive'] as const;
export type PARACategory = typeof PARA_CATEGORIES[number];

// PARA Category Descriptions for validation and documentation
export const PARA_CATEGORY_DESCRIPTIONS = {
  projects: 'Specific outcomes with deadlines and clear completion criteria',
  areas: 'Ongoing responsibilities and standards to maintain over time', 
  resources: 'Future reference topics and general knowledge for later use',
  archive: 'Inactive items from other categories that are no longer relevant',
} as const;

// Default Processing Options
export const DEFAULT_PROCESSING_OPTIONS = {
  modelPreference: 'auto' as const,
  qualityThreshold: 0.8,
  atomicityStrict: true,
} as const;

// Quality Thresholds for different content types
export const QUALITY_THRESHOLDS = {
  meeting_notes: { min: 0.6, max: 0.8 },
  fragments: { min: 0.65, max: 0.85 },  
  formal_content: { min: 0.75, max: 0.98 },
  methodology: { min: 0.8, max: 0.95 },
} as const;

// Model Selection Thresholds
export const MODEL_SELECTION = {
  COMPLEXITY_THRESHOLD: 0.4,
  LENGTH_THRESHOLD: 3000,
  QUALITY_THRESHOLD: 0.9,
} as const;