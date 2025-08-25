---
title: Gist Markdown Ingestion Specification
status: implemented
type: specification
date: 2025-08-22
tags: [pkm, ingestion, gist, tdd]
---

# Gist Markdown Ingestion

## Overview
Implements end-to-end ingestion of Markdown content originating from GitHub Gists using a TDD workflow.

## Requirements
- Accept local Markdown input with a `--gist-url` that records the source URL in frontmatter.
- Auto-append `#source/gist` tag when a gist URL is provided.
- Follow capture -> inbox -> PARA processing -> validation -> enrichment -> atomic note pipeline.
- Produce a final resource path and create an atomic note referencing it.

## Interfaces
- CLI: `scripts/ingest_markdown.py [--file|-] --gist-url <url> [--tags ...] [--vault <path>]`
- CLI: `scripts/pkm_ingest_pipeline.py --file <path> --gist-url <url> [--tags ...] [--vault <path>]`

## Quality Gates
- Frontmatter includes: `date`, `type`, `status`, `created`, `id`, `source`.
- Resource is categorized under `03-resources` unless a more specific PARA match is found.
- Atomic note created in `vault/permanent/notes` with backlink to the resource.

## TDD
- Unit test `test_gist_capture.py` verifies source metadata capture.
- Integration test `test_gist_ingestion_e2e.py` verifies full pipeline.

## Status
Implemented and covered by tests.

