"""
PKM Base Processor Module
DRY implementation - Common functionality extracted from all PKM processors
Following SOLID principles with shared utilities and patterns
"""

import os
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from ..exceptions import ProcessingError


class BasePkmProcessor:
    """
    Base class for all PKM processors implementing common patterns (DRY)
    
    Provides shared functionality:
    - Frontmatter operations (create, extract, combine)
    - File operations (write with UTF-8 encoding)
    - Directory management
    - Validation patterns
    - YAML operations with consistent settings
    """
    
    def __init__(self, vault_path: str):
        """Initialize base processor with vault path"""
        self.vault_path = Path(vault_path)
        
    # Common Validation Patterns (DRY)
    
    def _validate_non_empty_string(self, value: Any, field_name: str) -> None:
        """Validate that a value is a non-empty string (DRY pattern)"""
        if not value or not isinstance(value, str) or not value.strip():
            raise ProcessingError(f"{field_name} cannot be empty")
    
    # Common Directory Operations (DRY)
    
    def _ensure_directory_exists(self, directory_path: Path) -> None:
        """Ensure directory exists, creating if necessary (DRY pattern)"""
        directory_path.mkdir(parents=True, exist_ok=True)
    
    # Common File Operations (DRY)
    
    def _write_markdown_file(self, file_path: Path, content: str) -> None:
        """Write content to markdown file with UTF-8 encoding (DRY pattern)"""
        # Ensure parent directory exists
        self._ensure_directory_exists(file_path.parent)
        # Write with consistent encoding
        file_path.write_text(content, encoding='utf-8')
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read file content with UTF-8 encoding (DRY pattern)"""
        return file_path.read_text(encoding='utf-8')
    
    # Common Frontmatter Operations (DRY)
    
    def _extract_frontmatter_and_content(self, content: str) -> tuple[Dict[str, Any], str]:
        """Extract frontmatter and body content from markdown (DRY pattern)"""
        if not content.startswith('---'):
            return {}, content
        
        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}, content
            
            yaml_content = parts[1].strip()
            body_content = parts[2]
            
            if not yaml_content:
                return {}, body_content
                
            frontmatter = yaml.safe_load(yaml_content) or {}
            return frontmatter, body_content
            
        except yaml.YAMLError:
            # Return empty frontmatter on YAML errors
            return {}, content
    
    def _create_full_markdown_content(self, frontmatter: Dict[str, Any], body_content: str) -> str:
        """Combine frontmatter and content into full markdown (DRY pattern)"""
        if not frontmatter:
            return body_content
        
        yaml_content = yaml.dump(frontmatter, default_flow_style=False)
        return f"---\n{yaml_content}---\n\n{body_content}"
    
    def _update_file_frontmatter(self, file_path: Path, frontmatter_updates: Dict[str, Any]) -> None:
        """Update frontmatter in existing file (DRY pattern)"""
        content = self._read_file_content(file_path)
        existing_frontmatter, body_content = self._extract_frontmatter_and_content(content)
        
        # Merge updates into existing frontmatter
        existing_frontmatter.update(frontmatter_updates)
        
        # Write updated content
        updated_content = self._create_full_markdown_content(existing_frontmatter, body_content)
        self._write_markdown_file(file_path, updated_content)
    
    # Common YAML Operations (DRY)
    
    def _load_yaml_file(self, file_path: Path, default: Any = None) -> Any:
        """Load YAML file with consistent error handling (DRY pattern)"""
        if not file_path.exists():
            return default or {}
        
        try:
            content = self._read_file_content(file_path)
            return yaml.safe_load(content) or (default or {})
        except yaml.YAMLError:
            return default or {}
    
    def _save_yaml_file(self, file_path: Path, data: Any) -> None:
        """Save data to YAML file with consistent formatting (DRY pattern)"""
        yaml_content = yaml.dump(data, default_flow_style=False)
        self._write_markdown_file(file_path, yaml_content)
    
    # Common Timestamp Operations (DRY)
    
    def _create_iso_timestamp(self) -> str:
        """Create ISO format timestamp (DRY pattern)"""
        return datetime.now().isoformat()
    
    def _create_date_string(self) -> str:
        """Create date string in YYYY-MM-DD format (DRY pattern)"""
        return datetime.now().strftime('%Y-%m-%d')
    
    # Common Metadata Operations (DRY)
    
    def _add_processing_metadata(self, frontmatter: Dict[str, Any], processor_name: str) -> None:
        """Add common processing metadata to frontmatter (DRY pattern)"""
        frontmatter['processed_date'] = self._create_date_string()
        frontmatter['processed_by'] = processor_name
        frontmatter['processed_timestamp'] = self._create_iso_timestamp()