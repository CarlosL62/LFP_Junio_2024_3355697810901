class Token:
    def __init__(self, token, lexeme, line, column):
        self.token = token
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token: {self.token}, Lexema: {self.lexeme}, Linea: {self.line}, Columna: {self.column}"