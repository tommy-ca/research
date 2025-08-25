#!/usr/bin/env python3
"""
Simple Atomic Note Extraction from High-Value Content
Direct extraction without complex migration pipeline dependencies
"""

import os
import re
from pathlib import Path
from datetime import datetime

def extract_atomic_sections(content, source_file):
    """Extract potential atomic note sections from content"""
    sections = []
    current_section = {'title': '', 'content': '', 'level': 0}
    
    lines = content.split('\n')
    for line in lines:
        if line.startswith('#'):
            # Save previous section
            if current_section['content'].strip():
                sections.append(current_section.copy())
            
            # Start new section
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            current_section = {
                'title': title,
                'content': '',
                'level': level,
                'source': str(source_file)
            }
        else:
            current_section['content'] += line + '\n'
    
    # Don't forget the last section
    if current_section['content'].strip():
        sections.append(current_section)
    
    return sections

def create_atomic_note(section, target_dir):
    """Create atomic note file from section"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    
    # Sanitize title for filename
    sanitized_title = re.sub(r'[^\w\s-]', '', section['title'].lower())
    sanitized_title = re.sub(r'[-\s]+', '-', sanitized_title)[:50]
    
    filename = f"{timestamp}-{sanitized_title}.md"
    file_path = target_dir / filename
    
    # Create frontmatter
    frontmatter = f"""---
id: {timestamp}
title: "{section['title']}"
date: {datetime.now().strftime('%Y-%m-%d')}
type: atomic
source: {Path(section['source']).name}
extraction_method: header_split
created: {datetime.now().isoformat()}
---

# {section['title']}

{section['content'].strip()}

## Connections
- Related concepts: [[to-be-linked]]
"""
    
    # Write file
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path.write_text(frontmatter, encoding='utf-8')
    
    return filename

def main():
    """Extract atomic notes from high-value documents"""
    print("🧠 Simple atomic extraction from high-value content...")
    
    # High-value documents for atomic extraction  
    high_value_docs = [
        "docs/feynman-first-principles-pkm-research.md",
        "docs/knowledge-management-workflows.md",
        "docs/pkm-systems-analysis.md",
        "docs/pkm-architecture/PKM-SYSTEM-ARCHITECTURE.md",
        "docs/pkm-architecture/PKM-SYSTEM-SPECIFICATION.md"
    ]
    
    target_dir = Path("vault/permanent/notes/concepts")
    total_notes = 0
    
    for doc_path in high_value_docs:
        doc_file = Path(doc_path)
        if doc_file.exists():
            print(f"📝 Processing: {doc_file.name}")
            
            content = doc_file.read_text(encoding='utf-8')
            
            # Remove frontmatter for processing
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].strip()
            
            sections = extract_atomic_sections(content, doc_file)
            
            # Create atomic notes for sections with substantial content
            notes_created = 0
            for section in sections:
                if len(section['content'].strip()) > 100 and section['level'] <= 3:
                    filename = create_atomic_note(section, target_dir)
                    notes_created += 1
                    total_notes += 1
                    if notes_created >= 5:  # Limit to 5 per document
                        break
            
            print(f"✅ Created {notes_created} atomic notes from {doc_file.name}")
        else:
            print(f"⚠️ Document not found: {doc_path}")
    
    print(f"🎯 Total atomic notes created: {total_notes}")
    
    # Generate report
    report = f"""
=== SIMPLE ATOMIC EXTRACTION REPORT ===
Timestamp: {datetime.now().isoformat()}

Documents Processed: {len([doc for doc in high_value_docs if Path(doc).exists()])}
Total Atomic Notes Created: {total_notes}
Target Directory: vault/permanent/notes/concepts/

Status: SUCCESS
"""
    
    with open("simple-extraction-report.txt", "w") as f:
        f.write(report)
    
    print("📋 Report saved to: simple-extraction-report.txt")

if __name__ == "__main__":
    main()