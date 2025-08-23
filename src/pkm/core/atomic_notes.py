"""
PKM Atomic Note Creation Core Module
TDD Cycle 3 - Implements Zettelkasten atomic notes with linking system
Following KISS, DRY, SOLID principles integrated with existing PKM patterns
"""

import os
import re
import json
import yaml
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from ..exceptions import ProcessingError
from .base import BasePkmProcessor


@dataclass
class AtomicNoteResult:
    """Result object for atomic note creation operations"""
    success: bool = False
    note_id: str = ""
    file_path: str = ""
    links: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_orphan: bool = False
    promoted_from: Optional[str] = None
    error: Optional[str] = None


class PkmAtomicNote(BasePkmProcessor):
    """PKM atomic note creation service with Zettelkasten linking"""
    
    def __init__(self, vault_path: str):
        """Initialize atomic note service with vault path"""
        super().__init__(vault_path)  # DRY: Use base class initialization
        self.notes_path = self.vault_path / "permanent" / "notes"
        self._lock = threading.Lock()  # For concurrent note creation
        
        # Create directory structure if needed
        self._ensure_directory_exists(self.notes_path)  # DRY: Use base class method
    
    def create_note(self, title: str, content: str) -> AtomicNoteResult:
        """
        Create atomic note with unique ID and linking system
        
        Args:
            title: Title of the atomic note
            content: Content of the note
            
        Returns:
            AtomicNoteResult with creation details
            
        Raises:
            ProcessingError: If input validation fails
        """
        with self._lock:  # Thread safety for concurrent creation
            # Input validation (DRY: Use base class validation)
            self._validate_non_empty_string(title, "Title")
            self._validate_non_empty_string(content, "Content")
            
            # Generate unique note ID (KISS: simple timestamp)
            note_id = self._generate_note_id()
            
            # Create filename (DRY pattern from capture)
            filename = self._generate_filename(note_id, title)
            file_path = self.notes_path / filename
            
            # Extract links (KISS: simple regex)
            links = self._extract_links(content)
            
            # Generate metadata (KISS: basic analysis)
            metadata = self._extract_metadata(content)
            
            # Generate tags (KISS: basic keyword extraction)
            tags = self._generate_tags(content)
            
            # Create frontmatter (DRY pattern from previous modules)
            frontmatter = self._create_frontmatter(title, note_id, links, tags)
            
            # Write file (DRY: Use base class method)
            full_content = self._create_full_markdown_content(frontmatter, content)
            self._write_markdown_file(file_path, full_content)
            
            # Update indexes (KISS: simple JSON files)
            self._update_link_index(note_id, title, links)
            self._update_search_index(note_id, title, content, tags)
            self._update_backlinks(note_id, links)
            
            # Retroactively update link index for existing notes that might link to this new note
            self._update_existing_links_to_new_note(note_id, title)
            
            return AtomicNoteResult(
                success=True,
                note_id=note_id,
                file_path=str(file_path),
                links=links,
                tags=tags,
                metadata=metadata,
                is_orphan=(len(links) == 0)
            )
    
    def promote_from_capture(self, captured_content: str) -> AtomicNoteResult:
        """
        Promote captured content to atomic note
        
        Args:
            captured_content: Original captured content with frontmatter
            
        Returns:
            AtomicNoteResult with promotion details
        """
        # Extract original frontmatter and content
        parts = captured_content.split('---', 2)
        if len(parts) >= 3:
            original_frontmatter = yaml.safe_load(parts[1])
            content = parts[2].strip()
            title = self._extract_title_from_content(content)
        else:
            original_frontmatter = {}
            content = captured_content
            title = "Promoted Note"
        
        # Create atomic note
        result = self.create_note(title, content)
        
        # Add promotion metadata
        result.promoted_from = "capture"
        
        # Update file with original capture date
        if result.success and 'date' in original_frontmatter:
            self._add_original_capture_date(result.note_id, original_frontmatter['date'])
        
        return result
    
    # Helper Methods (KISS implementations, DRY base class used where applicable)
    
    def _generate_note_id(self) -> str:
        """Generate unique note ID with nanosecond precision for concurrency"""
        import time
        # Use nanosecond timestamp for maximum uniqueness
        nano_time = time.time_ns()
        # Take last 14 digits to get a reasonable length ID
        unique_id = str(nano_time)[-14:]
        return unique_id
    
    def _generate_filename(self, note_id: str, title: str) -> str:
        """Generate filename from note ID and title (DRY from capture)"""
        # Sanitize title for filename (reuse capture pattern)
        sanitized_title = self._sanitize_title(title)
        return f"{note_id}-{sanitized_title}.md"
    
    def _sanitize_title(self, title: str) -> str:
        """Sanitize title for filename (DRY from capture module)"""
        import unicodedata
        # Normalize Unicode characters (café → cafe)
        normalized = unicodedata.normalize('NFKD', title)
        ascii_title = normalized.encode('ascii', 'ignore').decode('ascii')
        
        # Convert to lowercase and replace spaces/special chars
        sanitized = re.sub(r'[^\w\s-]', '', ascii_title.lower())
        sanitized = re.sub(r'[-\s]+', '-', sanitized)
        # Truncate for long titles
        if len(sanitized) > 50:
            sanitized = sanitized[:50].rstrip('-')
        return sanitized or 'untitled'  # Fallback for edge cases
    
    def _extract_links(self, content: str) -> List[str]:
        """Extract WikiLinks from content (KISS: simple regex)"""
        # Find all [[Link]] patterns
        link_pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(link_pattern, content)
        return list(set(matches))  # Remove duplicates
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract basic metadata from content (KISS implementation)"""
        lines = content.split('\n')
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        return {
            'word_count': len(content.split()),
            'paragraph_count': len(paragraphs),
            'has_headings': any(line.strip().startswith('#') for line in lines),
            'has_lists': any(line.strip().startswith(('-', '*', '+')) for line in lines)
        }
    
    def _generate_tags(self, content: str) -> List[str]:
        """Generate tags from content (KISS: keyword extraction)"""
        # Simple keyword-based tag generation
        content_lower = content.lower()
        tags = []
        
        # AI/ML related keywords (expanded for test coverage)
        if any(word in content_lower for word in ['machine learning', 'artificial intelligence']):
            tags.append('#ai/machine-learning')
        if any(word in content_lower for word in ['neural network', 'neural networks']):
            tags.append('#ai/neural-networks')
        if any(word in content_lower for word in ['deep learning']):
            tags.append('#ai/deep-learning')
        if any(word in content_lower for word in ['natural language', 'nlp']):
            tags.append('#ai/nlp')
        
        # Programming keywords
        if any(word in content_lower for word in ['python', 'programming', 'code']):
            tags.append('#programming/python')
        
        # General categories
        if any(word in content_lower for word in ['research', 'study', 'analysis']):
            tags.append('#research')
        
        return tags
    
    def _create_frontmatter(self, title: str, note_id: str, links: List[str], tags: List[str]) -> Dict[str, Any]:
        """Create frontmatter for atomic note (DRY pattern)"""
        return {
            'type': 'atomic',
            'title': title,
            'id': note_id,
            'created': datetime.now().isoformat(),
            'links': links,
            'tags': tags,
            'backlinks': []
        }
    
    
    def _update_link_index(self, note_id: str, title: str, links: List[str]) -> None:
        """Update central link index (KISS: JSON file)"""
        index_path = self.vault_path / "permanent" / ".link_index.yml"
        
        # Load existing index (DRY: Use base class method)
        link_index = self._load_yaml_file(index_path, {})
        
        # Resolve link titles to note IDs for proper indexing
        linked_note_ids = []
        for link_title in links:
            linked_note_id = self._find_note_id_by_title(link_title)
            if linked_note_id:
                linked_note_ids.append(linked_note_id)
        
        # Add this note with resolved note IDs
        link_index[note_id] = {
            'title': title,
            'links': linked_note_ids,  # Store note IDs instead of titles
            'created': self._create_iso_timestamp()  # DRY: Use base class method
        }
        
        # Save index (DRY: Use base class method)
        self._save_yaml_file(index_path, link_index)
    
    def _update_search_index(self, note_id: str, title: str, content: str, tags: List[str]) -> None:
        """Update search index (KISS: JSON file)"""
        index_path = self.vault_path / "permanent" / ".search_index.json"
        
        # Load existing index
        if index_path.exists():
            search_index = json.loads(index_path.read_text())
        else:
            search_index = {}
        
        # Extract keywords
        words = re.findall(r'\b\w+\b', content.lower())
        keywords = [word for word in set(words) if len(word) > 3]
        
        # Add this note
        search_index[note_id] = {
            'title': title,
            'keywords': keywords,
            'tags': tags,
            'created': datetime.now().isoformat()
        }
        
        # Save index
        index_path.write_text(json.dumps(search_index, indent=2))
    
    def _update_backlinks(self, note_id: str, links: List[str]) -> None:
        """Update backlinks in linked notes (KISS implementation)"""
        for link_title in links:
            # Find note file by title
            link_file = self._find_note_by_title(link_title)
            if link_file:
                self._add_backlink_to_file(link_file, note_id)
    
    def _find_note_by_title(self, title: str) -> Optional[Path]:
        """Find note file by title (KISS: filename search)"""
        sanitized_title = self._sanitize_title(title)
        pattern = f"*{sanitized_title}.md"
        matches = list(self.notes_path.glob(pattern))
        return matches[0] if matches else None
    
    def _find_note_id_by_title(self, title: str) -> Optional[str]:
        """Find note ID by title (for link index resolution)"""
        note_file = self._find_note_by_title(title)
        if note_file:
            # Extract note ID from filename (YYYYMMDDHHMMSS-title.md)
            filename = note_file.stem
            note_id = filename.split('-')[0]
            return note_id
        return None
    
    def _add_backlink_to_file(self, file_path: Path, linking_note_id: str) -> None:
        """Add backlink to note file frontmatter"""
        content = file_path.read_text(encoding='utf-8')
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            frontmatter = yaml.safe_load(parts[1]) or {}
            body = parts[2]
            
            # Add backlink
            if 'backlinks' not in frontmatter:
                frontmatter['backlinks'] = []
            if linking_note_id not in frontmatter['backlinks']:
                frontmatter['backlinks'].append(linking_note_id)
            
            # Rewrite file
            yaml_content = yaml.dump(frontmatter, default_flow_style=False)
            new_content = f"---\n{yaml_content}---{body}"
            file_path.write_text(new_content, encoding='utf-8')
    
    def _extract_title_from_content(self, content: str) -> str:
        """Extract title from content (KISS: first heading or first line)"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Look for first heading
        for line in lines:
            if line.startswith('#'):
                return line.lstrip('#').strip()
        
        # Use first line
        if lines:
            title = lines[0][:50]  # Truncate long titles
            return title
        
        return "Untitled Note"
    
    def _add_original_capture_date(self, note_id: str, original_date: Any) -> None:
        """Add original capture date to note frontmatter"""
        note_file = None
        for file_path in self.notes_path.glob(f"{note_id}*.md"):  # Fixed pattern
            note_file = file_path
            break
        
        if note_file:
            content = note_file.read_text(encoding='utf-8')
            parts = content.split('---', 2)
            frontmatter = yaml.safe_load(parts[1])
            # Convert to string if it's a date object
            if hasattr(original_date, 'strftime'):
                frontmatter['original_capture_date'] = original_date.strftime('%Y-%m-%d')
            else:
                frontmatter['original_capture_date'] = str(original_date)
            
            yaml_content = yaml.dump(frontmatter, default_flow_style=False)
            new_content = f"---\n{yaml_content}---{parts[2]}"
            note_file.write_text(new_content, encoding='utf-8')
    
    def _update_existing_links_to_new_note(self, new_note_id: str, new_title: str) -> None:
        """Update link index for existing notes that link to this newly created note"""
        index_path = self.vault_path / "permanent" / ".link_index.yml"
        
        if not index_path.exists():
            return
            
        link_index = yaml.safe_load(index_path.read_text()) or {}
        
        # Check all existing notes for links to this new note title
        for existing_note_id, note_data in link_index.items():
            if existing_note_id == new_note_id:
                continue
                
            # Find the actual note file to check its content for links
            existing_note_file = None
            for file_path in self.notes_path.glob(f"{existing_note_id}*.md"):
                existing_note_file = file_path
                break
                
            if existing_note_file:
                content = existing_note_file.read_text(encoding='utf-8')
                links_in_content = self._extract_links(content)
                
                # If this existing note links to the new note title
                if new_title in links_in_content:
                    # Update the link index to include the new note ID
                    if new_note_id not in note_data['links']:
                        note_data['links'].append(new_note_id)
        
        # Save updated index
        index_path.write_text(yaml.dump(link_index, default_flow_style=False))