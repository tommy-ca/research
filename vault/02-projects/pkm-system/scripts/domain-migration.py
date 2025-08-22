#!/usr/bin/env python3
"""
Domain Knowledge Migration
Migrate remaining docs/ content to appropriate vault structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def migrate_domain_content():
    """Migrate remaining docs content to appropriate vault locations"""
    print("🧠 Starting domain knowledge migration...")
    
    # Migration mappings: source -> destination
    migrations = [
        # Agent and system architecture docs
        ("docs/AGENT-INTERACTION-ARCHITECTURE.md", "vault/02-projects/pkm-system/architecture/"),
        ("docs/AGENT-INTERACTION-SUMMARY.md", "vault/02-projects/pkm-system/architecture/"),
        ("docs/RESEARCH_AGENTS.md", "vault/02-projects/pkm-system/architecture/"),
        
        # Knowledge management implementations
        ("docs/FEATURE-KNOWLEDGE-MANAGEMENT.md", "vault/02-projects/pkm-system/implementation/"),
        ("docs/KM-SIMPLE-IMPLEMENTATION.md", "vault/02-projects/pkm-system/implementation/"),
        ("docs/KM-SIMPLIFICATION-COMPARISON.md", "vault/02-projects/pkm-system/implementation/"),
        ("docs/KM-SIMPLIFICATION-PLAN.md", "vault/02-projects/pkm-system/implementation/"),
        ("docs/KM-SIMPLIFICATION-RELEASE.md", "vault/02-projects/pkm-system/implementation/"),
        ("docs/KM-ULTRA-SIMPLE-SUMMARY.md", "vault/02-projects/pkm-system/implementation/"),
        
        # Custom commands and workflows
        ("docs/CUSTOM_COMMANDS.md", "vault/04-resources/workflows/"),
        ("docs/V2_SUMMARY.md", "vault/04-resources/summaries/"),
        
        # Research content
        ("docs/research/", "vault/04-resources/research/"),
        
        # Archive content  
        ("docs/archive-v1/", "vault/05-archives/docs-v1/"),
    ]
    
    total_migrated = 0
    
    for source, destination in migrations:
        source_path = Path(source)
        dest_path = Path(destination)
        
        if source_path.exists():
            # Create destination directory
            dest_path.mkdir(parents=True, exist_ok=True)
            
            if source_path.is_file():
                # Copy single file
                dest_file = dest_path / source_path.name
                shutil.copy2(source_path, dest_file)
                print(f"✅ Migrated: {source_path.name} -> {dest_path}")
                total_migrated += 1
            elif source_path.is_dir():
                # Copy directory contents
                for item in source_path.rglob('*'):
                    if item.is_file():
                        relative_path = item.relative_to(source_path)
                        dest_file = dest_path / relative_path
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dest_file)
                        total_migrated += 1
                print(f"✅ Migrated directory: {source_path} -> {dest_path}")
        else:
            print(f"⚠️ Source not found: {source_path}")
    
    print(f"🎯 Total files migrated: {total_migrated}")
    
    # Generate report
    report = f"""
=== DOMAIN KNOWLEDGE MIGRATION REPORT ===
Timestamp: {datetime.now().isoformat()}

Total Files Migrated: {total_migrated}
Migration Mappings: {len(migrations)}

Migration Structure:
- Agent/System Architecture -> vault/02-projects/pkm-system/architecture/
- Implementation Docs -> vault/02-projects/pkm-system/implementation/ 
- Workflows -> vault/04-resources/workflows/
- Research -> vault/04-resources/research/
- Archives -> vault/05-archives/docs-v1/

Status: SUCCESS
"""
    
    with open("domain-migration-report.txt", "w") as f:
        f.write(report)
    
    print("📋 Report saved to: domain-migration-report.txt")

if __name__ == "__main__":
    migrate_domain_content()