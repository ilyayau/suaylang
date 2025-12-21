import sys
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.compiler import Compiler
from suaylang.vm import VM

def main():
    import argparse
    parser = argparse.ArgumentParser(description="SuayLang VM CLI")
    parser.add_argument("file", help=".suay file to run")
    args = parser.parse_args()
    with open(args.file, "r", encoding="utf-8") as f:
        src = f.read()
    tokens = Lexer(src, filename=args.file).tokenize()
    program = Parser(tokens, src, filename=args.file).parse_program()
    code = Compiler().compile_program(program, name=args.file)
    vm = VM(source=src, filename=args.file)
    result, _ = vm.run_with_stats(code)
    print(result)

if __name__ == "__main__":
    main()
