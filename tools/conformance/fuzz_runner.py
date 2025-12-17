from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from suaylang.conformance import compare_observations, observe_interpreter, observe_vm


@dataclass(frozen=True)
class FuzzStats:
    seed: int
    n: int
    divergences: int
    ok: int
    runtime_errors: int
    lex_errors: int
    parse_errors: int
    internal_errors: int


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _gen_ident(rng: random.Random) -> str:
    # Keep names ASCII for readability in reports.
    return rng.choice(["a", "b", "c", "x", "y", "z", "n", "i", "acc"]) + str(
        rng.randrange(0, 20)
    )


def _gen_int(rng: random.Random, *, lo: int = -10, hi: int = 10) -> int:
    return rng.randrange(lo, hi + 1)


def _int_expr(rng: random.Random, *, lo: int = -10, hi: int = 10) -> str:
    v = _gen_int(rng, lo=lo, hi=hi)
    if v >= 0:
        return str(v)
    return f"(0 − {abs(v)})"


def _gen_small_list_expr(rng: random.Random) -> list[str]:
    n = rng.randrange(0, 8)
    return [_int_expr(rng, lo=-5, hi=9) for _ in range(n)]


def _expr(rng: random.Random, *, depth: int) -> str:
    if depth <= 0:
        leaf = rng.choice(["int", "bool", "unit"])
        if leaf == "int":
            return _int_expr(rng)
        if leaf == "bool":
            return rng.choice(["⊤", "⊥"])
        return "ø"

    kind = rng.choice(
        [
            "int",
            "bool",
            "unit",
            "binary",
            "tuple",
            "list",
            "variant",
        ]
    )

    if kind == "int":
        return _int_expr(rng)
    if kind == "bool":
        return rng.choice(["⊤", "⊥"])
    if kind == "unit":
        return "ø"

    if kind == "tuple":
        a = _expr(rng, depth=depth - 1)
        b = _expr(rng, depth=depth - 1)
        return f"({a} {b})"

    if kind == "list":
        xs = _gen_small_list_expr(rng)
        return "[" + " ".join(xs) + "]"

    if kind == "variant":
        tag = rng.choice(["Ok", "Err"])  # small set, stable across engines
        payload = _expr(rng, depth=depth - 1)
        return f"{tag}•({payload})"

    # binary
    op = rng.choice(["+", "−", "×", "%", "=", "≠", "<", "≤", ">", "≥"])
    left = _expr(rng, depth=depth - 1)
    right = _expr(rng, depth=depth - 1)
    return f"({left} {op} {right})"


_TEMPLATES = ["arith", "dispatch", "cycle_sum", "map_fold", "fib", "undef_name"]


def _program_template(rng: random.Random, *, subset_templates: set[str] | None) -> str:
    # Choose between a handful of templates. The goal is to produce programs that:
    # - terminate quickly
    # - are supported by the VM compiler
    # - sometimes exercise stdout via `say`
    allowed = _TEMPLATES
    if subset_templates is not None:
        unknown = sorted(set(subset_templates) - set(_TEMPLATES))
        if unknown:
            raise ValueError(f"Unknown templates in --subset: {unknown}")
        allowed = sorted(subset_templates)
    t = rng.choice(list(allowed))

    if t == "arith":
        x = _gen_ident(rng)
        y = _gen_ident(rng)
        e1 = _expr(rng, depth=3)
        e2 = _expr(rng, depth=3)
        final = _expr(rng, depth=3)
        return f"{x} ← {e1}\n{y} ← {e2}\nsay · (text · ({final}))\n{x} + {y}\n"

    if t == "dispatch":
        classify = _gen_ident(rng)
        n = rng.randrange(0, 30)
        return (
            f"{classify} ← ⌁(v)\n"
            "  v ▷ ⟪\n"
            "  ▷ Ok•x  ⇒ x + 1\n"
            "  ▷ Err•x ⇒ x + 2\n"
            "  ▷ _     ⇒ 0\n"
            "  ⟫\n"
            f"say · (text · ({classify} · (Ok•{n})))\n"
            f"{classify} · (Err•{n})\n"
        )

    if t == "cycle_sum":
        limit = rng.randrange(0, 200)
        return (
            "sum_to ← ⌁(n)\n"
            "  ⟲ (Step•(1 0)) ▷ ⟪\n"
            "  ▷ Done•acc     ⇒ ↯ acc\n"
            "  ▷ Step•(i acc) ⇒ ↩ (\n"
            "        (i > n) ▷ ⟪\n"
            "        ▷ ⊤ ⇒ Done•acc\n"
            "        ▷ ⊥ ⇒ Step•(i + 1  acc + i)\n"
            "        ⟫\n"
            "      )\n"
            "  ⟫\n"
            f"say · (text · (sum_to · {limit}))\n"
            f"sum_to · {limit}\n"
        )

    if t == "map_fold":
        xs = _gen_small_list_expr(rng)
        # Keep it deterministic and small.
        # total = fold (
        #   (a b) => a + (2*b + 1)
        # ) 0 (map (x)=>x [..])
        return (
            "xs ← [" + " ".join(xs) + "]\n"
            "ys ← map · (⌁(x) (2 × x) + 1) · xs\n"
            "total ← fold · (⌁(a b) a + b) · 0 · ys\n"
            "say · (text · total)\n"
            "total\n"
        )

    if t == "fib":
        n = rng.randrange(0, 25)
        return (
            "fib ← ⌁(n)\n"
            "  ⟲ (State•(0 0 1)) ▷ ⟪\n"
            "  ▷ Done•x           ⇒ ↯ x\n"
            "  ▷ State•(i a b)    ⇒ ↩ (\n"
            "        (i ≥ n) ▷ ⟪\n"
            "        ▷ ⊤ ⇒ Done•a\n"
            "        ▷ ⊥ ⇒ State•(i + 1  b  a + b)\n"
            "        ⟫\n"
            "      )\n"
            "  ⟫\n"
            f"say · (text · (fib · {n}))\n"
            f"fib · {n}\n"
        )

    # undef_name: trigger a runtime error in a controlled way.
    # This exercises termination behavior + error classification.
    name = _gen_ident(rng)
    return f"{name}\n"


def run_fuzz(
    *,
    n: int,
    seed: int,
    save_dir: Path,
    fail_fast: bool,
    save_non_ok: bool,
    save_non_ok_limit: int,
    subset_templates: set[str] | None = None,
    on_case: Callable[[int, int, str, Any, Any, bool, str], None] | None = None,
) -> tuple[FuzzStats, list[Path]]:
    rng = random.Random(seed)

    divergences = 0
    ok = 0
    runtime_errors = 0
    lex_errors = 0
    parse_errors = 0
    internal_errors = 0

    saved: list[Path] = []
    saved_non_ok: dict[str, int] = {"runtime": 0, "lex": 0, "parse": 0, "internal": 0}

    for i in range(1, n + 1):
        src = _program_template(rng, subset_templates=subset_templates)
        filename = f"<fuzz:{seed}:{i}>"
        interp = observe_interpreter(src, filename=filename)
        vm = observe_vm(src, filename=filename)
        res = compare_observations(interp, vm)

        if on_case is not None:
            on_case(i, seed, src, interp, vm, bool(res.ok), str(res.reason))

        if res.ok:
            if interp.termination == "ok":
                ok += 1
            elif interp.termination == "runtime":
                runtime_errors += 1
                if save_non_ok and saved_non_ok["runtime"] < save_non_ok_limit:
                    case_dir = save_dir / f"seed_{seed}" / f"non_ok_{i:06d}_runtime"
                    _write_text(case_dir / "program.suay", src)
                    _write_text(
                        case_dir / "observations.json",
                        json.dumps(
                            {
                                "seed": seed,
                                "i": i,
                                "interp": asdict(interp),
                                "vm": asdict(vm),
                            },
                            indent=2,
                            sort_keys=True,
                        )
                        + "\n",
                    )
                    saved.append(case_dir / "program.suay")
                    saved_non_ok["runtime"] += 1
            elif interp.termination == "lex":
                lex_errors += 1
                if save_non_ok and saved_non_ok["lex"] < save_non_ok_limit:
                    case_dir = save_dir / f"seed_{seed}" / f"non_ok_{i:06d}_lex"
                    _write_text(case_dir / "program.suay", src)
                    _write_text(
                        case_dir / "observations.json",
                        json.dumps(
                            {
                                "seed": seed,
                                "i": i,
                                "interp": asdict(interp),
                                "vm": asdict(vm),
                            },
                            indent=2,
                            sort_keys=True,
                        )
                        + "\n",
                    )
                    saved.append(case_dir / "program.suay")
                    saved_non_ok["lex"] += 1
            elif interp.termination == "parse":
                parse_errors += 1
                if save_non_ok and saved_non_ok["parse"] < save_non_ok_limit:
                    case_dir = save_dir / f"seed_{seed}" / f"non_ok_{i:06d}_parse"
                    _write_text(case_dir / "program.suay", src)
                    _write_text(
                        case_dir / "observations.json",
                        json.dumps(
                            {
                                "seed": seed,
                                "i": i,
                                "interp": asdict(interp),
                                "vm": asdict(vm),
                            },
                            indent=2,
                            sort_keys=True,
                        )
                        + "\n",
                    )
                    saved.append(case_dir / "program.suay")
                    saved_non_ok["parse"] += 1
            else:
                internal_errors += 1
                if save_non_ok and saved_non_ok["internal"] < save_non_ok_limit:
                    case_dir = save_dir / f"seed_{seed}" / f"non_ok_{i:06d}_internal"
                    _write_text(case_dir / "program.suay", src)
                    _write_text(
                        case_dir / "observations.json",
                        json.dumps(
                            {
                                "seed": seed,
                                "i": i,
                                "interp": asdict(interp),
                                "vm": asdict(vm),
                            },
                            indent=2,
                            sort_keys=True,
                        )
                        + "\n",
                    )
                    saved.append(case_dir / "program.suay")
                    saved_non_ok["internal"] += 1
            continue

        divergences += 1
        case_dir = save_dir / f"seed_{seed}" / f"case_{i:06d}"
        src_path = case_dir / "program.suay"
        meta_path = case_dir / "observations.json"
        _write_text(src_path, src)
        _write_text(
            meta_path,
            json.dumps(
                {
                    "seed": seed,
                    "i": i,
                    "reason": res.reason,
                    "interp": asdict(interp),
                    "vm": asdict(vm),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
        )
        saved.append(src_path)

        if fail_fast:
            break

    stats = FuzzStats(
        seed=seed,
        n=n,
        divergences=divergences,
        ok=ok,
        runtime_errors=runtime_errors,
        lex_errors=lex_errors,
        parse_errors=parse_errors,
        internal_errors=internal_errors,
    )
    return stats, saved


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="suay-fuzz",
        description="Differential fuzzing: Interpreter vs VM (safe subset)",
    )
    ap.add_argument("--n", type=int, default=2000, help="Number of programs to test")
    ap.add_argument("--seed", type=int, default=0, help="PRNG seed (reproducible)")
    ap.add_argument(
        "--save-dir",
        type=Path,
        default=Path("tools/conformance/fuzz_failures"),
        help="Where to save repro cases on divergence",
    )
    ap.add_argument(
        "--no-fail-fast",
        action="store_true",
        help="Keep running after divergences (still saves each repro case)",
    )
    ap.add_argument(
        "--save-non-ok",
        action="store_true",
        help="Also save a small number of non-ok (runtime/parse/lex) cases for inspection",
    )
    ap.add_argument(
        "--save-non-ok-limit",
        type=int,
        default=5,
        help="Max number of non-ok cases to save when --save-non-ok is set",
    )
    args = ap.parse_args()

    stats, saved = run_fuzz(
        n=args.n,
        seed=args.seed,
        save_dir=args.save_dir,
        fail_fast=not args.no_fail_fast,
        save_non_ok=bool(args.save_non_ok),
        save_non_ok_limit=int(args.save_non_ok_limit),
    )

    print("differential fuzzing: interpreter vs vm")
    print(
        f"seed={stats.seed} N={stats.n} divergences={stats.divergences} ok={stats.ok} "
        f"runtime={stats.runtime_errors} lex={stats.lex_errors} parse={stats.parse_errors} internal={stats.internal_errors}"
    )

    if stats.divergences:
        print("saved repro cases:")
        for p in saved[:10]:
            print(f"- {p}")
        if len(saved) > 10:
            print(f"... ({len(saved)} total)")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
