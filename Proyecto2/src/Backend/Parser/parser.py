from src.Backend.Lexer.token import Token
from src.Backend.Lexer.token_types import TokenTypes


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.syntax_errors = []
        # Token fin de entrada
        self.tokens.append(Token(TokenTypes.TK_EOF, '$', -1, -1))

    def parse(self):
        self.program()
        if len(self.tokens) > 0:
            self.syntax_errors.append(f"Syntax error: Unconsumed tokens at end of parsing.")

    #<program> ::= <statements>
    def program(self):
        self.statements()

    #<statements> ::= <statement> <statements>
    #              | ε
    def statements(self):
        while self.tokens[0].type != TokenTypes.TK_EOF:
            self.statement()
        self.tokens.pop(0)

    #<statement> ::= <declaration>
    #             | <function_call>
    def statement(self):
        if self.tokens[0].type == TokenTypes.TK_ARRAY:
            self.declaration()
        elif self.tokens[0].type == TokenTypes.TK_IDENTIFIER:
            self.function_call()
        else:
            self.syntax_errors.append(f"Syntax error: Unexpected token {self.tokens[0].lexeme} in line {self.tokens[0].line}")
            self.tokens.pop(0)  # Consume the unexpected token

    #<declaration> ::= TK_ARRAY TK_IDENTIFIER TK_EQUAL TK_NEW TK_ARRAY TK_LBRACKET <values> TK_RBRACKET TK_SEMICOLON
    def declaration(self):
        if self.tokens[0].type == TokenTypes.TK_ARRAY:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_IDENTIFIER:
                self.tokens.pop(0)
                if self.tokens[0].type == TokenTypes.TK_EQUAL:
                    self.tokens.pop(0)
                    if self.tokens[0].type == TokenTypes.TK_NEW:
                        self.tokens.pop(0)
                        if self.tokens[0].type == TokenTypes.TK_ARRAY:
                            self.tokens.pop(0)
                            if self.tokens[0].type == TokenTypes.TK_LBRACKET:
                                self.tokens.pop(0)
                                self.values()
                                if self.tokens[0].type == TokenTypes.TK_RBRACKET:
                                    self.tokens.pop(0)
                                    if self.tokens[0].type == TokenTypes.TK_SEMICOLON:
                                        self.tokens.pop(0)
                                    else:
                                        self.syntax_errors.append(
                                            f"Syntax error: Expected ';' in line {self.tokens[0].line}, but got {self.tokens[0].lexeme}")
                                else:
                                    self.syntax_errors.append(
                                        f"Syntax error: Expected ']' in line {self.tokens[0].line}")
                            else:
                                self.syntax_errors.append(f"Syntax error: Expected '[' in line {self.tokens[0].line}")
                        else:
                            self.syntax_errors.append(f"Syntax error: Expected 'Array' in line {self.tokens[0].line}")
                    else:
                        self.syntax_errors.append(f"Syntax error: Expected 'new' in line {self.tokens[0].line}")
                else:
                    self.syntax_errors.append(f"Syntax error: Expected '=' in line {self.tokens[0].line}")
            else:
                self.syntax_errors.append(f"Syntax error: Expected an identifier in line {self.tokens[0].line}")
        else:
            self.syntax_errors.append(f"Syntax error: Expected 'Array' in line {self.tokens[0].line}")

    #<values> ::= <value> TK_COMMA <values>
    #          | <value>
    def values(self):
        self.value()
        while self.tokens[0].type == TokenTypes.TK_COMMA:
            self.tokens.pop(0)
            self.value()

    #<value> ::= TK_NUMBER
    #         | TK_STRING
    def value(self):
        if self.tokens[0].type == TokenTypes.TK_NUMBER:
            self.tokens.pop(0)
        elif self.tokens[0].type == TokenTypes.TK_STRING:
            self.tokens.pop(0)
        else:
            self.syntax_errors.append(f"Syntax error: Expected a value in line {self.tokens[0].line}")

    #<function_call> ::= TK_IDENTIFIER TK_DOT <function> TK_SEMICOLON
    def function_call(self):
        if self.tokens[0].type == TokenTypes.TK_IDENTIFIER:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_DOT:
                self.tokens.pop(0)
                self.function()
                if self.tokens[0].type == TokenTypes.TK_SEMICOLON:
                    self.tokens.pop(0)
                else:
                    self.syntax_errors.append(
                        f"Syntax error: Expected ';' in line {self.tokens[0].line}, but got {self.tokens[0].lexeme}")
            else:
                self.syntax_errors.append(f"Syntax error: Expected '.' in line {self.tokens[0].line}")
        else:
            self.syntax_errors.append(f"Syntax error: Expected an identifier in line {self.tokens[0].line}")

    #<function> ::= <sort_function>
    #        | <save_function>
    def function(self):
        if self.tokens[0].type == TokenTypes.TK_SORT:
            self.sort_function()
        elif self.tokens[0].type == TokenTypes.TK_SAVE:
            self.save_function()
        else:
            self.syntax_errors.append(f"Syntax error: Unexpected function {self.tokens[0].lexeme} in line {self.tokens[0].line}")

    #<sort_function> ::= TK_SORT TK_LPARANTHESIS <sort_params> TK_RPARANTHESIS
    def sort_function(self):
        if self.tokens[0].type == TokenTypes.TK_SORT:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_LPARENTHESIS:
                self.tokens.pop(0)
                self.sort_params()
                if self.tokens[0].type == TokenTypes.TK_RPARENTHESIS:
                    self.tokens.pop(0)
                else:
                    self.syntax_errors.append(f"Syntax error: Expected ')' in line {self.tokens[0].line}")
            else:
                self.syntax_errors.append(f"Syntax error: Expected '(' in line {self.tokens[0].line}")
        else:
            self.syntax_errors.append(f"Syntax error: Expected 'sort' in line {self.tokens[0].line}")

    #<sort_params> ::= TK_ASC TK_EQUAL <boolean>
    def sort_params(self):
        if self.tokens[0].type == TokenTypes.TK_ASC:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_EQUAL:
                self.tokens.pop(0)
                self.boolean()
            else:
                self.syntax_errors.append(f"Syntax error: Expected '=' in line {self.tokens[0].line}")
        else:
            self.syntax_errors.append(f"Syntax error: Expected 'asc' in line {self.tokens[0].line}")

    #<boolean> ::= TK_TRUE
    #          | TK_FALSE
    def boolean(self):
        if self.tokens[0].type == TokenTypes.TK_TRUE:
            self.tokens.pop(0)
        elif self.tokens[0].type == TokenTypes.TK_FALSE:
            self.tokens.pop(0)
        else:
            self.syntax_errors.append(f"Syntax error: Expected a boolean value in line {self.tokens[0].line}")

    #<save_function> ::= TK_SAVE TK_LPARENTHESIS TK_STRING TK_RPARENTHESIS
    def save_function(self):
        if self.tokens[0].type == TokenTypes.TK_SAVE:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_LPARENTHESIS:
                self.tokens.pop(0)
                if self.tokens[0].type == TokenTypes.TK_STRING:
                    self.tokens.pop(0)
                    if self.tokens[0].type == TokenTypes.TK_RPARENTHESIS:
                        self.tokens.pop(0)
                    else:
                        self.syntax_errors.append(f"Syntax error: Expected ')' in line {self.tokens[0].line}")
                else:
                    self.syntax_errors.append(f"Syntax error: Expected a string in line {self.tokens[0].line}")
            else:
                self.syntax_errors.append(f"Syntax error: Expected '(' in line {self.tokens[0].line}")
        else:
            self.syntax_errors.append(f"Syntax error: Expected 'save' in line {self.tokens[0].line}")
