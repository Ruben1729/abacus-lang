from compilation_utils.tokens import LexicalTokens
import re


regex_rules = ([
    ('NEWLINE', r'\n'),
    ('WHITE_SPACE', r'[ \t]+'),
    ('KEYWORD', r'(pop)|(print_char)|(\[print_char\])|(print)|(dup)|(copy)|(over)|(fall)|(swap)|(while)|(for)|(do)|'
                r'(end)|(if)|(else)|(elif)|(fn)|(ret)|(let)|(\[print\])|(\[dup\])|(\[copy\])|(\[over\])|(\[fall\])'
                r'|(sizeof)|(int)|(bool)|(char)|(include)'),
    ('LITERAL', r'\d+(\.\d*)?'),
    ('OPERATOR', r'([+\/\-*%><=]|==|!=|<=|>=)'),
    ('MODIFIER', r'\[\d*\]'),
    ('COMMENT', 'r[#]'),
    ('STRING_LITERAL', r'"(?:\\["\\]|[^\n"\\])*"'),
    ('IDENTIFIER', r'[a-zA-Z][a-zA-Z_0-9]*'),
])


def tokenize(file_path: str):
    file = open(file_path, "r")
    code = file.read()
    file.close()

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in regex_rules)
    line = 1
    start = 0

    tokens = []

    is_include = False

    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()
        col = match.start() - start

        if LexicalTokens.get_id(kind) == LexicalTokens.LITERAL:
            value = float(value) if '.' in value else int(value)
        elif LexicalTokens.get_id(kind) == LexicalTokens.STRING_LITERAL:
            if is_include:
                tokens += tokenize(value[1:-1])
                is_include = False
        elif LexicalTokens.get_id(kind) == LexicalTokens.KEYWORD:
            is_include = True if value == "include" else False
        elif LexicalTokens.get_id(kind) == LexicalTokens.NEWLINE:
            start = match.end()
            line += 1

        tokens.append((LexicalTokens.get_id(kind), value, (line, col)))

    return tokens

