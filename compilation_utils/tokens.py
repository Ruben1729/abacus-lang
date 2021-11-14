from enum import IntEnum, Enum, auto

iota_counter = -1


def iota(restart=False):
    global iota_counter
    if restart:
        iota_counter = -1
    iota_counter += 1
    return iota_counter


class KeywordTokens(object):
    DUPLICATE = {
        "dup": "[esp]",
        "over": "[esp + 4]",
        "copy": "[esp + 4 * eax]",
        "[dup]": "[esp]",
        "[over]": "[esp + 4]",
        "[copy]": "[esp + 4 * eax]",
    }

    POP = ["pop", "print", "[print]", "drop", "[drop]"]

    FOR_COND = iota()
    WHILE_COND = iota()
    IF_COND = iota()
    ELIF_COND = iota()
    ELSE_COND = iota()
    FN_COND = iota()

    COND = {
        "if": IF_COND,
        "elif": ELIF_COND,
        "else": ELSE_COND
    }

    LOOPS = {
        "while": WHILE_COND,
        "for": FOR_COND,
    }


class OperatorTokens(object):
    CONDITIONS = {
        "!=": "ne",
        "<": "l",
        ">": "g",
        "==": "e",
        ">=": "ge",
        "<=": "le"
    }

    BASIC = {
        "+": "add",
        "-": "sub",
        "*": "imul",
        "u*": "mul"
    }

    DIV = {
        "/": "eax",
        "%": "edx"
    }


class ConditionalInstructions(Enum):
    WHILE = 'while'
    FOR = 'for'

    FN = 'fn'

    IF = 'if'
    ELIF = 'elif'
    ELSE = 'else'

    END = 'end'
    DO = 'do'


class StackInstructions(Enum):
    PUSH = 'push'

    SWAP = 'swap'

    POP = 'pop'
    PRINT = 'print'
    PRINT_CHAR = 'printchar'

    FALL = 'fall'

    DUP = 'dup'
    OVER = 'over'
    COPY = 'copy'


class IdentifierInstructions(Enum):
    SIZEOF = 'sizeof'

    CREATE = 'create'
    UPDATE = 'update'
    FUNCTION = 'fn'


LiteralOperations = ["!=", "<", ">", "==", ">=", "<=", "=", "+", "-", "*", "u*", "/", "%"]


class ValueType(IntEnum):
    INT = auto()
    BOOL = auto()
    ARR = auto()
    PTR = auto()


class LexicalTokens(Enum):
    KEYWORD = 'KEYWORD'  # pop, swap, int, double
    IDENTIFIER = 'IDENTIFIER'  # user defined variables
    LITERAL = 'LITERAL'  # 23, 24, 64
    STRING_LITERAL = 'STRING_LITERAL'  # "Hello World"
    OPERATOR = 'OPERATOR'  # * + - /
    COMMENT = 'COMMENT'  # #
    MODIFIER = 'MODIFIER'  # [], int
    NEWLINE = 'NEWLINE'  # \n
    WHITE_SPACE = 'WHITE_SPACE'  # \t

    @classmethod
    def get_id(cls, key):
        return cls(key)


class StackTypes(Enum):
    INT = 'int'
    LONG = 'long'
    DOUBLE = 'double'
    BOOL = 'bool'
    CHAR = 'char'
    PTR = 'ptr'
    OPERATION = 'op'

    @classmethod
    def getId(cls, key):
        return cls(key)


typesSize = {
    StackTypes.INT: 4,
    StackTypes.CHAR: 4,
    StackTypes.BOOL: 4
}
