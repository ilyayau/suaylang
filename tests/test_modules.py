import os
import tempfile
import unittest
import io
from contextlib import redirect_stdout

from suaylang.interpreter import run_source
from suaylang.runtime import SuayRuntimeError


class ModuleTests(unittest.TestCase):
    def _run_quiet(self, src: str, *, filename: str) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            run_source(src, filename=filename)

    def test_link_loads_value_from_module(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            math_path = os.path.join(d, "math.suay")
            main_path = os.path.join(d, "main.suay")

            with open(math_path, "w", encoding="utf-8") as f:
                f.write("x ← 41\n")

            with open(main_path, "w", encoding="utf-8") as f:
                f.write('m ← link · "./math"\n')
                f.write('say · (m · "x")\n')

            with open(main_path, "r", encoding="utf-8") as f:
                src = f.read()
            self._run_quiet(src, filename=main_path)

    def test_link_rejects_private_names(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            mod_path = os.path.join(d, "m.suay")
            main_path = os.path.join(d, "main.suay")

            with open(mod_path, "w", encoding="utf-8") as f:
                f.write("_p ← 1\n")

            with open(main_path, "w", encoding="utf-8") as f:
                f.write('m ← link · "./m"\n')
                f.write('say · (m · "_p")\n')

            with open(main_path, "r", encoding="utf-8") as f:
                src = f.read()
            with self.assertRaises(SuayRuntimeError) as ctx:
                self._run_quiet(src, filename=main_path)
            self.assertIn("private", str(ctx.exception))

    def test_link_detects_circular_module_load(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            a_path = os.path.join(d, "a.suay")
            b_path = os.path.join(d, "b.suay")
            main_path = os.path.join(d, "main.suay")

            with open(a_path, "w", encoding="utf-8") as f:
                f.write('b ← link · "./b"\n')
                f.write('_force ← b · "y"\n')
                f.write("x ← 1\n")

            with open(b_path, "w", encoding="utf-8") as f:
                f.write('a ← link · "./a"\n')
                f.write('_force ← a · "x"\n')
                f.write("y ← 2\n")

            with open(main_path, "w", encoding="utf-8") as f:
                f.write('a ← link · "./a"\n')
                f.write('say · (a · "x")\n')

            with open(main_path, "r", encoding="utf-8") as f:
                src = f.read()
            with self.assertRaises(SuayRuntimeError) as ctx:
                self._run_quiet(src, filename=main_path)
            self.assertIn("Circular module load", str(ctx.exception))

    def test_link_caches_modules_within_run(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            mod_path = os.path.join(d, "m.suay")
            main_path = os.path.join(d, "main.suay")

            # If the module re-executed, this would fail due to duplicate binding.
            with open(mod_path, "w", encoding="utf-8") as f:
                f.write("x ← 1\n")

            with open(main_path, "w", encoding="utf-8") as f:
                f.write('m1 ← link · "./m"\n')
                f.write('m2 ← link · "./m"\n')
                f.write('say · ((m1 · "x") = (m2 · "x"))\n')

            with open(main_path, "r", encoding="utf-8") as f:
                src = f.read()
            self._run_quiet(src, filename=main_path)
