---
title: "TDD and Specs-Driven Development Examples"
date: 2024-01-21
type: resource
tags: [tdd, specs, development, examples, pkm]
---

# TDD and Specs-Driven Development Examples for PKM

## Specification Template

### Example 1: PKM Capture Command Specification

```markdown
## Feature: PKM Quick Capture
Version: 1.0
Status: In Development

### Functional Requirements (IMPLEMENT NOW)
- FR-001: Accept text input and save to inbox
- FR-002: Generate unique timestamp-based filename
- FR-003: Add YAML frontmatter with metadata
- FR-004: Return confirmation with file location
- FR-005: Support optional source parameter

### Non-Functional Requirements (DEFER)
- NFR-001: Response time < 100ms (DEFER - Week 4)
- NFR-002: Handle 1000 concurrent captures (DEFER - Production)
- NFR-003: Encrypt sensitive content (DEFER - Security phase)
- NFR-004: Compress large captures (DEFER - Optimization)

### Acceptance Criteria
- [ ] Given text input, When capture command runs, Then file created in inbox
- [ ] Given no input, When capture runs, Then error message returned
- [ ] Given source URL, When capture runs, Then source added to frontmatter
- [ ] Given existing file, When capture runs, Then unique filename generated

### Test Cases
1. test_capture_creates_file() - File exists after capture
2. test_capture_adds_frontmatter() - Frontmatter contains required fields
3. test_capture_unique_filename() - No filename collisions
4. test_capture_empty_input() - Handles empty gracefully
5. test_capture_with_source() - Source parameter saved
```

## TDD Implementation Example

### Step 1: Write Tests First (RED Phase)

```python
# tests/test_pkm_capture.py
import pytest
from pathlib import Path
from datetime import datetime
from pkm.commands import capture

def test_capture_creates_file():
    """Test that capture creates a file in inbox"""
    # Arrange
    content = "Test note content"
    
    # Act
    result = capture(content)
    
    # Assert
    assert result.success == True
    assert Path(result.filepath).exists()
    assert "vault/0-inbox" in result.filepath

def test_capture_adds_frontmatter():
    """Test that captured file has correct frontmatter"""
    # Arrange
    content = "Test content"
    
    # Act
    result = capture(content)
    
    # Assert
    with open(result.filepath, 'r') as f:
        file_content = f.read()
    
    assert "---" in file_content
    assert "date:" in file_content
    assert "type: capture" in file_content
    assert "status: inbox" in file_content

def test_capture_unique_filename():
    """Test that multiple captures create unique files"""
    # Arrange
    content1 = "First capture"
    content2 = "Second capture"
    
    # Act
    result1 = capture(content1)
    result2 = capture(content2)
    
    # Assert
    assert result1.filepath != result2.filepath
    assert Path(result1.filepath).exists()
    assert Path(result2.filepath).exists()

def test_capture_empty_input():
    """Test that empty input is handled gracefully"""
    # Arrange
    content = ""
    
    # Act
    result = capture(content)
    
    # Assert
    assert result.success == False
    assert "Content cannot be empty" in result.error

def test_capture_with_source():
    """Test that source parameter is saved in frontmatter"""
    # Arrange
    content = "Web article content"
    source = "https://example.com/article"
    
    # Act
    result = capture(content, source=source)
    
    # Assert
    with open(result.filepath, 'r') as f:
        file_content = f.read()
    
    assert f"source: {source}" in file_content
```

### Step 2: Minimal Implementation (GREEN Phase)

```python
# pkm/commands/capture.py
from datetime import datetime
from pathlib import Path
import yaml

class CaptureResult:
    def __init__(self, success, filepath=None, error=None):
        self.success = success
        self.filepath = filepath
        self.error = error

def capture(content, source=None):
    """
    Minimal implementation to make tests pass
    Focus on FRs only, ignore NFRs for now
    """
    # FR-001: Validate input
    if not content:
        return CaptureResult(
            success=False, 
            error="Content cannot be empty"
        )
    
    # FR-002: Generate timestamp filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}.md"
    filepath = Path(f"vault/0-inbox/quick-capture/{filename}")
    
    # Ensure directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # FR-003: Create frontmatter
    frontmatter = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'type': 'capture',
        'status': 'inbox',
        'tags': []
    }
    
    # FR-005: Add source if provided
    if source:
        frontmatter['source'] = source
    
    # Build file content
    file_content = "---\n"
    file_content += yaml.dump(frontmatter, default_flow_style=False)
    file_content += "---\n\n"
    file_content += content
    
    # FR-001: Write file
    filepath.write_text(file_content)
    
    # FR-004: Return result
    return CaptureResult(
        success=True,
        filepath=str(filepath)
    )
```

### Step 3: Refactor (REFACTOR Phase)

```python
# pkm/commands/capture.py (refactored)
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import yaml

class CaptureResult:
    """Result object for capture operations"""
    def __init__(self, success: bool, filepath: str = None, error: str = None):
        self.success = success
        self.filepath = filepath
        self.error = error
        self.timestamp = datetime.now()

class PKMCapture:
    """PKM Capture Command - TDD Implemented"""
    
    def __init__(self, inbox_path: str = "vault/0-inbox/quick-capture"):
        self.inbox_path = Path(inbox_path)
        self.inbox_path.mkdir(parents=True, exist_ok=True)
    
    def capture(self, 
                content: str, 
                source: Optional[str] = None,
                tags: Optional[List[str]] = None) -> CaptureResult:
        """
        Capture content to PKM inbox
        
        Functional Requirements (Implemented):
        - FR-001: Save to inbox ✓
        - FR-002: Unique timestamp ✓  
        - FR-003: YAML frontmatter ✓
        - FR-004: Return confirmation ✓
        - FR-005: Optional source ✓
        
        Non-Functional Requirements (Deferred):
        - NFR-001: <100ms response (Week 4)
        - NFR-002: Concurrent handling (Production)
        """
        # Validate input (FR-001)
        if not content or not content.strip():
            return CaptureResult(
                success=False,
                error="Content cannot be empty"
            )
        
        # Generate unique filename (FR-002)
        filepath = self._generate_filepath()
        
        # Create frontmatter (FR-003)
        frontmatter = self._create_frontmatter(source, tags)
        
        # Build and write content
        file_content = self._format_content(frontmatter, content)
        filepath.write_text(file_content)
        
        # Return result (FR-004)
        return CaptureResult(
            success=True,
            filepath=str(filepath)
        )
    
    def _generate_filepath(self) -> Path:
        """Generate unique timestamped filepath"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        filename = f"{timestamp}.md"
        return self.inbox_path / filename
    
    def _create_frontmatter(self, 
                          source: Optional[str] = None,
                          tags: Optional[List[str]] = None) -> dict:
        """Create YAML frontmatter metadata"""
        frontmatter = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'type': 'capture',
            'status': 'inbox',
            'tags': tags or [],
            'created': datetime.now().isoformat()
        }
        
        if source:
            frontmatter['source'] = source
            
        return frontmatter
    
    def _format_content(self, frontmatter: dict, content: str) -> str:
        """Format complete file content with frontmatter"""
        return f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n{content}\n"

# Module-level function for backward compatibility
_default_capture = PKMCapture()
capture = _default_capture.capture
```

## FR-First Priority Example

### What We Build (FRs - Week 1-2)
```python
# IMPLEMENT NOW - User-facing features
def capture(content, source=None):
    """Basic capture that works"""
    # Simple file creation
    # Basic frontmatter
    # Return success
    pass

def process_inbox():
    """Process inbox items"""
    # Read files
    # Categorize by PARA
    # Move to folders
    pass

def create_daily_note():
    """Create today's note"""
    # Generate from template
    # Add date
    # Open for editing
    pass
```

### What We Defer (NFRs - Week 3-4 or Later)
```python
# DEFER - Performance optimizations
async def capture_async(content):
    """Async version for performance"""
    pass  # DEFER until proven needed

# DEFER - Scalability
class CaptureQueue:
    """Handle high-volume captures"""
    pass  # DEFER until scale requires

# DEFER - Advanced security
def encrypt_capture(content):
    """Encrypt sensitive captures"""
    pass  # DEFER until security phase

# DEFER - Monitoring
class CaptureMetrics:
    """Track capture performance"""
    pass  # DEFER until production
```

## Decision Framework

```python
def should_implement_now(feature):
    """
    FR-First Decision Framework
    Returns: HIGH, MEDIUM, LOW priority
    """
    # HIGH - Implement immediately
    if feature.is_user_facing and feature.delivers_value:
        return "HIGH"
    
    # HIGH - Core functionality
    if feature.is_core_workflow:
        return "HIGH"
    
    # MEDIUM - Enables other features
    if feature.enables_other_features:
        return "MEDIUM"
    
    # LOW - Defer NFRs
    if feature.is_optimization:
        return "LOW"
    
    if feature.is_monitoring:
        return "LOW"
    
    if feature.is_scaling:
        return "LOW"
    
    # Default to deferring
    return "LOW"
```

## Real PKM Implementation Priority

### Week 1-2: Core Features (HIGH Priority FRs)
- ✅ Note capture
- ✅ Daily notes
- ✅ Basic search
- ✅ Folder organization
- ✅ Templates

### Week 3-4: Extended Features (MEDIUM Priority FRs)
- ✅ Auto-categorization
- ✅ Link suggestions
- ✅ Basic NLP extraction
- ✅ Tagging

### Week 5+: Optimizations (LOW Priority NFRs)
- ⏸️ Response time optimization
- ⏸️ Concurrent processing
- ⏸️ Advanced caching
- ⏸️ Performance monitoring
- ⏸️ High availability

## TDD Checklist for New Features

- [ ] **Spec written?** Complete specification with FRs and NFRs
- [ ] **Tests written?** All test cases defined before code
- [ ] **FRs identified?** User-facing features listed
- [ ] **NFRs deferred?** Performance/scale pushed to later
- [ ] **Tests failing?** RED phase confirmed
- [ ] **Minimal code?** Just enough to pass tests
- [ ] **Tests passing?** GREEN phase achieved
- [ ] **Code improved?** REFACTOR phase complete
- [ ] **Spec validated?** Implementation matches specification
- [ ] **Documentation?** User docs and code comments

---

*TDD and Specs-Driven Development - Build the right thing, the right way*
*Always: Spec → Test → Code → Refactor*
*Never: Code without tests, NFRs before FRs*