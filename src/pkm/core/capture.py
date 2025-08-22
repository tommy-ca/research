"""
PKM Capture Core Module
Implements quick note capture functionality with TDD approach
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..exceptions import CaptureError


@dataclass
class CaptureResult:
    """Result object for capture operations"""
    success: bool
    file_path: str
    frontmatter: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[str] = None


class PkmCapture:
    """PKM note capture service"""
    
    def __init__(self, vault_path: str):
        """Initialize capture service with vault path"""
        self.vault_path = Path(vault_path)
        self.inbox_path = self.vault_path / "00-inbox"
        
    def capture(self, content: str, source: str = None, tags: List[str] = None) -> CaptureResult:
        """
        Capture content to PKM inbox with metadata
        
        Args:
            content: Text content to capture
            source: Source of the content (optional)
            tags: List of tags for the content (optional)
            
        Returns:
            CaptureResult with capture details
        """
        # Validate input
        if not content or not content.strip():
            raise CaptureError("Content cannot be empty")
        
        # Ensure inbox directory exists
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp and filename with guaranteed uniqueness
        import time
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y%m%d")
        time_str = timestamp.strftime("%H%M%S")
        timestamp_str = f"{date_str}{time_str}"
        filename = self._generate_filename(content)
        
        # Ensure uniqueness by checking for existing files and adding counter
        base_filename = f"{date_str}-{time_str}-{filename}"
        file_path = self.inbox_path / base_filename
        counter = 1
        while file_path.exists():
            # Add microsecond precision for uniqueness
            microseconds = timestamp.strftime("%f")[:3]  # First 3 digits of microseconds
            unique_filename = f"{date_str}-{time_str}{microseconds}-{filename}"
            file_path = self.inbox_path / unique_filename
            if not file_path.exists():
                break
            # If still conflicts, add counter
            stem = Path(unique_filename).stem
            suffix = Path(unique_filename).suffix
            unique_filename = f"{stem}-{counter}{suffix}"
            file_path = self.inbox_path / unique_filename
            counter += 1
        
        # Create frontmatter
        frontmatter = self._create_frontmatter(source, tags or [], timestamp)
        
        # Generate full content with frontmatter
        yaml_header = yaml.dump(frontmatter, default_flow_style=False)
        full_content = f"---\n{yaml_header}---\n\n{content}"
        
        # Write file
        file_path.write_text(full_content, encoding='utf-8')
        
        # Create metadata
        metadata = {
            'type': 'capture',
            'status': 'inbox',
            'timestamp': timestamp_str,
            'filename': file_path.name
        }
        
        # Return result with relative path for first test compatibility
        relative_path = f"00-inbox/{file_path.name}"
        return CaptureResult(
            success=True,
            file_path=relative_path,
            frontmatter=frontmatter,
            metadata=metadata
        )
    
    def _generate_filename(self, content: str) -> str:
        """Generate sanitized filename from content"""
        # Get first line or first 50 characters
        first_line = content.split('\n')[0].strip()
        title = first_line[:50] if len(first_line) > 50 else first_line
        
        # Remove markdown headers
        title = re.sub(r'^#+\s*', '', title)
        
        # Convert to lowercase and replace spaces/special chars
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        
        # Truncate to reasonable length for filename (37 chars max before .md)
        if len(slug) > 37:
            slug = slug[:37].rstrip('-')
        
        # Ensure minimum length
        if not slug or len(slug) < 3:
            slug = "captured-note"
        
        return f"{slug}.md"
    
    def _create_frontmatter(self, source: str, tags: List[str], timestamp: datetime) -> Dict[str, Any]:
        """Generate YAML frontmatter for captured content"""
        frontmatter = {
            'date': timestamp.strftime("%Y-%m-%d"),
            'type': 'capture',
            'status': 'inbox',
            'created': timestamp.isoformat(),
            'id': timestamp.strftime("%Y%m%d%H%M%S")
        }
        
        if source:
            frontmatter['source'] = source
            
        if tags:
            frontmatter['tags'] = tags
        else:
            frontmatter['tags'] = []
            
        return frontmatter