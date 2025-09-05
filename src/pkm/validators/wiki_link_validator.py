"""
PKM Validation System - Wiki-Link Validator
FR-VAL-003: Wiki-Link Validation Implementation

TDD GREEN Phase: Minimal implementation to make tests pass
Following SOLID principles: Single responsibility, dependency inversion
Following KISS principle: Simple, readable, minimal functionality  
Following DRY principle: Reuse patterns and avoid duplication
"""

from pathlib import Path
from typing import List, Dict, Any, Set
import re
from functools import lru_cache

from .base import BaseValidator, ValidationResult


class WikiLinkExtractor:
    """
    Extract wiki-style links from markdown content.
    Single responsibility: Only extracts links, doesn't validate them.
    """
    
    def __init__(self):
        """Initialize with basic wiki-link pattern"""
        # KISS: Simple regex for [[Link]] and [[Target|Alias]] patterns  
        # Handle nested brackets by using non-greedy match until ]]
        self.wiki_link_pattern = re.compile(r'\[\[(.*?)\]\]')
    
    def extract_links(self, content: str) -> List[str]:
        """Extract wiki-links from content - minimal implementation"""
        if not content:
            return []
            
        matches = self.wiki_link_pattern.findall(content)
        links = []
        
        for match in matches:
            # Handle alias format: [[Target|Alias]] -> extract "Target"
            if '|' in match:
                target = match.split('|', 1)[0]
            else:
                target = match
                
            # KISS: Simple cleanup - strip whitespace, ignore empty
            target = target.strip()
            if target:  # Ignore empty links
                links.append(target)
                
        return links


class VaultFileResolver:
    """
    Resolve wiki-link text to actual vault files.
    Single responsibility: Only handles file resolution logic.
    """
    
    def __init__(self, vault_path: Path):
        """Initialize with vault path and search configuration"""
        self.vault_path = Path(vault_path)
        
        # KISS: Hard-coded search paths and extensions for minimal implementation
        self.search_paths = [
            "permanent/notes",
            "02-projects", 
            "03-areas",
            "04-resources"
        ]
        self.file_extensions = [".md", ".txt", ".org"]
    
    def resolve_link(self, link_text: str) -> List[Path]:
        """Resolve link text to file paths - minimal implementation"""
        if not link_text:
            return []
            
        # KISS: Simple normalization - lowercase, replace spaces with dashes
        normalized = link_text.lower().replace(' ', '-')
        matches = []
        
        # Search through all configured paths
        for search_path in self.search_paths:
            search_dir = self.vault_path / search_path
            if not search_dir.exists():
                continue
                
            # Try each file extension in priority order
            for ext in self.file_extensions:
                candidate = search_dir / f"{normalized}{ext}"
                if candidate.exists():
                    matches.append(candidate)
                    break  # KISS: First match wins per directory
                    
        return matches


class WikiLinkValidationRules:
    """
    Centralized validation rules and error messages.
    Following DRY principle: Single source of truth for rules.
    """
    
    def __init__(self):
        """Initialize validation rules and error templates"""
        # Search paths for documentation
        self.SEARCH_PATHS = [
            "permanent/notes",
            "02-projects", 
            "03-areas",
            "04-resources"
        ]
        
        # File extension priority order
        self.FILE_EXTENSIONS = [".md", ".txt", ".org"]
        
        # Error message templates
        self.ERROR_MESSAGES = {
            'broken_wiki_link': "Wiki-link '{link_text}' not found in vault. Check spelling or create the referenced note.",
            'ambiguous_wiki_link': "Wiki-link '{link_text}' matches multiple files: {matches}. Use more specific link text.",
            'empty_wiki_link': "Empty wiki-link found. Remove empty [[]] or add link text.",
        }
    
    def format_error_message(self, error_type: str, **kwargs) -> str:
        """Format error message with contextual information"""
        template = self.ERROR_MESSAGES.get(error_type, "Unknown wiki-link validation error")
        
        try:
            return template.format(**kwargs)
        except KeyError:
            return template


class WikiLinkValidator(BaseValidator):
    """
    Validates wiki-links in PKM markdown files.
    Integrates WikiLinkExtractor and VaultFileResolver.
    Following SOLID: Single responsibility, dependency injection.
    """
    
    def __init__(self, vault_path: Path):
        """Initialize with vault path and components"""
        self.vault_path = Path(vault_path)
        
        # Dependency injection: Components can be replaced for testing
        self.extractor = WikiLinkExtractor()
        self.resolver = VaultFileResolver(vault_path)
        self.rules = WikiLinkValidationRules()
    
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """Validate wiki-links in markdown file - minimal implementation"""
        results = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Extract all wiki-links from content
            links = self.extractor.extract_links(content)
            
            # KISS: Performance optimization - check unique links only
            unique_links = list(set(links))
            
            for link in unique_links:
                # Handle empty links specially
                if not link or link.isspace():
                    results.append(ValidationResult(
                        file_path=file_path,
                        rule="empty-wiki-link",
                        severity="error",
                        message=self.rules.format_error_message('empty_wiki_link')
                    ))
                    continue
                
                # Resolve link to actual files
                resolved_files = self.resolver.resolve_link(link)
                
                if len(resolved_files) == 0:
                    # Broken link - no matches found
                    results.append(ValidationResult(
                        file_path=file_path,
                        rule="broken-wiki-link", 
                        severity="error",
                        message=self.rules.format_error_message('broken_wiki_link', link_text=link)
                    ))
                elif len(resolved_files) > 1:
                    # Ambiguous link - multiple matches
                    match_paths = [str(f) for f in resolved_files]
                    results.append(ValidationResult(
                        file_path=file_path,
                        rule="ambiguous-wiki-link",
                        severity="warning",
                        message=self.rules.format_error_message('ambiguous_wiki_link', 
                                                               link_text=link,
                                                               matches=", ".join(match_paths))
                    ))
                # Single match = valid link, no error needed
                
        except FileNotFoundError:
            results.append(ValidationResult(
                file_path=file_path,
                rule="file-not-found",
                severity="error", 
                message=f"File not found: {file_path}"
            ))
        except Exception as e:
            results.append(ValidationResult(
                file_path=file_path,
                rule="validation-error",
                severity="error",
                message=f"Wiki-link validation error: {e}"
            ))
            
        return results