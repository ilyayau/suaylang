import os
import subprocess
import tempfile
import unittest


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUAY = os.path.join(REPO_ROOT, "suay")


def _run_cli(
    cmd: str, src: str, *, timeout_s: float = 10.0
) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".suay", delete=False, encoding="utf-8"
    ) as f:
        f.write(src)
        path = f.name
    try:
        return subprocess.run(
            [SUAY, cmd, path],
            text=True,
            capture_output=True,
            cwd=REPO_ROOT,
            timeout=timeout_s,
        )
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


class StressTests(unittest.TestCase):
    def assertNoTraceback(self, p: subprocess.CompletedProcess[str]) -> None:
        combined = (p.stdout or "") + "\n" + (p.stderr or "")
        self.assertNotIn("Traceback (most recent call last)", combined)

    # --- Malformed programs ---

    def test_malformed_unexpected_character_is_clean_error(self) -> None:
        p = _run_cli("check", "say · @\n")
        self.assertNotEqual(p.returncode, 0)
        self.assertNoTraceback(p)
        self.assertIn("lexical error", p.stderr)

    def test_malformed_unterminated_string_is_clean_error(self) -> None:
        p = _run_cli("check", 'say · "unterminated\n')
        self.assertNotEqual(p.returncode, 0)
        self.assertNoTraceback(p)
        self.assertIn("lexical error", p.stderr)

    def test_malformed_dispatch_missing_fat_arrow_is_clean_error(self) -> None:
        # Missing ⇒
        p = _run_cli("check", "1 ▷ ⟪ ▷ _ 1 ⟫\n")
        self.assertNotEqual(p.returncode, 0)
        self.assertNoTraceback(p)
        self.assertIn("syntax error", p.stderr)

    # --- Deeply nested expressions ---

    def test_deeply_nested_parentheses_do_not_crash(self) -> None:
        # Goal: trigger parser recursion limit and ensure we still surface a clean ParseError.
        depth = 1800
        src = ("(" * depth) + "1" + (")" * depth) + "\n"
        p = _run_cli("check", src, timeout_s=10.0)
        self.assertNotEqual(p.returncode, 0)
        self.assertNoTraceback(p)
        self.assertIn("error", p.stderr)

    # --- Large recursion depth (runtime) ---

    def test_large_recursion_depth_is_clean_runtime_error(self) -> None:
        # No 'if' in the language; use dispatch as a base-case conditional.
        # This should eventually hit Python recursion limits (or run very slowly), but must not traceback.
        src = (
            "loop ← ⌁(n) n ▷ ⟪\n"
            "  ▷ 0 ⇒ 0\n"
            "  ▷ _ ⇒ loop · (n - 1)\n"
            "⟫\n"
            "say · (loop · 2000)\n"
        )
        p = _run_cli("run", src, timeout_s=10.0)
        self.assertNotEqual(p.returncode, 0)
        self.assertNoTraceback(p)
        self.assertIn("runtime error", p.stderr)

    # --- Large number of variables ---

    def test_many_bindings_parse_successfully(self) -> None:
        # Stress lexer+parser and scope bookkeeping without executing heavy work.
        # Keep size moderate so CI/dev runs stay fast.
        n = 3000
        lines = [f"x{i} ← {i}" for i in range(n)]
        lines.append("say · x2999")
        src = "\n".join(lines) + "\n"
        p = _run_cli("check", src, timeout_s=10.0)
        self.assertEqual(p.returncode, 0, msg=p.stderr)
        self.assertNoTraceback(p)

    # --- Worst-case-ish parsing scenarios ---

    def test_long_left_associative_chain_parses(self) -> None:
        # Long chain of infix ops: should not be quadratic or blow recursion.
        n = 8000
        expr = " + ".join(["1"] * n)
        src = f"say · ({expr})\n"
        p = _run_cli("check", src, timeout_s=10.0)
        self.assertEqual(p.returncode, 0, msg=p.stderr)
        self.assertNoTraceback(p)
