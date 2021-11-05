import sys
from compilation_utils.lexer import lexer

file_path = sys.argv[2]

lexer.tokenize(file_path)
