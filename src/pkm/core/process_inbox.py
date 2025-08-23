"""
PKM Inbox Processing Core Module
Implements automated inbox processing with PARA categorization using TDD approach
"""

import os
import re
import yaml
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..exceptions import ProcessingError


@dataclass
class ProcessResult:
    """Result object for inbox processing operations"""
    success: bool = True
    files_found: int = 0
    files_processed: int = 0
    categorized: Dict[str, str] = field(default_factory=dict)  # filename -> category
    errors: Dict[str, str] = field(default_factory=dict)  # filename -> error message
    report: str = ""


class PkmInboxProcessor:
    """PKM inbox processing service with PARA categorization"""

    # Default PARA type mappings
    PARA_TYPE_MAPPING = {
        'project': '02-projects',
        'area': '03-areas',
        'resource': '04-resources',
        'archive': '05-archives',
    }

    # PARA categorization keywords (ordered by specificity)
    PARA_KEYWORDS = {
        '05-archives': ['archived', 'archive', 'completed', 'historical', 'old', 'inactive', 'deprecated'],
        '02-projects': ['deadline', 'project', 'goal', 'deliverable', 'launch'],
        '03-areas': ['area', 'ongoing', 'maintain', 'responsibility', 'routine', 'habit'],
        '04-resources': ['reference', 'resource', 'learn', 'information', 'documentation', 'tutorial'],
    }

    DEFAULT_CATEGORY = '04-resources'

    def __init__(self, vault_path: str, para_mapping: Dict[str, str] | None = None):
        """Initialize inbox processor with vault path"""
        self.vault_path = Path(vault_path)
        self.inbox_path = self.vault_path / "00-inbox"

        # Allow overriding PARA mapping (e.g., to 02/03/04/05 scheme)
        self.para_type_mapping = para_mapping or self.PARA_TYPE_MAPPING

        # PARA directories
        self.para_dirs = {
            category: self.vault_path / category
            for category in self.para_type_mapping.values()
        }
    
    def process_inbox(self) -> ProcessResult:
        """
        Process all items in inbox with PARA categorization
        
        Returns:
            ProcessResult with processing details and summary
        """
        result = ProcessResult()
        
        # FR-001: Read inbox items
        if not self.inbox_path.exists():
            result.report = "Inbox directory does not exist"
            return result
            
        md_files = list(self.inbox_path.glob("*.md"))
        result.files_found = len(md_files)
        
        if result.files_found == 0:
            result.report = "Inbox is empty"
            return result
        
        # Process each file
        for md_file in md_files:
            try:
                self._process_single_file(md_file, result)
            except Exception as e:
                result.errors[md_file.name] = str(e)
                continue
        
        # FR-006: Generate report
        result.report = self._generate_report(result)
        
        return result
    
    def _process_single_file(self, file_path: Path, result: ProcessResult) -> None:
        """Process a single file through the PARA workflow"""
        try:
            # FR-002: Extract metadata
            content = file_path.read_text(encoding='utf-8')
            frontmatter = self._extract_frontmatter(content)
            
            # FR-003: Categorize by PARA
            category = self._categorize_content(content, frontmatter)
            
            # FR-004: Move to target folder
            target_path = self._move_file(file_path, category)
            
            # FR-005: Update frontmatter
            self._update_frontmatter(target_path, category)
            
            # Record success
            result.categorized[file_path.name] = category
            result.files_processed += 1
            
        except yaml.YAMLError:
            result.errors[file_path.name] = "Invalid frontmatter"
        except Exception as e:
            result.errors[file_path.name] = str(e)
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter from markdown content"""
        if not self._has_frontmatter(content):
            return {}
        
        try:
            yaml_content = self._extract_yaml_content(content)
            if not yaml_content:
                return {}
                
            return yaml.safe_load(yaml_content) or {}
            
        except yaml.YAMLError:
            raise yaml.YAMLError("Invalid frontmatter YAML")
    
    def _has_frontmatter(self, content: str) -> bool:
        """Check if content has YAML frontmatter"""
        return content.startswith('---')
    
    def _extract_yaml_content(self, content: str) -> str:
        """Extract YAML content from frontmatter"""
        parts = content.split('---', 2)
        if len(parts) < 3:
            return ""
        return parts[1].strip()
    
    def _categorize_content(self, content: str, frontmatter: Dict[str, Any]) -> str:
        """Categorize content according to PARA method"""
        # Priority 1: Explicit type in frontmatter
        frontmatter_type = frontmatter.get('type')
        if frontmatter_type in self.para_type_mapping:
            return self.para_type_mapping[frontmatter_type]
        
        # Priority 2: Content-based keyword analysis
        return self._categorize_by_keywords(content)
    
    def _categorize_by_keywords(self, content: str) -> str:
        """Categorize content based on keyword analysis"""
        content_lower = content.lower()
        
        # Check keywords in order of specificity (archives first, then projects, areas, resources)
        for category, keywords in self.PARA_KEYWORDS.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        # Default fallback for ambiguous content
        return self.DEFAULT_CATEGORY
    
    def _move_file(self, source_path: Path, target_category: str) -> Path:
        """Move file to target PARA directory"""
        target_dir = self.para_dirs[target_category]
        
        # Create target directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_path = target_dir / source_path.name
        
        # Handle file conflicts by adding number suffix
        if target_path.exists():
            counter = 1
            stem = source_path.stem
            suffix = source_path.suffix
            while target_path.exists():
                new_name = f"{stem}-{counter}{suffix}"
                target_path = target_dir / new_name
                counter += 1
        
        # Move the file
        shutil.move(str(source_path), str(target_path))
        return target_path
    
    def _update_frontmatter(self, file_path: Path, category: str) -> None:
        """Add processing metadata to frontmatter"""
        content = file_path.read_text(encoding='utf-8')
        
        # Extract existing frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                existing_yaml = parts[1].strip()
                body_content = parts[2]
                
                # Parse existing frontmatter
                try:
                    frontmatter = yaml.safe_load(existing_yaml) or {}
                except yaml.YAMLError:
                    frontmatter = {}
            else:
                frontmatter = {}
                body_content = content
        else:
            frontmatter = {}
            body_content = content
        
        # Add processing metadata
        frontmatter['processed_date'] = datetime.now().strftime('%Y-%m-%d')
        frontmatter['processed_by'] = 'pkm-inbox-processor'
        frontmatter['category'] = category
        
        # Reconstruct file with updated frontmatter
        yaml_content = yaml.dump(frontmatter, default_flow_style=False)
        new_content = f"---\n{yaml_content}---{body_content}"
        
        file_path.write_text(new_content, encoding='utf-8')
    
    def _generate_report(self, result: ProcessResult) -> str:
        """Generate human-readable processing report"""
        lines = []
        
        if result.files_found == 0:
            return "Inbox is empty"
        
        # Summary
        files_word = "file" if result.files_processed == 1 else "files"
        lines.append(f"{result.files_processed} {files_word} processed successfully")
        if result.errors:
            error_count = len(result.errors)
            error_word = "error" if error_count == 1 else "errors"
            lines.append(f"{error_count} {error_word} encountered")
        
        # Categorization breakdown
        category_counts = {}
        for category in result.categorized.values():
            category_counts[category] = category_counts.get(category, 0) + 1
        
        if category_counts:
            lines.append("\nCategorization breakdown:")
            for category, count in sorted(category_counts.items()):
                lines.append(f"  {category}: {count}")
        
        # Error details
        if result.errors:
            lines.append("\nErrors:")
            for filename, error in result.errors.items():
                lines.append(f"  {filename}: {error}")
        
        return "\n".join(lines)