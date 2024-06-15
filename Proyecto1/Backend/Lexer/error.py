class Error:
    def __init__(self, type, lexeme, line, column) -> None:
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __str__(self):
        return f'Error: {self.type.name}, Lexema: {self.lexeme}, Linea: {self.line}, Columna: {self.column}'