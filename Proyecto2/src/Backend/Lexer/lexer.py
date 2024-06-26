from src.Backend.Lexer.token import Token
from src.Backend.Lexer.token_types import TokenTypes


class Lexer:
    def __init__(self, text_entry):
        self.text_entry = text_entry
        self.tokens = []

    def is_valid_character(self, character):
        return character in ['=', ',', '.', ';', '(', ')', '[', ']']

    def is_whitespace(self, character):
        return character in [' ', '\t', '\n']

    def add_token(self, type, lexeme, line, column):
        token = Token(type=type, lexeme=lexeme, line=line, column=column)
        self.tokens.append(token)

    def recognize_keywords(self):
        for token in self.tokens:
            if token.lexeme == 'Array':
                token.type = TokenTypes.TK_ARRAY
            elif token.lexeme == 'new':
                token.type = TokenTypes.TK_NEW
            elif token.lexeme == 'sort':
                token.type = TokenTypes.TK_SORT
            elif token.lexeme == 'asc':
                token.type = TokenTypes.TK_ASC
            elif token.lexeme == 'TRUE':
                token.type = TokenTypes.TK_TRUE
            elif token.lexeme == 'FALSE':
                token.type = TokenTypes.TK_FALSE
            elif token.lexeme == 'save':
                token.type = TokenTypes.TK_SAVE

    def analyze(self):
        current_line = 1
        current_column = 1
        lexeme = ""
        status = 0
        start_column = 1

        i = 0
        while i < len(self.text_entry):
            character = self.text_entry[i]
            print(f'Procesando carácter: {character} ({current_line}, {current_column}), Estado: {status}')

            # Language analysis
            if status == 0:
                # Comment detection
                if character == '/' and i + 1 < len(self.text_entry) and self.text_entry[i + 1] in ['/', '*']:
                    lexeme += character
                    status = -1
                # Identifier detection
                elif character.isalpha():
                    lexeme += character
                    status = 1
                # Symbol detection
                elif self.is_valid_character(character):
                    lexeme += character
                    start_column = current_column
                    if lexeme == '=':
                        self.add_token(TokenTypes.TK_EQUAL, lexeme, current_line, start_column)
                    elif lexeme == ',':
                        self.add_token(TokenTypes.TK_COMMA, lexeme, current_line, start_column)
                    elif lexeme == '.':
                        self.add_token(TokenTypes.TK_DOT, lexeme, current_line, start_column)
                    elif lexeme == ';':
                        self.add_token(TokenTypes.TK_SEMICOLON, lexeme, current_line, start_column)
                    elif lexeme == '(':
                        self.add_token(TokenTypes.TK_LPARENTHESIS, lexeme, current_line, start_column)
                    elif lexeme == ')':
                        self.add_token(TokenTypes.TK_RPARENTHESIS, lexeme, current_line, start_column)
                    elif lexeme == '[':
                        self.add_token(TokenTypes.TK_LBRACKET, lexeme, current_line, start_column)
                    elif lexeme == ']':
                        self.add_token(TokenTypes.TK_RBRACKET, lexeme, current_line, start_column)
                    lexeme = ""
                # String detection
                elif character == '"':
                    lexeme += character
                    status = 3
                # Number detection
                elif character.isnumeric():
                    lexeme += character
                    status = 4
                # Whitespace detection
                elif self.is_whitespace(character):
                    if character == '\n':
                        current_line += 0
                        current_column = 1
                    else:
                        current_column += 1
                # Error detection
                else:
                    self.add_token(TokenTypes.TK_ERROR, character, current_line, current_column)
            # Comment detection (continuation)
            elif status == -1:
                if character == '/':
                    status = -2
                elif character == '*':
                    status = -3
                else:
                    self.add_token(TokenTypes.TK_ERROR, lexeme, current_line, start_column)
                    lexeme = ""
                    status = 0
                    continue
                lexeme += character
            elif status == -2:
                if character == '\n':
                    status = 0
                lexeme = ""  # Clear lexeme for single-line comments
            elif status == -3:
                lexeme += character
                if character == '*' and i + 1 < len(self.text_entry) and self.text_entry[i + 1] == '/':
                    lexeme += '/'
                    i += 1
                    status = 0
                    lexeme = ""
            # Identifier detection (continuation)
            elif status == 1:
                if character.isalnum() or character == '_':
                    lexeme += character
                else:
                    start_column = current_column - len(lexeme)
                    self.add_token(TokenTypes.TK_IDENTIFIER, lexeme, current_line, start_column)
                    lexeme = ""
                    status = 0
                    continue
            # String detection (continuation)
            elif status == 3:
                if character == '"':
                    lexeme += character
                    start_column = current_column - len(lexeme)
                    self.add_token(TokenTypes.TK_STRING, lexeme, current_line, start_column)
                    lexeme = ""
                    status = 0
                elif character == '\n':
                    start_column = current_column - len(lexeme)
                    self.add_token(TokenTypes.TK_ERROR, lexeme, current_line, start_column)
                    lexeme = ""
                    status = 0
                else:
                    lexeme += character
            # Number detection (continuation)
            elif status == 4:
                if character.isnumeric():
                    lexeme += character
                elif character == '.':
                    lexeme += character
                    status = 5
                else:
                    start_column = current_column - len(lexeme)
                    self.add_token(TokenTypes.TK_NUMBER, lexeme, current_line, start_column)
                    lexeme = ""
                    status = 0
                    continue
            # Decimal number detection (continuation)
            elif status == 5:
                if character.isnumeric():
                    lexeme += character
                else:
                    start_column = current_column - len(lexeme)
                    self.add_token(TokenTypes.TK_NUMBER, lexeme, current_line, start_column)
                    lexeme = ""
                    status = 0
                    continue

            if character == '\n':
                current_line += 1
                current_column = 1
            else:
                current_column += 1

            i += 1

        # End of the loop
        if lexeme:
            start_column = current_column - len(lexeme)
            if status == 1:
                self.add_token(TokenTypes.TK_IDENTIFIER, lexeme, current_line, start_column)
            elif status == 4 or status == 5:
                self.add_token(TokenTypes.TK_NUMBER, lexeme, current_line, start_column)
            elif status == 3:
                self.add_token(TokenTypes.TK_ERROR, lexeme, current_line, start_column)

        # Recognize keywords and update token types
        self.recognize_keywords()
        print(f'Análisis léxico finalizado. {len(self.tokens)} tokens encontrados.')
