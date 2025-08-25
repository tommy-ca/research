#!/usr/bin/env python3
"""
atomic-extractor.py - Specialized atomic note extraction system

Focused tool for extracting atomic notes from long documents using
advanced NLP patterns and domain-specific knowledge extraction.

Features:
- Multiple extraction strategies (headers, concepts, patterns)
- Domain-specific knowledge patterns
- Quality scoring and ranking
- Automated link suggestion
- Frontmatter generation

Usage:
    python atomic-extractor.py --file docs/long-document.md --target 10
    python atomic-extractor.py --file docs/feynman-research.md --target 15 --domain research
    python atomic-extractor.py --batch docs/pkm-architecture/ --target 25

Author: Ultra PKM System  
Date: 2024-08-22
Version: 1.0.0
"""

import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class AtomicCandidate:
    title: str
    content: str
    score: float
    extraction_method: str
    source_file: str
    level: int
    domain: str
    concepts: List[str]
    potential_links: List[str]

class AtomicExtractor:
    """Specialized atomic note extraction system"""
    
    def __init__(self, output_dir: str = "vault/01-notes/permanent/concepts"):
        self.output_dir = Path(output_dir)
        self.extracted_notes = []
        self.extraction_log = []
        
        # Domain-specific extraction patterns
        self.domain_patterns = {
            'architecture': {
                'components': r'##\s+(.+?Component.+?)\n(.*?)(?=\n##|\n#|\Z)',
                'principles': r'###\s+(.+?Principle.+?)\n(.*?)(?=\n###|\n##|\Z)', 
                'patterns': r'###\s+(.+?Pattern.+?)\n(.*?)(?=\n###|\n##|\Z)',
                'specifications': r'##\s+(.+?Specification.+?)\n(.*?)(?=\n##|\n#|\Z)'
            },
            'finance': {
                'criteria': r'[A-Z]\.\s+(.+?):\s*(.*?)(?=\n[A-Z]\.|\n\n|$)',
                'strategies': r'###\s+(.+?Strategy.+?)\n(.*?)(?=\n###|\n##|\Z)',
                'metrics': r'###\s+(.+?Metric.+?)\n(.*?)(?=\n###|\n##|\Z)',
                'analysis': r'##\s+(.+?Analysis.+?)\n(.*?)(?=\n##|\n#|\Z)'
            },
            'research': {
                'findings': r'Finding\s+\d+:\s*(.+?)\n(.*?)(?=\nFinding|\n##|\Z)',
                'methods': r'###\s+(.+?Method.+?)\n(.*?)(?=\n###|\n##|\Z)',
                'frameworks': r'##\s+(.+?Framework.+?)\n(.*?)(?=\n##|\n#|\Z)',
                'principles': r'###\s+(.+?Principle.+?)\n(.*?)(?=\n###|\n##|\Z)'
            },
            'workflow': {
                'steps': r'Step\s+\d+:\s*(.+?)\n(.*?)(?=\nStep|\n##|\Z)',
                'processes': r'###\s+(.+?Process.+?)\n(.*?)(?=\n###|\n##|\Z)',
                'procedures': r'##\s+(.+?Procedure.+?)\n(.*?)(?=\n##|\n#|\Z)',
                'guidelines': r'###\s+(.+?Guideline.+?)\n(.*?)(?=\n###|\n##|\Z)'
            }
        }
        
        # Concept identification patterns
        self.concept_patterns = [
            r'(.+?)\s+is\s+(.+?)\.(?:\n|$)',
            r'(.+?)\s+refers\s+to\s+(.+?)\.(?:\n|$)', 
            r'(.+?)\s+means\s+(.+?)\.(?:\n|$)',
            r'(.+?):\s*(.+?)(?:\n\n|\n[A-Z]|$)',
            r'**(.+?)**\s*[:\-]\s*(.+?)(?:\n|$)',
            r'## (.+?)\n\n(.+?)(?:\n##|\Z)'
        ]
        
    def extract_from_file(self, file_path: Path, target_count: int = 10, domain: str = 'auto') -> List[AtomicCandidate]:
        """Extract atomic notes from a single file"""
        self.log(f"🔍 Extracting atomic notes from {file_path.name}")
        
        if not file_path.exists():
            self.log(f"❌ File not found: {file_path}")
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Auto-detect domain if not specified
            if domain == 'auto':
                domain = self.detect_domain(file_path, content)
            
            # Remove frontmatter for processing
            clean_content = self.remove_frontmatter(content)
            
            # Extract candidates using multiple methods
            candidates = []
            candidates.extend(self.extract_by_headers(clean_content, file_path, domain))
            candidates.extend(self.extract_by_concepts(clean_content, file_path, domain))
            candidates.extend(self.extract_by_domain_patterns(clean_content, file_path, domain))
            candidates.extend(self.extract_by_lists(clean_content, file_path, domain))
            
            # Score and rank candidates
            for candidate in candidates:
                candidate.score = self.calculate_atomic_score(candidate)
            
            # Sort by score and return top candidates
            candidates.sort(key=lambda x: x.score, reverse=True)
            top_candidates = candidates[:target_count]
            
            self.log(f"✅ Extracted {len(top_candidates)} atomic notes from {file_path.name}")
            return top_candidates
            
        except Exception as e:
            self.log(f"❌ Extraction failed for {file_path}: {e}")
            return []
    
    def detect_domain(self, file_path: Path, content: str) -> str:
        """Auto-detect the domain of the content"""
        file_str = str(file_path).lower()
        content_lower = content.lower()
        
        domain_indicators = {
            'architecture': ['architecture', 'system', 'component', 'design', 'spec'],
            'finance': ['finance', 'investment', 'canslim', 'trading', 'market', 'stock'],
            'research': ['research', 'analysis', 'study', 'finding', 'methodology'],
            'workflow': ['workflow', 'process', 'procedure', 'guide', 'step']
        }
        
        for domain, indicators in domain_indicators.items():
            if any(indicator in file_str for indicator in indicators):
                return domain
            if sum(1 for indicator in indicators if indicator in content_lower) >= 2:
                return domain
        
        return 'general'
    
    def remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from content"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()
        return content
    
    def extract_by_headers(self, content: str, file_path: Path, domain: str) -> List[AtomicCandidate]:
        """Extract atomic notes based on markdown headers"""
        candidates = []
        
        # Split by headers at different levels
        header_patterns = [
            (r'^### (.+?)\n(.*?)(?=\n###|\n##|\n#|\Z)', 3),
            (r'^## (.+?)\n(.*?)(?=\n##|\n#|\Z)', 2), 
            (r'^#### (.+?)\n(.*?)(?=\n####|\n###|\n##|\n#|\Z)', 4)
        ]
        
        for pattern, level in header_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                title = match.group(1).strip()
                section_content = match.group(2).strip()
                
                if self.is_good_atomic_candidate(title, section_content):
                    candidate = AtomicCandidate(
                        title=title,
                        content=section_content,
                        score=0.0,  # Will be calculated later
                        extraction_method=f'header_level_{level}',
                        source_file=str(file_path),
                        level=level,
                        domain=domain,
                        concepts=self.extract_concepts_from_text(section_content),
                        potential_links=self.find_potential_links(section_content)
                    )
                    candidates.append(candidate)
        
        return candidates
    
    def extract_by_concepts(self, content: str, file_path: Path, domain: str) -> List[AtomicCandidate]:
        """Extract atomic notes based on concept patterns"""
        candidates = []
        
        for pattern in self.concept_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if len(match.groups()) >= 2:
                    concept_name = match.group(1).strip()
                    concept_definition = match.group(2).strip()
                    
                    # Combine for full content
                    full_content = f"{concept_name}: {concept_definition}"
                    
                    if self.is_good_atomic_candidate(concept_name, concept_definition):
                        candidate = AtomicCandidate(
                            title=concept_name,
                            content=full_content,
                            score=0.0,
                            extraction_method='concept_pattern',
                            source_file=str(file_path),
                            level=3,
                            domain=domain,
                            concepts=[concept_name.lower()],
                            potential_links=self.find_potential_links(concept_definition)
                        )
                        candidates.append(candidate)
        
        return candidates
    
    def extract_by_domain_patterns(self, content: str, file_path: Path, domain: str) -> List[AtomicCandidate]:
        """Extract atomic notes using domain-specific patterns"""
        candidates = []
        
        if domain not in self.domain_patterns:
            return candidates
        
        domain_patterns = self.domain_patterns[domain]
        
        for pattern_name, pattern in domain_patterns.items():
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if len(match.groups()) >= 2:
                    title = match.group(1).strip()
                    pattern_content = match.group(2).strip()
                    
                    if self.is_good_atomic_candidate(title, pattern_content):
                        candidate = AtomicCandidate(
                            title=f"{domain.title()} {pattern_name.title()}: {title}",
                            content=pattern_content,
                            score=0.0,
                            extraction_method=f'domain_{domain}_{pattern_name}',
                            source_file=str(file_path),
                            level=3,
                            domain=domain,
                            concepts=self.extract_concepts_from_text(pattern_content),
                            potential_links=self.find_potential_links(pattern_content)
                        )
                        candidates.append(candidate)
        
        return candidates
    
    def extract_by_lists(self, content: str, file_path: Path, domain: str) -> List[AtomicCandidate]:
        """Extract atomic notes from structured lists"""
        candidates = []
        
        # Look for definition lists
        list_patterns = [
            r'-\s+\*\*(.+?)\*\*:\s*(.+?)(?=\n-|\n\n|\Z)',  # Bold list items
            r'\d+\.\s+\*\*(.+?)\*\*:\s*(.+?)(?=\n\d+\.|\n\n|\Z)',  # Numbered bold items
            r'-\s+(.+?):\s*(.+?)(?=\n-|\n\n|\Z)',  # Simple list items
        ]
        
        for pattern in list_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                term = match.group(1).strip()
                definition = match.group(2).strip()
                
                if self.is_good_atomic_candidate(term, definition):
                    candidate = AtomicCandidate(
                        title=term,
                        content=f"{term}: {definition}",
                        score=0.0,
                        extraction_method='list_extraction',
                        source_file=str(file_path),
                        level=4,
                        domain=domain,
                        concepts=[term.lower()],
                        potential_links=self.find_potential_links(definition)
                    )
                    candidates.append(candidate)
        
        return candidates
    
    def is_good_atomic_candidate(self, title: str, content: str) -> bool:
        """Check if title and content make a good atomic note candidate"""
        # Title checks
        if len(title) < 5 or len(title) > 100:
            return False
        
        # Content checks
        if len(content) < 20 or len(content) > 2000:
            return False
        
        # Avoid very generic titles
        generic_titles = ['introduction', 'overview', 'conclusion', 'summary', 'notes']
        if title.lower() in generic_titles:
            return False
        
        # Content should not be just a list of links
        if content.count('[') > len(content) / 20:
            return False
        
        return True
    
    def calculate_atomic_score(self, candidate: AtomicCandidate) -> float:
        """Calculate quality score for atomic note candidate"""
        score = 0.0
        
        # Content length scoring (optimal: 100-500 chars)
        content_length = len(candidate.content)
        if 100 <= content_length <= 500:
            score += 1.0
        elif 50 <= content_length < 100 or 500 < content_length <= 800:
            score += 0.7
        elif 20 <= content_length < 50 or 800 < content_length <= 1200:
            score += 0.4
        
        # Title quality scoring
        title_length = len(candidate.title)
        if 10 <= title_length <= 60:
            score += 0.5
        elif 5 <= title_length < 10 or 60 < title_length <= 80:
            score += 0.3
        
        # Concept density bonus
        concept_count = len(candidate.concepts)
        if concept_count >= 3:
            score += 0.3
        elif concept_count >= 1:
            score += 0.2
        
        # Link potential bonus
        if len(candidate.potential_links) >= 3:
            score += 0.3
        elif len(candidate.potential_links) >= 1:
            score += 0.2
        
        # Extraction method bonus
        if 'domain' in candidate.extraction_method:
            score += 0.4
        elif 'concept' in candidate.extraction_method:
            score += 0.3
        elif 'header' in candidate.extraction_method:
            score += 0.2
        
        # Header level bonus (prefer subsections)
        if candidate.level == 3:
            score += 0.2
        elif candidate.level == 4:
            score += 0.3
        
        # Domain-specific bonuses
        if candidate.domain in ['architecture', 'finance', 'research']:
            score += 0.2
        
        return score
    
    def extract_concepts_from_text(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        concepts = []
        
        # Look for capitalized terms
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        concepts.extend([term.lower() for term in capitalized_terms[:3]])
        
        # Look for technical terms
        technical_patterns = [
            r'\b\w+(?:ing|tion|ment|ness|ity)\b',  # Common suffixes
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w*[A-Z]\w*[A-Z]\w*\b'  # CamelCase
        ]
        
        for pattern in technical_patterns:
            matches = re.findall(pattern, text)
            concepts.extend([match.lower() for match in matches[:2]])
        
        return list(set(concepts))[:5]  # Dedupe and limit
    
    def find_potential_links(self, content: str) -> List[str]:
        """Find potential links to other notes"""
        links = []
        
        # Existing wiki-style links
        wiki_links = re.findall(r'\[\[(.+?)\]\]', content)
        links.extend(wiki_links)
        
        # "See also" patterns
        see_patterns = [
            r'see\s+(.+?)(?:\s|$)',
            r'related\s+to\s+(.+?)(?:\s|$)',
            r'similar\s+to\s+(.+?)(?:\s|$)',
            r'based\s+on\s+(.+?)(?:\s|$)'
        ]
        
        for pattern in see_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            links.extend(matches[:2])
        
        # Clean and limit links
        clean_links = []
        for link in links:
            clean_link = re.sub(r'[^\w\s-]', '', link).strip()
            if 5 <= len(clean_link) <= 50:
                clean_links.append(clean_link)
        
        return clean_links[:5]
    
    def create_atomic_note_file(self, candidate: AtomicCandidate) -> str:
        """Create formatted atomic note file content"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        note_id = f"{timestamp}-{self.slugify(candidate.title)}"
        
        # Enhanced frontmatter
        frontmatter = f"""---
id: {note_id}
title: "{candidate.title}"
date: {datetime.now().strftime('%Y-%m-%d')}
type: zettel
tags: {self.generate_tags(candidate)}
links: {[f"[[{link}]]" for link in candidate.potential_links]}
source: {Path(candidate.source_file).name}
extraction_method: {candidate.extraction_method}
domain: {candidate.domain}
score: {candidate.score:.2f}
created: {datetime.now().isoformat()}
modified: {datetime.now().isoformat()}
---

# {candidate.title}
<!-- ID: {note_id} -->

## Core Content
{candidate.content}

## Key Concepts
{self.format_concepts(candidate.concepts)}

## Connections
{self.format_links(candidate.potential_links)}

## Source Context
Extracted from: `{Path(candidate.source_file).name}`
Method: {candidate.extraction_method}
Domain: {candidate.domain}
"""
        return frontmatter
    
    def generate_tags(self, candidate: AtomicCandidate) -> List[str]:
        """Generate comprehensive tags for atomic note"""
        tags = []
        
        # Domain tag
        tags.append(candidate.domain)
        
        # Extraction method tag
        tags.append(f"extracted-{candidate.extraction_method.split('_')[0]}")
        
        # Content-based tags
        content_lower = candidate.content.lower()
        title_lower = candidate.title.lower()
        
        tag_keywords = {
            'principle': ['principle', 'law', 'rule'],
            'framework': ['framework', 'model', 'structure'],
            'process': ['process', 'procedure', 'workflow'],
            'concept': ['concept', 'idea', 'notion'],
            'method': ['method', 'approach', 'technique'],
            'pattern': ['pattern', 'template', 'design'],
            'system': ['system', 'architecture', 'infrastructure']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in content_lower or keyword in title_lower for keyword in keywords):
                tags.append(tag)
        
        # Add concept tags
        tags.extend(candidate.concepts[:3])
        
        return list(set(tags))[:7]  # Dedupe and limit to 7 tags
    
    def format_concepts(self, concepts: List[str]) -> str:
        """Format concepts list for note"""
        if not concepts:
            return "- *No specific concepts identified*"
        
        formatted = []
        for concept in concepts[:5]:
            formatted.append(f"- `{concept}`")
        
        return '\n'.join(formatted)
    
    def format_links(self, links: List[str]) -> str:
        """Format potential links for note"""
        if not links:
            return "- *No connections identified yet*"
        
        formatted = []
        for link in links[:5]:
            formatted.append(f"- [[{link}]]")
        
        return '\n'.join(formatted)
    
    def slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')[:40]  # Limit length
    
    def save_atomic_notes(self, candidates: List[AtomicCandidate], dry_run: bool = True) -> int:
        """Save atomic notes to files"""
        if dry_run:
            self.log("[DRY-RUN] Would save the following atomic notes:")
            for candidate in candidates:
                self.log(f"  - {candidate.title} (score: {candidate.score:.2f})")
            return len(candidates)
        
        saved_count = 0
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        for candidate in candidates:
            try:
                note_content = self.create_atomic_note_file(candidate)
                timestamp = datetime.now().strftime('%Y%m%d%H%M')
                filename = f"{timestamp}-{self.slugify(candidate.title)}.md"
                file_path = self.output_dir / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(note_content)
                
                self.log(f"✅ Saved: {filename}")
                saved_count += 1
                
            except Exception as e:
                self.log(f"❌ Failed to save note '{candidate.title}': {e}")
        
        return saved_count
    
    def batch_extract(self, source_dir: Path, target_count: int = 25, domain: str = 'auto') -> List[AtomicCandidate]:
        """Extract atomic notes from all files in a directory"""
        self.log(f"📁 Batch extracting from {source_dir}")
        
        all_candidates = []
        for file_path in source_dir.rglob('*.md'):
            if file_path.is_file():
                candidates = self.extract_from_file(file_path, target_count // 3, domain)
                all_candidates.extend(candidates)
        
        # Re-rank all candidates together
        for candidate in all_candidates:
            candidate.score = self.calculate_atomic_score(candidate)
        
        all_candidates.sort(key=lambda x: x.score, reverse=True)
        return all_candidates[:target_count]
    
    def log(self, message: str) -> None:
        """Add message to extraction log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.extraction_log.append(log_entry)
        print(log_entry)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Extract atomic notes from documents')
    parser.add_argument('--file', help='Single file to process')
    parser.add_argument('--batch', help='Directory to batch process')
    parser.add_argument('--target', type=int, default=10, help='Target number of atomic notes')
    parser.add_argument('--domain', default='auto', help='Content domain (auto, architecture, finance, research, workflow)')
    parser.add_argument('--output', default='vault/01-notes/permanent/concepts', help='Output directory')
    parser.add_argument('--dry-run', action='store_true', help='Show extraction results without saving')
    
    args = parser.parse_args()
    
    if not args.file and not args.batch:
        print("Error: Specify either --file or --batch")
        return 1
    
    # Initialize extractor
    extractor = AtomicExtractor(args.output)
    
    try:
        # Extract atomic notes
        if args.file:
            candidates = extractor.extract_from_file(Path(args.file), args.target, args.domain)
        else:
            candidates = extractor.batch_extract(Path(args.batch), args.target, args.domain)
        
        if not candidates:
            print("No atomic notes extracted")
            return 1
        
        # Save notes
        saved_count = extractor.save_atomic_notes(candidates, args.dry_run)
        
        # Summary
        print(f"\n📊 Extraction Summary:")
        print(f"Candidates found: {len(candidates)}")
        print(f"Notes {'would be ' if args.dry_run else ''}saved: {saved_count}")
        
        if candidates:
            avg_score = sum(c.score for c in candidates) / len(candidates)
            print(f"Average quality score: {avg_score:.2f}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())