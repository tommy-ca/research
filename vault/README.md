# PKM Vault

This is the primary knowledge vault following PKM best practices and organizational principles.

## Structure Overview

### 00-inbox/
Capture zone for all incoming information before processing.

### 01-notes/
Atomic notes organized by permanence level (Zettelkasten method).

### 02-projects/
Active projects with associated notes and resources (PARA method).

### 03-areas/
Ongoing life areas requiring continuous attention (PARA method).

### 04-resources/
Reference materials and templates (PARA method).

### 05-archives/
Inactive content preserved for reference (PARA method).

### 06-synthesis/
Generated insights, summaries, and teaching materials.

### 07-journal/
Time-based entries and reflections.

### 08-media/
Multimedia content storage with S3 backing.

### 09-data/
Structured data using Lance (vectors) and Parquet (analytics).

### .pkm/
System configuration and metadata.

## Storage Backends

- **Local/Git**: Markdown files and small assets
- **S3**: Large media files and backups
- **Lance**: Vector embeddings and similarity search
- **Parquet**: Analytics and structured data

## Naming Conventions

- Atomic notes: `YYYYMMDD-HHMMSS-title-slug.md`
- Daily notes: `YYYY-MM-DD.md`
- Projects: `prj-XXX-description/`
- Media: `{type}-{timestamp}-{description}.{ext}`

---

*PKM Vault Structure v1.0*