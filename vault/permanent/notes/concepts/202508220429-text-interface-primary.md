---
id: 202508220429
title: "Text Interface (Primary)"
date: 2025-08-22
type: atomic
source: PKM-SYSTEM-ARCHITECTURE.md
extraction_method: header_split
created: 2025-08-22T04:29:54.173584
---

# Text Interface (Primary)

Users work directly with markdown files, and Claude Code automatically processes changes:

```yaml
text_interface:
  user_actions:
    - Create new markdown files
    - Edit existing notes
    - Organize files in folders
    - Commit changes to Git
  
  automatic_processing:
    on_file_save:
      - Syntax validation
      - Frontmatter extraction
      - Content analysis
      - Link detection
    
    on_file_create:
      - Template application
      - Metadata generation
      - Initial processing
      - Inbox placement
    
    on_file_move:
      - Link updates
      - Reference tracking
      - Category assignment
    
    on_git_commit:
      - Batch processing
      - Lakehouse sync
      - Version tracking
```

## Connections
- Related concepts: [[to-be-linked]]
