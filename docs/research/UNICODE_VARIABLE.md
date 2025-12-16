# Unicode syntax as a research variable (SuayLang v0.1)

SuayLang uses Unicode operators and delimiters as a deliberate design choice.
This document frames that choice as a *research variable* with explicit trade-offs.

## Claim (narrow)

Unicode-heavy surface syntax may improve *semantic clarity* by:
- reducing overloading of ASCII tokens;
- making control-flow operators visually distinct (`▷`, `⟲`, `↩`, `↯`);
- making binding/mutation visually distinct (`←` vs `⇐`).

This is a hypothesis about *symbol-level disambiguation*, not a claim about universal readability.

## Costs (practical, not hypothetical)

### Accessibility and input
- Some users cannot easily type Unicode operators.
- Some environments have restricted keyboard layouts.

### Tooling and font rendering
- Fonts may render operators ambiguously or inconsistently.
- LSP/editor features may degrade if tokenization is brittle.

### Collaboration and copy/paste
- Diffs and code review may be harder if reviewers cannot visually distinguish similar glyphs.

## Current mitigation (v0.1)

- The v0.1 contract accepts ASCII fallbacks for a limited set of operators (e.g. `-` for unary minus) where it does not compromise the core research question.
- The VS Code extension provides syntax highlighting and minimal LSP support.

## Risks to evaluation

- Any readability claims are confounded by:
  - reviewer familiarity with Unicode glyphs,
  - font quality,
  - editor rendering and input method.

Therefore, SuayLang’s evaluation must:
- report the exact glyphs used;
- not overclaim readability improvements;
- treat tooling readiness as part of the artifact.

## ASCII redesign proposal (positioning)

The repository contains an ASCII redesign discussion (see docs/ACCESSIBILITY_REDESIGN.md).
For research framing, this is positioned as:
- a future *controlled experiment* (Unicode vs ASCII surface forms),
- not a retreat from the language’s core design.

A defensible future experiment would:
- keep core semantics fixed;
- provide mechanically equivalent surface forms;
- compare comprehension and error rates under controlled conditions.
