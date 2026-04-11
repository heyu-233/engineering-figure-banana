# Engineering Figure Banana

A Codex skill for generating publication-style engineering figures with Gemini-compatible image endpoints and for rendering exact quantitative plots locally.

## 5-Minute Quick Start

1. Copy or clone this repository into `$HOME/.codex/skills/engineering-figure-banana`
2. Copy the env and key templates into `$HOME/.codex/secrets/` and fill in your provider values
3. Run:
   - `. "$HOME/.codex/skills/engineering-figure-banana/scripts/load_nanobanana_env.ps1"`
   - `& "$HOME/.codex/skills/engineering-figure-banana/scripts/check_setup.ps1"`
   - then the minimal image test from this README

Fastest Windows path:

```powershell
& "$HOME/.codex/skills/engineering-figure-banana/scripts/install_skill.ps1"
```

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

This repository is provider-neutral:

- it can work with the official Google Gemini API
- it can also work with third-party Gemini-compatible relays
- model names, auth mode, and endpoint URL may vary by provider

## Repository Layout

- `SKILL.md` - main skill instructions
- `agents/openai.yaml` - UI metadata for Codex skill discovery
- `scripts/` - prompt builders, image generation, env bootstrap, and plotting tools
- `references/` - built-in templates and style references
- `providers.md` - provider-neutral compatibility notes for official Google and third-party relays
- `secrets/nanobanana.env.example` - copyable local env template

## Prerequisites / Requirements

- Python 3.10 or newer is recommended
- Codex skill runtime is required if you want this repository to be discovered and invoked as a Codex skill
- Node.js is not required for the normal Python workflow, but `scripts/generate_image.js` is available if you want to use the JavaScript version
- PowerShell is recommended on Windows for loading local secrets with `scripts/load_nanobanana_env.ps1`

Recommended Python packages:

- `requests`
- `numpy`
- `matplotlib`
- `pandas`
- `seaborn`

Minimal install example:

```powershell
pip install -r requirements.txt
```

## Modes

The skill supports two working modes:

- `image mode`
  - Best for conceptual figures such as system architecture diagrams, algorithm workflows, graphical abstracts, and electronics schematics
  - Use this when the figure is mainly explanatory and visual structure matters more than exact numeric geometry
- `plot mode`
  - Best for benchmark charts, ablation plots, heatmaps, scatter plots, trend curves, and other quantitative publication figures
  - Use this when exact values, axes, and geometric fidelity matter

Rule of thumb:

- If numeric truth matters, use `plot mode`
- If the figure is conceptual or schematic, use `image mode`
- If a figure mixes both, generate the conceptual structure with `image mode` and keep the quantitative panels in `plot mode`

Language behavior:

- If you do not pass `--lang`, Chinese technical background now defaults to Chinese figure labels (`zh`)
- English technical background defaults to English labels (`en`)
- Even in Chinese figures, standard English symbols, abbreviations, and formula variables should still be preserved where technically appropriate

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

## Quick Start in 3 Steps

### 1) Copy the skill

Put this repository at:

- `$HOME/.codex/skills/engineering-figure-banana`

### 2) Configure local secrets

This repository does not include real secrets.

Create these local files outside the repo under:

- `$HOME/.codex/secrets/nanobanana.env`
- `$HOME/.codex/secrets/nanobanana_api_key.txt`

You can start from the repository template:

- `secrets/nanobanana.env.example`

Official Google example:

```env
NANOBANANA_BASE_URL=https://generativelanguage.googleapis.com
NANOBANANA_DEFAULT_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_HIGHRES_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_AUTH_MODE=google
```

Third-party relay example:

```env
NANOBANANA_BASE_URL=https://your-relay.example.com
NANOBANANA_DEFAULT_MODEL=<your-default-image-model>
NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>
NANOBANANA_AUTH_MODE=bearer
NANOBANANA_ALLOW_THIRD_PARTY=1
```

The API key file should contain only your current valid key on one line.

## Provider Compatibility

This skill is designed to be compatible with different provider setups.

Supported patterns:

- official Google Gemini API
- third-party Gemini-compatible relays
- custom provider setups that expose a Gemini-like image endpoint

What may differ between providers:

- base URL
- model naming
- auth header mode
- availability of higher-resolution image models
- whether file or image upload behavior matches the official endpoint exactly

Recommended publishing stance:

- treat the official Google endpoint as the reference configuration
- treat third-party relays as optional compatibility paths
- never hardcode your personal relay endpoint or private provider assumptions into shared setup instructions

For more detail, see:

- `providers.md`

### 3) Run a minimal test

Load local env:

```powershell
. "$HOME/.codex/skills/engineering-figure-banana/scripts/load_nanobanana_env.ps1"
```

Run a minimal image-generation test:

```powershell
python "$HOME/.codex/skills/engineering-figure-banana/scripts/generate_image.py" `
  --figure-template system-architecture `
  --lang en `
  "A retrieval-augmented generation system with OCR, chunking, embedding, vector search, reranking, and answer synthesis."
```

Optional prompt-build test:

```powershell
python "$HOME/.codex/skills/engineering-figure-banana/scripts/build_engineering_figure_prompt.py" `
  --figure-template algorithm-workflow `
  --lang zh `
  "A multimodal industrial monitoring workflow for anomaly detection and early warning."
```

## Chinese Figure Notes

- Chinese labels can be generated directly in the image
- Keep Chinese labels concise, readable, and well spaced
- For dense academic figures, prefer fewer but clearer labels rather than paragraph-like text blocks
- Preserve standard English symbols, abbreviations, and formula variables where they improve technical clarity
- Do not force awkward full-Chinese replacements for notation such as `FFT`, `CNN`, `pH`, `IoU`, `loss`, or variables like `x`, `y`, `t`, and `sigma`
- When the prompt/background is mainly Chinese and `--lang` is not specified, the skill now defaults to Chinese labels automatically

## AutoFigure-Edit Handoff

This repository can optionally work with a local [AutoFigure-Edit](https://github.com/ResearAI/AutoFigure-Edit) deployment as a downstream post-processing path.

- Treat Banana as the first-pass draft generation stage
- Treat AutoFigure-Edit as an optional editable-SVG reconstruction or refinement stage
- This is not a guaranteed built-in one-click conversion path in the upstream project
- Direct `Banana image -> editable SVG` conversion depends on your local AutoFigure-Edit setup and any wrapper scripts you add around it

## Example Outputs / Screenshots

You can place repository-safe examples under:

- `docs/examples/`

Recommended examples to showcase:

- a system architecture figure
- an algorithm workflow figure
- an electronics or embedded-system schematic
- a benchmark or ablation plot
- a Chinese-label figure example

Current example:

### Linux Kernel System Diagram

Detailed publication-style Linux kernel architecture overview with user space, system call boundary, kernel subsystems, and hardware layer.

![Linux kernel system diagram](docs/examples/linux-kernel-system-1.jpg)

Why this section matters:

- it helps visitors understand the visual style before installation
- it makes the repository look more complete and trustworthy
- it shows the difference between `image mode` and `plot mode`
- it gives future users a quick expectation of output quality and supported scenarios

When adding screenshots, prefer:

- publication-style white backgrounds
- cropped images that focus on the figure itself
- filenames that explain the scenario, such as `system-architecture-zh.png`
- examples that do not expose secrets, private data, or copyrighted source figures

## Troubleshooting

### `nanobanana_api_key.txt` not found

- Make sure the file exists at `$HOME/.codex/secrets/nanobanana_api_key.txt`
- If you set `NANOBANANA_API_KEY_FILE`, make sure it points to a real file on the current machine
- If you migrated from another computer, remove stale absolute paths from `nanobanana.env`

### `NANOBANANA_BASE_URL` not set

- Add `NANOBANANA_BASE_URL=...` to `$HOME/.codex/secrets/nanobanana.env`
- Or pass `--base-url` directly to `generate_image.py`
- Then reload the env in the same shell session with `load_nanobanana_env.ps1`

### Third-party relay blocked by safety checks

- The generator refuses to send keys or files to non-official Gemini-compatible endpoints unless you explicitly allow it
- Set `NANOBANANA_ALLOW_THIRD_PARTY=1` in `nanobanana.env`
- Or pass `--allow-third-party` for that command
- Only do this when you trust the relay you are using

### Chinese text is too dense or blurry

- Shorten labels and remove paragraph-like text inside the image
- Ask for larger label regions, cleaner spacing, and centered labels
- Keep descriptive labels in Chinese, but preserve technical abbreviations and formula variables in English
- For exact charts, use `plot mode` when geometry matters

## Notes

- Keep real API keys out of the repository
- Keep local machine paths out of committed examples where possible
- For exact quantitative figures, prefer the plotting scripts instead of text-to-image generation
- For Chinese figures, keep labels readable and preserve standard English symbols or formula variables when they improve technical clarity
- Keep provider-specific endpoints, pricing assumptions, and private relay details out of the public repository unless they are clearly labeled as optional examples
