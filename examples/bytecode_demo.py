import os
import sys

# Allow running from a source checkout without installation.
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.compiler import Compiler
from suaylang.vm import VM


def main() -> int:
    path = os.path.join(ROOT, "examples", "hello.suay")
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tokens = Lexer(src, filename=path).tokenize()
    program = Parser(tokens, src, filename=path).parse_program()

    code = Compiler().compile_program(program, name="hello")
    print("== Bytecode ==")
    print(code.disassemble())
    print("== Execute ==")
    VM(source=src, filename=path).run(code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
