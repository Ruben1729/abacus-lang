from enum import IntEnum, Enum, auto


class LexicalTokens(Enum):
    KEYWORD = 'KEYWORD'  # pop, swap
    IDENTIFIER = 'IDENTIFIER'  # int, double
    LITERAL = 'LITERAL'  # 23, 24, 64
    STRING_LITERAL = 'STRING_LITERAL'  # "Hello World"
    OPERATOR = 'OPERATOR'  # * + - /
    NEWLINE = 'NEWLINE'  # \n
    WHITE_SPACE = 'WHITE_SPACE'  # \t

    @classmethod
    def get_id(cls, key):
        return cls(key)


class StackTypes(IntEnum):
    INT = auto()
    LONG = auto()
    DOUBLE = auto()
    PTR = auto()
    OPERATION = auto()
