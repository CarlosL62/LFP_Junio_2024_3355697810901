class Error:
    def __init__(self, token, lexeme, line, column) -> None:
        self.token = token
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __str__(self):
        return f'Error: {self.token}, Lexema: {self.lexeme}, Linea: {self.line}, Columna: {self.column}'