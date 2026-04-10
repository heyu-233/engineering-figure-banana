# Engineering Figure Banana

A Codex skill for generating publication-style engineering figures with Gemini-compatible image endpoints and for rendering exact quantitative plots locally.

This skill is designed for:

- system architecture diagrams
- algorithm workflows
- electronics and embedded-system schematics
- graphical abstracts
- benchmark charts, ablation plots, heatmaps, scatter plots, and other publication figures

It also includes:

- Chinese prompt/template support for engineering and materials-science figures
- journal-friendly low-saturation color guidance
- optional local handoff notes for AutoFigure-Edit editable-SVG refinement

## Repository Layout

- `SKILL.md` - main skill instructions
- `agents/openai.yaml` - UI metadata for Codex skill discovery
- `scripts/` - prompt builders, image generation, env bootstrap, and plotting tools
- `references/` - built-in templates and style references

## Install

Copy this directory into your local Codex user skills directory:

```powershell
Copy-Item -Recurse -Force . "$HOME/.codex/skills/engineering-figure-banana"
```

Or clone it directly:

```powershell
git clone <your-repo-url> "$HOME/.codex/skills/engineering-figure-banana"
```

Then restart Codex or open a new Codex session so the skill can be discovered.

## Local Secrets Setup

This repository does not include real secrets.

Create these local files outside the repo under:

- `$HOME/.codex/secrets/nanobanana.env`
- `$HOME/.codex/secrets/nanobanana_api_key.txt`

Example `nanobanana.env`:

```env
NANOBANANA_BASE_URL=https://new.apipudding.com
NANOBANANA_DEFAULT_MODEL=<your-default-image-model>
NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>
NANOBANANA_AUTH_MODE=bearer
NANOBANANA_ALLOW_THIRD_PARTY=1
```

The API key file should contain only your current valid key on one line.

## Load Local Env

```powershell
. "$HOME/.codex/skills/engineering-figure-banana/scripts/load_nanobanana_env.ps1"
```

## Minimal Image Test

```powershell
python "$HOME/.codex/skills/engineering-figure-banana/scripts/generate_image.py" `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

## Minimal Prompt-Build Test

```powershell
python "$HOME/.codex/skills/engineering-figure-banana/scripts/build_engineering_figure_prompt.py" `
  --figure-template algorithm-workflow `
  --lang zh `
  "A multimodal industrial monitoring workflow for anomaly detection and early warning."
```

## Notes

- Keep real API keys out of the repository.
- Keep local machine paths out of committed examples where possible.
- For exact quantitative figures, prefer the plotting scripts instead of text-to-image generation.
- For Chinese figures, keep labels readable and preserve standard English symbols or formula variables when they improve technical clarity.
