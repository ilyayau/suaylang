# Diagrams for SuayLang

## How to regenerate SVG/PNG diagrams

1. Edit the Mermaid source files in docs/diagrams/src/ (e.g., architecture_overview.mmd).
2. Export to SVG (committed) and update ASCII fallbacks:
   ```sh
   mmdc -i docs/diagrams/src/architecture_overview.mmd -o docs/diagrams/architecture_overview.svg
   mmdc -i docs/diagrams/src/equivalence_flow.mmd -o docs/diagrams/equivalence_flow.svg
   mmdc -i docs/diagrams/src/pipeline.mmd -o docs/diagrams/pipeline.svg
   ```
3. Update ASCII fallbacks (committed) under docs/diagrams/ascii/.
4. README references only docs/diagrams/*.svg (Mermaid is never required).

## Mermaid CLI install
- `npm install -g @mermaid-js/mermaid-cli`

## Note
- Only valid Mermaid syntax should be in .mmd files.
- Do not include markdown or prose in Mermaid blocks.

## ASCII fallbacks (required)
- docs/diagrams/ascii/architecture_overview.txt
- docs/diagrams/ascii/equivalence_flow.txt
- docs/diagrams/ascii/pipeline.txt
