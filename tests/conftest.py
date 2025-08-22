"""
PKM System Testing Configuration and Fixtures
Pytest configuration for comprehensive TDD framework
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

@pytest.fixture
def temp_vault():
    """Create temporary vault structure for testing"""
    temp_dir = tempfile.mkdtemp()
    vault_path = Path(temp_dir) / "test_vault"
    
    # Create standard vault structure
    vault_dirs = [
        "00-inbox",
        "01-projects", 
        "02-areas",
        "03-resources", 
        "04-archives",
        "permanent/notes",
        "daily",
        "templates"
    ]
    
    for dir_name in vault_dirs:
        (vault_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    yield vault_path
    
    # Cleanup
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_content():
    """Provide sample content for testing"""
    return {
        "capture": "Quick note about quantum computing principles",
        "project": "# Research Project\n\nObjective: Study quantum algorithms\nDeadline: 2024-12-31",
        "area": "# Personal Finance\n\nOngoing management of investments and budgeting",
        "resource": "# Quantum Computing Resources\n\nKey papers and references for quantum research"
    }

@pytest.fixture
def test_frontmatter():
    """Standard frontmatter for test notes"""
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": "test",
        "tags": ["test", "automated"],
        "status": "draft"
    }