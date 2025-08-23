# Compound Engineering Tasks: PKM System Implementation

## Task Overview

This document provides detailed task breakdowns for PKM system implementation following **compound engineering principles**, where complex systems are built through systematic decomposition, parallel development, and orchestration via Claude Code.

## Workstream Organization

### Parallel Development Strategy
```yaml
workstreams:
  WS-A: "Primitives (Level 1) - Foundation Components"
  WS-B: "Retrieval (Level 2+3) - Search and Discovery"
  WS-C: "Content (Level 2+3) - Generation and Publishing"
  WS-D: "Orchestration (Level 4) - Claude Code Integration"

timeline:
  weeks_1_2: [WS-A]
  weeks_3_4: [WS-B, WS-C] # parallel after WS-A completion
  weeks_5_6: [WS-B, WS-C] # continued parallel
  weeks_7_8: [WS-D] # integrates all previous workstreams
```

---

## Workstream A: Foundation Components (Weeks 1-2)

### WS-A-001: VaultManager Implementation
**Priority**: 🔴 Critical  
**Effort**: 12 hours  
**Dependencies**: None  
**Workstream**: A (Foundation)  
**Level**: 1 (Primitive)  

#### Description
Implement the foundational VaultManager component that provides file system abstraction for the PKM vault. This component serves as the primary interface between the system and the file system.

#### Interface Definition
```python
# interfaces/vault_interface.py - DEFINE FIRST
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Note:
    path: str
    title: str
    content: str
    frontmatter: dict
    links: List[str]
    created: datetime
    modified: datetime

class VaultInterface(ABC):
    @abstractmethod
    def read_note(self, path: str) -> Note:
        """Read a note from the vault"""
        pass
    
    @abstractmethod
    def write_note(self, note: Note) -> bool:
        """Write a note to the vault"""
        pass
    
    @abstractmethod
    def list_notes(self, folder: str = "") -> List[str]:
        """List all notes in a folder"""
        pass
    
    @abstractmethod
    def delete_note(self, path: str) -> bool:
        """Delete a note from the vault"""
        pass
    
    @abstractmethod
    def note_exists(self, path: str) -> bool:
        """Check if a note exists"""
        pass
```

#### TDD Implementation
```python
# tests/unit/test_vault_manager.py - WRITE FIRST
import pytest
from pathlib import Path
from vault.vault_manager import VaultManager
from interfaces.vault_interface import Note

def test_vault_manager_reads_existing_note():
    vault = VaultManager("test_vault")
    note = vault.read_note("test-note.md")
    assert note.title == "Test Note"
    assert note.content is not None
    assert isinstance(note.frontmatter, dict)

def test_vault_manager_writes_new_note():
    vault = VaultManager("test_vault")
    note = Note(
        path="new-note.md",
        title="New Note",
        content="This is a test note.",
        frontmatter={"tags": ["test"]},
        links=[],
        created=datetime.now(),
        modified=datetime.now()
    )
    result = vault.write_note(note)
    assert result is True
    assert vault.note_exists("new-note.md")

def test_vault_manager_lists_notes_in_folder():
    vault = VaultManager("test_vault")
    notes = vault.list_notes("02-projects")
    assert len(notes) > 0
    assert all(note.endswith(".md") for note in notes)

def test_vault_manager_deletes_note():
    vault = VaultManager("test_vault")
    # Create test note first
    test_note = Note(path="delete-me.md", title="Delete Me", content="Test")
    vault.write_note(test_note)
    
    # Delete and verify
    result = vault.delete_note("delete-me.md")
    assert result is True
    assert not vault.note_exists("delete-me.md")

def test_vault_manager_handles_missing_note():
    vault = VaultManager("test_vault")
    with pytest.raises(FileNotFoundError):
        vault.read_note("nonexistent.md")
```

#### Acceptance Criteria
- [ ] VaultManager implements VaultInterface completely
- [ ] All CRUD operations work correctly
- [ ] Proper error handling for missing files
- [ ] Path validation and security checks
- [ ] Performance: <10ms for typical operations
- [ ] 100% test coverage with TDD approach

---

### WS-A-002: MarkdownParser Implementation
**Priority**: 🔴 Critical  
**Effort**: 8 hours  
**Dependencies**: None  
**Workstream**: A (Foundation)  
**Level**: 1 (Primitive)  

#### Description
Implement markdown parsing and metadata extraction component that processes note content and extracts frontmatter, links, and structure.

#### Interface Definition
```python
# interfaces/parser_interface.py - DEFINE FIRST
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ParsedContent:
    frontmatter: Dict[str, Any]
    content: str
    links: List[str]
    headings: List[str]
    tags: List[str]
    word_count: int

class ParserInterface(ABC):
    @abstractmethod
    def parse(self, content: str) -> ParsedContent:
        """Parse markdown content and extract metadata"""
        pass
    
    @abstractmethod
    def extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter"""
        pass
    
    @abstractmethod
    def extract_links(self, content: str) -> List[str]:
        """Extract all [[wikilinks]]"""
        pass
    
    @abstractmethod
    def extract_tags(self, content: str) -> List[str]:
        """Extract #tags from content"""
        pass
```

#### TDD Implementation
```python
# tests/unit/test_markdown_parser.py - WRITE FIRST
def test_parser_extracts_frontmatter():
    parser = MarkdownParser()
    content = """---
title: Test Note
tags: [test, sample]
date: 2024-01-01
---
# Test Content"""
    
    result = parser.parse(content)
    assert result.frontmatter["title"] == "Test Note"
    assert result.frontmatter["tags"] == ["test", "sample"]
    assert result.frontmatter["date"] == "2024-01-01"

def test_parser_extracts_wikilinks():
    parser = MarkdownParser()
    content = "This links to [[other-note]] and [[another-note]]."
    
    result = parser.parse(content)
    assert "other-note" in result.links
    assert "another-note" in result.links
    assert len(result.links) == 2

def test_parser_extracts_tags_from_content():
    parser = MarkdownParser()
    content = "This is a note about #machine-learning and #ai."
    
    result = parser.parse(content)
    assert "machine-learning" in result.tags
    assert "ai" in result.tags

def test_parser_extracts_headings():
    parser = MarkdownParser()
    content = """# Main Title
## Section 1
### Subsection
## Section 2"""
    
    result = parser.parse(content)
    expected_headings = ["Main Title", "Section 1", "Subsection", "Section 2"]
    assert result.headings == expected_headings

def test_parser_counts_words():
    parser = MarkdownParser()
    content = "This is a test with exactly seven words."
    
    result = parser.parse(content)
    assert result.word_count == 7
```

#### Acceptance Criteria
- [ ] MarkdownParser implements ParserInterface completely
- [ ] YAML frontmatter parsing with error handling
- [ ] Wikilink extraction with proper regex
- [ ] Tag extraction from content
- [ ] Heading hierarchy extraction
- [ ] Word count calculation
- [ ] Performance: <5ms for typical notes
- [ ] 100% test coverage with TDD approach

---

### WS-A-003: IndexManager Implementation
**Priority**: 🔴 Critical  
**Effort**: 16 hours  
**Dependencies**: WS-A-001, WS-A-002  
**Workstream**: A (Foundation)  
**Level**: 1 (Primitive)  

#### Description
Implement search indexing and metadata management component that builds and maintains indices for content search, tag lookup, and link graphs.

#### Interface Definition
```python
# interfaces/index_interface.py - DEFINE FIRST
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    path: str
    title: str
    relevance_score: float
    snippet: str
    metadata: Dict[str, Any]

class IndexInterface(ABC):
    @abstractmethod
    def build_content_index(self) -> bool:
        """Build full-text search index"""
        pass
    
    @abstractmethod
    def build_metadata_index(self) -> bool:
        """Build metadata search index"""
        pass
    
    @abstractmethod
    def search_content(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search content with relevance scoring"""
        pass
    
    @abstractmethod
    def search_metadata(self, **filters) -> List[SearchResult]:
        """Search by metadata filters"""
        pass
    
    @abstractmethod
    def update_note_index(self, path: str) -> bool:
        """Update index for single note"""
        pass
```

#### TDD Implementation
```python
# tests/unit/test_index_manager.py - WRITE FIRST
def test_index_manager_builds_content_index():
    vault = MockVaultManager()
    parser = MockMarkdownParser()
    index = IndexManager(vault, parser)
    
    result = index.build_content_index()
    assert result is True
    
    # Test search functionality
    results = index.search_content("machine learning")
    assert len(results) > 0
    assert all(r.relevance_score > 0 for r in results)

def test_index_manager_searches_content_with_relevance():
    vault = MockVaultManager()
    parser = MockMarkdownParser()
    index = IndexManager(vault, parser)
    index.build_content_index()
    
    results = index.search_content("artificial intelligence", limit=5)
    assert len(results) <= 5
    # Results should be sorted by relevance
    for i in range(len(results) - 1):
        assert results[i].relevance_score >= results[i + 1].relevance_score

def test_index_manager_builds_metadata_index():
    vault = MockVaultManager()
    parser = MockMarkdownParser()
    index = IndexManager(vault, parser)
    
    result = index.build_metadata_index()
    assert result is True
    
    # Test metadata search
    results = index.search_metadata(tag="research")
    assert len(results) > 0
    assert all("research" in r.metadata.get("tags", []) for r in results)

def test_index_manager_updates_single_note():
    vault = MockVaultManager()
    parser = MockMarkdownParser()
    index = IndexManager(vault, parser)
    index.build_content_index()
    
    # Update index for specific note
    result = index.update_note_index("test-note.md")
    assert result is True
    
    # Verify note is searchable
    results = index.search_content("updated content")
    assert len(results) > 0

def test_index_manager_handles_malformed_content():
    vault = MockVaultManager()
    parser = MockMarkdownParser()
    index = IndexManager(vault, parser)
    
    # Should handle parsing errors gracefully
    result = index.build_content_index()
    assert result is True  # Should complete even with errors
```

#### Acceptance Criteria
- [ ] IndexManager implements IndexInterface completely
- [ ] Full-text search with TF-IDF scoring
- [ ] Metadata indexing with flexible filters
- [ ] Incremental index updates
- [ ] Search result ranking and snippets
- [ ] Error handling for malformed content
- [ ] Performance: <100ms for typical searches
- [ ] 100% test coverage with TDD approach

---

## Workstream B: Retrieval Engine and Agent (Weeks 3-6)

### WS-B-001: RetrievalEngine Implementation
**Priority**: 🔴 Critical  
**Effort**: 20 hours  
**Dependencies**: WS-A (all foundation components)  
**Workstream**: B (Retrieval)  
**Level**: 2 (Engine)  

#### Description
Implement the core retrieval engine that provides search, get, and links functionality. This engine composes the foundation components to deliver high-level retrieval operations.

#### Interface Definition
```python
# interfaces/retrieval_interface.py - DEFINE FIRST
from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any
from dataclasses import dataclass

@dataclass
class SearchResult:
    path: str
    title: str
    relevance_score: float
    snippet: str
    metadata: Dict[str, Any]
    links: List[str]

@dataclass
class LinkResult:
    source_note: str
    related_notes: List[str]
    connection_strength: List[float]
    link_types: List[str]  # ["direct", "bidirectional", "semantic"]

class RetrievalInterface(ABC):
    @abstractmethod
    def search(self, query: str, method: str = "hybrid", limit: int = 10) -> List[SearchResult]:
        """Search notes using specified method"""
        pass
    
    @abstractmethod
    def get(self, identifier: str, type: str = "auto") -> Union[Note, List[Note]]:
        """Retrieve specific notes or collections"""
        pass
    
    @abstractmethod
    def links(self, note_id: str, operation: str = "related", depth: int = 2) -> LinkResult:
        """Discover and analyze note relationships"""
        pass
```

#### TDD Implementation
```python
# tests/unit/test_retrieval_engine.py - WRITE FIRST
def test_retrieval_engine_hybrid_search():
    vault = MockVaultManager()
    index = MockIndexManager()
    parser = MockMarkdownParser()
    engine = RetrievalEngine(vault, index, parser)
    
    results = engine.search("machine learning", method="hybrid", limit=5)
    assert len(results) <= 5
    assert all(r.relevance_score > 0 for r in results)
    assert all(r.snippet is not None for r in results)

def test_retrieval_engine_get_by_id():
    vault = MockVaultManager()
    index = MockIndexManager()
    parser = MockMarkdownParser()
    engine = RetrievalEngine(vault, index, parser)
    
    note = engine.get("note-123", type="id")
    assert note.path == "note-123"
    assert note.content is not None

def test_retrieval_engine_get_by_tag():
    vault = MockVaultManager()
    index = MockIndexManager()
    parser = MockMarkdownParser()
    engine = RetrievalEngine(vault, index, parser)
    
    notes = engine.get("research", type="tag")
    assert isinstance(notes, list)
    assert len(notes) > 0
    assert all("research" in note.frontmatter.get("tags", []) for note in notes)

def test_retrieval_engine_discovers_links():
    vault = MockVaultManager()
    index = MockIndexManager()
    parser = MockMarkdownParser()
    engine = RetrievalEngine(vault, index, parser)
    
    result = engine.links("blockchain-note", operation="related", depth=2)
    assert result.source_note == "blockchain-note"
    assert len(result.related_notes) > 0
    assert len(result.connection_strength) == len(result.related_notes)

def test_retrieval_engine_suggests_new_links():
    vault = MockVaultManager()
    index = MockIndexManager()
    parser = MockMarkdownParser()
    engine = RetrievalEngine(vault, index, parser)
    
    result = engine.links("isolated-note", operation="suggest", depth=1)
    assert result.source_note == "isolated-note"
    assert len(result.related_notes) > 0
    # Suggestions should have lower confidence than direct links
    assert all(0 < strength < 0.8 for strength in result.connection_strength)
```

#### Acceptance Criteria
- [ ] RetrievalEngine implements RetrievalInterface completely
- [ ] Hybrid search combining content and metadata
- [ ] Multiple get operations (by ID, tag, type, date range)
- [ ] Link discovery with relationship analysis
- [ ] Link suggestion for connecting isolated notes
- [ ] Performance: <100ms for searches, <50ms for gets
- [ ] 100% test coverage with TDD approach

---

### WS-B-002: PkmRetrievalAgent Implementation
**Priority**: 🔴 Critical  
**Effort**: 16 hours  
**Dependencies**: WS-B-001  
**Workstream**: B (Retrieval)  
**Level**: 3 (Agent)  

#### Description
Implement the PKM retrieval agent that orchestrates retrieval operations and provides a natural language interface. This agent manages the user interaction layer for retrieval operations.

#### Interface Definition
```python
# interfaces/agent_interface.py - DEFINE FIRST
from abc import ABC, abstractmethod
from typing import Dict, Any

class AgentInterface(ABC):
    @abstractmethod
    def handle_command(self, command: str, parameters: Dict[str, Any] = None) -> str:
        """Process a command and return response"""
        pass
    
    @abstractmethod
    def parse_intent(self, natural_language: str) -> Dict[str, Any]:
        """Parse natural language into structured intent"""
        pass
    
    @abstractmethod
    def format_response(self, data: Any, format: str = "default") -> str:
        """Format response data for user presentation"""
        pass
```

#### TDD Implementation
```python
# tests/unit/test_pkm_retrieval_agent.py - WRITE FIRST
def test_retrieval_agent_handles_search_command():
    retrieval_engine = MockRetrievalEngine()
    agent = PkmRetrievalAgent(retrieval_engine)
    
    response = agent.handle_command("/pkm-search machine learning --limit=5")
    assert "Found 5 results" in response
    assert "machine learning" in response.lower()
    assert "relevance" in response.lower()

def test_retrieval_agent_handles_get_command():
    retrieval_engine = MockRetrievalEngine()
    agent = PkmRetrievalAgent(retrieval_engine)
    
    response = agent.handle_command("/pkm-get note-123 --format=summary")
    assert "note-123" in response
    assert len(response) < 500  # summary format should be concise

def test_retrieval_agent_handles_links_command():
    retrieval_engine = MockRetrievalEngine()
    agent = PkmRetrievalAgent(retrieval_engine)
    
    response = agent.handle_command("/pkm-links blockchain-note --operation=related")
    assert "blockchain-note" in response
    assert "related notes" in response.lower()
    assert "connections" in response.lower()

def test_retrieval_agent_parses_natural_language():
    retrieval_engine = MockRetrievalEngine()
    agent = PkmRetrievalAgent(retrieval_engine)
    
    intent = agent.parse_intent("Find notes about artificial intelligence from last month")
    assert intent["operation"] == "search"
    assert "artificial intelligence" in intent["query"]
    assert intent["date_filter"] is not None

def test_retrieval_agent_formats_response():
    retrieval_engine = MockRetrievalEngine()
    agent = PkmRetrievalAgent(retrieval_engine)
    
    mock_results = [MockSearchResult("test-note", 0.95, "Test snippet")]
    response = agent.format_response(mock_results, format="detailed")
    assert "test-note" in response
    assert "0.95" in response  # relevance score
    assert "Test snippet" in response
```

#### Acceptance Criteria
- [ ] PkmRetrievalAgent implements AgentInterface completely
- [ ] Command parsing for /pkm-search, /pkm-get, /pkm-links
- [ ] Natural language intent parsing
- [ ] Multiple response formats (summary, detailed, json)
- [ ] Error handling with user-friendly messages
- [ ] Performance: <10ms overhead beyond engine operations
- [ ] 100% test coverage with TDD approach

---

## Workstream C: Content Engine and Agent (Weeks 3-6)

### WS-C-001: ContentEngine Implementation
**Priority**: 🔴 Critical  
**Effort**: 24 hours  
**Dependencies**: WS-A (foundation), WS-B-001 (retrieval engine)  
**Workstream**: C (Content)  
**Level**: 2 (Engine)  

#### Description
Implement the content generation engine that transforms PKM knowledge into various content formats with audience adaptation. This engine leverages retrieval capabilities to gather knowledge and synthesis capabilities to create content.

#### Interface Definition
```python
# interfaces/content_interface.py - DEFINE FIRST
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Content:
    title: str
    content: str
    format: str
    audience: str
    word_count: int
    sources: List[str]
    metadata: Dict[str, Any]
    quality_score: float

@dataclass
class ContentOutline:
    title: str
    sections: List[str]
    format: str
    estimated_length: int
    target_audience: str

class ContentInterface(ABC):
    @abstractmethod
    def generate_content(self, topic: str, audience: str, format: str, 
                        sources: List[str] = None) -> Content:
        """Generate content for specific topic, audience, and format"""
        pass
    
    @abstractmethod
    def create_outline(self, topic: str, format: str, depth: str = "medium") -> ContentOutline:
        """Create structured outline for content"""
        pass
    
    @abstractmethod
    def adapt_for_audience(self, content: str, target_audience: str) -> str:
        """Adapt content complexity and style for audience"""
        pass
    
    @abstractmethod
    def publish_content(self, content: Content, platform: str) -> bool:
        """Prepare content for publishing platform"""
        pass
```

#### TDD Implementation
```python
# tests/unit/test_content_engine.py - WRITE FIRST
def test_content_engine_generates_blog_post():
    vault = MockVaultManager()
    retrieval = MockRetrievalEngine()
    synthesizer = MockSynthesizerAgent()
    feynman = MockFeynmanAgent()
    engine = ContentEngine(vault, retrieval, synthesizer, feynman)
    
    content = engine.generate_content("machine learning", "students", "blog_post")
    assert content.format == "blog_post"
    assert content.audience == "students"
    assert content.word_count >= 800  # typical blog post length
    assert content.quality_score > 0.7
    assert len(content.sources) > 0

def test_content_engine_creates_outline():
    vault = MockVaultManager()
    retrieval = MockRetrievalEngine()
    synthesizer = MockSynthesizerAgent()
    feynman = MockFeynmanAgent()
    engine = ContentEngine(vault, retrieval, synthesizer, feynman)
    
    outline = engine.create_outline("blockchain technology", "tutorial", "comprehensive")
    assert outline.title is not None
    assert len(outline.sections) >= 5  # comprehensive should have many sections
    assert outline.format == "tutorial"
    assert outline.estimated_length > 0

def test_content_engine_adapts_for_audience():
    vault = MockVaultManager()
    retrieval = MockRetrievalEngine()
    synthesizer = MockSynthesizerAgent()
    feynman = MockFeynmanAgent()
    engine = ContentEngine(vault, retrieval, synthesizer, feynman)
    
    expert_content = "Neural networks utilize backpropagation algorithms..."
    adapted = engine.adapt_for_audience(expert_content, "beginner")
    assert adapted != expert_content  # content should change
    assert len(adapted.split()) >= len(expert_content.split())  # more explanation

def test_content_engine_publishes_content():
    vault = MockVaultManager()
    retrieval = MockRetrievalEngine()
    synthesizer = MockSynthesizerAgent()
    feynman = MockFeynmanAgent()
    engine = ContentEngine(vault, retrieval, synthesizer, feynman)
    
    content = Content(
        title="Test Post",
        content="Test content",
        format="blog_post",
        audience="general",
        word_count=100,
        sources=["source1.md"],
        metadata={},
        quality_score=0.8
    )
    
    result = engine.publish_content(content, "blog")
    assert result is True
```

#### Acceptance Criteria
- [ ] ContentEngine implements ContentInterface completely
- [ ] Content generation for multiple formats (blog, academic, tutorial, social)
- [ ] Audience adaptation with complexity adjustment
- [ ] Content outlining with configurable depth
- [ ] Publishing preparation for multiple platforms
- [ ] Quality scoring and validation
- [ ] Performance: <5 minutes for blog posts, <30 minutes for papers
- [ ] 100% test coverage with TDD approach

---

### WS-C-002: PkmContentAgent Implementation
**Priority**: 🔴 Critical  
**Effort**: 20 hours  
**Dependencies**: WS-C-001  
**Workstream**: C (Content)  
**Level**: 3 (Agent)  

#### Description
Implement the PKM content agent that orchestrates content creation workflows and provides natural language interface for content generation commands.

#### TDD Implementation
```python
# tests/unit/test_pkm_content_agent.py - WRITE FIRST
def test_content_agent_creates_content():
    content_engine = MockContentEngine()
    retrieval_engine = MockRetrievalEngine()
    agent = PkmContentAgent(content_engine, retrieval_engine)
    
    response = agent.handle_command("/content-create AI --audience=students --format=tutorial")
    assert "tutorial" in response.lower()
    assert "created successfully" in response
    assert "students" in response

def test_content_agent_adapts_existing_content():
    content_engine = MockContentEngine()
    retrieval_engine = MockRetrievalEngine()
    agent = PkmContentAgent(content_engine, retrieval_engine)
    
    response = agent.handle_command("/content-adapt research-paper.md --audience=general")
    assert "adapted for general audience" in response
    assert "research-paper.md" in response

def test_content_agent_creates_outline():
    content_engine = MockContentEngine()
    retrieval_engine = MockRetrievalEngine()
    agent = PkmContentAgent(content_engine, retrieval_engine)
    
    response = agent.handle_command("/content-outline blockchain --format=course --depth=comprehensive")
    assert "outline created" in response.lower()
    assert "blockchain" in response
    assert "course" in response

def test_content_agent_publishes_content():
    content_engine = MockContentEngine()
    retrieval_engine = MockRetrievalEngine()
    agent = PkmContentAgent(content_engine, retrieval_engine)
    
    response = agent.handle_command("/content-publish tutorial.md --platform=blog --publish=true")
    assert "published successfully" in response
    assert "blog" in response

def test_content_agent_parses_natural_language():
    content_engine = MockContentEngine()
    retrieval_engine = MockRetrievalEngine()
    agent = PkmContentAgent(content_engine, retrieval_engine)
    
    intent = agent.parse_intent("Create a beginner-friendly tutorial about machine learning")
    assert intent["operation"] == "create"
    assert intent["topic"] == "machine learning"
    assert intent["audience"] == "beginner"
    assert intent["format"] == "tutorial"
```

#### Acceptance Criteria
- [ ] PkmContentAgent implements AgentInterface completely
- [ ] Command parsing for all content creation commands
- [ ] Natural language intent parsing for content requests
- [ ] Integration with existing synthesis and feynman agents
- [ ] Multiple output formats and response styles
- [ ] Error handling with actionable feedback
- [ ] Performance: <20ms overhead beyond engine operations
- [ ] 100% test coverage with TDD approach

---

## Workstream D: Claude Code Orchestration (Weeks 7-8)

### WS-D-001: Command Router Implementation
**Priority**: 🔴 Critical  
**Effort**: 16 hours  
**Dependencies**: WS-B-002, WS-C-002  
**Workstream**: D (Orchestration)  
**Level**: 4 (Orchestration)  

#### Description
Implement the command router that parses user intent, dispatches to appropriate agents, and coordinates multi-agent workflows through Claude Code integration.

#### Interface Definition
```python
# interfaces/router_interface.py - DEFINE FIRST
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class Intent:
    command: str
    agent: str
    parameters: Dict[str, Any]
    confidence: float
    context: Dict[str, Any]

@dataclass
class WorkflowStep:
    agent: str
    command: str
    parameters: Dict[str, Any]
    dependencies: List[str]

class RouterInterface(ABC):
    @abstractmethod
    def parse_intent(self, user_input: str) -> Intent:
        """Parse natural language into structured intent"""
        pass
    
    @abstractmethod
    def route_command(self, intent: Intent) -> str:
        """Route command to appropriate agent"""
        pass
    
    @abstractmethod
    def orchestrate_workflow(self, workflow: List[WorkflowStep]) -> Dict[str, Any]:
        """Coordinate multi-agent workflow"""
        pass
```

#### TDD Implementation
```python
# tests/unit/test_command_router.py - WRITE FIRST
def test_router_parses_search_intent():
    retrieval_agent = MockRetrievalAgent()
    content_agent = MockContentAgent()
    router = CommandRouter({"retrieval": retrieval_agent, "content": content_agent})
    
    intent = router.parse_intent("Search for machine learning papers")
    assert intent.command == "search"
    assert intent.agent == "retrieval"
    assert "machine learning papers" in intent.parameters["query"]
    assert intent.confidence > 0.8

def test_router_routes_to_correct_agent():
    retrieval_agent = MockRetrievalAgent()
    content_agent = MockContentAgent()
    router = CommandRouter({"retrieval": retrieval_agent, "content": content_agent})
    
    intent = Intent(
        command="search",
        agent="retrieval",
        parameters={"query": "machine learning"},
        confidence=0.95,
        context={}
    )
    
    response = router.route_command(intent)
    assert response is not None
    assert retrieval_agent.handle_command.called

def test_router_orchestrates_multi_agent_workflow():
    retrieval_agent = MockRetrievalAgent()
    content_agent = MockContentAgent()
    router = CommandRouter({"retrieval": retrieval_agent, "content": content_agent})
    
    workflow = [
        WorkflowStep("retrieval", "search", {"query": "AI"}, []),
        WorkflowStep("content", "create", {"topic": "AI", "format": "tutorial"}, ["step_1"])
    ]
    
    result = router.orchestrate_workflow(workflow)
    assert result["status"] == "completed"
    assert result["steps_completed"] == 2
    assert result["final_output"] is not None

def test_router_handles_ambiguous_intent():
    retrieval_agent = MockRetrievalAgent()
    content_agent = MockContentAgent()
    router = CommandRouter({"retrieval": retrieval_agent, "content": content_agent})
    
    intent = router.parse_intent("create something about AI")
    assert intent.confidence < 0.7  # should be low confidence
    assert "clarification" in intent.context
```

#### Acceptance Criteria
- [ ] CommandRouter implements RouterInterface completely
- [ ] Natural language intent parsing with confidence scoring
- [ ] Command routing to appropriate agents
- [ ] Multi-agent workflow orchestration
- [ ] Context management across workflow steps
- [ ] Error handling and fallback strategies
- [ ] Performance: <50ms for routing, <5s for workflows
- [ ] 100% test coverage with TDD approach

---

### WS-D-002: Claude Code Integration
**Priority**: 🔴 Critical  
**Effort**: 20 hours  
**Dependencies**: WS-D-001  
**Workstream**: D (Orchestration)  
**Level**: 4 (Orchestration)  

#### Description
Implement the Claude Code integration layer that provides natural language interface to the PKM system and manages complex multi-agent workflows.

#### TDD Implementation
```python
# tests/integration/test_claude_code_integration.py - WRITE FIRST
def test_claude_code_processes_search_command():
    system = PkmSystem()  # Fully integrated system
    
    response = system.process_claude_command("/pkm-search machine learning --limit=5")
    assert "Found 5 results" in response
    assert "machine learning" in response.lower()
    assert response.count("•") == 5  # 5 bullet points for results

def test_claude_code_processes_content_creation():
    system = PkmSystem()
    
    response = system.process_claude_command("/content-create AI --audience=students --format=tutorial")
    assert "tutorial created" in response.lower()
    assert "AI" in response
    assert "students" in response
    assert "vault/06-synthesis" in response  # saved location

def test_claude_code_handles_multi_step_workflow():
    system = PkmSystem()
    
    response = system.process_natural_language(
        "Search for blockchain research and create a beginner tutorial from the findings"
    )
    assert "search completed" in response.lower()
    assert "tutorial created" in response.lower()
    assert "blockchain" in response
    assert "beginner" in response

def test_claude_code_provides_contextual_help():
    system = PkmSystem()
    
    response = system.process_claude_command("/help content-create")
    assert "/content-create" in response
    assert "audience" in response
    assert "format" in response
    assert "examples:" in response.lower()

def test_claude_code_handles_errors_gracefully():
    system = PkmSystem()
    
    response = system.process_claude_command("/pkm-search nonexistent-topic --limit=100")
    assert "no results found" in response.lower()
    assert "try" in response.lower()  # suggestions provided
```

#### Acceptance Criteria
- [ ] Claude Code commands processed correctly
- [ ] Natural language workflow processing
- [ ] Context-aware help and documentation
- [ ] Error handling with helpful suggestions
- [ ] Response formatting for user clarity
- [ ] Integration with all agents and engines
- [ ] Performance: <1s for simple commands, <10s for workflows
- [ ] 100% test coverage with TDD approach

---

## Integration Testing Strategy

### Component Integration Tests
```python
# tests/integration/test_component_integration.py
def test_vault_manager_integrates_with_index_manager():
    """Test that VaultManager and IndexManager work together"""
    vault = VaultManager("test_vault")
    parser = MarkdownParser()
    index = IndexManager(vault, parser)
    
    # Add a note through VaultManager
    note = Note(path="integration-test.md", title="Integration Test", content="Test content")
    vault.write_note(note)
    
    # Index should find the new note
    index.update_note_index("integration-test.md")
    results = index.search_content("Test content")
    assert len(results) > 0
    assert "integration-test.md" in [r.path for r in results]

def test_retrieval_engine_integrates_with_content_engine():
    """Test that RetrievalEngine provides data to ContentEngine"""
    vault = VaultManager("test_vault")
    index = IndexManager(vault, MarkdownParser())
    retrieval = RetrievalEngine(vault, index, MarkdownParser())
    content = ContentEngine(vault, retrieval, MockSynthesizer(), MockFeynman())
    
    # Content engine should use retrieval engine for source material
    generated_content = content.generate_content("test topic", "students", "blog_post")
    assert len(generated_content.sources) > 0
    # Sources should be valid paths found by retrieval engine
    for source in generated_content.sources:
        assert vault.note_exists(source)
```

### End-to-End Workflow Tests
```python
# tests/e2e/test_complete_workflows.py
def test_complete_research_to_content_workflow():
    """Test full workflow from research to published content"""
    system = PkmSystem()
    
    # 1. Research phase: search for existing knowledge
    search_response = system.process_claude_command("/pkm-search machine learning")
    assert "Found" in search_response
    
    # 2. Content creation phase: generate tutorial from research
    create_response = system.process_claude_command(
        "/content-create machine-learning --audience=students --format=tutorial --sources=auto"
    )
    assert "tutorial created" in create_response.lower()
    
    # 3. Publishing phase: prepare for blog
    publish_response = system.process_claude_command(
        "/content-publish machine-learning-tutorial.md --platform=blog"
    )
    assert "ready for publishing" in publish_response.lower()
    
    # 4. Verify content exists in vault
    vault = VaultManager("test_vault")
    assert vault.note_exists("machine-learning-tutorial.md")

def test_complete_knowledge_discovery_workflow():
    """Test knowledge discovery and insight generation"""
    system = PkmSystem()
    
    # Natural language workflow
    response = system.process_natural_language(
        "Explore connections between blockchain and cryptocurrency, then create insights summary"
    )
    
    assert "connections found" in response.lower()
    assert "insights generated" in response.lower()
    assert "summary created" in response.lower()
    
    # Verify outputs exist
    vault = VaultManager("test_vault")
    assert vault.note_exists("blockchain-cryptocurrency-insights.md")
```

## Success Metrics for Compound Engineering

### Development Efficiency Metrics
```yaml
development_metrics:
  parallel_development:
    target: ">70% of work done in parallel"
    measurement: "workstream overlap percentage"
  
  integration_efficiency:
    target: "<5% time spent on integration issues"
    measurement: "integration bugs / total development time"
  
  component_reuse:
    target: ">80% of components used by multiple agents"
    measurement: "component dependency graph analysis"
  
  interface_compliance:
    target: "100% interface adherence"
    measurement: "automated interface compliance tests"
```

### System Performance Metrics
```yaml
performance_metrics:
  component_performance:
    vault_operations: "<10ms"
    parsing_operations: "<5ms"
    indexing_operations: "<100ms"
    search_operations: "<100ms"
  
  agent_performance:
    retrieval_agent: "<150ms total"
    content_agent: "<5s for blog posts"
    command_routing: "<50ms"
  
  end_to_end_performance:
    simple_commands: "<1s"
    complex_workflows: "<10s"
    content_generation: "<5 minutes"
```

### Quality Metrics
```yaml
quality_metrics:
  test_coverage:
    unit_tests: ">95%"
    integration_tests: ">90%"
    e2e_tests: ">80%"
  
  interface_stability:
    breaking_changes: "0 per release"
    backward_compatibility: "100%"
  
  error_handling:
    graceful_degradation: ">99%"
    user_friendly_errors: ">95%"
```

---

**Compound Engineering Implementation Status**: ✅ **Ready for Parallel Development**  
**Total Tasks**: 8 major components across 4 workstreams  
**Implementation Approach**: Interface-first TDD with parallel workstreams  
**Integration Strategy**: Systematic composition with Claude Code orchestration  
**Success Framework**: Comprehensive metrics for development efficiency, performance, and quality

This compound engineering approach transforms PKM system development from a monolithic challenge into systematic, parallel development of independently testable components that compose into sophisticated capabilities through Claude Code's natural language orchestration layer.