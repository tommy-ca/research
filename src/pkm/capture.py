"""
PKM Capture Module - FR-001 Implementation

TDD GREEN Phase: Minimal implementation to make tests pass
Following KISS principle: Simple, readable, single-purpose functions

This is intentionally minimal - following TDD GREEN phase approach
"""

from pathlib import Path
from datetime import datetime
from typing import NamedTuple, Optional, List
import yaml


class CaptureResult(NamedTuple):
    """Result of capture operation - simple data structure"""
    filename: str
    filepath: Path
    frontmatter: dict
    content: str
    success: bool
    error: Optional[str] = None


class FrontmatterData(NamedTuple):
    """Frontmatter structure - separate concern from content"""
    date: str
    type: str
    tags: List[str]
    status: str
    source: str


def pkm_capture(content: str, vault_path: Optional[Path] = None) -> CaptureResult:
    """Capture content to PKM inbox - KISS refactored version"""
    # Handle input validation
    if content is None:
        return _create_error_result("Content cannot be None")
    
    if content.strip() == "":
        content = "<!-- Empty capture - add content here -->"
    
    # Setup paths
    vault_path = vault_path or Path.cwd() / "vault"
    filepath = _prepare_capture_file(vault_path)
    
    # Create content and save
    frontmatter = _create_capture_frontmatter()
    file_content = _format_markdown_file(frontmatter, content)
    
    try:
        filepath.write_text(file_content)
        return CaptureResult(
            filename=filepath.name,
            filepath=filepath,
            frontmatter=frontmatter,
            content=content,
            success=True
        )
    except Exception as e:
        return _create_error_result(str(e))


# Helper functions following SRP (Single Responsibility Principle)

def _create_error_result(error_message: str) -> CaptureResult:
    """Create error result - SRP helper"""
    return CaptureResult(
        filename="",
        filepath=Path(),
        frontmatter={},
        content="",
        success=False,
        error=error_message
    )


def _prepare_capture_file(vault_path: Path) -> Path:
    """Prepare capture file path - SRP helper"""
    inbox_path = vault_path / "00-inbox"
    inbox_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}.md"
    return inbox_path / filename


def _create_capture_frontmatter() -> dict:
    """Create capture frontmatter - SRP helper"""
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": "capture",
        "tags": [],
        "status": "draft",
        "source": "capture_command"
    }


def _format_markdown_file(frontmatter: dict, content: str) -> str:
    """Format markdown file with frontmatter - SRP helper"""
    return "---\n" + yaml.dump(frontmatter) + "---\n" + content


# Legacy functions for backward compatibility
def create_daily_note_frontmatter(capture_date: datetime) -> dict:
    """Create frontmatter for daily note - separate concern"""
    return {
        "date": capture_date.strftime("%Y-%m-%d"),
        "type": "capture", 
        "tags": [],
        "status": "draft",
        "source": "capture_command"
    }


def generate_capture_filename() -> str:
    """Generate timestamp-based filename"""
    return datetime.now().strftime("%Y%m%d%H%M%S") + ".md"