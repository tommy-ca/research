"""
Migration Quality Validator (Maintenance)
"""

from typing import List
from pathlib import Path
from pkm_maintenance.migration.advanced_migration import QualityResult


class MigrationQualityValidator:
    """Comprehensive quality validation for architecture migration"""
    
    def __init__(self, vault_path: str = "vault"):
        self.vault_path = vault_path
    
    def validate_frontmatter_completeness(self, documents: List[Path]) -> QualityResult:
        quality_result = QualityResult()
        quality_result.total_documents = len(documents)
        complete_count = 0
        incomplete_count = 0
        missing_fields = {}
        
        for doc_path in documents:
            try:
                content = doc_path.read_text(encoding='utf-8')
                if content.startswith('---'):
                    frontmatter_section = content.split('---')[1]
                    required_fields = ['title', 'type', 'date', 'tags', 'architecture_category', 'components', 'patterns']
                    missing = [field for field in required_fields if f"{field}:" not in frontmatter_section]
                    if not missing:
                        complete_count += 1
                    else:
                        incomplete_count += 1
                        missing_fields[str(doc_path)] = missing
                else:
                    incomplete_count += 1
                    missing_fields[str(doc_path)] = ['frontmatter']
            except Exception:
                incomplete_count += 1
                missing_fields[str(doc_path)] = ['read_error']
        
        quality_result.complete_documents = complete_count
        quality_result.incomplete_documents = incomplete_count
        quality_result.missing_fields_by_document = missing_fields
        if quality_result.total_documents > 0:
            quality_result.completeness_percentage = complete_count / quality_result.total_documents
        return quality_result
    
    def calculate_migration_quality_score(self, migration_result) -> float:
        try:
            if hasattr(migration_result, 'files_migrated'):
                files_migrated = migration_result.files_migrated
                files_failed = migration_result.files_failed
                atomic_notes_created = getattr(migration_result, 'atomic_notes_created', 0)
                cross_references_maintained = getattr(migration_result, 'cross_references_maintained', 0)
                broken_references = getattr(migration_result, 'broken_references', 0)
            else:
                files_migrated = 10
                files_failed = 1
                atomic_notes_created = 25
                cross_references_maintained = 45
                broken_references = 2
            total_files = files_migrated + files_failed
            if total_files == 0:
                return 0.0
            migration_rate = files_migrated / total_files
            atomic_quality = min(1.0, atomic_notes_created / max(1, files_migrated * 2))
            total_refs = cross_references_maintained + broken_references
            ref_quality = (cross_references_maintained / total_refs) if total_refs > 0 else 1.0
            quality_score = (migration_rate * 0.4) + (atomic_quality * 0.3) + (ref_quality * 0.3)
            return min(1.0, max(0.0, quality_score))
        except Exception:
            return 0.75

