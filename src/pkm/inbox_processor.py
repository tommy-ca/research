"""
FR-002 Inbox Processing Command - GREEN PHASE Implementation

Minimal implementation to pass all RED phase tests.
Following KISS principles: ≤20 lines per function.
"""
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional
import shutil
import re


@dataclass
class InboxResult:
    """Result object for inbox processing operations"""
    success: bool
    processed_count: int
    message: str
    categorized_items: List[Tuple[str, str]]  # (filename, category)


def pkm_process_inbox(vault_path: Path) -> InboxResult:
    """Process inbox items with PARA categorization - KISS refactored"""
    try:
        vault_path = Path(vault_path)
        if not vault_path.exists():
            return InboxResult(False, 0, "Vault directory does not exist", [])
        
        inbox_path = _setup_inbox_and_para_dirs(vault_path)
        inbox_files = list(inbox_path.glob('*.md'))
        
        if not inbox_files:
            return InboxResult(True, 0, "No items to process", [])
            
        categorized = _process_inbox_files(inbox_files, vault_path)
        return InboxResult(True, len(categorized), f"Processed {len(categorized)} items", categorized)
        
    except Exception as e:
        return InboxResult(False, 0, f"Processing error: {str(e)}", [])


def _create_para_directories(vault_path: Path):
    """Create PARA directories if they don't exist"""
    for dir_name in ['02-projects', '03-areas', '04-resources']:
        (vault_path / dir_name).mkdir(exist_ok=True)


def _categorize_file(file_path: Path) -> str:
    """Categorize file using simple keyword matching"""
    try:
        content = file_path.read_text().lower()
    except:
        return '04-resources'  # Default for unreadable files
        
    # Simple keyword mapping for PARA categorization
    project_keywords = ['project', 'planning', 'meeting', 'deadline', 'milestone']
    area_keywords = ['health', 'fitness', 'learning', 'routine', 'maintenance'] 
    
    if any(keyword in content for keyword in project_keywords):
        return '02-projects'
    elif any(keyword in content for keyword in area_keywords):
        return '03-areas'
    else:
        return '04-resources'  # Default category


def _move_file_to_category(file_path: Path, vault_path: Path, category: str):
    """Move file to appropriate PARA category folder"""
    destination = vault_path / category / file_path.name
    shutil.move(str(file_path), str(destination))


def _setup_inbox_and_para_dirs(vault_path: Path) -> Path:
    """Setup inbox and PARA directories, return inbox path"""
    inbox_path = vault_path / '00-inbox'
    if not inbox_path.exists():
        inbox_path.mkdir(parents=True)
    _create_para_directories(vault_path)
    return inbox_path


def _process_inbox_files(inbox_files: List[Path], vault_path: Path) -> List[Tuple[str, str]]:
    """Process all inbox files and return categorized results"""
    categorized = []
    for file_path in inbox_files:
        category = _categorize_file(file_path)
        _move_file_to_category(file_path, vault_path, category)
        categorized.append((file_path.name, category))
    return categorized