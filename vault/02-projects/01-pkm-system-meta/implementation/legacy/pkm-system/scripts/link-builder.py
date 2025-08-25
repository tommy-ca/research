#!/usr/bin/env python3
"""
link-builder.py - Automated link building and validation system

Builds bidirectional links between notes, validates link integrity,
and suggests new connections based on content similarity and concepts.

Features:
- Automatic link discovery and validation
- Bidirectional link creation and maintenance
- Similarity-based link suggestions
- Orphan note detection and resolution
- Link network analysis and optimization

Usage:
    python link-builder.py --build-all --vault vault/
    python link-builder.py --validate --fix-broken
    python link-builder.py --suggest --similarity-threshold 0.7
    python link-builder.py --analyze --generate-report

Author: Ultra PKM System
Date: 2024-08-22
Version: 1.0.0
"""

import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import hashlib

@dataclass
class Note:
    path: Path
    title: str
    content: str
    existing_links: List[str]
    backlinks: List[str]
    tags: List[str]
    concepts: List[str]
    note_id: Optional[str] = None
    
@dataclass
class LinkSuggestion:
    source_note: str
    target_note: str
    similarity_score: float
    suggestion_reason: str
    confidence: float

class LinkBuilder:
    """Automated link building and validation system"""
    
    def __init__(self, vault_root: str = "vault"):
        self.vault_root = Path(vault_root)
        self.notes = {}  # path -> Note
        self.link_graph = defaultdict(set)  # note_id -> set of linked note_ids
        self.orphan_notes = set()
        self.broken_links = []
        self.link_suggestions = []
        self.log_entries = []
        
        # Link patterns for detection
        self.link_patterns = [
            r'\[\[(.+?)\]\]',  # Wiki-style links
            r'\[(.+?)\]\((.+?)\.md\)',  # Markdown links to .md files
            r'see\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # "see Something" references
            r'related\s+to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'  # "related to Something"
        ]
        
    def discover_all_notes(self) -> Dict[str, Note]:
        """Discover and parse all notes in the vault"""
        self.log("🔍 Discovering all notes in vault...")
        
        notes = {}
        note_patterns = [
            "**/*.md",
            "*/notes/**/*.md", 
            "*/permanent/**/*.md",
            "daily/**/*.md"
        ]
        
        for pattern in note_patterns:
            for note_path in self.vault_root.glob(pattern):
                if note_path.is_file() and self.is_note_file(note_path):
                    note = self.parse_note(note_path)
                    if note:
                        notes[str(note_path)] = note
        
        self.notes = notes
        self.log(f"✅ Discovered {len(notes)} notes")
        return notes
    
    def is_note_file(self, file_path: Path) -> bool:
        """Check if file is a valid note file"""
        # Skip certain files
        skip_patterns = [
            'README.md',
            'CHANGELOG.md', 
            'LICENSE.md',
            '.git',
            'node_modules'
        ]
        
        file_str = str(file_path)
        return not any(pattern in file_str for pattern in skip_patterns)
    
    def parse_note(self, note_path: Path) -> Optional[Note]:
        """Parse a note file and extract metadata"""
        try:
            with open(note_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter = self.extract_frontmatter(content)
            
            # Extract title
            title = self.extract_title(content, frontmatter, note_path)
            
            # Extract existing links
            existing_links = self.extract_existing_links(content)
            
            # Extract tags
            tags = self.extract_tags(content, frontmatter)
            
            # Extract concepts
            concepts = self.extract_concepts(content)
            
            # Get note ID
            note_id = frontmatter.get('id') or self.generate_note_id(note_path)
            
            note = Note(
                path=note_path,
                title=title,
                content=content,
                existing_links=existing_links,
                backlinks=[],  # Will be populated later
                tags=tags,
                concepts=concepts,
                note_id=note_id
            )
            
            return note
            
        except Exception as e:
            self.log(f"❌ Failed to parse note {note_path}: {e}")
            return None
    
    def extract_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from note content"""
        frontmatter = {}
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1]
                # Simple YAML parsing (basic key: value pairs)
                for line in frontmatter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        
                        # Handle lists
                        if value.startswith('[') and value.endswith(']'):
                            value = [item.strip().strip('"\'') for item in value[1:-1].split(',') if item.strip()]
                        
                        frontmatter[key] = value
        
        return frontmatter
    
    def extract_title(self, content: str, frontmatter: Dict, note_path: Path) -> str:
        """Extract note title from frontmatter, content, or filename"""
        # Try frontmatter first
        if 'title' in frontmatter:
            return frontmatter['title']
        
        # Try first H1 header
        h1_match = re.search(r'^# (.+?)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        # Fall back to filename
        return note_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    def extract_existing_links(self, content: str) -> List[str]:
        """Extract all existing links from note content"""
        links = []
        
        for pattern in self.link_patterns:
            matches = re.findall(pattern, content)
            if isinstance(matches[0], tuple) if matches else False:
                # Handle tuple results (like markdown links)
                links.extend([match[0] for match in matches])
            else:
                links.extend(matches)
        
        # Clean and deduplicate
        clean_links = []
        for link in links:
            clean_link = link.strip()
            if clean_link and clean_link not in clean_links:
                clean_links.append(clean_link)
        
        return clean_links
    
    def extract_tags(self, content: str, frontmatter: Dict) -> List[str]:
        """Extract tags from frontmatter and content"""
        tags = []
        
        # From frontmatter
        if 'tags' in frontmatter:
            fm_tags = frontmatter['tags']
            if isinstance(fm_tags, list):
                tags.extend(fm_tags)
            elif isinstance(fm_tags, str):
                # Handle string format like "[tag1, tag2]"
                tags.extend([tag.strip() for tag in fm_tags.strip('[]').split(',') if tag.strip()])
        
        # From content (hashtags)
        hashtag_matches = re.findall(r'#(\w+)', content)
        tags.extend(hashtag_matches)
        
        return list(set(tags))  # Deduplicate
    
    def extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts from note content"""
        concepts = []
        
        # Look for emphasized terms
        emphasized = re.findall(r'\*\*(.+?)\*\*', content)
        concepts.extend([term.lower() for term in emphasized if len(term) < 50])
        
        # Look for definition patterns
        definition_patterns = [
            r'(.+?) is (.+?)(?:\.|$)',
            r'(.+?) refers to (.+?)(?:\.|$)',
            r'(.+?):\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) >= 2:
                    term = match[0].strip().lower()
                    if 5 <= len(term) <= 30:
                        concepts.append(term)
        
        # Look for capitalized terms (proper nouns, technical terms)
        caps_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        concepts.extend([term.lower() for term in caps_terms if 3 <= len(term) <= 30])
        
        # Deduplicate and limit
        return list(set(concepts))[:10]
    
    def generate_note_id(self, note_path: Path) -> str:
        """Generate a unique note ID based on path"""
        path_str = str(note_path.relative_to(self.vault_root))
        return hashlib.md5(path_str.encode()).hexdigest()[:8]
    
    def build_link_graph(self) -> None:
        """Build the link graph from all notes"""
        self.log("🔗 Building link graph...")
        
        # Map titles and IDs to note paths for link resolution
        title_to_path = {}
        id_to_path = {}
        
        for path, note in self.notes.items():
            title_to_path[note.title.lower()] = path
            if note.note_id:
                id_to_path[note.note_id] = path
        
        # Build graph
        for path, note in self.notes.items():
            note_id = note.note_id or path
            
            for link_text in note.existing_links:
                # Try to resolve link
                target_path = self.resolve_link(link_text, title_to_path, id_to_path)
                if target_path:
                    target_note = self.notes[target_path]
                    target_id = target_note.note_id or target_path
                    
                    # Add to graph
                    self.link_graph[note_id].add(target_id)
                    
                    # Add backlink
                    target_note.backlinks.append(note.title)
                else:
                    # Broken link
                    self.broken_links.append((path, link_text))
        
        self.log(f"✅ Built link graph with {sum(len(links) for links in self.link_graph.values())} connections")
    
    def resolve_link(self, link_text: str, title_to_path: Dict, id_to_path: Dict) -> Optional[str]:
        """Resolve a link text to an actual note path"""
        link_lower = link_text.lower().strip()
        
        # Try exact title match
        if link_lower in title_to_path:
            return title_to_path[link_lower]
        
        # Try ID match
        if link_text in id_to_path:
            return id_to_path[link_text]
        
        # Try partial title match
        for title, path in title_to_path.items():
            if link_lower in title or title in link_lower:
                return path
        
        return None
    
    def find_orphan_notes(self) -> Set[str]:
        """Find notes with no incoming or outgoing links"""
        all_note_ids = set()
        linked_note_ids = set()
        
        for path, note in self.notes.items():
            note_id = note.note_id or path
            all_note_ids.add(note_id)
            
            # Notes with outgoing links
            if note.existing_links:
                linked_note_ids.add(note_id)
            
            # Notes with incoming links  
            if note.backlinks:
                linked_note_ids.add(note_id)
        
        self.orphan_notes = all_note_ids - linked_note_ids
        self.log(f"🔍 Found {len(self.orphan_notes)} orphan notes")
        return self.orphan_notes
    
    def suggest_links_by_similarity(self, similarity_threshold: float = 0.7) -> List[LinkSuggestion]:
        """Suggest links based on content similarity"""
        self.log(f"🧠 Generating link suggestions (threshold: {similarity_threshold})")
        
        suggestions = []
        note_list = list(self.notes.items())
        
        for i, (path1, note1) in enumerate(note_list):
            for j, (path2, note2) in enumerate(note_list[i+1:], i+1):
                # Skip if already linked
                note1_id = note1.note_id or path1
                note2_id = note2.note_id or path2
                
                if note2_id in self.link_graph.get(note1_id, set()):
                    continue
                
                # Calculate similarity
                similarity = self.calculate_similarity(note1, note2)
                
                if similarity >= similarity_threshold:
                    reason = self.get_similarity_reason(note1, note2)
                    confidence = min(similarity, 0.95)  # Cap confidence
                    
                    suggestion = LinkSuggestion(
                        source_note=note1.title,
                        target_note=note2.title,
                        similarity_score=similarity,
                        suggestion_reason=reason,
                        confidence=confidence
                    )
                    suggestions.append(suggestion)
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        self.link_suggestions = suggestions[:50]  # Limit to top 50
        
        self.log(f"✅ Generated {len(self.link_suggestions)} link suggestions")
        return self.link_suggestions
    
    def calculate_similarity(self, note1: Note, note2: Note) -> float:
        """Calculate similarity between two notes"""
        similarity_score = 0.0
        
        # Tag overlap (weight: 0.3)
        if note1.tags and note2.tags:
            tag_overlap = len(set(note1.tags) & set(note2.tags)) / len(set(note1.tags) | set(note2.tags))
            similarity_score += tag_overlap * 0.3
        
        # Concept overlap (weight: 0.4)
        if note1.concepts and note2.concepts:
            concept_overlap = len(set(note1.concepts) & set(note2.concepts)) / len(set(note1.concepts) | set(note2.concepts))
            similarity_score += concept_overlap * 0.4
        
        # Content similarity (weight: 0.3)
        content_similarity = self.simple_content_similarity(note1.content, note2.content)
        similarity_score += content_similarity * 0.3
        
        return similarity_score
    
    def simple_content_similarity(self, content1: str, content2: str) -> float:
        """Simple content similarity based on word overlap"""
        # Extract meaningful words
        words1 = set(self.extract_meaningful_words(content1))
        words2 = set(self.extract_meaningful_words(content2))
        
        if not words1 or not words2:
            return 0.0
        
        overlap = len(words1 & words2)
        union = len(words1 | words2)
        
        return overlap / union if union > 0 else 0.0
    
    def extract_meaningful_words(self, content: str) -> List[str]:
        """Extract meaningful words from content"""
        # Remove frontmatter and formatting
        clean_content = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
        clean_content = re.sub(r'[#*\[\](){}]', ' ', clean_content)
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', clean_content.lower())
        
        # Filter out common words
        stopwords = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how',
            'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its',
            'let', 'put', 'say', 'she', 'too', 'use', 'that', 'with', 'have', 'this',
            'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much',
            'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long',
            'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were'
        }
        
        meaningful_words = [word for word in words if word not in stopwords and len(word) > 3]
        return meaningful_words[:20]  # Limit for performance
    
    def get_similarity_reason(self, note1: Note, note2: Note) -> str:
        """Get reason for similarity between notes"""
        reasons = []
        
        # Shared tags
        shared_tags = set(note1.tags) & set(note2.tags)
        if shared_tags:
            reasons.append(f"Shared tags: {', '.join(list(shared_tags)[:3])}")
        
        # Shared concepts
        shared_concepts = set(note1.concepts) & set(note2.concepts)
        if shared_concepts:
            reasons.append(f"Shared concepts: {', '.join(list(shared_concepts)[:3])}")
        
        # Content similarity
        content_sim = self.simple_content_similarity(note1.content, note2.content)
        if content_sim > 0.3:
            reasons.append(f"Content similarity: {content_sim:.1%}")
        
        return "; ".join(reasons) if reasons else "General similarity"
    
    def validate_existing_links(self) -> List[Tuple[str, str]]:
        """Validate all existing links and find broken ones"""
        self.log("🔍 Validating existing links...")
        
        broken_links = []
        
        for path, note in self.notes.items():
            for link in note.existing_links:
                if not self.is_valid_link(link):
                    broken_links.append((path, link))
        
        self.broken_links = broken_links
        self.log(f"⚠️ Found {len(broken_links)} broken links")
        return broken_links
    
    def is_valid_link(self, link: str) -> bool:
        """Check if a link is valid (points to an existing note)"""
        # Build title mapping if not done
        if not hasattr(self, '_title_to_path'):
            self._title_to_path = {note.title.lower(): path for path, note in self.notes.items()}
        
        link_lower = link.lower().strip()
        return link_lower in self._title_to_path
    
    def fix_broken_links(self, dry_run: bool = True) -> int:
        """Attempt to fix broken links automatically"""
        self.log(f"🔧 {'[DRY-RUN] ' if dry_run else ''}Attempting to fix broken links...")
        
        fixed_count = 0
        
        for note_path, broken_link in self.broken_links:
            # Try to find similar titles
            suggested_target = self.find_similar_title(broken_link)
            
            if suggested_target:
                if not dry_run:
                    self.replace_link_in_file(Path(note_path), broken_link, suggested_target)
                    
                self.log(f"{'[DRY-RUN] ' if dry_run else ''}Fixed: '{broken_link}' → '{suggested_target}' in {Path(note_path).name}")
                fixed_count += 1
            else:
                self.log(f"❌ Could not fix broken link: '{broken_link}' in {Path(note_path).name}")
        
        return fixed_count
    
    def find_similar_title(self, broken_link: str) -> Optional[str]:
        """Find a similar title for a broken link"""
        broken_lower = broken_link.lower()
        
        best_match = None
        best_score = 0.0
        
        for note_path, note in self.notes.items():
            title_lower = note.title.lower()
            
            # Calculate simple similarity
            score = 0.0
            
            # Exact substring match
            if broken_lower in title_lower or title_lower in broken_lower:
                score += 0.8
            
            # Word overlap
            broken_words = set(broken_lower.split())
            title_words = set(title_lower.split())
            
            if broken_words and title_words:
                overlap = len(broken_words & title_words) / len(broken_words | title_words)
                score += overlap * 0.6
            
            if score > best_score and score > 0.5:  # Minimum similarity threshold
                best_score = score
                best_match = note.title
        
        return best_match
    
    def replace_link_in_file(self, file_path: Path, old_link: str, new_link: str) -> None:
        """Replace a link in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace various link formats
            patterns = [
                (f'[[{old_link}]]', f'[[{new_link}]]'),
                (f'[{old_link}]', f'[{new_link}]'),
                (old_link, new_link)
            ]
            
            for old_pattern, new_pattern in patterns:
                content = content.replace(old_pattern, new_pattern)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            self.log(f"❌ Failed to replace link in {file_path}: {e}")
    
    def generate_link_network_report(self) -> str:
        """Generate comprehensive link network analysis report"""
        report_lines = [
            "=" * 60,
            "🔗 LINK NETWORK ANALYSIS REPORT",
            "=" * 60,
            f"Generated: {datetime.now().isoformat()}",
            "",
            "📊 NETWORK STATISTICS:",
            f"Total Notes: {len(self.notes)}",
            f"Total Links: {sum(len(links) for links in self.link_graph.values())}",
            f"Average Links per Note: {sum(len(links) for links in self.link_graph.values()) / len(self.notes) if self.notes else 0:.1f}",
            f"Orphan Notes: {len(self.orphan_notes)}",
            f"Broken Links: {len(self.broken_links)}",
            "",
            "🔍 LINK SUGGESTIONS:",
            f"Generated Suggestions: {len(self.link_suggestions)}",
        ]
        
        # Top link suggestions
        if self.link_suggestions:
            report_lines.append("\nTop Link Suggestions:")
            for i, suggestion in enumerate(self.link_suggestions[:10], 1):
                report_lines.append(f"{i}. {suggestion.source_note} ↔ {suggestion.target_note}")
                report_lines.append(f"   Score: {suggestion.similarity_score:.2f} | Reason: {suggestion.suggestion_reason}")
        
        # Most connected notes
        if self.link_graph:
            connected_notes = [(note_id, len(links)) for note_id, links in self.link_graph.items()]
            connected_notes.sort(key=lambda x: x[1], reverse=True)
            
            report_lines.append("\nMost Connected Notes:")
            for i, (note_id, link_count) in enumerate(connected_notes[:10], 1):
                note_title = self.get_note_title_by_id(note_id)
                report_lines.append(f"{i}. {note_title}: {link_count} links")
        
        # Orphan notes
        if self.orphan_notes:
            report_lines.append(f"\nOrphan Notes ({len(self.orphan_notes)}):")
            for orphan_id in list(self.orphan_notes)[:20]:  # Show first 20
                orphan_title = self.get_note_title_by_id(orphan_id)
                report_lines.append(f"- {orphan_title}")
        
        # Broken links
        if self.broken_links:
            report_lines.append(f"\nBroken Links ({len(self.broken_links)}):")
            for note_path, broken_link in self.broken_links[:20]:  # Show first 20
                note_name = Path(note_path).name
                report_lines.append(f"- {note_name}: '{broken_link}'")
        
        report_lines.extend([
            "",
            "=" * 60,
            "End of Report"
        ])
        
        return "\n".join(report_lines)
    
    def get_note_title_by_id(self, note_id: str) -> str:
        """Get note title by ID"""
        for path, note in self.notes.items():
            if (note.note_id or path) == note_id:
                return note.title
        return f"Unknown ({note_id[:8]})"
    
    def log(self, message: str) -> None:
        """Add message to log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.log_entries.append(log_entry)
        print(log_entry)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Build and validate note links')
    parser.add_argument('--vault', default='vault', help='Vault directory path')
    parser.add_argument('--build-all', action='store_true', help='Build complete link graph')
    parser.add_argument('--validate', action='store_true', help='Validate existing links')
    parser.add_argument('--fix-broken', action='store_true', help='Fix broken links')
    parser.add_argument('--suggest', action='store_true', help='Generate link suggestions')
    parser.add_argument('--similarity-threshold', type=float, default=0.7, help='Similarity threshold for suggestions')
    parser.add_argument('--analyze', action='store_true', help='Analyze link network')
    parser.add_argument('--generate-report', action='store_true', help='Generate analysis report')
    parser.add_argument('--dry-run', action='store_true', help='Show results without making changes')
    
    args = parser.parse_args()
    
    # Initialize link builder
    builder = LinkBuilder(args.vault)
    
    try:
        # Discover all notes
        builder.discover_all_notes()
        
        if args.build_all:
            builder.build_link_graph()
            builder.find_orphan_notes()
        
        if args.validate:
            builder.validate_existing_links()
            
            if args.fix_broken:
                fixed_count = builder.fix_broken_links(args.dry_run)
                print(f"{'[DRY-RUN] ' if args.dry_run else ''}Fixed {fixed_count} broken links")
        
        if args.suggest:
            builder.suggest_links_by_similarity(args.similarity_threshold)
        
        if args.analyze or args.generate_report:
            # Ensure we have the data
            if not builder.link_graph:
                builder.build_link_graph()
                builder.find_orphan_notes()
            if not builder.link_suggestions:
                builder.suggest_links_by_similarity(args.similarity_threshold)
            
            report = builder.generate_link_network_report()
            
            if args.generate_report:
                report_file = f"link-network-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
                with open(report_file, 'w') as f:
                    f.write(report)
                print(f"📋 Report saved to: {report_file}")
            else:
                print(report)
        
        return 0
        
    except Exception as e:
        print(f"❌ Link building failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())