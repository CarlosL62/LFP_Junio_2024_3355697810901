from enum import Enum, auto


class TokenTypes(Enum):
    # specified tokens for the lexer
    STRING = auto()

    SIMBOL = auto()  # simbolo
    # operators
    ASSIGN = auto()  # ->
    GREATER = auto()  # >
    COLON = auto()  # :

    # delimiters
    LBRAKET = auto()  # [
    RBRAKET = auto()  # ]
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    SEMICOLON = auto()  # ;
    COMMA = auto()  # ,
    DOTDOTDOT = auto()  # ...

    # keywords
    KEYWORD = auto()  # nombre, nodos, conexiones
    NAME = auto() # nombre
    NODES = auto() # nodos
    CONECTIONS = auto() # conexiones

    # errors
    ERROR = auto()  # error token