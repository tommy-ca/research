"""
PKM Validation System - Wiki-Link Schema Definitions
FR-VAL-003: Wiki-Link Schema and Validation Rules

TDD REFACTOR Phase: Extract schema definitions for maintainability and reuse
Following DRY principle: Single source of truth for validation rules
"""

import re
from typing import Set, List
from functools import lru_cache


class WikiLinkPatterns:
    """
    Centralized wiki-link regex patterns - DRY principle
    Pre-compiled for performance optimization
    """
    
    # Main wiki-link pattern - handles nested brackets with non-greedy matching
    WIKI_LINK_PATTERN = re.compile(r'\[\[(.*?)\]\]')
    
    # Empty wiki-link pattern for validation
    EMPTY_WIKI_LINK_PATTERN = re.compile(r'\[\[\s*\]\]')
    
    # Pattern for alias splitting (Target|Alias format)
    ALIAS_SEPARATOR = '|'
    
    @classmethod
    def extract_links(cls, content: str) -> List[str]:
        """Extract wiki-links using optimized patterns"""
        if not content:
            return []
            
        matches = cls.WIKI_LINK_PATTERN.findall(content)
        links = []
        
        for match in matches:
            # Handle alias format: [[Target|Alias]] -> extract "Target"
            if cls.ALIAS_SEPARATOR in match:
                target = match.split(cls.ALIAS_SEPARATOR, 1)[0]
            else:
                target = match
                
            # Clean and validate
            target = target.strip()
            if target:  # Ignore empty links
                links.append(target)
                
        return links
    
    @classmethod
    def has_empty_links(cls, content: str) -> bool:
        """Check for empty wiki-link patterns"""
        return bool(cls.EMPTY_WIKI_LINK_PATTERN.search(content))


class VaultStructureRules:
    """
    Centralized vault structure and file resolution rules - DRY principle
    Configurable search behavior for different PKM systems
    """
    
    # Default PKM vault search paths in priority order
    DEFAULT_SEARCH_PATHS: List[str] = [
        "permanent/notes",      # Zettelkasten atomic notes
        "02-projects",          # PARA method projects  
        "03-areas",             # PARA method areas
        "04-resources",         # PARA method resources
        "daily",                # Daily notes
        "00-inbox",             # Capture inbox
        "05-archives"           # Archived content
    ]
    
    # File extension priority order - markdown first
    DEFAULT_FILE_EXTENSIONS: List[str] = [".md", ".txt", ".org", ".rst"]
    
    def __init__(self, search_paths: List[str] = None, file_extensions: List[str] = None):
        """Initialize with configurable paths and extensions"""
        self.search_paths = search_paths or self.DEFAULT_SEARCH_PATHS
        self.file_extensions = file_extensions or self.DEFAULT_FILE_EXTENSIONS
    
    @staticmethod
    @lru_cache(maxsize=1000)
    def normalize_filename(link_text: str) -> str:
        """
        Normalize link text to filesystem-friendly format
        Cached for performance with repeated normalizations
        """
        if not link_text:
            return ""
            
        # KISS: Simple normalization rules
        normalized = link_text.lower()
        normalized = normalized.replace(' ', '-')
        normalized = re.sub(r'[^\w\-.]', '-', normalized)  # Replace special chars
        normalized = re.sub(r'-+', '-', normalized)        # Collapse multiple dashes
        normalized = normalized.strip('-')                  # Remove leading/trailing dashes
        
        return normalized


class WikiLinkValidationRules:
    """
    Centralized validation rules and enhanced error messages
    Following DRY principle: Single source of truth for rules
    """
    
    def __init__(self, vault_structure: VaultStructureRules = None):
        """Initialize validation rules with comprehensive error templates"""
        
        # Backward compatibility: Include search paths and extensions for tests
        self._vault_structure = vault_structure or VaultStructureRules()
        self.SEARCH_PATHS = self._vault_structure.search_paths
        self.FILE_EXTENSIONS = self._vault_structure.file_extensions
        
        # Enhanced error message templates with actionable suggestions
        self.ERROR_MESSAGES = {
            'broken_wiki_link': (
                "Wiki-link '{link_text}' not found in vault. "
                "Suggestions: 1) Check spelling, 2) Create the note, or 3) Update the link target."
            ),
            'ambiguous_wiki_link': (
                "Wiki-link '{link_text}' has multiple matches: {matches}. "
                "Use more specific link text or include path information."
            ),
            'empty_wiki_link': (
                "Empty wiki-link found ([[]]). "
                "Either remove the empty link or add the target note name."
            ),
            'invalid_link_format': (
                "Invalid wiki-link format: {link_text}. "
                "Use [[Target Note]] or [[Target Note|Display Text]] format."
            )
        }
        
        # Validation severity levels
        self.SEVERITY_LEVELS = {
            'broken_wiki_link': 'error',
            'ambiguous_wiki_link': 'warning', 
            'empty_wiki_link': 'error',
            'invalid_link_format': 'error'
        }
        
        # Performance thresholds
        self.PERFORMANCE_THRESHOLDS = {
            'max_links_per_file': 200,      # Warn if file has too many links
            'max_validation_time_ms': 100,   # Warn if validation is too slow
            'cache_size_limit': 1000         # LRU cache size for performance
        }
    
    def format_error_message(self, error_type: str, **kwargs) -> str:
        """Format error message with enhanced context and suggestions"""
        template = self.ERROR_MESSAGES.get(error_type, "Unknown wiki-link validation error")
        
        try:
            # Special handling for ambiguous links - format file paths nicely
            if error_type == 'ambiguous_wiki_link' and 'matches' in kwargs:
                matches = kwargs['matches']
                if isinstance(matches, list):
                    # Format as numbered list for better readability
                    formatted_matches = ', '.join(f"{i+1}) {match}" for i, match in enumerate(matches))
                    kwargs['matches'] = formatted_matches
                    
            return template.format(**kwargs)
        except KeyError as e:
            # Fallback with debug information
            return f"{template} (Missing template variable: {e})"
    
    def get_severity(self, error_type: str) -> str:
        """Get severity level for error type"""
        return self.SEVERITY_LEVELS.get(error_type, 'error')


class WikiLinkPerformanceOptimizer:
    """
    Performance optimization utilities for wiki-link validation
    Implements caching and batch processing strategies
    """
    
    def __init__(self, cache_size: int = 1000):
        """Initialize with configurable cache size"""
        self.cache_size = cache_size
        self._file_resolution_cache = {}
        self._content_hash_cache = {}
    
    @lru_cache(maxsize=1000)
    def get_content_hash(self, content: str) -> str:
        """Get hash of content for caching validation results"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()
    
    def should_skip_validation(self, file_path, content_hash: str) -> bool:
        """Check if file validation can be skipped based on cache"""
        cached_hash = self._content_hash_cache.get(str(file_path))
        return cached_hash == content_hash
    
    def cache_validation_result(self, file_path, content_hash: str):
        """Cache successful validation result"""
        self._content_hash_cache[str(file_path)] = content_hash
        
        # Maintain cache size limit
        if len(self._content_hash_cache) > self.cache_size:
            # Remove oldest entries (simple FIFO)
            oldest_key = next(iter(self._content_hash_cache))
            del self._content_hash_cache[oldest_key]


# Export commonly used classes for convenience
__all__ = [
    'WikiLinkPatterns',
    'VaultStructureRules', 
    'WikiLinkValidationRules',
    'WikiLinkPerformanceOptimizer'
]