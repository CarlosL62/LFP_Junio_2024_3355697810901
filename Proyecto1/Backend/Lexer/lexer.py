from Backend.Lexer.token import Token
from Backend.Lexer.error import Error
from Backend.Lexer.tokenTypes import TokenTypes

class Lexer:

    def __init__(self, textEntry):
        self.textEntry = textEntry
        self.validTokens = []
        self.errorTokens = []

    def recognizeSimbols(self, validTokens):
        for token in validTokens:
            if token.lexeme == ';':
                token.type = TokenTypes.SEMICOLON
            elif token.lexeme == '[':
                token.type = TokenTypes.LBRAKET
            elif token.lexeme == ']':
                token.type = TokenTypes.RBRAKET
            elif token.lexeme == ':':
                token.type = TokenTypes.COLON
            elif token.lexeme == ',':
                token.type = TokenTypes.COMMA
            elif token.lexeme == '>':
                token.type = TokenTypes.GREATER

    def isValidCharacter(self, character):
        return character in [';', '[', ']', ':', ',', '>']

    def isWhitespace(self, character):
        return character in [' ', '\t', '\n']

    def add_token(self, type, lexeme, line, start_column, end_column):
        token = Token(type=type, lexeme=lexeme, line=line, column=start_column)
        self.validTokens.append(token)

    def add_error(self, lexeme, line, start_column, end_column):
        error = Error(type=TokenTypes.ERROR, lexeme=lexeme, line=line, column=start_column)
        self.errorTokens.append(error)

    def analyze(self):
        line = 1
        column = 1
        lexeme = ""
        status = 0
        start_column = 1

        i = 0
        while i < len(self.textEntry):
            character = self.textEntry[i]
            print(f'Procesando carácter: {character} ({line}, {column}), Estado: {status}')

            if status == 0:
                if character.isalpha():
                    lexeme += character
                    status = 1
                    start_column = column
                elif character == "-":
                    lexeme += character
                    status = 2
                    start_column = column
                elif character == "'":
                    lexeme += character
                    status = 3
                    start_column = column
                elif self.isValidCharacter(character):
                    lexeme += character
                    self.add_token(TokenTypes.SIMBOL, lexeme, line, column, column)
                    lexeme = ""
                elif character == '.':
                    lexeme += character
                    status = 5
                    start_column = column
                elif self.isWhitespace(character):
                    if character == '\n':
                        line += 0
                        column = 0
                else:
                    self.add_error(character, line, column, column)
            elif status == 1:
                if character.isalnum():
                    lexeme += character
                else:
                    if lexeme == "nombre":
                        self.add_token(TokenTypes.NAME, lexeme, line, start_column, column)
                    elif lexeme == "nodos":
                        self.add_token(TokenTypes.NODES, lexeme, line, start_column, column)
                    elif lexeme == "conexiones":
                        self.add_token(TokenTypes.CONECTIONS, lexeme, line, start_column, column)
                    else:
                        self.add_error(lexeme, line, start_column, column)
                    lexeme = ""
                    status = 0
                    continue
            elif status == 2:
                if character == ">":
                    lexeme += character
                    self.add_token(TokenTypes.ASSIGN, lexeme, line, start_column, column)
                    lexeme = ""
                    status = 0
                else:
                    self.add_error(lexeme, line, start_column, column)
                    lexeme = ""
                    status = 0
            elif status == 3:
                if character == "'":
                    lexeme += character
                    self.add_token(TokenTypes.STRING, lexeme, line, start_column, column)
                    lexeme = ""
                    status = 0
                else:
                    lexeme += character
            elif status == 5:
                if character == '.':
                    lexeme += character
                    if lexeme == '...':
                        self.add_token(TokenTypes.DOTDOTDOT, lexeme, line, start_column, column)
                        lexeme = ""
                        status = 0
                else:
                    self.add_error(lexeme, line, start_column, column)
                    lexeme = ""
                    status = 0

            if character == '\n':
                line += 1
                column = 0
            column += 1
            i += 1

        if status == 1:
            if lexeme == "nombre":
                self.add_token(TokenTypes.NAME, lexeme, line, start_column, column)
            elif lexeme == "nodos":
                self.add_token(TokenTypes.NODES, lexeme, line, start_column, column)
            elif lexeme == "conexiones":
                self.add_token(TokenTypes.CONECTIONS, lexeme, line, start_column, column)
            else:
                self.add_error(lexeme, line, start_column, column)
        elif status == 3:
            self.add_error(lexeme, line, start_column, column)

        # recognize simbols
        self.recognizeSimbols(self.validTokens)

        print(f'Análisis completado. Último estado: {status}')
