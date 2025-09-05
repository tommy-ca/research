"""
PKM Validation System - Wiki-Link Validator
FR-VAL-003: Wiki-Link Validation Implementation

TDD REFACTOR Phase: Production-optimized implementation with extracted schemas
Following SOLID principles: Single responsibility, dependency inversion
Following KISS principle: Simple, readable, maintainable code
Following DRY principle: Reuse centralized schemas and patterns
"""

from pathlib import Path
from typing import List, Dict, Any, Set, Optional
import re
from functools import lru_cache
import time

from .base import BaseValidator, ValidationResult
from .schemas.wiki_link_schema import (
    WikiLinkPatterns,
    VaultStructureRules,
    WikiLinkValidationRules,
    WikiLinkPerformanceOptimizer
)


class WikiLinkExtractor:
    """
    Extract wiki-style links from markdown content.
    Single responsibility: Only extracts links, doesn't validate them.
    
    REFACTOR: Now uses centralized patterns and performance optimization
    """
    
    def __init__(self, patterns: WikiLinkPatterns = None):
        """Initialize with configurable patterns for dependency injection"""
        self.patterns = patterns or WikiLinkPatterns()
    
    def extract_links(self, content: str) -> List[str]:
        """Extract wiki-links from content using optimized patterns"""
        return self.patterns.extract_links(content)


class VaultFileResolver:
    """
    Resolve wiki-link text to actual vault files.
    Single responsibility: Only handles file resolution logic.
    
    REFACTOR: Now uses configurable rules and caching for performance
    """
    
    def __init__(self, vault_path: Path, structure_rules: VaultStructureRules = None):
        """Initialize with vault path and configurable structure rules"""
        self.vault_path = Path(vault_path)
        self.rules = structure_rules or VaultStructureRules()
        
        # Performance optimization: Cache file system scan results
        self._file_cache = {}
        self._last_scan_time = 0
        self._cache_ttl = 60  # Cache for 60 seconds
    
    @lru_cache(maxsize=500)
    def resolve_link(self, link_text: str) -> List[Path]:
        """
        Resolve link text to file paths with performance optimization
        
        REFACTOR: Added caching and configurable search behavior
        """
        if not link_text:
            return []
            
        # Use centralized filename normalization
        normalized = self.rules.normalize_filename(link_text)
        matches = []
        
        # Check if we need to refresh file cache
        current_time = time.time()
        if current_time - self._last_scan_time > self._cache_ttl:
            self._refresh_file_cache()
        
        # Search through all configured paths
        for search_path in self.rules.search_paths:
            search_dir = self.vault_path / search_path
            if not search_dir.exists():
                continue
                
            # Try each file extension in priority order
            for ext in self.rules.file_extensions:
                candidate = search_dir / f"{normalized}{ext}"
                if candidate.exists():
                    matches.append(candidate)
                    break  # First match wins per directory (performance optimization)
                    
        return matches
    
    def _refresh_file_cache(self):
        """Refresh internal file cache for performance"""
        self._file_cache.clear()
        self._last_scan_time = time.time()
        # Could add more sophisticated caching here if needed


class WikiLinkValidator(BaseValidator):
    """
    Validates wiki-links in PKM markdown files.
    Integrates WikiLinkExtractor and VaultFileResolver with performance optimization.
    
    REFACTOR: Enhanced with schema-driven validation, caching, and better error messages
    Following SOLID: Single responsibility, dependency injection, extensible design
    """
    
    def __init__(self, 
                 vault_path: Path,
                 extractor: WikiLinkExtractor = None,
                 resolver: VaultFileResolver = None,
                 rules: WikiLinkValidationRules = None,
                 optimizer: WikiLinkPerformanceOptimizer = None):
        """
        Initialize with dependency injection for all components
        
        REFACTOR: Full dependency injection for testing and extensibility
        """
        self.vault_path = Path(vault_path)
        
        # Dependency injection with sensible defaults
        self.extractor = extractor or WikiLinkExtractor()
        self.resolver = resolver or VaultFileResolver(vault_path)
        self.rules = rules or WikiLinkValidationRules()
        self.optimizer = optimizer or WikiLinkPerformanceOptimizer()
        
        # Performance tracking
        self._validation_stats = {
            'files_processed': 0,
            'cache_hits': 0,
            'total_links_processed': 0
        }
    
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """
        Validate wiki-links in markdown file with performance optimization
        
        REFACTOR: Added caching, performance tracking, and enhanced error reporting
        """
        results = []
        validation_start = time.time()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Performance optimization: Skip validation if content unchanged
            content_hash = self.optimizer.get_content_hash(content)
            if self.optimizer.should_skip_validation(file_path, content_hash):
                self._validation_stats['cache_hits'] += 1
                return results  # Return cached result (empty = no errors)
            
            # Extract all wiki-links from content using optimized extractor
            links = self.extractor.extract_links(content)
            self._validation_stats['total_links_processed'] += len(links)
            
            # Check for empty wiki-link patterns that weren't caught by extraction
            if WikiLinkPatterns.has_empty_links(content):
                results.append(ValidationResult(
                    file_path=file_path,
                    rule="empty-wiki-link", 
                    severity=self.rules.get_severity('empty_wiki_link'),
                    message=self.rules.format_error_message('empty_wiki_link')
                ))

            # Performance optimization: Process unique links only to avoid duplicate resolution
            unique_links = list(set(links))
            
            for link in unique_links:
                # Handle empty links specially  
                if not link or link.isspace():
                    results.append(ValidationResult(
                        file_path=file_path,
                        rule="empty-wiki-link",
                        severity=self.rules.get_severity('empty_wiki_link'),
                        message=self.rules.format_error_message('empty_wiki_link')
                    ))
                    continue
                
                # Resolve link to actual files using optimized resolver
                resolved_files = self.resolver.resolve_link(link)
                
                if len(resolved_files) == 0:
                    # Broken link - no matches found
                    results.append(ValidationResult(
                        file_path=file_path,
                        rule="broken-wiki-link", 
                        severity=self.rules.get_severity('broken_wiki_link'),
                        message=self.rules.format_error_message('broken_wiki_link', link_text=link)
                    ))
                elif len(resolved_files) > 1:
                    # Ambiguous link - multiple matches with enhanced error message
                    match_paths = [str(f.relative_to(self.vault_path)) for f in resolved_files]
                    results.append(ValidationResult(
                        file_path=file_path,
                        rule="ambiguous-wiki-link",
                        severity=self.rules.get_severity('ambiguous_wiki_link'),
                        message=self.rules.format_error_message('ambiguous_wiki_link', 
                                                               link_text=link,
                                                               matches=match_paths)
                    ))
                # Single match = valid link, no error needed
            
            # Performance optimization: Cache successful validation
            if not results:  # Only cache if no errors found
                self.optimizer.cache_validation_result(file_path, content_hash)
            
            # Track performance
            validation_time = (time.time() - validation_start) * 1000  # Convert to milliseconds
            if validation_time > self.rules.PERFORMANCE_THRESHOLDS['max_validation_time_ms']:
                # Could add performance warning here if needed
                pass
                
        except FileNotFoundError:
            results.append(ValidationResult(
                file_path=file_path,
                rule="file-not-found",
                severity="error", 
                message=f"File not found: {file_path}"
            ))
        except UnicodeDecodeError as e:
            results.append(ValidationResult(
                file_path=file_path,
                rule="encoding-error",
                severity="error",
                message=f"File encoding error - ensure file is UTF-8 encoded: {e}"
            ))
        except Exception as e:
            results.append(ValidationResult(
                file_path=file_path,
                rule="validation-error",
                severity="error",
                message=f"Wiki-link validation error: {e}"
            ))
        
        # Update statistics
        self._validation_stats['files_processed'] += 1
        return results
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get performance statistics for monitoring and optimization"""
        return self._validation_stats.copy()


# Convenience functions for external usage
def get_wiki_link_patterns() -> WikiLinkPatterns:
    """Get wiki-link patterns instance for external use"""
    return WikiLinkPatterns()


def get_vault_structure_rules() -> VaultStructureRules:
    """Get vault structure rules instance for external use"""  
    return VaultStructureRules()


def get_wiki_link_validation_rules() -> WikiLinkValidationRules:
    """Get validation rules instance for external use"""
    return WikiLinkValidationRules()


# Export commonly used classes for convenience
__all__ = [
    'WikiLinkValidator',
    'WikiLinkExtractor',
    'VaultFileResolver',
    'get_wiki_link_patterns',
    'get_vault_structure_rules', 
    'get_wiki_link_validation_rules'
]