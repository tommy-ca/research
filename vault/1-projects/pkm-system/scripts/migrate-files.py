#!/usr/bin/env python3
"""
migrate-files.py - Bulk file migration with PARA categorization

This script automates the migration of files from the old structure
to the PKM vault following PARA principles.

Usage:
    python migrate-files.py --source <dir> --map migration-map.json --dry-run
    python migrate-files.py --source docs/ --map migration-map.json --execute

Author: PKM System
Date: 2024-01-21
Version: 1.0.0
"""

import os
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class PkmMigrator:
    """Migrate files to PKM vault structure following PARA method"""
    
    def __init__(self, vault_root: str = "vault"):
        self.vault_root = Path(vault_root)
        self.migration_log = []
        self.stats = {
            'files_moved': 0,
            'folders_created': 0,
            'errors': 0
        }
        
    def load_migration_map(self, map_file: str) -> Dict:
        """Load migration mapping from JSON file"""
        if map_file.endswith('.md'):
            # Parse markdown migration map
            return self.parse_markdown_map(map_file)
        else:
            with open(map_file, 'r') as f:
                return json.load(f)
    
    def parse_markdown_map(self, md_file: str) -> Dict:
        """Parse migration map from markdown format"""
        migration_map = {
            'projects': {},
            'areas': {},
            'resources': {},
            'archives': {}
        }
        
        # Simple parser for markdown migration map
        # Format: `source/path/*` → `vault/destination/`
        with open(md_file, 'r') as f:
            lines = f.readlines()
            
        current_category = None
        for line in lines:
            if '1️⃣ PROJECTS' in line:
                current_category = 'projects'
            elif '2️⃣ AREAS' in line:
                current_category = 'areas'
            elif '3️⃣ RESOURCES' in line:
                current_category = 'resources'
            elif '4️⃣ ARCHIVES' in line:
                current_category = 'archives'
            elif '→' in line and current_category:
                # Parse migration rule
                parts = line.split('→')
                if len(parts) == 2:
                    source = parts[0].strip().strip('`- ')
                    dest = parts[1].strip().strip('`')
                    if source and dest:
                        migration_map[current_category][source] = dest
                        
        return migration_map
    
    def categorize_file(self, file_path: Path, migration_map: Dict) -> str:
        """Determine PARA category for a file"""
        file_str = str(file_path)
        
        # Check each category's rules
        for category in ['projects', 'areas', 'resources', 'archives']:
            for pattern, destination in migration_map.get(category, {}).items():
                if self.matches_pattern(file_str, pattern):
                    return destination
                    
        # Default categorization based on content
        return self.default_categorization(file_path)
    
    def matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if file matches migration pattern"""
        # Handle wildcards
        pattern = pattern.replace('*', '')
        return pattern in file_path
    
    def default_categorization(self, file_path: Path) -> str:
        """Default PARA categorization based on file characteristics"""
        file_str = str(file_path).lower()
        
        # Projects: Active work
        if any(word in file_str for word in ['implementation', 'current', 'active', 'wip']):
            return "vault/1-projects/uncategorized/"
            
        # Areas: Ongoing responsibilities
        if any(word in file_str for word in ['process', 'workflow', 'standard', 'guide']):
            return "vault/2-areas/uncategorized/"
            
        # Resources: Reference materials
        if any(word in file_str for word in ['reference', 'template', 'example', 'framework']):
            return "vault/3-resources/uncategorized/"
            
        # Archives: Old/completed
        if any(word in file_str for word in ['old', 'archive', 'deprecated', 'legacy']):
            return "vault/4-archives/uncategorized/"
            
        return "vault/0-inbox/uncategorized/"
    
    def migrate_file(self, source: Path, destination: str, dry_run: bool = True) -> bool:
        """Migrate a single file to destination"""
        dest_path = Path(destination)
        
        # Handle directory destinations
        if destination.endswith('/'):
            dest_path = dest_path / source.name
            
        # Create parent directories
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        if dry_run:
            self.migration_log.append(f"[DRY-RUN] Would move: {source} → {dest_path}")
            return True
        else:
            try:
                shutil.move(str(source), str(dest_path))
                self.migration_log.append(f"[SUCCESS] Moved: {source} → {dest_path}")
                self.stats['files_moved'] += 1
                return True
            except Exception as e:
                self.migration_log.append(f"[ERROR] Failed to move {source}: {e}")
                self.stats['errors'] += 1
                return False
    
    def add_frontmatter(self, file_path: Path) -> None:
        """Add frontmatter to migrated markdown file"""
        if file_path.suffix != '.md':
            return
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Check if frontmatter exists
        if content.startswith('---'):
            return
            
        # Generate frontmatter
        frontmatter = f"""---
date: {datetime.now().strftime('%Y-%m-%d')}
type: migrated
status: review
tags: [migrated, needs-review]
source: migration-phase-2
---

"""
        
        with open(file_path, 'w') as f:
            f.write(frontmatter + content)
    
    def run_migration(self, source_dir: str, migration_map: Dict, 
                     dry_run: bool = True) -> Dict:
        """Run the complete migration process"""
        source_path = Path(source_dir)
        
        # Find all files to migrate
        files_to_migrate = []
        for file_path in source_path.rglob('*'):
            if file_path.is_file() and '.git' not in str(file_path):
                files_to_migrate.append(file_path)
        
        print(f"Found {len(files_to_migrate)} files to migrate")
        
        # Migrate each file
        for file_path in files_to_migrate:
            destination = self.categorize_file(file_path, migration_map)
            self.migrate_file(file_path, destination, dry_run)
            
            if not dry_run and destination != "vault/0-inbox/uncategorized/":
                # Add frontmatter to successfully migrated files
                dest_file = Path(destination) / file_path.name
                self.add_frontmatter(dest_file)
        
        return self.stats
    
    def generate_report(self) -> str:
        """Generate migration report"""
        report = ["=" * 50]
        report.append("PKM Migration Report")
        report.append("=" * 50)
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append(f"Files Moved: {self.stats['files_moved']}")
        report.append(f"Folders Created: {self.stats['folders_created']}")
        report.append(f"Errors: {self.stats['errors']}")
        report.append("\nMigration Log:")
        report.extend(self.migration_log[-20:])  # Last 20 entries
        report.append("=" * 50)
        
        return "\n".join(report)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Migrate files to PKM vault structure')
    parser.add_argument('--source', required=True, help='Source directory to migrate')
    parser.add_argument('--map', required=True, help='Migration map file (JSON or MD)')
    parser.add_argument('--dry-run', action='store_true', help='Perform dry run without moving files')
    parser.add_argument('--execute', action='store_true', help='Execute the migration')
    
    args = parser.parse_args()
    
    if not args.dry_run and not args.execute:
        print("Error: Specify either --dry-run or --execute")
        return 1
    
    # Initialize migrator
    migrator = PkmMigrator()
    
    # Load migration map
    migration_map = migrator.load_migration_map(args.map)
    
    # Run migration
    dry_run = args.dry_run
    stats = migrator.run_migration(args.source, migration_map, dry_run)
    
    # Generate and print report
    report = migrator.generate_report()
    print(report)
    
    # Save report
    report_file = f"migration-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())

# TDD Tests (to be moved to tests/test_migrate_files.py)
"""
def test_categorize_file():
    migrator = PkmMigrator()
    
    # Test project categorization
    assert "projects" in migrator.categorize_file(
        Path("docs/implementation.md"), {}
    )
    
    # Test resource categorization  
    assert "resources" in migrator.categorize_file(
        Path("docs/framework.md"), {}
    )

def test_migration_dry_run():
    migrator = PkmMigrator()
    # Test dry run doesn't move files
    # Test logging works correctly
    pass

def test_frontmatter_addition():
    # Test frontmatter is added correctly
    # Test existing frontmatter is preserved
    pass
"""