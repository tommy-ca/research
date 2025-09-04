"""
FR-004 Basic Note Search - GREEN PHASE Implementation

Minimal implementation to pass all RED phase tests.
Following KISS principles: ≤20 lines per function.
Uses ripgrep (rg) for fast searching.
"""
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import subprocess
import re


@dataclass
class SearchMatch:
    """Individual search match result"""
    file_path: Path
    line_number: int
    content: str
    relevance_score: float


@dataclass
class SearchResult:
    """Result object for search operations"""
    success: bool
    matches: List[SearchMatch]
    total_matches: int
    query: str
    message: str


def pkm_search(query: str, vault_path: Path) -> SearchResult:
    """Search across vault content - KISS implementation"""
    try:
        if not query or (isinstance(query, str) and query.strip() == ""):
            return SearchResult(False, [], 0, query or "", "Query cannot be empty")
        
        vault_path = Path(vault_path)
        if not vault_path.exists():
            return SearchResult(False, [], 0, query, "Vault directory does not exist")
        
        matches = _search_with_ripgrep(query, vault_path)
        ranked_matches = _rank_matches_by_relevance(matches, query)
        
        if not ranked_matches:
            return SearchResult(True, [], 0, query, "No matches found")
            
        message = f"Found {len(ranked_matches)} matches"
        return SearchResult(True, ranked_matches, len(ranked_matches), query, message)
        
    except Exception as e:
        return SearchResult(False, [], 0, query or "", f"Search error: {str(e)}")


def _search_with_ripgrep(query: str, vault_path: Path) -> List[SearchMatch]:
    """Use ripgrep to search for content - KISS refactored"""
    try:
        result = subprocess.run(_get_ripgrep_args(query, vault_path), 
                              capture_output=True, text=True, timeout=30)
        
        matches = []
        for line in result.stdout.strip().split('\n'):
            if ':' in line and line.strip():
                match = _parse_ripgrep_line(line)
                if match:
                    matches.append(match)
        
        return matches
        
    except (subprocess.SubprocessError, subprocess.TimeoutExpired):
        return []


def _parse_ripgrep_line(line: str) -> Optional[SearchMatch]:
    """Parse ripgrep output line into SearchMatch"""
    parts = line.split(':', 2)
    if len(parts) >= 3:
        file_path = Path(parts[0])
        try:
            line_number = int(parts[1])
            content = parts[2].strip()
            return SearchMatch(file_path, line_number, content, 1.0)
        except ValueError:
            return None
    return None


def _get_ripgrep_args(query: str, vault_path: Path) -> List[str]:
    """Get ripgrep command arguments"""
    return [
        'rg', 
        '--line-number',
        '--ignore-case', 
        '--type', 'md',
        '--context', '0',
        query,
        str(vault_path)
    ]


def _rank_matches_by_relevance(matches: List[SearchMatch], query: str) -> List[SearchMatch]:
    """Rank matches by relevance score"""
    query_lower = query.lower()
    
    for match in matches:
        # Simple relevance scoring: count occurrences of query terms
        content_lower = match.content.lower()
        match.relevance_score = content_lower.count(query_lower)
        
        # Boost score for exact matches
        if query_lower in content_lower:
            match.relevance_score += 1
    
    # Sort by relevance score (highest first)
    return sorted(matches, key=lambda m: m.relevance_score, reverse=True)