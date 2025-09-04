"""
Integration Testing Utilities - GREEN PHASE Implementation

Minimal implementation to support RED phase integration tests.
Following KISS principles: ≤20 lines per function.
"""
import tempfile
import shutil
from pathlib import Path
from datetime import date
from typing import List
import sys
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from pkm.capture import pkm_capture
from pkm.inbox_processor import pkm_process_inbox
from pkm.daily import pkm_daily
from pkm.search import pkm_search
from pkm.linker import pkm_link


class VaultTestSetup:
    """Context manager for test vault setup - KISS implementation"""
    
    def __init__(self):
        self.temp_dir = None
        self.path = None
    
    def __enter__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / 'vault'
        self._create_vault_structure()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir:
            self.temp_dir.cleanup()
    
    def _create_vault_structure(self):
        """Create basic vault directory structure"""
        directories = ['00-inbox', '02-projects', '03-areas', '04-resources', '05-archives']
        for dir_name in directories:
            (self.path / dir_name).mkdir(parents=True, exist_ok=True)
        
        # Create daily directory structure
        today = date.today()
        month_name = today.strftime("%B")
        daily_dir = self.path / 'daily' / str(today.year) / f"{today.month:02d}-{month_name}"
        daily_dir.mkdir(parents=True, exist_ok=True)
    
    def has_inbox_files(self) -> bool:
        """Check if inbox has files"""
        inbox_dir = self.path / '00-inbox'
        return inbox_dir.exists() and any(inbox_dir.glob('*.md'))
    
    def has_project_files(self) -> bool:
        """Check if projects directory has files"""
        projects_dir = self.path / '02-projects'
        return projects_dir.exists() and any(projects_dir.glob('*.md'))
    
    def has_processed_files(self) -> bool:
        """Check if any PARA directory has processed files"""
        para_dirs = ['02-projects', '03-areas', '04-resources']
        for dir_name in para_dirs:
            para_dir = self.path / dir_name
            if para_dir.exists() and any(para_dir.glob('*.md')):
                return True
        return False
    
    def has_daily_note_for_today(self) -> bool:
        """Check if today's daily note exists"""
        daily_note = self.get_daily_note_for_today()
        return daily_note and daily_note.exists()
    
    def get_daily_note_for_today(self) -> Path:
        """Get path to today's daily note"""
        today = date.today()
        month_name = today.strftime("%B")
        daily_dir = self.path / 'daily' / str(today.year) / f"{today.month:02d}-{month_name}"
        return daily_dir / f"{today.strftime('%Y-%m-%d')}.md"
    
    def get_first_project_file(self) -> Path:
        """Get first project file for testing"""
        projects_dir = self.path / '02-projects'
        for file in projects_dir.glob('*.md'):
            return file
        return None
    
    def get_processed_files(self) -> List[Path]:
        """Get all processed files from PARA directories"""
        files = []
        para_dirs = ['02-projects', '03-areas', '04-resources']
        for dir_name in para_dirs:
            para_dir = self.path / dir_name
            if para_dir.exists():
                files.extend(list(para_dir.glob('*.md')))
        return files
    
    def get_files_containing(self, text: str) -> List[Path]:
        """Get files containing specific text"""
        matching_files = []
        for md_file in self.path.rglob('*.md'):
            try:
                content = md_file.read_text().lower()
                if text.lower() in content:
                    matching_files.append(md_file)
            except:
                continue
        return matching_files


class IntegrationTestRunner:
    """Test runner for integration tests - KISS implementation"""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self._capture_counter = 0
    
    def run_capture(self, content: str):
        """Run capture command and return result"""
        import time
        from datetime import datetime
        # Add delay to ensure unique timestamps (1 second for timestamp resolution)
        time.sleep(1.0)
        
        # For integration tests, modify content slightly to ensure uniqueness
        unique_content = f"{content} [test-{self._capture_counter}]"
        self._capture_counter += 1
        return pkm_capture(unique_content, vault_path=self.vault_path)
    
    def run_process_inbox(self):
        """Run inbox processing command and return result"""
        return pkm_process_inbox(vault_path=self.vault_path)
    
    def run_daily(self):
        """Run daily note creation command and return result"""
        return pkm_daily(vault_path=self.vault_path)
    
    def run_search(self, query: str):
        """Run search command and return result"""
        return pkm_search(query, vault_path=self.vault_path)
    
    def run_link(self, note_path: Path):
        """Run link generation command and return result"""
        return pkm_link(note_path, vault_path=self.vault_path, interactive=False)