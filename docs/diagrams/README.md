# Diagrams for SuayLang

## How to regenerate SVG/PNG diagrams

1. Edit the Mermaid source files in this folder (e.g., architecture.mmd, research_flow.mmd).
2. Use the Mermaid CLI or VS Code extension to export to SVG/PNG:
   ```sh
   mmdc -i architecture.mmd -o ../assets/architecture.svg
   mmdc -i research_flow.mmd -o ../assets/research_flow.svg
   ```
3. Place the generated images in docs/assets/.
4. The README references these images for GitHub rendering.

## Mermaid CLI install
- `npm install -g @mermaid-js/mermaid-cli`

## Note
- Only valid Mermaid syntax should be in .mmd files.
- Do not include markdown or prose in Mermaid blocks.
