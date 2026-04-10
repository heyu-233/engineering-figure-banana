# Engineering Figure Templates

Use these templates for computer science, electronics, algorithms, and general engineering-paper figures that should be generated with Nano Banana or Gemini image models.

## Default publication rules

Apply these defaults unless the user requests otherwise:

- white background
- concise Helvetica- or Arial-like sans-serif labels
- modular vector-friendly blocks and arrows
- blue for the proposed path or core component
- green for improved states, validated outputs, or successful paths
- red for competing baselines, bottlenecks, failure paths, or error sources
- neutral gray for infrastructure, background modules, or context
- clear reading order from left to right or top to bottom
- short labels that remain legible at single-column width

If the figure is actually quantitative, switch to exact `plot` mode instead of asking the image model to hallucinate charts.

## Template families

- `graphical-abstract`
  Compact research-story overview for a paper cover graphic or summary panel.
- `system-architecture`
  Model or system block diagram with data flow, modules, and outputs.
- `algorithm-workflow`
  Stepwise algorithm pipeline, training or inference loop, or decision flow.
- `electronic-schematic`
  Circuit-level, embedded-system, sensor-chain, FPGA, or mixed-signal block schematic.

## Usage rules

- Insert the user's technical background into the `Technical Background` slot.
- Keep names faithful to the user input.
- If the user does not provide exact numbers, use placeholders or qualitative labels.
- Never fabricate benchmark improvements, device dimensions, frequencies, voltages, or timing values.
- If the user names a venue, append that style preference after the template rather than rewriting the core template.
