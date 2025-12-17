# Related work (analysis, not name-dropping)

SuayLang is positioned as a small research artifact for (i) **explicit control-flow semantics** and (ii) **evidence-producing interpreter↔VM validation**.

The key comparison dimension is not “feature count,” but *how* a language/implementation supports falsifiable equivalence claims and inspection.

- **Operational semantics framing:** Treating an interpreter as baseline is aligned with operational views of semantics [@plotkin1981] [@kahn1987], while acknowledging that the VM remains an implementation artifact.
- **Pattern matching:** SuayLang’s `dispatch` resembles expression-shaped pattern matching; classic compilation work emphasizes decision trees and coverage properties [@maranget2008].
- **Differential testing:** Disagreements between two implementations are counterexamples in the sense of differential testing [@mckeeman1998]; property-based approaches motivate seeded generation and shrinkable cases [@quickcheck2000].
- **Compiler/VM bug-finding via generation:** Csmith-style approaches show that random program generation plus differential oracles can find real backend bugs [@csmith2011].
- **Educational interpreter/VM patterns:** Crafting Interpreters provides an implementation template; SuayLang’s difference is that equivalence evidence and scope statements are treated as first-class artifacts [@craftinginterpreters2021].

See the comparison table for concrete “similarity/difference/why it matters”: [docs/research/RELATED_WORK_TABLE.md](RELATED_WORK_TABLE.md)
