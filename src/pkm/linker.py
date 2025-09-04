"""
FR-005 Simple Link Generation - GREEN PHASE Implementation

Minimal implementation to pass all RED phase tests.
Following KISS principles: ≤20 lines per function.
"""
from pathlib import Path
from dataclasses import dataclass
from typing import List, Set, Optional
import re
from collections import Counter


@dataclass 
class LinkSuggestion:
    """Individual link suggestion"""
    target_file: Path
    link_text: str
    relevance_score: float
    preview_text: str
    bidirectional: bool = True


@dataclass
class LinkResult:
    """Result object for link operations"""
    success: bool
    suggestions: List[LinkSuggestion]
    target_file: Path
    message: str


def pkm_link(target_file: Path, vault_path: Path, interactive: bool = False) -> LinkResult:
    """Generate link suggestions for a note - KISS implementation"""
    try:
        if not target_file.exists():
            return LinkResult(False, [], target_file, "Target file does not exist")
        
        if not vault_path.exists():
            return LinkResult(False, [], target_file, "Vault directory does not exist")
        
        target_keywords = _extract_keywords(target_file)
        candidates = _find_candidate_notes(vault_path, target_file)
        suggestions = _generate_suggestions(candidates, target_keywords)
        
        if interactive and suggestions:
            suggestions = _process_user_interaction(suggestions)
            
        message = f"Found {len(suggestions)} link suggestions" if suggestions else "No suitable links found"
        return LinkResult(True, suggestions, target_file, message)
        
    except Exception as e:
        return LinkResult(False, [], target_file, f"Link generation error: {str(e)}")


def _extract_keywords(note_path: Path) -> Set[str]:
    """Extract meaningful keywords from note content"""
    try:
        content = note_path.read_text().lower()
        # Remove frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            content = parts[2] if len(parts) > 2 else content
        
        # Simple keyword extraction: alphanumeric words longer than 3 chars
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content)
        
        # Filter out common stop words
        stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 
                     'have', 'were', 'said', 'each', 'which', 'their', 'what', 'make'}
        
        return set(word for word in words if word not in stop_words)
        
    except:
        return set()


def _find_candidate_notes(vault_path: Path, exclude_file: Path) -> List[Path]:
    """Find all markdown files in vault except target"""
    candidates = []
    for md_file in vault_path.rglob('*.md'):
        if md_file != exclude_file and md_file.is_file():
            candidates.append(md_file)
    return candidates


def _generate_suggestions(candidates: List[Path], target_keywords: Set[str]) -> List[LinkSuggestion]:
    """Generate and rank link suggestions"""
    suggestions = []
    
    for candidate in candidates:
        candidate_keywords = _extract_keywords(candidate)
        shared_keywords = target_keywords.intersection(candidate_keywords)
        
        if shared_keywords:
            relevance_score = len(shared_keywords) + (len(shared_keywords) * 0.5)  # Boost for more keywords
            link_text = f"[[{candidate.stem}]]"
            preview_text = _get_preview_text(candidate)
            
            suggestion = LinkSuggestion(
                target_file=candidate,
                link_text=link_text,
                relevance_score=relevance_score,
                preview_text=preview_text,
                bidirectional=True
            )
            suggestions.append(suggestion)
    
    # Sort by relevance score (highest first)
    return sorted(suggestions, key=lambda s: s.relevance_score, reverse=True)


def _get_preview_text(note_path: Path) -> str:
    """Get preview text from note"""
    try:
        content = note_path.read_text()
        # Remove frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            content = parts[2] if len(parts) > 2 else content
        
        # Get first 150 characters
        preview = content.strip()[:150]
        return preview + '...' if len(content.strip()) > 150 else preview
        
    except:
        return "Preview not available"


def _process_user_interaction(suggestions: List[LinkSuggestion]) -> List[LinkSuggestion]:
    """Process user interaction for accepting/rejecting suggestions"""
    accepted = []
    
    for suggestion in suggestions:
        try:
            response = input(f"Link to {suggestion.target_file.name}? (y/n): ").lower().strip()
            if response == 'y':
                accepted.append(suggestion)
        except (EOFError, KeyboardInterrupt):
            break
    
    return accepted