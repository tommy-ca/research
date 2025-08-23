# PKM Vault

This is the primary knowledge vault following PKM best practices and organizational principles.

## Structure Overview

### 00-inbox/
Capture zone for all incoming information before processing.
Files captured here are processed automatically into PARA.

### 01-notes/
Atomic notes organized by permanence level (Zettelkasten method).
Contains `permanent/notes/` for Zettelkasten; index at `permanent/index.md`.

### 02-projects/
Active projects with associated notes and resources (PARA method).
Subdirectories should be numbered: `NN-project-name/`.

### 03-areas/
Ongoing life areas requiring continuous attention (PARA method).
Subdirectories should be numbered: `NN-area-name/`.

### 04-resources/
Reference materials and templates (PARA method).
Subdirectories should be numbered: `NN-topic/` (e.g., `10-architecture/`).

### 05-archives/
Inactive content preserved for reference (PARA method).
Subdirectories should be numbered: `NN-archive-scope/`.

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

- Atomic notes: `YYYYMMDDHHMMSS-title-slug.md`
- Daily notes: `YYYY-MM-DD.md`
- Projects: `prj-XXX-description/`

## Enforcement

- Use `scripts/validate_vault_structure.py` to validate directory layout.
- Ingestion and inbox processing use PARA mapping `02/03/04/05`.
- Media: `{type}-{timestamp}-{description}.{ext}`

---

*PKM Vault Structure v1.0*