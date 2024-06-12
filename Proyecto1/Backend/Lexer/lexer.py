from Proyecto1.Backend.Lexer.token import Token
from Proyecto1.Backend.Lexer.error import Error


class Lexer:

    def __init__(self, textEntry):
        self.textEntry = textEntry
        self.validTokens = []
        self.errorTokens = []

    def isValidCharacter(self, character):
        return character in [';', '[', ']', ':', ',', '{', '}', '>']

    def isWhitespace(self, character):
        return character in [' ', '\t', '\n']

    def recognizeKeyWords(self):
        keywords = ["nombre", "nodos", "conexiones"]
        for token in self.validTokens:
            if token.lexeme in keywords:
                token.token = "PALABRA_RESERVADA"

    def recognizeSimbols(self):
        for token in self.validTokens:
            if token.lexeme == ";":
                token.token = "PUNTO_Y_COMA"
            elif token.lexeme == "[":
                token.token = "D_CORCHETE"
            elif token.lexeme == "]":
                token.token = "I_CORCHETE"
            elif token.lexeme == ":":
                token.token = "DOS_PUNTOS"
            elif token.lexeme == ",":
                token.token = "COMA"
            elif token.lexeme == "{":
                token.token = "D_LLAVE"
            elif token.lexeme == "}":
                token.token = "I_LLAVE"
            elif token.lexeme == ">":
                token.token = "SEMI_FLECHA"



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
                else:
                    error = Error(token="ERROR LÉXICO", lexeme=character, line=line, column=column)
                    error.__str__()
                    self.errorTokens.append(error)
            elif status == 1:
                if character.isalnum():
                    lexeme += character
                    print(f'Estado 1: {lexeme}')
                else:
                    token = Token(token="IDENTIFICADOR", lexeme=lexeme, line=line, column=column)
                    token.__str__()
                    self.validTokens.append(token)
                    lexeme = ""
                    status = 0
                    if not self.isWhitespace(character) and not self.isValidCharacter(character):
                        error = Error(token="ERROR LÉXICO", lexeme=character, line=line, column=column)
                        error.__str__()
                        self.errorTokens.append(error)
                    continue
            elif status == 2:
                if character == ">":
                    lexeme += character
                    token = Token(token="FLECHA", lexeme=lexeme, line=line, column=column)
                    token.__str__()
                    self.validTokens.append(token)
                    lexeme = ""
                    status = 0
                else:
                    error = Error(token="ERROR LÉXICO", lexeme=lexeme, line=line, column=column)
                    error.__str__()
                    self.errorTokens.append(error)
                    lexeme = ""
                    status = 0
            elif status == 3:
                if character == "'":
                    lexeme += character
                    token = Token(token="CADENA", lexeme=lexeme, line=line, column=column)
                    token.__str__()
                    self.validTokens.append(token)
                    lexeme = ""
                    status = 0
                else:
                    lexeme += character
                    print(f'Estado 3: {lexeme}')
            elif status == 4:
                token = Token(token="SIMBOLO", lexeme=lexeme, line=line, column=column)
                token.__str__()
                self.validTokens.append(token)
                lexeme = ""
                status = 0

            if character == '\n':
                line += 1
                column = 1
            else:
                column += 1

        if status == 1:
            token = Token(token="IDENTIFICADOR", lexeme=lexeme, line=line, column=column)
            token.__str__()
            self.validTokens.append(token)
        elif status == 3:
            error = Error(token="ERROR LÉXICO", lexeme=lexeme, line=line, column=column)
            error.__str__()
            self.errorTokens.append(error)

        # recognizes keywords and symbols and changes to an appropriate token
        self.recognizeKeyWords()
        self.recognizeSimbols()
        print(f'Análisis completado. Último estado: {status}')



# Ejemplo de uso
text = '''nombre4 -> 'Grafo Ejemplo'
nodos -> [
    'nodoA'dsf: 'Nodo 1',
    'nodoB': 'Nodo 2',
    'nodoC': 'Nod4o 3'
];
conexiones -> [
    'nodoA' > 'nodoB',
    'nodoA' > 'nodfgoC'
];
'''
lexer = Lexer(text)
lexer.analyze()

print("=====================================")
print("Tokens válidos:")
for token in lexer.validTokens:
    print(token)
print("Tokens inválidos:")
for token in lexer.errorTokens:
    print(token)
