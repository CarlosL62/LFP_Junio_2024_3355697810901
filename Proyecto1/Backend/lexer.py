class Lexer:
    def __init__(self, textEntry):
        self.textEntry = textEntry

    token = {"token": "IDENTIFICADOR", "lexeme": "num1", "line": "1", "column": "1"}
    validTokens = []
    errorTokens = []
    validTokens.append(token)
    print(validTokens)

    def isValidCharacter(self, character):
        return character in [';', '[', ']', ':', ',', '{', '}', '>']

    def isWhitespace(self, character):
        return character in [' ', '\t', '\n']

    def analyze(self):
        line = 1
        column = 1
        lexeme = ""

        status = 0

        for character in self.textEntry:
            print(f'Procesando carácter: {character} ({line}, {column}), Estado: {status}')

            if status == 0:
                if character.isalpha():
                    lexeme += character
                    status = 1
                    print(f'Estado 1: {lexeme}')
                elif character == "-":
                    lexeme += character
                    status = 2
                    print(f'Estado 2: {lexeme}')
                elif character == "'":
                    lexeme += character
                    status = 3
                    print(f'Estado 3: {lexeme}')
                elif self.isValidCharacter(character):
                    lexeme += character
                    status = 4
                    print(f'Estado 4: {lexeme}')
                elif self.isWhitespace(character):
                    if character == '\n':
                        line += 1
                        column = 0
                    # Los espacios en blanco y saltos de línea son ignorados
                else:
                    print(f'ERROR LÉXICO: {character} ({line}, {column})')
                    token = {"token": "ERROR LÉXICO", "lexeme": character, "line": line, "column": column}
                    self.errorTokens.append(token)
            elif status == 1:
                if character.isalnum():
                    lexeme += character
                    print(f'Estado 1: {lexeme}')
                else:
                    print(f'Token IDENTIFICADOR: {lexeme} ({line}, {column})')
                    token = {"token": "IDENTIFICADOR", "lexeme": lexeme, "line": line, "column": column}
                    self.validTokens.append(token)
                    print(f'ERROR LÉXICO: {character} ({line}, {column})')
                    token = {"token": "ERROR LÉXICO", "lexeme": character, "line": line, "column": column}
                    self.errorTokens.append(token)
                    lexeme = ""
                    status = 0
                    continue
            elif status == 2:
                if character == ">":
                    lexeme += character
                    print(f'Token ARROW: {lexeme} ({line}, {column})')
                    lexeme = ""
                    status = 0
                else:
                    print(f'ERROR LÉXICO: {character} ({line}, {column})')
                    lexeme = ""
                    status = 0
            elif status == 3:
                if character == "'":
                    lexeme += character
                    print(f'Token STRING: {lexeme} ({line}, {column})')
                    lexeme = ""
                    status = 0
                else:
                    lexeme += character
                    print(f'Estado 3: {lexeme}')
            elif status == 4:
                print(f'Token SIMBOLO: {lexeme} ({line}, {column})')
                lexeme = ""
                status = 0

            # increase line and column
            if character == '\n':
                line += 1
                column = 1
            else:
                column += 1

        # ends the analysis
        if status == 1:
            print(f'Token IDENTIFICADOR: {lexeme} ({line}, {column})')
        elif status == 3:
            print(f'ERROR LÉXICO: Cadena sin cerrar ({line}, {column})')

        print(f'Análisis completado. Último estado: {status}')


# Ejemplo de uso
text = '''nombre- -> 'Grafo Ejemplo'
nodos -> [
    'nodoA': 'Nodo 1',
    'nodoB': 'Nodo 2',
    'nodoC': 'Nodo 3'
];
conexiones -> [
    'nodoA' > 'nodoB',
    'nodoA' > 'nodoC'
];
'''
lexer = Lexer(text)
lexer.analyze()
