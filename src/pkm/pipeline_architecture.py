#!/usr/bin/env python3
"""
PKM Processing Pipeline Architecture

Implements the complete PKM ingestion and processing pipeline following
TDD principles and specs-driven development from CLAUDE.md.

Architecture Components:
1. Inbox Processor - Reads and validates inbox items
2. Content Parser - Extracts structured data from markdown
3. Concept Extractor - Identifies key concepts using NLP
4. Atomic Note Generator - Creates permanent atomic notes
5. Link Discovery Engine - Finds bidirectional relationships
6. PARA Categorizer - Classifies content by PARA method
7. Tag Generator - Creates hierarchical tag systems
8. Knowledge Graph Indexer - Updates searchable indexes
"""

import os
import re
import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class PkmItem:
    """Represents a PKM item with metadata and content"""
    file_path: Path
    title: str
    content: str
    frontmatter: Dict
    created_date: datetime
    tags: Set[str] = field(default_factory=set)
    links: Set[str] = field(default_factory=set)
    concepts: List[str] = field(default_factory=list)
    para_category: Optional[str] = None
    
@dataclass
class AtomicNote:
    """Represents an atomic note in the permanent collection"""
    id: str
    title: str
    content: str
    tags: Set[str]
    links: Set[str]
    source_files: List[str]
    created_date: datetime
    updated_date: datetime

class PkmProcessor(ABC):
    """Abstract base class for PKM processing components"""
    
    @abstractmethod
    def process(self, item: PkmItem) -> PkmItem:
        """Process a PKM item and return the enhanced version"""
        pass

class InboxProcessor(PkmProcessor):
    """Processes items from the inbox directory"""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.inbox_path = vault_path / "00-inbox"
        
    def get_inbox_items(self) -> List[PkmItem]:
        """Retrieve all items from inbox for processing"""
        items = []
        
        for md_file in self.inbox_path.glob("*.md"):
            if md_file.name.startswith('.'):
                continue
                
            try:
                item = self._parse_markdown_file(md_file)
                items.append(item)
            except Exception as e:
                print(f"Error processing {md_file}: {e}")
                continue
                
        return items
    
    def _parse_markdown_file(self, file_path: Path) -> PkmItem:
        """Parse a markdown file into a PKM item"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_raw = parts[1]
                content_body = parts[2].strip()
            else:
                frontmatter_raw = ""
                content_body = content
        else:
            frontmatter_raw = ""
            content_body = content
            
        # Parse frontmatter
        try:
            frontmatter = yaml.safe_load(frontmatter_raw) if frontmatter_raw else {}
        except yaml.YAMLError:
            frontmatter = {}
            
        # Extract title
        title = frontmatter.get('title', self._extract_title_from_content(content_body))
        if not title:
            title = file_path.stem
            
        # Create PKM item
        return PkmItem(
            file_path=file_path,
            title=title,
            content=content_body,
            frontmatter=frontmatter,
            created_date=datetime.fromisoformat(frontmatter.get('date', datetime.now().isoformat())),
            tags=set(frontmatter.get('tags', [])),
            links=set(self._extract_links(content_body))
        )
    
    def _extract_title_from_content(self, content: str) -> str:
        """Extract title from markdown content"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return ""
    
    def _extract_links(self, content: str) -> List[str]:
        """Extract [[wiki-style]] links from content"""
        pattern = r'\[\[([^\]]+)\]\]'
        return re.findall(pattern, content)
    
    def process(self, item: PkmItem) -> PkmItem:
        """Process inbox item - validation and enhancement"""
        # Validate required fields
        if not item.title:
            raise ValueError(f"Item {item.file_path} missing title")
        
        # Set default PARA category based on tags
        if 'project' in item.tags:
            item.para_category = 'project'
        elif 'area' in item.tags:
            item.para_category = 'area'
        elif 'resource' in item.tags:
            item.para_category = 'resource'
        else:
            item.para_category = 'resource'  # Default
            
        return item

class ConceptExtractor(PkmProcessor):
    """Extracts key concepts from content using rule-based NLP"""
    
    def __init__(self):
        # Common technical terms and domain concepts
        self.crypto_terms = {
            'blockchain', 'bitcoin', 'ethereum', 'defi', 'nft', 'token',
            'smart contract', 'consensus', 'proof of stake', 'proof of work',
            'mining', 'staking', 'yield farming', 'liquidity pool', 'dex', 'cex',
            'lakehouse', 'data warehouse', 'etl', 'streaming', 'batch processing',
            'kafka', 'spark', 'parquet', 'iceberg', 'delta lake'
        }
        
        self.technical_patterns = [
            r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w+(?:-\w+)+\b',  # Hyphenated terms
        ]
    
    def process(self, item: PkmItem) -> PkmItem:
        """Extract concepts from the item content"""
        concepts = set()
        
        # Extract domain-specific terms
        content_lower = item.content.lower()
        for term in self.crypto_terms:
            if term in content_lower:
                concepts.add(term)
        
        # Extract technical patterns
        for pattern in self.technical_patterns:
            matches = re.findall(pattern, item.content)
            concepts.update(matches)
        
        # Extract from headers
        headers = re.findall(r'^#+\s*(.+)$', item.content, re.MULTILINE)
        for header in headers:
            # Clean and add significant headers
            clean_header = re.sub(r'[^\w\s]', '', header).strip()
            if len(clean_header.split()) <= 4:  # Short phrases only
                concepts.add(clean_header.lower())
        
        item.concepts = list(concepts)
        return item

class AtomicNoteGenerator(PkmProcessor):
    """Generates atomic notes from processed content"""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.permanent_path = vault_path / "permanent" / "notes"
        self.permanent_path.mkdir(parents=True, exist_ok=True)
        
    def process(self, item: PkmItem) -> PkmItem:
        """Generate atomic notes from the item's concepts"""
        atomic_notes = []
        
        # Create atomic notes for major concepts
        for concept in item.concepts[:10]:  # Limit to top 10 concepts
            if len(concept) < 3:  # Skip very short concepts
                continue
                
            atomic_note = self._create_atomic_note(concept, item)
            if atomic_note:
                atomic_notes.append(atomic_note)
        
        # Store references to created atomic notes
        item.frontmatter['atomic_notes'] = [note.id for note in atomic_notes]
        
        return item
    
    def _create_atomic_note(self, concept: str, source_item: PkmItem) -> Optional[AtomicNote]:
        """Create an atomic note for a specific concept"""
        # Generate unique ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        concept_slug = re.sub(r'[^\w\-]', '', concept.replace(' ', '-')).lower()
        note_id = f"{timestamp}-{concept_slug}"
        
        # Check if note already exists
        note_path = self.permanent_path / f"{note_id}.md"
        if note_path.exists():
            return None
        
        # Extract relevant content about this concept
        content_sections = self._extract_concept_content(concept, source_item.content)
        
        if not content_sections:
            return None
            
        # Create atomic note content
        note_content = f"""# {concept.title()}

{content_sections}

## Related Concepts

*Add related concept links here*

## Sources

- [[{source_item.file_path.stem}]]

---
*Concept extracted: {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        # Create frontmatter
        frontmatter = {
            'date': datetime.now().isoformat(),
            'type': 'zettel',
            'tags': list(source_item.tags) + ['concept', concept_slug],
            'status': 'draft',
            'links': [source_item.file_path.stem],
            'concept': concept
        }
        
        # Write atomic note file
        full_content = f"""---
{yaml.dump(frontmatter, default_flow_style=False)}---

{note_content}"""
        
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return AtomicNote(
            id=note_id,
            title=concept.title(),
            content=note_content,
            tags=set(frontmatter['tags']),
            links=set(frontmatter['links']),
            source_files=[str(source_item.file_path)],
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
    
    def _extract_concept_content(self, concept: str, content: str) -> str:
        """Extract content sections relevant to the concept"""
        lines = content.split('\n')
        relevant_lines = []
        
        # Find lines containing the concept
        for i, line in enumerate(lines):
            if concept.lower() in line.lower():
                # Add context around the concept
                start = max(0, i-2)
                end = min(len(lines), i+3)
                context = lines[start:end]
                relevant_lines.extend(context)
                relevant_lines.append('')  # Add separator
        
        # Remove duplicates and empty lines at the end
        unique_lines = []
        for line in relevant_lines:
            if line not in unique_lines:
                unique_lines.append(line)
                
        return '\n'.join(unique_lines).strip()

class LinkDiscoveryEngine(PkmProcessor):
    """Discovers and creates bidirectional links between notes"""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        
    def process(self, item: PkmItem) -> PkmItem:
        """Discover potential links to other notes"""
        # This would implement similarity matching, keyword overlap, etc.
        # For now, we'll implement a basic version
        
        existing_notes = self._get_existing_notes()
        potential_links = self._find_potential_links(item, existing_notes)
        
        item.links.update(potential_links)
        
        return item
    
    def _get_existing_notes(self) -> List[str]:
        """Get list of existing note titles for linking"""
        notes = []
        
        # Scan permanent notes
        permanent_path = self.vault_path / "permanent" / "notes"
        if permanent_path.exists():
            for md_file in permanent_path.glob("*.md"):
                notes.append(md_file.stem)
        
        return notes
    
    def _find_potential_links(self, item: PkmItem, existing_notes: List[str]) -> Set[str]:
        """Find potential links based on content similarity"""
        potential_links = set()
        
        # Simple keyword matching
        for note_name in existing_notes:
            # Extract keywords from note name
            note_keywords = note_name.lower().replace('-', ' ').split()
            
            # Check if any keywords appear in content
            content_lower = item.content.lower()
            for keyword in note_keywords:
                if len(keyword) > 3 and keyword in content_lower:
                    potential_links.add(note_name)
                    break
        
        return potential_links

class ParaCategorizer(PkmProcessor):
    """Categorizes content using the PARA method"""
    
    def __init__(self):
        self.project_indicators = {
            'implement', 'build', 'create', 'develop', 'design', 'plan',
            'roadmap', 'timeline', 'deadline', 'milestone', 'deliverable'
        }
        
        self.area_indicators = {
            'maintain', 'monitor', 'standard', 'process', 'policy',
            'ongoing', 'responsibility', 'governance', 'compliance'
        }
        
        self.resource_indicators = {
            'reference', 'documentation', 'guide', 'tutorial', 'example',
            'template', 'framework', 'library', 'tool', 'research'
        }
    
    def process(self, item: PkmItem) -> PkmItem:
        """Categorize item using PARA method"""
        content_lower = item.content.lower()
        scores = {
            'project': 0,
            'area': 0,
            'resource': 0,
            'archive': 0
        }
        
        # Score based on indicators
        for indicator in self.project_indicators:
            if indicator in content_lower:
                scores['project'] += 1
                
        for indicator in self.area_indicators:
            if indicator in content_lower:
                scores['area'] += 1
                
        for indicator in self.resource_indicators:
            if indicator in content_lower:
                scores['resource'] += 1
        
        # Check if it's archived content (old dates, completed status)
        if item.frontmatter.get('status') == 'completed':
            scores['archive'] += 2
            
        # Determine category
        item.para_category = max(scores.keys(), key=lambda k: scores[k])
        
        # Default to resource if no clear category
        if scores[item.para_category] == 0:
            item.para_category = 'resource'
            
        return item

class TagGenerator(PkmProcessor):
    """Generates hierarchical tags for content"""
    
    def __init__(self):
        self.tag_hierarchy = {
            'crypto': ['bitcoin', 'ethereum', 'defi', 'nft', 'blockchain'],
            'data': ['analytics', 'storage', 'processing', 'pipeline'],
            'architecture': ['lakehouse', 'warehouse', 'streaming', 'batch'],
            'technology': ['kafka', 'spark', 'parquet', 'iceberg', 'delta-lake'],
            'vendor': ['databricks', 'snowflake', 'hyperline', 'trm-labs']
        }
    
    def process(self, item: PkmItem) -> PkmItem:
        """Generate relevant tags for the item"""
        generated_tags = set()
        content_lower = item.content.lower()
        
        # Generate tags from hierarchy
        for parent_tag, child_tags in self.tag_hierarchy.items():
            child_matches = [tag for tag in child_tags if tag in content_lower]
            if child_matches:
                generated_tags.add(parent_tag)
                generated_tags.update(child_matches)
        
        # Add concept-based tags
        for concept in item.concepts:
            concept_tag = concept.lower().replace(' ', '-')
            if len(concept_tag) > 2:
                generated_tags.add(concept_tag)
        
        # Merge with existing tags
        item.tags.update(generated_tags)
        
        return item

class KnowledgeGraphIndexer(PkmProcessor):
    """Updates knowledge graph indexes and search functionality"""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.index_path = vault_path / ".pkm" / "indexes"
        self.index_path.mkdir(parents=True, exist_ok=True)
    
    def process(self, item: PkmItem) -> PkmItem:
        """Update knowledge graph indexes"""
        # Update concept index
        self._update_concept_index(item)
        
        # Update tag index
        self._update_tag_index(item)
        
        # Update link index
        self._update_link_index(item)
        
        return item
    
    def _update_concept_index(self, item: PkmItem):
        """Update the concept-to-notes mapping"""
        concept_index_path = self.index_path / "concepts.json"
        
        # Load existing index
        if concept_index_path.exists():
            with open(concept_index_path, 'r') as f:
                concept_index = json.load(f)
        else:
            concept_index = {}
        
        # Update index with item's concepts
        for concept in item.concepts:
            if concept not in concept_index:
                concept_index[concept] = []
            
            note_ref = str(item.file_path.stem)
            if note_ref not in concept_index[concept]:
                concept_index[concept].append(note_ref)
        
        # Save updated index
        with open(concept_index_path, 'w') as f:
            json.dump(concept_index, f, indent=2)
    
    def _update_tag_index(self, item: PkmItem):
        """Update the tag-to-notes mapping"""
        tag_index_path = self.index_path / "tags.json"
        
        # Load existing index
        if tag_index_path.exists():
            with open(tag_index_path, 'r') as f:
                tag_index = json.load(f)
        else:
            tag_index = {}
        
        # Update index with item's tags
        for tag in item.tags:
            if tag not in tag_index:
                tag_index[tag] = []
            
            note_ref = str(item.file_path.stem)
            if note_ref not in tag_index[tag]:
                tag_index[tag].append(note_ref)
        
        # Save updated index
        with open(tag_index_path, 'w') as f:
            json.dump(tag_index, f, indent=2)
    
    def _update_link_index(self, item: PkmItem):
        """Update bidirectional link index"""
        link_index_path = self.index_path / "links.json"
        
        # Load existing index
        if link_index_path.exists():
            with open(link_index_path, 'r') as f:
                link_index = json.load(f)
        else:
            link_index = {}
        
        note_name = item.file_path.stem
        
        # Update outgoing links
        if note_name not in link_index:
            link_index[note_name] = {'outgoing': [], 'incoming': []}
        
        link_index[note_name]['outgoing'] = list(item.links)
        
        # Update incoming links for linked notes
        for linked_note in item.links:
            if linked_note not in link_index:
                link_index[linked_note] = {'outgoing': [], 'incoming': []}
            
            if note_name not in link_index[linked_note]['incoming']:
                link_index[linked_note]['incoming'].append(note_name)
        
        # Save updated index
        with open(link_index_path, 'w') as f:
            json.dump(link_index, f, indent=2)

class PkmPipeline:
    """Main PKM processing pipeline orchestrator"""
    
    def __init__(self, vault_path: Path):
        self.vault_path = Path(vault_path)
        
        # Initialize processors
        self.inbox_processor = InboxProcessor(self.vault_path)
        self.concept_extractor = ConceptExtractor()
        self.atomic_note_generator = AtomicNoteGenerator(self.vault_path)
        self.link_discovery_engine = LinkDiscoveryEngine(self.vault_path)
        self.para_categorizer = ParaCategorizer()
        self.tag_generator = TagGenerator()
        self.knowledge_graph_indexer = KnowledgeGraphIndexer(self.vault_path)
        
        # Processing pipeline order
        self.processors = [
            self.concept_extractor,
            self.para_categorizer,
            self.tag_generator,
            self.atomic_note_generator,
            self.link_discovery_engine,
            self.knowledge_graph_indexer
        ]
    
    def process_inbox(self) -> List[PkmItem]:
        """Process all items in the inbox"""
        # Get inbox items
        items = self.inbox_processor.get_inbox_items()
        
        print(f"Found {len(items)} items in inbox")
        
        processed_items = []
        for item in items:
            try:
                print(f"Processing: {item.title}")
                
                # Run through processing pipeline
                processed_item = item
                for processor in self.processors:
                    processed_item = processor.process(processed_item)
                
                # Move to appropriate PARA category
                self._categorize_item(processed_item)
                
                processed_items.append(processed_item)
                
                print(f"✓ Processed: {item.title} -> {processed_item.para_category}")
                
            except Exception as e:
                print(f"✗ Error processing {item.title}: {e}")
                continue
        
        return processed_items
    
    def _categorize_item(self, item: PkmItem):
        """Move item to appropriate PARA category folder"""
        # Determine target directory
        category_map = {
            'project': '02-projects',
            'area': '03-areas', 
            'resource': '04-resources',
            'archive': '05-archives'
        }
        
        target_dir = self.vault_path / category_map.get(item.para_category, '04-resources')
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Move file (for now, just update frontmatter to indicate processing)
        item.frontmatter['processed'] = True
        item.frontmatter['para_category'] = item.para_category
        item.frontmatter['processed_date'] = datetime.now().isoformat()
        item.frontmatter['concepts'] = item.concepts
        item.frontmatter['tags'] = list(item.tags)
        item.frontmatter['links'] = list(item.links)
        
        # Update original file with processing metadata
        self._update_item_file(item)
    
    def _update_item_file(self, item: PkmItem):
        """Update the original item file with processing metadata"""
        frontmatter_yaml = yaml.dump(item.frontmatter, default_flow_style=False)
        
        updated_content = f"""---
{frontmatter_yaml}---

{item.content}"""
        
        with open(item.file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

def main():
    """Main execution function for testing"""
    vault_path = Path("./vault")
    pipeline = PkmPipeline(vault_path)
    
    # Process inbox
    processed_items = pipeline.process_inbox()
    
    print(f"\nProcessing complete. {len(processed_items)} items processed.")
    
    # Print summary
    for item in processed_items:
        print(f"- {item.title}: {len(item.concepts)} concepts, {len(item.tags)} tags, {item.para_category}")

if __name__ == "__main__":
    main()