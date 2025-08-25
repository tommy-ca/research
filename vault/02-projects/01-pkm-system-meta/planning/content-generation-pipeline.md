# Content Generation Pipeline Plan (Silver → Gold)

## Context
We follow the PKM pipeline from capture → ingestion → processing → atomic knowledge. This plan focuses on turning the “silver layer” (normalized atomic notes + graph) into a “gold layer” of publishable content assets (articles, courses, emails, social posts) via retrieval-driven workflows.

## Lakehouse Analogy
- Bronze: Raw captures in `vault/00-inbox/` (heterogeneous, unvalidated)
- Silver: Normalized atomic notes with metadata, tags, Feynman explanations, and links in `vault/permanent/` + indexes/graphs
- Gold: Composed content assets in `vault/06-synthesis/content/` (structured, publication-ready)

## Objectives
- Robust knowledge extraction → consistent “silver” artifacts
- Powerful retrieval → composable content briefs/outlines
- Reproducible assembly → deterministic content packages

## Inputs (Silver Layer)
- Atomic notes with frontmatter (id, title, tags, links)
- Feynman explanations and ELI5 variants
- Link graph (wikilinks) and similarity hints
- Retrieval services: search, get, links

## Outputs (Gold Layer)
- Article briefs, outlines, and drafts
- Course syllabi, module outlines, lesson plans
- Email sequences (nurture, launch, update)
- Social media post sets (thread, short posts)

## Core Workflows
1) Topic Brief (retrieval-first)
- Input: `topic` or seed note(s)
- Steps: retrieve → cluster → synthesize → gaps → brief
- Output: `brief.md` with objectives, audience, sources, key points

2) Article Outline
- Input: `brief.md` or curated notes
- Steps: retrieve supporting notes → structure sections → assign evidence → Feynman check
- Output: `outline.md` with headings, claims, evidence references

3) Draft Assembly (deterministic)
- Input: `outline.md`
- Steps: section-by-section synthesis with citations → peer/self review prompts → revision checklist
- Output: `draft.md` with citation links to source notes

4) Course Builder
- Input: topic + level + audience
- Steps: retrieve → learning objectives → module map → lesson outlines → assessments
- Output: `course/` folder with `syllabus.md`, `modules/*`

5) Email/Social Packages
- Input: brief/draft
- Steps: extract key messages → adapt per channel → schedule metadata
- Output: `emails/*.md`, `social/*.md`

## Retrieval Contracts (Silver Services)
- search(query, type?, tags?, limit) → ranked list with score
- get(ident) → metadata + excerpt + path
- links(ident, threshold) → related notes with rationale

## Feynman Integration
- Each major section must include an ELI5 subsection
- Gap detector flags missing prerequisites
- Complexity checks: surface, functional, structural understanding labels

## Directory Targets (Gold)
- vault/06-synthesis/content/
  - articles/<slug>/{brief.md, outline.md, draft.md}
  - courses/<slug>/{syllabus.md, modules/}
  - emails/<campaign>/<N>.md
  - social/<campaign>/<N>.md

## Acceptance Criteria
- Deterministic outputs from same inputs (idempotent planning)
- All assets include provenance links to silver notes
- Retrieval steps logged (query, selection rationale)
- Feynman checks present in briefs/outlines

## Risks & Mitigations
- Hallucination → constrain to retrieved notes + cite
- Drift from silver → embed note IDs, validate links
- Inconsistency → templates + response envelope

## Next Steps
- Implement “Silver Services” API (search/get/links) with tests
- Add content templates and example pipelines
- Create Claude commands stubs: `/content-brief`, `/content-outline`, `/content-draft`
