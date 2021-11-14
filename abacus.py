import sys
from compilation_utils.lexer import tokenize
from compilation_utils.parser import parse_tokens, generate_asm, static_type_check
from compilation_utils.asm_generator import asm_generator
from compilation_utils.compiler import AbacusCompiler


file_path = sys.argv[len(sys.argv) - 1]

tokens = tokenize(file_path)
print(tokens)
instructions = parse_tokens(tokens)
type_ins = instructions.copy()
generate_asm(instructions)
# static_type_check(type_ins)

compiler = AbacusCompiler(file_path, asm_generator)


doCompile = "-c" in sys.argv or "--compile" in sys.argv
doGenerate = "-g" in sys.argv or "--generate" in sys.argv
doBuild = "-b" in sys.argv or "--build" in sys.argv
doLink = "-l" in sys.argv or "--link" in sys.argv
doRun = "-r" in sys.argv or "--run" in sys.argv

if doCompile or doGenerate:
    compiler.generate()
if doCompile or doBuild:
    compiler.build()
if doCompile or doLink:
    compiler.link()

if doRun:
    compiler.execute()
