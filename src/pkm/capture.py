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
    """
    Capture content to PKM inbox
    
    TDD GREEN Phase: Minimal implementation to pass tests
    Following KISS: Simple file creation with basic frontmatter
    """
    # Handle None content (error case)
    if content is None:
        return CaptureResult(
            filename="",
            filepath=Path(),
            frontmatter={},
            content="",
            success=False,
            error="Content cannot be None"
        )
    
    # Handle empty content (placeholder case)
    if content.strip() == "":
        content = "<!-- Empty capture - add content here -->"
    
    # Default vault path
    if vault_path is None:
        vault_path = Path.cwd() / "vault"
    
    # Create inbox directory if missing
    inbox_path = vault_path / "00-inbox"
    inbox_path.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp-based filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}.md"
    filepath = inbox_path / filename
    
    # Create basic frontmatter
    frontmatter = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": "capture",
        "tags": [],
        "status": "draft", 
        "source": "capture_command"
    }
    
    # Create markdown file with frontmatter
    file_content = "---\n" + yaml.dump(frontmatter) + "---\n" + content
    
    try:
        filepath.write_text(file_content)
        return CaptureResult(
            filename=filename,
            filepath=filepath,
            frontmatter=frontmatter,
            content=content,
            success=True
        )
    except Exception as e:
        return CaptureResult(
            filename="",
            filepath=Path(),
            frontmatter={},
            content="",
            success=False,
            error=str(e)
        )


# Following SRP: Separate frontmatter creation
def create_daily_note_frontmatter(capture_date: datetime) -> dict:
    """Create frontmatter for daily note - separate concern"""
    return {
        "date": capture_date.strftime("%Y-%m-%d"),
        "type": "capture", 
        "tags": [],
        "status": "draft",
        "source": "capture_command"
    }


# Following KISS: Simple filename generation
def generate_capture_filename() -> str:
    """Generate timestamp-based filename"""
    return datetime.now().strftime("%Y%m%d%H%M%S") + ".md"