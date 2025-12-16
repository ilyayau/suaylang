# Unicode-heavy syntax trade-off (SuayLang)

SuayLang uses Unicode operators and delimiters as a deliberate design choice.
This document treats Unicode syntax as a controlled design variable rather than an incidental aesthetic decision.

## Benefits

Potential benefits (narrowly stated):
- **Symbol-level disambiguation**: visually distinct operators reduce overloading of ASCII tokens.
- **Control-flow salience**: `dispatch`/`cycle` glyphs (`▷`, `⟲`, `↩`, `↯`) make control transitions explicit and visually prominent.
- **Binding vs mutation clarity**: distinct arrows (`←` vs `⇐`) reduce reliance on keyword conventions.

These are hypotheses about *notation*, not claims about universal readability.

## Costs

Practical costs affecting evaluation and adoption:
- **Input difficulty**: typing Unicode requires editor/IME support and may be slow.
- **Accessibility**: some users cannot easily type or visually distinguish glyphs.
- **Font/rendering variability**: glyphs may be ambiguous or poorly rendered.
- **Tooling friction**: tokenization, LSP, and search may be less robust in some environments.

## Mitigations

Current mitigations in the repository:
- Editor support: VS Code syntax highlighting and minimal LSP.
- Documentation: grammar and contract explicitly define the symbols.
- Limited ASCII fallbacks for a small set of operators (where documented), without removing Unicode.

## Why not removed

Unicode is not removed because it is part of the research space being explored:
- The language’s explicit control-flow operators are intended to be salient and unambiguous.
- Removing Unicode would change the surface form and collapse an important experimental variable.

The ASCII redesign discussion is positioned as future work:
- a controlled experiment comparing surface forms while holding semantics fixed,
- not a semantic redesign of the language.
