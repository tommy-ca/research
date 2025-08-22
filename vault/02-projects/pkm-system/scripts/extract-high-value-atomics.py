#!/usr/bin/env python3
"""
High-Value Content Atomic Extraction
Process critical documents and extract atomic notes using the ultra-migration-pipeline
"""

import os
import sys
from pathlib import Path

# Add the scripts directory to the path to import the ultra-migration-pipeline
sys.path.insert(0, str(Path(__file__).parent))

from ultra_migration_pipeline import UltraMigrationPipeline

def main():
    """Extract atomic notes from high-value content"""
    
    # Initialize the migration pipeline
    pipeline = UltraMigrationPipeline("vault")
    
    print("🧠 Extracting atomic notes from high-value content...")
    
    # High-value documents for atomic extraction
    high_value_docs = [
        "vault/permanent/notes/methods/feynman-first-principles-pkm-research.md",
        "vault/02-projects/pkm-system/architecture/PKM-SYSTEM-ARCHITECTURE.md",
        "vault/02-projects/pkm-system/architecture/PKM-SYSTEM-SPECIFICATION.md",
        "vault/02-projects/pkm-system/architecture/KNOWLEDGE-EXTRACTION-FRAMEWORK.md",
        "vault/02-projects/pkm-system/knowledge-management-workflows.md",
        "vault/02-projects/pkm-system/pkm-systems-analysis.md"
    ]
    
    total_atomic_notes = 0
    
    for doc_path in high_value_docs:
        doc_file = Path(doc_path)
        if doc_file.exists():
            print(f"📝 Processing: {doc_file.name}")
            
            # Extract 10-15 atomic notes per document
            atomic_notes = pipeline.extract_atomic_notes(doc_file, target_count=12)
            
            # Save atomic notes to permanent/notes/concepts
            atomic_dir = Path("vault/permanent/notes/concepts")
            atomic_dir.mkdir(parents=True, exist_ok=True)
            
            for note in atomic_notes:
                pipeline.save_atomic_note(note, atomic_dir)
                total_atomic_notes += 1
            
            print(f"✅ Extracted {len(atomic_notes)} atomic notes from {doc_file.name}")
        else:
            print(f"⚠️ Document not found: {doc_path}")
    
    print(f"🎯 Total atomic notes extracted: {total_atomic_notes}")
    
    # Generate summary report
    report = f"""
=== HIGH-VALUE ATOMIC EXTRACTION REPORT ===
Timestamp: {pipeline._create_iso_timestamp()}

Documents Processed: {len([doc for doc in high_value_docs if Path(doc).exists()])}
Total Atomic Notes Created: {total_atomic_notes}
Target Directory: vault/permanent/notes/concepts/

Status: SUCCESS
"""
    
    with open("high-value-extraction-report.txt", "w") as f:
        f.write(report)
    
    print("📋 Report saved to: high-value-extraction-report.txt")

if __name__ == "__main__":
    main()