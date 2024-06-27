from enum import Enum, auto


class TokenTypes(Enum):

    TK_IDENTIFIER = auto()
    TK_NEW = auto()
    TK_ARRAY = auto()
    TK_SORT = auto()
    TK_SAVE = auto()
    TK_ASC = auto()
    TK_TRUE = auto()
    TK_FALSE = auto()

    TK_EQUAL = auto()
    TK_COMMA = auto()
    TK_DOT = auto()
    TK_SEMICOLON = auto()
    TK_LPARENTHESIS = auto()
    TK_RPARENTHESIS = auto()
    TK_LBRACKET = auto()
    TK_RBRACKET = auto()

    TK_NUMBER = auto()
    TK_STRING = auto()

    TK_ERROR = auto()
    TK_EOF = auto()