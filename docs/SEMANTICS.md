# Minimal formal semantics (SuayLang v1-scope)

This document defines a minimal big-step semantics for the v1-scope subset of SuayLang.

## Syntax categories
- $e$ — expression
- $v$ — value
- $\rho$ — environment (mapping names to values)
- $k$ — error kind (lex, parse, runtime, internal)
- $s$ — source span (line, column)

## Evaluation relation
- $\langle e, \rho \rangle \Downarrow \langle v, \rho' \rangle$ — expression $e$ evaluates to value $v$ in environment $\rho'$
- $\langle e, \rho \rangle \Downarrow_{err} \langle k, s \rangle$ — $e$ raises error $k$ at span $s$


## Rules

### 1. Let/binding
$\frac{\langle e_1, \rho \rangle \Downarrow v_1 \quad \langle e_2, \rho[x \mapsto v_1] \rangle \Downarrow v_2}{\langle x \leftarrow e_1; e_2, \rho \rangle \Downarrow v_2}$

### 2. Function application
$\frac{\langle e_f, \rho \rangle \Downarrow \lambda x. e_{body} \quad \langle e_{arg}, \rho \rangle \Downarrow v_{arg} \quad \langle e_{body}, \rho[x \mapsto v_{arg}] \rangle \Downarrow v_{res}}{\langle e_f . e_{arg}, \rho \rangle \Downarrow v_{res}}$

### 3. If-expression (pattern match/dispatch)
$\frac{\langle e_{cond}, \rho \rangle \Downarrow v_{cond} \quad v_{cond} = \text{true} \quad \langle e_{then}, \rho \rangle \Downarrow v_{then}}{\langle \text{if } e_{cond} \text{ then } e_{then} \text{ else } e_{else}, \rho \rangle \Downarrow v_{then}}$

$\frac{\langle e_{cond}, \rho \rangle \Downarrow v_{cond} \quad v_{cond} = \text{false} \quad \langle e_{else}, \rho \rangle \Downarrow v_{else}}{\langle \text{if } e_{cond} \text{ then } e_{then} \text{ else } e_{else}, \rho \rangle \Downarrow v_{else}}$

### 4. Dispatch/match
$\frac{\langle e_{scrut}, \rho \rangle \Downarrow v_{scrut} \quad \text{match}(v_{scrut}, p_i) = \text{yes} \quad \langle e_i, \rho' \rangle \Downarrow v_i}{\langle e_{scrut} \mid> \{p_1 => e_1; ...; p_n => e_n\}, \rho \rangle \Downarrow v_i}$

### 5. Cycle/loop-expression
$\frac{\langle e_{seed}, \rho \rangle \Downarrow v_{seed} \quad \langle \text{cycle}(v_{seed}), \rho \rangle \Downarrow v_{final}}{\langle \text{cycle } e_{seed} \mid> \{...\}, \rho \rangle \Downarrow v_{final}}$

(Details: Each cycle arm matches state and either continues (recurse) or finishes (returns value).)

### 6. Break/continue/return
- `<< expr` in cycle: terminates loop, returns value.
- `>> expr` in cycle: continues with new state.

### 7. Error model
- Any rule may yield $\Downarrow_{err} \langle k, s \rangle$ if evaluation fails with error kind $k$ at span $s$.
- Error kinds: lex, parse, runtime, internal.
- Spans: always reported as (line, column), 1-based.

## Undefined/out-of-scope
- Concurrency, async, JIT, macros, static typing, module system beyond current MVP.
- Any behavior not covered by the above rules is undefined.

---

**See also:**
- [docs/RESEARCH.md](RESEARCH.md)
- [docs/SPEC_V1_SCOPE.md](SPEC_V1_SCOPE.md)
- [docs/COMPARISON.md](COMPARISON.md)
