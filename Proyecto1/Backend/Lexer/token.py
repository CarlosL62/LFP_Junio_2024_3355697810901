class Token:
    def __init__(self, type, lexeme, line, column):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token: {self.type.name}, Lexema: {self.lexeme}, Linea: {self.line}, Columna: {self.column}"