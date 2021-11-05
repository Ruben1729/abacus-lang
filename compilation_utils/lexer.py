from compilation_utils.tokens import LexicalTokens
import re


class Lexer(object):
    def __init__(self):
        self.regex_rules = []
        self.tokens = []

    def add_regex_rule(self, regex_rule: str):
        self.regex_rules.append(str)

    def set_regex_rules(self, regex_rules: list):
        self.regex_rules = regex_rules

    def tokenize(self, file_path: str):
        file = open(file_path, "r")
        code = file.read()
        file.close()

        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.regex_rules)
        line = 1
        start = 0

        for match in re.finditer(tok_regex, code):
            kind = match.lastgroup
            value = match.group()
            col = match.start() - start

            if LexicalTokens.get_id(kind) == LexicalTokens.LITERAL:
                value = float(value) if '.' in value else int(value)

            self.tokens.append((kind, (line, col), value))


lexer = Lexer()
lexer.set_regex_rules([
    ('NEWLINE', r'\n'),
    ('WHITE_SPACE', r'[ \t]+'),
    ('KEYWORD', r'(while)|(if)|(for)|(do)|(end)|(else)'),
    ('LITERAL', r'\d+(\.\d*)?'),
    ('OPERATOR', r'[+\-*/]'),
    ('STRING_LITERAL', r'"(?:\\["\\]|[^\n"\\])*"'),
    ('IDENTIFIER', r'[a-zA-Z][a-zA-Z_0-9]*'),
])
