# PKM Capture Command

## Command
`/pkm-capture`

## Description
Quickly capture any thought, idea, or content into the PKM inbox for later processing.

## Syntax
```
/pkm-capture "content" [--source="url_or_reference"] [--tags="tag1,tag2"]
```

## Parameters
- `content` (required): The text to capture
- `--source` (optional): Source URL or reference
- `--tags` (optional): Comma-separated tags

## Examples
```bash
# Simple capture
/pkm-capture "Interesting idea about knowledge graphs"

# With source
/pkm-capture "LLMs can enhance PKM systems" --source="https://example.com/article"

# With tags
/pkm-capture "Review PARA method implementation" --tags="pkm,organization,todo"
```

## Implementation
1. Creates timestamped file in `vault/0-inbox/quick-capture/`
2. Adds frontmatter with metadata
3. Preserves source and context
4. Ready for processing with `/pkm-process`

## Workflow Integration
- Use for quick thoughts during the day
- Capture before context is lost
- Process inbox regularly (daily/weekly)
- Zero inbox as goal

## Related Commands
- `/pkm-process` - Process inbox items
- `/pkm-web` - Capture web content
- `/pkm-daily` - Add to daily note