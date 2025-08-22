"""
TDD Cycle 4 - Advanced Migration Pipeline Tests
RED Phase: Comprehensive failing tests for architecture document migration

Tests for AdvancedMigrationPipeline class that processes critical architecture 
documents from docs/pkm-architecture/ with atomic extraction and quality gates.

Following TDD methodology: Write failing tests first, then implement to pass.
"""

import pytest
import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass
from typing import List, Dict, Any

# Import will fail initially - expected in TDD RED phase
try:
    from src.pkm.core.advanced_migration import (
        AdvancedMigrationPipeline, 
        ArchitectureMigrationResult,
        AtomicExtractionResult,
        QualityResult,
        CrossRefIndex
    )
    from src.pkm.processors.architecture_processor import ArchitectureDocumentProcessor
    from src.pkm.validators.migration_validator import MigrationQualityValidator
    from src.pkm.exceptions import ProcessingError
except ImportError:
    # Expected during RED phase - tests written before implementation
    AdvancedMigrationPipeline = None
    ArchitectureMigrationResult = None
    AtomicExtractionResult = None
    QualityResult = None
    CrossRefIndex = None
    ArchitectureDocumentProcessor = None
    MigrationQualityValidator = None
    ProcessingError = Exception


@dataclass
class MockArchitectureDocument:
    """Mock architecture document for testing"""
    filename: str
    content: str
    expected_atomic_notes: int
    expected_components: List[str]
    expected_patterns: List[str]


class TestAdvancedMigrationPipeline:
    """TDD Cycle 4 tests for advanced migration pipeline with architecture focus"""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            vault_dir = temp_path / "vault"
            docs_dir = temp_path / "docs"
            arch_dir = docs_dir / "pkm-architecture"
            
            # Create directory structure
            vault_dir.mkdir()
            docs_dir.mkdir()
            arch_dir.mkdir()
            (vault_dir / "02-projects" / "pkm-system" / "architecture").mkdir(parents=True)
            (vault_dir / "permanent" / "notes" / "concepts").mkdir(parents=True)
            
            yield {
                'temp': temp_path,
                'vault': vault_dir,
                'docs': docs_dir,
                'arch': arch_dir
            }

    @pytest.fixture
    def advanced_migration_pipeline(self, temp_dirs):
        """Fixture providing configured AdvancedMigrationPipeline"""
        if AdvancedMigrationPipeline is None:
            pytest.skip("AdvancedMigrationPipeline not implemented yet (TDD RED phase)")
        return AdvancedMigrationPipeline(vault_path=str(temp_dirs['vault']))

    @pytest.fixture
    def mock_architecture_documents(self, temp_dirs):
        """Create mock architecture documents for testing"""
        documents = [
            MockArchitectureDocument(
                filename="PKM-SYSTEM-SPECIFICATION.md",
                content="""---
title: PKM System Specification
type: specification
---

# PKM System Specification

## Core Components

### Data Ingestion Component
The data ingestion component handles all input sources including markdown files, web content, and structured data.

### Knowledge Extraction Framework  
The knowledge extraction framework applies NLP techniques to identify concepts, entities, and relationships.

### Storage Architecture
The storage architecture implements a medallion pattern with Bronze, Silver, and Gold layers.

## Design Patterns

### Lakehouse Pattern
Implementation of lakehouse architecture for unified batch and streaming processing.

### Event-Driven Architecture
Asynchronous processing using event-driven patterns for scalability.

## System Requirements

### Functional Requirements
- FR-001: System shall process markdown files with 99.9% accuracy
- FR-002: System shall extract atomic concepts from long documents
- FR-003: System shall maintain bidirectional links between concepts

### Non-Functional Requirements  
- NFR-001: System shall process 1000 documents per hour
- NFR-002: System shall maintain 99.9% uptime
""",
                expected_atomic_notes=8,
                expected_components=["Data Ingestion Component", "Knowledge Extraction Framework", "Storage Architecture"],
                expected_patterns=["Lakehouse Pattern", "Event-Driven Architecture"]
            ),
            MockArchitectureDocument(
                filename="PKM-SYSTEM-ARCHITECTURE.md", 
                content="""---
title: PKM System Architecture
type: architecture
---

# PKM System Architecture

## System Overview
The PKM system follows a three-tier architecture with presentation, business logic, and data tiers.

## Component Architecture

### Presentation Layer
- Web interface for user interaction
- CLI tools for automation
- API endpoints for integration

### Business Logic Layer  
- Capture service for content ingestion
- Processing service for NLP operations
- Synthesis service for knowledge generation

### Data Layer
- Document storage in S3-compatible systems
- Metadata storage in PostgreSQL  
- Vector embeddings in Lance format

## Integration Patterns

### Service Mesh Architecture
Microservices communicate through service mesh for reliability and observability.

### API Gateway Pattern
Single entry point for all client requests with authentication and rate limiting.
""",
                expected_atomic_notes=6,
                expected_components=["Presentation Layer", "Business Logic Layer", "Data Layer"],
                expected_patterns=["Service Mesh Architecture", "API Gateway Pattern"]
            ),
            MockArchitectureDocument(
                filename="KNOWLEDGE-EXTRACTION-FRAMEWORK.md",
                content="""---
title: Knowledge Extraction Framework
type: framework
---

# Knowledge Extraction Framework

## Extraction Pipeline

### Content Preprocessing
Text normalization, markdown parsing, metadata extraction from frontmatter.

### Concept Identification
Named entity recognition, concept extraction, relationship mapping using spaCy and transformers.

### Atomic Note Generation  
Automatic creation of atomic notes from identified concepts following Zettelkasten principles.

## Quality Metrics

### Extraction Accuracy
Target 95% accuracy for concept identification validated against manual annotation.

### Atomic Note Quality
Atomic notes should be self-contained, properly linked, and follow length constraints.
""",
                expected_atomic_notes=5,
                expected_components=["Content Preprocessing", "Concept Identification", "Atomic Note Generation"],
                expected_patterns=["Extraction Pipeline"]
            )
        ]
        
        # Write mock documents to temp directory
        for doc in documents:
            doc_path = temp_dirs['arch'] / doc.filename
            doc_path.write_text(doc.content, encoding='utf-8')
        
        return documents

    # ===============================================================================
    # CATEGORY A: BATCH ARCHITECTURE PROCESSING TESTS
    # ===============================================================================

    def test_migrates_entire_pkm_architecture_directory(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should migrate all architecture documents from docs/pkm-architecture/ to vault"""
        # Arrange
        source_dir = str(temp_dirs['arch'])
        expected_file_count = len(mock_architecture_documents)
        
        # Act
        result = advanced_migration_pipeline.migrate_architecture_directory(source_dir)
        
        # Assert
        assert result.success is True
        assert result.files_migrated == expected_file_count
        assert result.files_failed == 0
        assert result.overall_quality_score >= 0.85
        
        # Verify source directory is empty
        remaining_files = list(temp_dirs['arch'].glob("*.md"))
        assert len(remaining_files) == 0, f"Expected empty source directory, found {[f.name for f in remaining_files]}"
        
        # Verify files in vault
        vault_arch_files = list((temp_dirs['vault'] / "02-projects" / "pkm-system" / "architecture").glob("*.md"))
        assert len(vault_arch_files) == expected_file_count

    def test_preserves_document_relationships_during_migration(self, advanced_migration_pipeline, temp_dirs):
        """Should maintain cross-references between architecture documents"""
        # Arrange - Create documents with internal references
        doc_a_content = """# Document A
        This references [[Document B]] and [[Document C]] for implementation details.
        See also [[Storage Architecture]] for data persistence patterns.
        """
        
        doc_b_content = """# Document B  
        This document is referenced by [[Document A]] and provides details for [[Document C]].
        """
        
        (temp_dirs['arch'] / "document-a.md").write_text(doc_a_content)
        (temp_dirs['arch'] / "document-b.md").write_text(doc_b_content)
        
        # Act
        result = advanced_migration_pipeline.migrate_architecture_directory(str(temp_dirs['arch']))
        
        # Assert
        assert result.cross_references_maintained >= 4  # Number of [[]] references
        assert result.broken_references == 0
        
        # Verify cross-reference index was created
        cross_ref_index = advanced_migration_pipeline.get_cross_reference_index()
        assert len(cross_ref_index.references) >= 4

    def test_applies_architecture_specific_processing_rules(self, advanced_migration_pipeline, temp_dirs):
        """Should apply specialized processing for architecture documents"""
        # Arrange
        architecture_content = """# System Architecture
        ## Components
        - Database Layer: PostgreSQL for metadata
        - Storage Layer: S3 for document storage  
        - Processing Layer: Python services
        
        ## Patterns
        - Repository Pattern for data access
        - Factory Pattern for service creation
        - Observer Pattern for event handling
        """
        
        (temp_dirs['arch'] / "system-architecture.md").write_text(architecture_content)
        
        # Act  
        result = advanced_migration_pipeline.migrate_architecture_directory(str(temp_dirs['arch']))
        
        # Assert
        assert result.architecture_specific_processing is True
        assert result.components_identified >= 3
        assert result.patterns_identified >= 3
        assert result.component_relationships_mapped > 0

    # ===============================================================================
    # CATEGORY B: ATOMIC NOTE EXTRACTION FROM SPECIFICATIONS
    # ===============================================================================

    def test_extracts_atomic_concepts_from_system_specification(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should extract 8+ atomic notes from PKM-SYSTEM-SPECIFICATION.md"""
        # Arrange
        spec_doc = next(doc for doc in mock_architecture_documents if doc.filename == "PKM-SYSTEM-SPECIFICATION.md")
        spec_file_path = temp_dirs['arch'] / spec_doc.filename
        
        # Act
        result = advanced_migration_pipeline.extract_specification_atomics(str(spec_file_path))
        
        # Assert
        assert result.success is True
        assert len(result.atomic_notes) >= spec_doc.expected_atomic_notes
        assert all(note.type == "specification-concept" for note in result.atomic_notes)
        assert all(len(note.content) < 1000 for note in result.atomic_notes)  # Atomic size constraint
        assert all(note.source_document == spec_doc.filename for note in result.atomic_notes)
        
        # Verify atomic notes are properly formatted
        for note in result.atomic_notes:
            assert note.has_frontmatter is True
            assert note.has_unique_id is True
            assert len(note.title) > 0
            assert note.quality_score >= 0.7

    def test_creates_component_atomic_notes_from_architecture(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should identify and atomize system components from architecture docs"""
        # Arrange
        arch_doc = next(doc for doc in mock_architecture_documents if doc.filename == "PKM-SYSTEM-ARCHITECTURE.md")
        arch_file_path = temp_dirs['arch'] / arch_doc.filename
        
        # Act
        result = advanced_migration_pipeline.extract_architecture_components(str(arch_file_path))
        
        # Assert
        assert result.success is True
        assert len(result.component_atomic_notes) >= len(arch_doc.expected_components)
        
        # Verify each expected component was extracted
        extracted_component_titles = [note.title for note in result.component_atomic_notes]
        for expected_component in arch_doc.expected_components:
            assert any(expected_component in title for title in extracted_component_titles), \
                f"Expected component '{expected_component}' not found in extracted titles: {extracted_component_titles}"
        
        # Verify component notes have appropriate metadata
        for note in result.component_atomic_notes:
            assert note.type == "architecture-component"
            assert note.category == "system-architecture"
            assert len(note.relationships) > 0  # Components should relate to other components

    def test_extracts_design_patterns_as_atomic_concepts(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should identify architectural patterns and create atomic notes"""
        # Arrange
        spec_doc = next(doc for doc in mock_architecture_documents if doc.filename == "PKM-SYSTEM-SPECIFICATION.md")
        spec_file_path = temp_dirs['arch'] / spec_doc.filename
        
        # Act
        result = advanced_migration_pipeline.extract_design_patterns(str(spec_file_path))
        
        # Assert
        assert result.success is True
        assert len(result.pattern_atomic_notes) >= len(spec_doc.expected_patterns)
        
        # Verify pattern-specific metadata
        for pattern_note in result.pattern_atomic_notes:
            assert pattern_note.type == "design-pattern"
            assert pattern_note.has_implementation_details is True
            assert pattern_note.has_use_cases is True
            assert len(pattern_note.related_patterns) >= 0

    def test_creates_cross_reference_links_between_atomic_notes(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should create bidirectional links between related atomic concepts"""
        # Arrange
        source_dir = str(temp_dirs['arch'])
        
        # Act
        result = advanced_migration_pipeline.migrate_architecture_directory(source_dir)
        
        # Assert
        assert result.cross_references_created > 0
        
        # Verify atomic notes have bidirectional links
        atomic_notes = result.all_atomic_notes_created
        linked_notes = [note for note in atomic_notes if len(note.bidirectional_links) > 0]
        
        assert len(linked_notes) >= len(atomic_notes) * 0.8  # 80% of notes should be linked
        
        # Verify bidirectional consistency
        for note in linked_notes:
            for linked_note_id in note.bidirectional_links:
                linked_note = next((n for n in atomic_notes if n.id == linked_note_id), None)
                assert linked_note is not None
                assert note.id in linked_note.bidirectional_links, \
                    f"Bidirectional link missing: {note.id} links to {linked_note_id} but not vice versa"

    # ===============================================================================
    # CATEGORY C: QUALITY GATES AND VALIDATION
    # ===============================================================================

    def test_enforces_migration_quality_standards(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should enforce quality thresholds for technical document migration"""
        # Arrange
        source_dir = str(temp_dirs['arch'])
        quality_threshold = 0.85
        
        # Act
        result = advanced_migration_pipeline.migrate_architecture_directory(source_dir)
        
        # Assert
        assert result.meets_quality_threshold(quality_threshold) is True
        assert result.overall_quality_score >= quality_threshold
        
        # Detailed quality validation
        quality_result = advanced_migration_pipeline.validate_migration_quality(result)
        assert quality_result.frontmatter_completeness >= 0.98  # 98% have complete frontmatter
        assert quality_result.atomic_extraction_completeness >= 0.90  # 90% have atomic extraction
        assert quality_result.cross_reference_integrity >= 0.95  # 95% cross-references maintained
        assert quality_result.para_categorization_accuracy >= 0.98  # 98% correctly categorized

    def test_validates_frontmatter_completeness_for_architecture_docs(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should ensure all migrated docs have complete technical frontmatter"""
        # Arrange
        source_dir = str(temp_dirs['arch'])
        
        # Act
        result = advanced_migration_pipeline.migrate_architecture_directory(source_dir)
        
        # Assert
        migrated_files = result.migrated_files
        
        for migrated_file in migrated_files:
            file_content = Path(migrated_file.target_path).read_text(encoding='utf-8')
            
            # Verify frontmatter exists and is complete
            assert file_content.startswith('---'), f"Missing frontmatter in {migrated_file.filename}"
            
            frontmatter_lines = file_content.split('---')[1].strip().split('\n')
            frontmatter_dict = {}
            for line in frontmatter_lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter_dict[key.strip()] = value.strip()
            
            # Required frontmatter fields for architecture documents
            required_fields = ['title', 'type', 'date', 'tags', 'architecture_category', 'components', 'patterns']
            for field in required_fields:
                assert field in frontmatter_dict, f"Missing required field '{field}' in {migrated_file.filename}"
                assert len(frontmatter_dict[field]) > 0, f"Empty value for field '{field}' in {migrated_file.filename}"

    def test_creates_cross_reference_index_for_architecture_concepts(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should build comprehensive cross-reference index"""
        # Arrange
        source_dir = str(temp_dirs['arch'])
        
        # Act
        result = advanced_migration_pipeline.migrate_architecture_directory(source_dir)
        cross_ref_index = advanced_migration_pipeline.build_cross_reference_index(result.migrated_files)
        
        # Assert
        assert cross_ref_index is not None
        assert len(cross_ref_index.document_references) == len(mock_architecture_documents)
        assert len(cross_ref_index.concept_references) >= 20  # Should identify many concepts
        assert cross_ref_index.bidirectional_consistency_score >= 0.95
        
        # Verify index structure
        for doc_ref in cross_ref_index.document_references:
            assert doc_ref.source_document is not None
            assert doc_ref.target_document is not None
            assert len(doc_ref.referenced_concepts) > 0
            assert doc_ref.link_type in ['internal', 'concept', 'component', 'pattern']

    def test_validates_atomic_note_quality_distribution(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should ensure atomic notes meet quality distribution requirements"""
        # Arrange
        source_dir = str(temp_dirs['arch'])
        
        # Act
        result = advanced_migration_pipeline.migrate_architecture_directory(source_dir)
        
        # Assert - Quality distribution analysis
        atomic_notes = result.all_atomic_notes_created
        quality_scores = [note.quality_score for note in atomic_notes]
        
        # Quality distribution requirements
        assert len(quality_scores) >= 25, "Should create at least 25 atomic notes from architecture docs"
        assert sum(score >= 0.8 for score in quality_scores) / len(quality_scores) >= 0.7, \
            "At least 70% of atomic notes should have quality score ≥ 0.8"
        assert sum(score >= 0.9 for score in quality_scores) >= 5, \
            "At least 5 atomic notes should have quality score ≥ 0.9"
        assert all(score >= 0.5 for score in quality_scores), \
            "All atomic notes should have minimum quality score ≥ 0.5"

    # ===============================================================================
    # CATEGORY D: INTEGRATION AND ERROR HANDLING
    # ===============================================================================

    def test_integrates_with_existing_tdd_foundation(self, advanced_migration_pipeline, temp_dirs):
        """Should properly integrate with BasePkmProcessor and existing TDD foundation"""
        # Arrange
        test_content = "# Test Architecture\nThis is a test document for integration validation."
        test_file = temp_dirs['arch'] / "test-integration.md"
        test_file.write_text(test_content)
        
        # Act  
        result = advanced_migration_pipeline.migrate_architecture_directory(str(temp_dirs['arch']))
        
        # Assert - Verify integration with existing patterns
        assert hasattr(advanced_migration_pipeline, '_validate_non_empty_string')  # From BasePkmProcessor
        assert hasattr(advanced_migration_pipeline, '_write_markdown_file')  # From BasePkmProcessor
        assert hasattr(advanced_migration_pipeline, '_extract_frontmatter_and_content')  # From BasePkmProcessor
        
        # Verify PARA categorization (from TDD Cycle 2)
        migrated_file = result.migrated_files[0]
        assert "02-projects" in migrated_file.target_path  # Proper PARA categorization
        
        # Verify atomic note integration (from TDD Cycle 3)
        if len(result.all_atomic_notes_created) > 0:
            atomic_note = result.all_atomic_notes_created[0]
            assert hasattr(atomic_note, 'bidirectional_links')  # From TDD Cycle 3

    def test_handles_migration_errors_gracefully(self, advanced_migration_pipeline, temp_dirs):
        """Should handle various error conditions during migration"""
        # Arrange - Create problematic documents
        
        # Document with invalid YAML frontmatter
        invalid_yaml_doc = temp_dirs['arch'] / "invalid-yaml.md"
        invalid_yaml_doc.write_text("""---
title: "Unclosed quote
invalid: yaml: structure
---
# Content
""")
        
        # Document with no content
        empty_doc = temp_dirs['arch'] / "empty.md"
        empty_doc.write_text("")
        
        # Document with only frontmatter
        no_content_doc = temp_dirs['arch'] / "no-content.md"
        no_content_doc.write_text("---\ntitle: Only Frontmatter\n---")
        
        # Act
        result = advanced_migration_pipeline.migrate_architecture_directory(str(temp_dirs['arch']))
        
        # Assert - Should handle errors gracefully
        assert result.success is True  # Overall operation succeeds
        assert result.files_failed > 0  # Some files failed as expected
        assert result.files_migrated >= 0  # Some files may have succeeded
        assert len(result.error_details) > 0  # Error details recorded
        
        # Verify error handling doesn't crash the pipeline
        for error in result.error_details:
            assert error.error_type in ['invalid_yaml', 'empty_content', 'no_content', 'processing_error']
            assert error.filename is not None
            assert error.error_message is not None

    def test_validates_thread_safety_for_concurrent_migration(self, advanced_migration_pipeline, temp_dirs):
        """Should handle concurrent migration operations safely"""
        # Arrange
        import threading
        import time
        
        # Create multiple test documents
        for i in range(5):
            doc_content = f"# Architecture Document {i}\nThis is document {i} content."
            (temp_dirs['arch'] / f"concurrent-doc-{i}.md").write_text(doc_content)
        
        results = []
        
        def migrate_single_doc(doc_index):
            """Migrate a single document concurrently"""
            single_doc_dir = temp_dirs['temp'] / f"single_{doc_index}"
            single_doc_dir.mkdir()
            
            # Copy one document to isolated directory
            source_doc = temp_dirs['arch'] / f"concurrent-doc-{doc_index}.md"
            target_doc = single_doc_dir / source_doc.name
            target_doc.write_text(source_doc.read_text())
            
            # Migrate
            result = advanced_migration_pipeline.migrate_architecture_directory(str(single_doc_dir))
            results.append((doc_index, result))
        
        # Act - Run concurrent migrations
        threads = []
        for i in range(5):
            thread = threading.Thread(target=migrate_single_doc, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Assert - All migrations should succeed without conflicts
        assert len(results) == 5
        for doc_index, result in results:
            assert result.success is True, f"Migration failed for document {doc_index}"
            assert result.files_migrated == 1, f"Expected 1 file migrated for document {doc_index}"

    # ===============================================================================
    # CATEGORY E: PERFORMANCE AND SCALABILITY VALIDATION  
    # ===============================================================================

    def test_migration_performance_within_acceptable_limits(self, advanced_migration_pipeline, temp_dirs, mock_architecture_documents):
        """Should complete migration within performance thresholds"""
        import time
        
        # Arrange
        source_dir = str(temp_dirs['arch'])
        max_duration_seconds = 30  # Should complete within 30 seconds
        
        # Act
        start_time = time.time()
        result = advanced_migration_pipeline.migrate_architecture_directory(source_dir)
        end_time = time.time()
        
        migration_duration = end_time - start_time
        
        # Assert
        assert migration_duration < max_duration_seconds, \
            f"Migration took {migration_duration:.2f}s, expected < {max_duration_seconds}s"
        assert result.performance_metrics.total_duration == pytest.approx(migration_duration, abs=1.0)
        assert result.performance_metrics.documents_per_second >= 0.1  # At least 0.1 docs/second


# ===============================================================================
# ADDITIONAL TEST CLASSES FOR SPECIALIZED COMPONENTS
# ===============================================================================

class TestArchitectureDocumentProcessor:
    """Tests for specialized architecture document processing"""
    
    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            vault_dir = temp_path / "vault"
            vault_dir.mkdir()
            yield {'temp': temp_path, 'vault': vault_dir}
    
    @pytest.fixture
    def architecture_processor(self, temp_dirs):
        """Fixture providing ArchitectureDocumentProcessor"""
        if ArchitectureDocumentProcessor is None:
            pytest.skip("ArchitectureDocumentProcessor not implemented yet (TDD RED phase)")
        return ArchitectureDocumentProcessor(vault_path=str(temp_dirs['vault']))
    
    def test_identifies_system_components_from_architecture_text(self, architecture_processor):
        """Should identify system components from architecture descriptions"""
        # Arrange
        architecture_text = """
        The system consists of three main components:
        1. Data Ingestion Service - handles incoming data streams
        2. Processing Engine - applies NLP transformations
        3. Storage Layer - persists processed information
        
        Additional components include:
        - Authentication Service for security
        - Monitoring Service for observability
        """
        
        # Act
        components = architecture_processor.identify_system_components(architecture_text)
        
        # Assert
        assert len(components) >= 5
        component_names = [comp.name for comp in components]
        
        expected_components = [
            "Data Ingestion Service",
            "Processing Engine", 
            "Storage Layer",
            "Authentication Service",
            "Monitoring Service"
        ]
        
        for expected in expected_components:
            assert any(expected in name for name in component_names), \
                f"Expected component '{expected}' not found in {component_names}"

    def test_extracts_design_patterns_from_architecture_descriptions(self, architecture_processor):
        """Should identify architectural patterns from descriptions"""
        # Arrange
        pattern_text = """
        The architecture implements several key patterns:
        
        Repository Pattern: Data access abstraction for different storage backends
        Factory Pattern: Dynamic creation of processing components
        Observer Pattern: Event notification system for real-time updates  
        Singleton Pattern: Single instance of configuration manager
        Strategy Pattern: Pluggable algorithms for different content types
        """
        
        # Act
        patterns = architecture_processor.extract_design_patterns(pattern_text)
        
        # Assert
        assert len(patterns) >= 5
        pattern_names = [pattern.name for pattern in patterns]
        
        expected_patterns = [
            "Repository Pattern",
            "Factory Pattern",
            "Observer Pattern", 
            "Singleton Pattern",
            "Strategy Pattern"
        ]
        
        for expected in expected_patterns:
            assert any(expected in name for name in pattern_names), \
                f"Expected pattern '{expected}' not found in {pattern_names}"


class TestMigrationQualityValidator:
    """Tests for migration quality validation framework"""
    
    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            vault_dir = temp_path / "vault"
            vault_dir.mkdir()
            yield {'temp': temp_path, 'vault': vault_dir}
    
    @pytest.fixture 
    def quality_validator(self, temp_dirs):
        """Fixture providing MigrationQualityValidator"""
        if MigrationQualityValidator is None:
            pytest.skip("MigrationQualityValidator not implemented yet (TDD RED phase)")
        return MigrationQualityValidator(vault_path=str(temp_dirs['vault']))
    
    def test_validates_frontmatter_completeness_standards(self, quality_validator, temp_dirs):
        """Should validate frontmatter completeness against defined standards"""
        # Arrange
        complete_doc = temp_dirs['vault'] / "complete.md"
        complete_doc.write_text("""---
title: Complete Document
type: architecture
date: 2024-08-22
tags: [architecture, system]
architecture_category: core
components: [service-a, service-b]
patterns: [repository, factory]
---
# Content
""")
        
        incomplete_doc = temp_dirs['vault'] / "incomplete.md" 
        incomplete_doc.write_text("""---
title: Incomplete Document
---
# Content
""")
        
        # Act
        completeness_result = quality_validator.validate_frontmatter_completeness([complete_doc, incomplete_doc])
        
        # Assert
        assert completeness_result.total_documents == 2
        assert completeness_result.complete_documents == 1
        assert completeness_result.incomplete_documents == 1
        assert completeness_result.completeness_percentage == 0.5
        assert len(completeness_result.missing_fields_by_document) == 1

    def test_calculates_migration_quality_scores_accurately(self, quality_validator, temp_dirs):
        """Should calculate accurate quality scores for migration results"""
        # Arrange - Create mock migration result
        mock_migration_result = MagicMock()
        mock_migration_result.files_migrated = 10
        mock_migration_result.files_failed = 1  
        mock_migration_result.atomic_notes_created = 25
        mock_migration_result.cross_references_maintained = 45
        mock_migration_result.broken_references = 2
        
        # Act
        quality_score = quality_validator.calculate_migration_quality_score(mock_migration_result)
        
        # Assert
        assert 0.0 <= quality_score <= 1.0  # Score should be between 0 and 1
        assert quality_score >= 0.7, "Quality score should be reasonably high for good migration result"


# ===============================================================================
# INTEGRATION TESTS WITH REAL ARCHITECTURE DOCUMENTS
# ===============================================================================

class TestRealArchitectureDocumentMigration:
    """Integration tests using real architecture documents from docs/pkm-architecture/"""
    
    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            vault_dir = temp_path / "vault"
            vault_dir.mkdir()
            yield {'temp': temp_path, 'vault': vault_dir}
    
    @pytest.fixture
    def advanced_migration_pipeline(self, temp_dirs):
        """Fixture providing configured AdvancedMigrationPipeline"""
        if AdvancedMigrationPipeline is None:
            pytest.skip("AdvancedMigrationPipeline not implemented yet (TDD RED phase)")
        return AdvancedMigrationPipeline(vault_path=str(temp_dirs['vault']))
    
    @pytest.fixture
    def real_docs_available(self):
        """Check if real docs/pkm-architecture/ directory exists"""
        real_arch_dir = Path("docs/pkm-architecture/")
        if not real_arch_dir.exists():
            pytest.skip("Real docs/pkm-architecture/ directory not available")
        
        real_docs = list(real_arch_dir.glob("*.md"))
        if len(real_docs) == 0:
            pytest.skip("No markdown files in docs/pkm-architecture/")
            
        return real_arch_dir, real_docs
    
    def test_processes_real_pkm_system_specification(self, advanced_migration_pipeline, real_docs_available):
        """Should successfully process the real PKM-SYSTEM-SPECIFICATION.md file"""
        # Arrange
        real_arch_dir, real_docs = real_docs_available
        
        spec_file = real_arch_dir / "PKM-SYSTEM-SPECIFICATION.md"
        if not spec_file.exists():
            pytest.skip("PKM-SYSTEM-SPECIFICATION.md not found in docs/pkm-architecture/")
        
        # Act
        result = advanced_migration_pipeline.extract_specification_atomics(str(spec_file))
        
        # Assert
        assert result.success is True
        assert len(result.atomic_notes) >= 8, "Should extract at least 8 atomic concepts from real specification"
        assert result.overall_quality_score >= 0.7, "Real document processing should meet quality standards"
        
        # Verify atomic notes are meaningful
        for atomic_note in result.atomic_notes:
            assert len(atomic_note.content.strip()) >= 100, "Atomic notes should have substantial content"
            assert len(atomic_note.title.strip()) >= 10, "Atomic notes should have descriptive titles"


# These tests should ALL FAIL initially (TDD RED phase)
# Implementation comes next (GREEN phase)  
# Then refactoring for optimization (REFACTOR phase)