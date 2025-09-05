"""
FR-003 Daily Note Creation - GREEN PHASE Implementation

Minimal implementation to pass all RED phase tests.
Following KISS principles: ≤20 lines per function.
"""
from pathlib import Path
from dataclasses import dataclass
from datetime import date
import datetime
from typing import List


@dataclass
class DailyNoteResult:
    """Result object for daily note operations"""
    success: bool
    note_path: Path
    was_existing: bool
    created_directories: List[str]
    message: str


def pkm_daily(vault_path: Path, today: date = None) -> DailyNoteResult:
    """Create/open today's daily note - KISS implementation"""
    try:
        vault_path = Path(vault_path)
        if not vault_path.exists():
            return DailyNoteResult(False, Path(), False, [], "Vault directory does not exist")
        
        if today is None:
            today = datetime.date.today()
        note_path, created_dirs = _create_daily_path_and_dirs(vault_path, today)
        was_existing = note_path.exists()
        
        if not was_existing:
            _create_daily_note_with_template(note_path, today)
            
        message = f"{'Opened existing' if was_existing else 'Created new'} daily note"
        return DailyNoteResult(True, note_path, was_existing, created_dirs, message)
        
    except Exception as e:
        return DailyNoteResult(False, Path(), False, [], f"Daily note error: {str(e)}")


def _create_daily_path_and_dirs(vault_path: Path, today: date) -> tuple[Path, List[str]]:
    """Create daily note path and required directories"""
    month_name = today.strftime("%B")  # Full month name
    month_folder = f"{today.month:02d}-{month_name}"
    
    year_dir = vault_path / 'daily' / str(today.year)
    month_dir = year_dir / month_folder
    note_path = month_dir / f"{today.strftime('%Y-%m-%d')}.md"
    
    created_dirs = []
    for dir_path in [year_dir, month_dir]:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(dir_path))
            
    return note_path, created_dirs


def _create_daily_note_with_template(note_path: Path, today: date):
    """Create daily note with frontmatter template"""
    template = f"""---
date: {today.strftime('%Y-%m-%d')}
type: daily
tags: [daily]
---

# Daily Note - {today.strftime('%B %d, %Y')}

## Tasks
- [ ] 

## Notes

## Links

"""
    note_path.write_text(template)