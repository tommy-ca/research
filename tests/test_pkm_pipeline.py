#!/usr/bin/env python3
"""
Test Suite for PKM Processing Pipeline

Following TDD principles from CLAUDE.md - tests written first to define
expected behavior, then implementation follows.

Tests cover:
1. Inbox processing and parsing
2. Concept extraction accuracy
3. Atomic note generation
4. Link discovery and bidirectional linking
5. PARA categorization logic
6. Tag generation and hierarchy
7. Knowledge graph indexing
8. End-to-end pipeline integration
"""

import pytest
import tempfile
import shutil
import json
import yaml
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

# Import the PKM pipeline components
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from pkm.pipeline_architecture import (
    PkmItem, AtomicNote, InboxProcessor, ConceptExtractor,
    AtomicNoteGenerator, LinkDiscoveryEngine, ParaCategorizer,
    TagGenerator, KnowledgeGraphIndexer, PkmPipeline
)

class TestPkmItem:
    """Test PKM item data structure"""
    
    def test_pkm_item_creation(self):
        """Test creating a PKM item with required fields"""
        item = PkmItem(
            file_path=Path("/test/item.md"),
            title="Test Item",
            content="Test content",
            frontmatter={'date': '2025-09-02'},
            created_date=datetime.now()
        )
        
        assert item.title == "Test Item"
        assert item.content == "Test content"
        assert isinstance(item.tags, set)
        assert isinstance(item.links, set)
        assert isinstance(item.concepts, list)

class TestInboxProcessor:
    """Test inbox processing functionality"""
    
    @pytest.fixture
    def temp_vault(self):
        """Create temporary vault structure for testing"""
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir)
        inbox_path = vault_path / "00-inbox"
        inbox_path.mkdir(parents=True)
        
        # Create test markdown file
        test_content = """---
date: 2025-09-02
type: capture
tags: [crypto, lakehouse]
status: captured
---

# Test Crypto Research

This is test content about **blockchain** and **data lakes**.

## Key Findings

- Apache Iceberg is better than Delta Lake
- Real-time processing has trade-offs
- [[related-note]] should be linked

## Technical Details

The system uses Kafka for streaming and Spark for processing.
"""
        
        test_file = inbox_path / "test-research.md"
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        yield vault_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_get_inbox_items(self, temp_vault):
        """Test retrieving items from inbox directory"""
        processor = InboxProcessor(temp_vault)
        items = processor.get_inbox_items()
        
        assert len(items) == 1
        assert items[0].title == "Test Crypto Research"
        assert "blockchain" in items[0].content
        assert "crypto" in items[0].tags
        assert "related-note" in items[0].links
    
    def test_parse_markdown_file(self, temp_vault):
        """Test parsing markdown with frontmatter"""
        processor = InboxProcessor(temp_vault)
        test_file = temp_vault / "00-inbox" / "test-research.md"
        
        item = processor._parse_markdown_file(test_file)
        
        assert item.title == "Test Crypto Research"
        assert item.frontmatter['type'] == 'capture'
        assert 'crypto' in item.tags
        assert 'lakehouse' in item.tags
        assert len(item.links) == 1
        assert 'related-note' in item.links
    
    def test_extract_title_from_content(self, temp_vault):
        """Test extracting title from markdown headers"""
        processor = InboxProcessor(temp_vault)
        
        content = "# Main Title\n\nSome content here"
        title = processor._extract_title_from_content(content)
        
        assert title == "Main Title"
    
    def test_extract_links(self, temp_vault):
        """Test extracting wiki-style links"""
        processor = InboxProcessor(temp_vault)
        
        content = "See [[first-link]] and [[second-link]] for more info."
        links = processor._extract_links(content)
        
        assert len(links) == 2
        assert "first-link" in links
        assert "second-link" in links

class TestConceptExtractor:
    """Test concept extraction functionality"""
    
    @pytest.fixture
    def sample_item(self):
        """Create sample PKM item for testing"""
        return PkmItem(
            file_path=Path("/test/crypto-research.md"),
            title="Crypto Lakehouse Analysis",
            content="""
            # Apache Iceberg vs Delta Lake Comparison
            
            This analysis covers blockchain data processing using modern
            data lakehouse architectures. Key technologies include:
            
            - Apache Kafka for streaming
            - Apache Spark for batch processing  
            - Real-time analytics with low latency
            - ACID transactions for data integrity
            
            ## DeFi Protocol Integration
            
            Decentralized Finance (DeFi) protocols require special handling.
            Smart contracts generate high-frequency event data.
            """,
            frontmatter={'tags': ['crypto', 'architecture']},
            created_date=datetime.now()
        )
    
    def test_extract_crypto_concepts(self, sample_item):
        """Test extraction of crypto-specific terms"""
        extractor = ConceptExtractor()
        processed_item = extractor.process(sample_item)
        
        # Should extract crypto domain terms
        assert 'blockchain' in processed_item.concepts
        assert 'defi' in processed_item.concepts
        assert 'smart contract' in processed_item.concepts
    
    def test_extract_technical_concepts(self, sample_item):
        """Test extraction of technical terms and acronyms"""
        extractor = ConceptExtractor()
        processed_item = extractor.process(sample_item)
        
        # Should extract technical terms
        assert 'kafka' in processed_item.concepts
        assert 'spark' in processed_item.concepts
        
        # Should extract proper nouns
        concepts_str = ' '.join(processed_item.concepts)
        assert 'Apache' in concepts_str or 'Iceberg' in concepts_str
    
    def test_extract_header_concepts(self, sample_item):
        """Test extraction of concepts from headers"""
        extractor = ConceptExtractor()
        processed_item = extractor.process(sample_item)
        
        # Should extract concepts from headers - check actual extracted concepts
        concepts = processed_item.concepts
        assert 'defi' in concepts
        assert any('Apache' in c for c in concepts)  # Apache Kafka, Apache Iceberg, etc.
        assert 'Protocol Integration' in concepts

class TestAtomicNoteGenerator:
    """Test atomic note generation"""
    
    @pytest.fixture
    def temp_vault_with_permanent(self):
        """Create vault with permanent notes directory"""
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir)
        permanent_path = vault_path / "permanent" / "notes"
        permanent_path.mkdir(parents=True)
        
        yield vault_path
        
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_item_with_concepts(self):
        """Sample item with extracted concepts"""
        return PkmItem(
            file_path=Path("/test/research.md"),
            title="Test Research",
            content="Apache Kafka is a distributed streaming platform...",
            frontmatter={},
            created_date=datetime.now(),
            concepts=['kafka', 'streaming', 'distributed systems']
        )
    
    def test_create_atomic_note(self, temp_vault_with_permanent, sample_item_with_concepts):
        """Test creating atomic note for a concept"""
        generator = AtomicNoteGenerator(temp_vault_with_permanent)
        
        atomic_note = generator._create_atomic_note('kafka', sample_item_with_concepts)
        
        assert atomic_note is not None
        assert 'Kafka' in atomic_note.title
        assert 'kafka' in atomic_note.tags
        assert len(atomic_note.source_files) == 1
    
    def test_atomic_note_file_creation(self, temp_vault_with_permanent, sample_item_with_concepts):
        """Test that atomic note files are actually created"""
        generator = AtomicNoteGenerator(temp_vault_with_permanent)
        
        generator._create_atomic_note('streaming', sample_item_with_concepts)
        
        # Check that file was created
        permanent_path = temp_vault_with_permanent / "permanent" / "notes"
        note_files = list(permanent_path.glob("*-streaming.md"))
        assert len(note_files) == 1
        
        # Check file content
        with open(note_files[0], 'r') as f:
            content = f.read()
        
        assert '# Streaming' in content
        assert 'Apache Kafka' in content  # Content extraction
        assert 'Sources' in content
    
    def test_process_generates_atomic_notes(self, temp_vault_with_permanent, sample_item_with_concepts):
        """Test that processing generates atomic notes"""
        generator = AtomicNoteGenerator(temp_vault_with_permanent)
        
        processed_item = generator.process(sample_item_with_concepts)
        
        # Should have references to created atomic notes
        assert 'atomic_notes' in processed_item.frontmatter
        assert len(processed_item.frontmatter['atomic_notes']) > 0

class TestLinkDiscoveryEngine:
    """Test link discovery functionality"""
    
    @pytest.fixture
    def temp_vault_with_notes(self):
        """Create vault with existing notes for linking"""
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir)
        permanent_path = vault_path / "permanent" / "notes"
        permanent_path.mkdir(parents=True)
        
        # Create existing notes
        existing_notes = [
            "kafka-streaming-fundamentals.md",
            "apache-spark-processing.md",
            "blockchain-data-analysis.md"
        ]
        
        for note in existing_notes:
            note_path = permanent_path / note
            with open(note_path, 'w') as f:
                f.write(f"# {note.replace('.md', '').replace('-', ' ').title()}")
        
        yield vault_path
        
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_item_for_linking(self):
        """Sample item that should link to existing notes"""
        return PkmItem(
            file_path=Path("/test/new-research.md"),
            title="New Research",
            content="""
            This research builds on Kafka streaming concepts and 
            Apache Spark processing capabilities. The blockchain
            data requires special handling.
            """,
            frontmatter={},
            created_date=datetime.now()
        )
    
    def test_get_existing_notes(self, temp_vault_with_notes):
        """Test retrieving list of existing notes"""
        engine = LinkDiscoveryEngine(temp_vault_with_notes)
        notes = engine._get_existing_notes()
        
        assert len(notes) == 3
        assert "kafka-streaming-fundamentals" in notes
        assert "apache-spark-processing" in notes
        assert "blockchain-data-analysis" in notes
    
    def test_find_potential_links(self, temp_vault_with_notes, sample_item_for_linking):
        """Test finding potential links based on content"""
        engine = LinkDiscoveryEngine(temp_vault_with_notes)
        existing_notes = engine._get_existing_notes()
        
        potential_links = engine._find_potential_links(sample_item_for_linking, existing_notes)
        
        # Should find links based on content keywords
        assert "kafka-streaming-fundamentals" in potential_links
        assert "apache-spark-processing" in potential_links
        assert "blockchain-data-analysis" in potential_links
    
    def test_process_adds_links(self, temp_vault_with_notes, sample_item_for_linking):
        """Test that processing adds discovered links"""
        engine = LinkDiscoveryEngine(temp_vault_with_notes)
        
        processed_item = engine.process(sample_item_for_linking)
        
        assert len(processed_item.links) > 0
        # Should contain at least one discovered link
        link_found = any('kafka' in link or 'spark' in link or 'blockchain' in link 
                        for link in processed_item.links)
        assert link_found

class TestParaCategorizer:
    """Test PARA method categorization"""
    
    def test_project_categorization(self):
        """Test identification of project content"""
        categorizer = ParaCategorizer()
        
        project_item = PkmItem(
            file_path=Path("/test/project.md"),
            title="Implement Crypto Analytics Dashboard",
            content="""
            # Project Plan: Crypto Analytics Dashboard
            
            ## Deliverables
            - Design user interface mockups
            - Implement real-time data pipeline  
            - Build dashboard components
            - Create deployment roadmap
            
            Timeline: 8 weeks with milestone reviews.
            """,
            frontmatter={},
            created_date=datetime.now()
        )
        
        processed_item = categorizer.process(project_item)
        assert processed_item.para_category == 'project'
    
    def test_area_categorization(self):
        """Test identification of area content"""
        categorizer = ParaCategorizer()
        
        area_item = PkmItem(
            file_path=Path("/test/area.md"),
            title="Data Governance Standards",
            content="""
            # Data Governance Policy
            
            This document defines ongoing responsibilities for:
            - Data quality monitoring and maintenance
            - Compliance with regulatory standards
            - Security policy enforcement
            - Standard operating procedures
            
            These processes require continuous monitoring.
            """,
            frontmatter={},
            created_date=datetime.now()
        )
        
        processed_item = categorizer.process(area_item)
        assert processed_item.para_category == 'area'
    
    def test_resource_categorization(self):
        """Test identification of resource content"""
        categorizer = ParaCategorizer()
        
        resource_item = PkmItem(
            file_path=Path("/test/resource.md"),
            title="Apache Kafka Documentation",
            content="""
            # Kafka Reference Guide
            
            This documentation covers:
            - Configuration examples
            - API reference materials
            - Troubleshooting guide
            - Best practices framework
            
            Use this as a reference for implementation.
            """,
            frontmatter={},
            created_date=datetime.now()
        )
        
        processed_item = categorizer.process(resource_item)
        assert processed_item.para_category == 'resource'
    
    def test_archive_categorization(self):
        """Test identification of archived content"""
        categorizer = ParaCategorizer()
        
        archive_item = PkmItem(
            file_path=Path("/test/archive.md"),
            title="Completed Project Review",
            content="Project completed successfully...",
            frontmatter={'status': 'completed'},
            created_date=datetime.now()
        )
        
        processed_item = categorizer.process(archive_item)
        assert processed_item.para_category == 'archive'

class TestTagGenerator:
    """Test tag generation functionality"""
    
    def test_hierarchical_tag_generation(self):
        """Test generation of hierarchical tags"""
        generator = TagGenerator()
        
        crypto_item = PkmItem(
            file_path=Path("/test/crypto.md"),
            title="DeFi Analysis",
            content="""
            Analysis of Bitcoin and Ethereum DeFi protocols.
            Using Kafka for data processing and Databricks
            for analytics on blockchain transaction data.
            """,
            frontmatter={},
            created_date=datetime.now(),
            concepts=['defi', 'bitcoin', 'ethereum', 'kafka']
        )
        
        processed_item = generator.process(crypto_item)
        
        # Should generate parent tags
        assert 'crypto' in processed_item.tags
        assert 'data' in processed_item.tags
        assert 'technology' in processed_item.tags
        
        # Should generate child tags
        assert 'bitcoin' in processed_item.tags
        assert 'ethereum' in processed_item.tags
        assert 'defi' in processed_item.tags
        assert 'kafka' in processed_item.tags
    
    def test_concept_based_tag_generation(self):
        """Test tag generation from concepts"""
        generator = TagGenerator()
        
        item_with_concepts = PkmItem(
            file_path=Path("/test/concepts.md"),
            title="Technical Analysis",
            content="Technical content...",
            frontmatter={},
            created_date=datetime.now(),
            concepts=['real-time processing', 'batch analytics', 'data pipeline']
        )
        
        processed_item = generator.process(item_with_concepts)
        
        # Should convert concepts to tags
        assert 'real-time-processing' in processed_item.tags
        assert 'batch-analytics' in processed_item.tags
        assert 'data-pipeline' in processed_item.tags

class TestKnowledgeGraphIndexer:
    """Test knowledge graph indexing"""
    
    @pytest.fixture
    def temp_vault_for_indexing(self):
        """Create vault with indexing directory"""
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir)
        index_path = vault_path / ".pkm" / "indexes"
        index_path.mkdir(parents=True)
        
        yield vault_path
        
        shutil.rmtree(temp_dir)
    
    def test_update_concept_index(self, temp_vault_for_indexing):
        """Test updating concept index"""
        indexer = KnowledgeGraphIndexer(temp_vault_for_indexing)
        
        test_item = PkmItem(
            file_path=Path("/test/item.md"),
            title="Test Item",
            content="Test content",
            frontmatter={},
            created_date=datetime.now(),
            concepts=['kafka', 'streaming', 'data-processing']
        )
        
        indexer._update_concept_index(test_item)
        
        # Check that concept index was created
        concept_index_path = temp_vault_for_indexing / ".pkm" / "indexes" / "concepts.json"
        assert concept_index_path.exists()
        
        with open(concept_index_path, 'r') as f:
            concept_index = json.load(f)
        
        assert 'kafka' in concept_index
        assert 'item' in concept_index['kafka']
    
    def test_update_tag_index(self, temp_vault_for_indexing):
        """Test updating tag index"""
        indexer = KnowledgeGraphIndexer(temp_vault_for_indexing)
        
        test_item = PkmItem(
            file_path=Path("/test/tagged-item.md"),
            title="Tagged Item",
            content="Content",
            frontmatter={},
            created_date=datetime.now(),
            tags={'crypto', 'blockchain', 'analysis'}
        )
        
        indexer._update_tag_index(test_item)
        
        # Check tag index
        tag_index_path = temp_vault_for_indexing / ".pkm" / "indexes" / "tags.json"
        assert tag_index_path.exists()
        
        with open(tag_index_path, 'r') as f:
            tag_index = json.load(f)
        
        assert 'crypto' in tag_index
        assert 'tagged-item' in tag_index['crypto']
    
    def test_update_link_index(self, temp_vault_for_indexing):
        """Test updating bidirectional link index"""
        indexer = KnowledgeGraphIndexer(temp_vault_for_indexing)
        
        test_item = PkmItem(
            file_path=Path("/test/linked-item.md"),
            title="Linked Item", 
            content="Content",
            frontmatter={},
            created_date=datetime.now(),
            links={'target-note', 'another-note'}
        )
        
        indexer._update_link_index(test_item)
        
        # Check link index
        link_index_path = temp_vault_for_indexing / ".pkm" / "indexes" / "links.json"
        assert link_index_path.exists()
        
        with open(link_index_path, 'r') as f:
            link_index = json.load(f)
        
        # Should have outgoing links
        assert 'linked-item' in link_index
        assert 'target-note' in link_index['linked-item']['outgoing']
        
        # Should create incoming links for targets
        assert 'target-note' in link_index
        assert 'linked-item' in link_index['target-note']['incoming']

class TestPkmPipelineIntegration:
    """Test end-to-end pipeline integration"""
    
    @pytest.fixture
    def complete_test_vault(self):
        """Create complete vault structure for integration testing"""
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir)
        
        # Create directory structure
        (vault_path / "00-inbox").mkdir(parents=True)
        (vault_path / "02-projects").mkdir(parents=True)
        (vault_path / "03-areas").mkdir(parents=True)
        (vault_path / "04-resources").mkdir(parents=True)
        (vault_path / "05-archives").mkdir(parents=True)
        (vault_path / "permanent" / "notes").mkdir(parents=True)
        
        # Create test research files
        crypto_research = """---
date: 2025-09-02
type: capture
tags: [crypto, research]
status: captured
---

# Crypto Lakehouse Solutions Analysis

This comprehensive analysis covers modern data lakehouse architectures
for cryptocurrency data processing.

## Key Technologies

- **Apache Iceberg**: Table format with ACID transactions
- **Apache Kafka**: Distributed streaming platform
- **Apache Spark**: Unified analytics engine
- **Delta Lake**: Open-source storage framework

## Vendor Analysis

Leading vendors include Databricks, Snowflake, and emerging
Web3-native solutions like Hyperline.

## Implementation Patterns

Real-time streaming architectures require careful consideration
of latency vs throughput trade-offs.
"""
        
        (vault_path / "00-inbox" / "crypto-lakehouse-research.md").write_text(crypto_research)
        
        yield vault_path
        
        shutil.rmtree(temp_dir)
    
    def test_complete_pipeline_processing(self, complete_test_vault):
        """Test complete pipeline from inbox to processed notes"""
        pipeline = PkmPipeline(complete_test_vault)
        
        # Process inbox
        processed_items = pipeline.process_inbox()
        
        # Should have processed items
        assert len(processed_items) == 1
        item = processed_items[0]
        
        # Should have extracted concepts
        assert len(item.concepts) > 0
        
        # Should have generated tags
        assert len(item.tags) > 2  # Original + generated
        
        # Should have assigned PARA category
        assert item.para_category in ['project', 'area', 'resource', 'archive']
        
        # Should have updated frontmatter
        assert item.frontmatter['processed'] == True
        assert 'processed_date' in item.frontmatter
        assert 'concepts' in item.frontmatter
    
    def test_atomic_notes_created(self, complete_test_vault):
        """Test that atomic notes are created during processing"""
        pipeline = PkmPipeline(complete_test_vault)
        
        # Process inbox
        pipeline.process_inbox()
        
        # Check for created atomic notes
        permanent_path = complete_test_vault / "permanent" / "notes"
        atomic_notes = list(permanent_path.glob("*.md"))
        
        # Should have created at least some atomic notes
        assert len(atomic_notes) > 0
        
        # Check atomic note content
        first_note = atomic_notes[0]
        with open(first_note, 'r') as f:
            content = f.read()
        
        assert content.startswith('---')  # Has frontmatter
        assert '# ' in content  # Has title
        assert 'Sources' in content  # Has source reference
    
    def test_indexes_updated(self, complete_test_vault):
        """Test that knowledge graph indexes are updated"""
        pipeline = PkmPipeline(complete_test_vault)
        
        # Process inbox
        pipeline.process_inbox()
        
        # Check for created indexes
        index_path = complete_test_vault / ".pkm" / "indexes"
        
        concepts_index = index_path / "concepts.json"
        tags_index = index_path / "tags.json" 
        links_index = index_path / "links.json"
        
        assert concepts_index.exists()
        assert tags_index.exists()
        assert links_index.exists()
        
        # Check index content
        with open(concepts_index, 'r') as f:
            concepts = json.load(f)
        
        assert len(concepts) > 0  # Should have indexed concepts

# Performance and edge case tests
class TestPipelinePerformance:
    """Test pipeline performance and edge cases"""
    
    def test_empty_inbox_handling(self):
        """Test handling of empty inbox"""
        with tempfile.TemporaryDirectory() as temp_dir:
            vault_path = Path(temp_dir)
            (vault_path / "00-inbox").mkdir(parents=True)
            
            pipeline = PkmPipeline(vault_path)
            items = pipeline.process_inbox()
            
            assert len(items) == 0
    
    def test_malformed_markdown_handling(self):
        """Test handling of malformed markdown files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            vault_path = Path(temp_dir)
            inbox_path = vault_path / "00-inbox"
            inbox_path.mkdir(parents=True)
            
            # Create malformed file
            malformed_file = inbox_path / "malformed.md"
            malformed_file.write_text("---\nbroken yaml: [invalid\n---\n# Content")
            
            processor = InboxProcessor(vault_path)
            items = processor.get_inbox_items()
            
            # Should handle gracefully
            assert len(items) == 1  # Should still process
            assert items[0].frontmatter == {}  # Empty frontmatter for malformed
    
    def test_large_content_processing(self):
        """Test processing of large content files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            vault_path = Path(temp_dir)
            inbox_path = vault_path / "00-inbox"
            inbox_path.mkdir(parents=True)
            
            # Create large content file
            large_content = "# Large File\n\n" + "Large content paragraph. " * 1000
            large_file = inbox_path / "large.md"
            large_file.write_text(large_content)
            
            processor = InboxProcessor(vault_path)
            items = processor.get_inbox_items()
            
            assert len(items) == 1
            assert len(items[0].content) > 10000  # Should handle large files

if __name__ == "__main__":
    pytest.main([__file__, "-v"])