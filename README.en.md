# Engineering Figure Banana

Engineering Figure Banana is not a general academic-figure platform. It is an agent-native skill for engineering and CS paper figures, designed to separate conceptual diagrams from exact quantitative plots.

## Positioning

This repository focuses on the figure-production layer inside an existing research workflow.

It is a good fit for:

- researchers who already know what figure they need
- Codex or agent users who want figure generation inside their research workflow
- users who need both method diagrams and exact quantitative plots
- authors in CS, systems, algorithms, electronics, and embedded domains

It is intentionally not centered on:

- a full paper-upload web app
- one-click end-to-end automation for every research task
- a broad all-discipline illustration platform

## Core Differentiation

### 1. Agent-native rather than platform-centric

- meant to be invoked from Codex workflows
- easy to compose with writing, coding, and experiment-analysis tasks
- emphasizes controllability over UI-heavy orchestration

### 2. Conceptual diagrams and quantitative plots use different pipelines

- `image mode`: system architecture, algorithm workflow, graphical abstract, engineering schematic
- `plot mode`: bar charts, trend curves, heatmaps, scatter plots, multi-panel publication figures

This is the key idea: paper figures should not be treated as a single generic prompt problem.

### 3. Optimized for engineering and CS papers

- system architecture
- algorithm workflow
- hardware block diagram
- benchmark / ablation / heatmap / scatter

### 4. Publication-oriented output quality

- white backgrounds
- compact, readable labels
- bilingual technical readability
- local exact plotting for numeric figures
- export-ready `png / pdf / svg`

## Recommended Workflow

The best workflow is usually:

1. Use `ai-research-writing-guide` to decide:
   - what claim the figure should support
   - what figure type is appropriate
   - what panel or module structure is required
   - what caption logic must be preserved
2. Use `engineering-figure-banana` to render the final figure

Recommended upstream handoff fields:

- figure goal
- figure type
- panel plan or module list
- must-keep terms
- output language
- visual constraints

## Repository Layout

- `README.md`: bilingual landing page
- `README.zh-CN.md`: full Chinese guide
- `README.en.md`: full English guide
- `SKILL.md`: internal Codex skill instructions
- `scripts/`: setup, checks, prompt building, generation, and plotting
- `references/`: templates and publication-style references
- `examples/figure-briefs/`: reusable figure-brief starters
- `docs/examples/`: public showcase files and notes
- `providers.md`: provider-compatibility notes

## Two Modes

### `image mode`

Best for:

- system architecture diagrams
- algorithm workflows
- graphical abstracts
- electronics or embedded-system schematics
- reference-inspired redraws

Use this when visual structure matters more than exact numeric geometry.

### `plot mode`

Best for:

- benchmark bar charts
- ablation plots
- trend curves
- heatmaps
- scatter plots
- multi-panel result figures

Use this when exact values, axes, and geometry must stay correct.

Rule of thumb:

- if numeric truth matters, use `plot mode`
- if the figure is conceptual, use `image mode`
- if a figure mixes both, render the quantitative panels locally first and keep image generation for explanatory panels

## Quick Start

### 1. Put the repo in the Codex skill directory

```powershell
$HOME/.codex/skills/engineering-figure-banana
```

### 2. Configure local secrets

Prepare these files outside the repo:

- `$HOME/.codex/secrets/nanobanana.env`
- `$HOME/.codex/secrets/nanobanana_api_key.txt`

Templates are included here:

- `secrets/nanobanana.env.example`
- `secrets/nanobanana_api_key.txt.example`

### 3. Run setup and dependency checks

```powershell
& "$HOME/.codex/skills/engineering-figure-banana/scripts/install_and_test.ps1" -RunSetupCheck
```

### 4. Load env vars

```powershell
. "$HOME/.codex/skills/engineering-figure-banana/scripts/load_nanobanana_env.ps1"
```

### 5. Run a minimal image test

```powershell
python "$HOME/.codex/skills/engineering-figure-banana/scripts/generate_image.py" `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

## Example Gallery

The repository currently includes:

- autonomous-driving overview examples
- cooperative object tracking example
- multi-agent safety overview example
- Linux kernel system diagram example
- one supplementary health-monitoring deployment reference image

See:

- `docs/examples/README.md`

## Why Bilingual Docs Matter

This project benefits from bilingual documentation:

- GitHub discovery is more global and English-heavy
- social promotion in Chinese communities works better with Chinese docs
- the target audience includes both domestic graduate students and international agent / open-source users
- bilingual docs reduce friction and make repo sharing easier

Recommended doc strategy:

- `README.md`: bilingual landing page
- `README.zh-CN.md`: full Chinese guide
- `README.en.md`: full English guide
- gradually make key docs such as `providers.md` bilingual as well

## One-Line Public Description

Use this line in social posts or the repo intro:

> Engineering Figure Banana is an agent-native figure workflow for engineering and CS papers: image models for conceptual diagrams, local rendering for exact quantitative plots.

## Notes

- never commit real API keys
- prefer local plotting for exact quantitative figures
- avoid hardcoding private relay endpoints in public docs unless they are clearly labeled as optional examples
