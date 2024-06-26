from src.Backend.Lexer.token import Token
from src.Backend.Lexer.token_types import TokenTypes
from src.Backend.Parser.declaration import Declaration
from src.Backend.Parser.sort_function import SortFunction
from src.Backend.Parser.save_function import SaveFunction


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.syntax_errors = []
        # Token fin de entrada
        self.tokens.append(Token(TokenTypes.TK_EOF, '$', -1, -1))

    # Symbol table
    # This will be used to store the variables declared in the program and the functions called
    symbol_table = []

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
            self.recover_from_error()

    #<declaration> ::= TK_ARRAY TK_IDENTIFIER TK_EQUAL TK_NEW TK_ARRAY TK_LBRACKET <values> TK_RBRACKET TK_SEMICOLON
    def declaration(self):
        declaration = Declaration()
        if self.tokens[0].type == TokenTypes.TK_ARRAY:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_IDENTIFIER:
                declaration.identifier = self.tokens.pop(0)
                if self.tokens[0].type == TokenTypes.TK_EQUAL:
                    self.tokens.pop(0)
                    if self.tokens[0].type == TokenTypes.TK_NEW:
                        self.tokens.pop(0)
                        if self.tokens[0].type == TokenTypes.TK_ARRAY:
                            self.tokens.pop(0)
                            if self.tokens[0].type == TokenTypes.TK_LBRACKET:
                                self.tokens.pop(0)
                                declaration.values = self.values()
                                if self.tokens[0].type == TokenTypes.TK_RBRACKET:
                                    self.tokens.pop(0)
                                    if self.tokens[0].type == TokenTypes.TK_SEMICOLON:
                                        self.tokens.pop(0)
                                        # Declaration is correct
                                        print("ID: ", declaration.identifier.lexeme)
                                        print("Values: ")
                                        for value in declaration.values:
                                            print(value.lexeme)
                                        self.symbol_table.append(declaration)
                                    else:
                                        self.syntax_errors.append(
                                            f"Syntax error: Expected ';' in line {self.tokens[0].line}, but got {self.tokens[0].lexeme}")
                                else:
                                    self.syntax_errors.append(
                                        f"Syntax error: Expected ']' in line {self.tokens[0].line}")
                                    self.recover_from_error()
                            else:
                                self.syntax_errors.append(f"Syntax error: Expected '[' in line {self.tokens[0].line}")
                                self.recover_from_error()
                        else:
                            self.syntax_errors.append(f"Syntax error: Expected 'Array' in line {self.tokens[0].line}")
                            self.recover_from_error()
                    else:
                        self.syntax_errors.append(f"Syntax error: Expected 'new' in line {self.tokens[0].line}")
                        self.recover_from_error()
                else:
                    self.syntax_errors.append(f"Syntax error: Expected '=' in line {self.tokens[0].line}")
                    self.recover_from_error()
            else:
                self.syntax_errors.append(f"Syntax error: Expected an identifier in line {self.tokens[0].line}")
                self.recover_from_error()
        else:
            self.syntax_errors.append(f"Syntax error: Expected 'Array' in line {self.tokens[0].line}")
            self.recover_from_error()

    #<values> ::= <value> TK_COMMA <values>
    #          | <value>
    def values(self):
        list = []
        item = self.value()
        list.append(item)
        while self.tokens[0].type == TokenTypes.TK_COMMA:
            self.tokens.pop(0)
            item = self.value()
            list.append(item)
        return list

    #<value> ::= TK_NUMBER
    #         | TK_STRING
    def value(self):
        if self.tokens[0].type == TokenTypes.TK_NUMBER:
            return self.tokens.pop(0)
        elif self.tokens[0].type == TokenTypes.TK_STRING:
            return self.tokens.pop(0)
        else:
            self.syntax_errors.append(f"Syntax error: Expected a value in line {self.tokens[0].line}")

    sort_function_declared = SortFunction()
    save_function_declared = SaveFunction()

    #<function_call> ::= TK_IDENTIFIER TK_DOT <function> TK_SEMICOLON
    def function_call(self):
        if self.tokens[0].type == TokenTypes.TK_IDENTIFIER:
            self.identifier = self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_DOT:
                self.tokens.pop(0)
                function_accepted = self.function()
                if self.tokens[0].type == TokenTypes.TK_SEMICOLON:
                    self.tokens.pop(0)
                    if function_accepted == self.SORT_FUNCTION:
                        # Sort function is correct
                        print("Sort function called")
                        print("ID: ", self.sort_function_declared.identifier.lexeme)
                        print("Params: ", self.sort_function_declared.boolean.lexeme)
                        self.symbol_table.append(self.sort_function_declared)
                    elif function_accepted == self.SAVE_FUNCTION:
                        # Save function is correct
                        print("Save function called")
                        print("ID: ", self.save_function_declared.identifier.lexeme)
                        print("Route: ", self.save_function_declared.route.lexeme)
                        self.symbol_table.append(self.save_function_declared)
                else:
                    self.syntax_errors.append(
                        f"Syntax error: Expected ';' in line {self.tokens[0].line}, but got {self.tokens[0].lexeme}")
            else:
                self.syntax_errors.append(f"Syntax error: Expected '.' in line {self.tokens[0].line}")
        else:
            self.syntax_errors.append(f"Syntax error: Expected an identifier in line {self.tokens[0].line}")

    SORT_FUNCTION = 1
    SAVE_FUNCTION = 2
    identifier = None

    #<function> ::= <sort_function>
    #        | <save_function>
    def function(self):
        if self.tokens[0].type == TokenTypes.TK_SORT:
            self.sort_function_declared = SortFunction()
            self.sort_function_declared.identifier = self.identifier
            sort_function_correct = self.sort_function()
            if sort_function_correct:
                return self.SORT_FUNCTION
        elif self.tokens[0].type == TokenTypes.TK_SAVE:
            self.save_function_declared = SaveFunction()
            self.save_function_declared.identifier = self.identifier
            save_function_correct = False
            save_function_correct = self.save_function()
            if save_function_correct:
                return self.SAVE_FUNCTION
        else:
            self.syntax_errors.append(f"Syntax error: Unexpected function {self.tokens[0].lexeme} in line {self.tokens[0].line}")

    #<sort_function> ::= TK_SORT TK_LPARANTHESIS <sort_params> TK_RPARANTHESIS
    def sort_function(self):
        if self.tokens[0].type == TokenTypes.TK_SORT:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_LPARENTHESIS:
                self.tokens.pop(0)
                param = self.sort_params()
                if self.tokens[0].type == TokenTypes.TK_RPARENTHESIS:
                    self.tokens.pop(0)
                    sort_function_correct = True
                    # Sort function is correct
                    if param is not None:
                        self.sort_function_declared.boolean = param
                    else:
                        self.sort_function_declared.boolean = Token(TokenTypes.TK_TRUE, 'true', -1, -1)
                    return sort_function_correct
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
                return self.boolean()
            else:
                self.syntax_errors.append(f"Syntax error: Expected '=' in line {self.tokens[0].line}")
        else:
            self.syntax_errors.append(f"Syntax error: Expected 'asc' in line {self.tokens[0].line}")

    #<boolean> ::= TK_TRUE
    #          | TK_FALSE
    def boolean(self):
        if self.tokens[0].type == TokenTypes.TK_TRUE:
            return self.tokens.pop(0)
        elif self.tokens[0].type == TokenTypes.TK_FALSE:
            return self.tokens.pop(0)
        else:
            self.syntax_errors.append(f"Syntax error: Expected a boolean value in line {self.tokens[0].line}")
            return None

    #<save_function> ::= TK_SAVE TK_LPARENTHESIS TK_STRING TK_RPARENTHESIS
    def save_function(self):
        if self.tokens[0].type == TokenTypes.TK_SAVE:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_LPARENTHESIS:
                self.tokens.pop(0)
                if self.tokens[0].type == TokenTypes.TK_STRING:
                    string = self.tokens.pop(0)
                    if self.tokens[0].type == TokenTypes.TK_RPARENTHESIS:
                        self.tokens.pop(0)
                        self.save_function_declared.route = string
                        save_function_correct = True
                        return save_function_correct
                    else:
                        self.syntax_errors.append(f"Syntax error: Expected ')' in line {self.tokens[0].line}")
                else:
                    self.syntax_errors.append(f"Syntax error: Expected a string in line {self.tokens[0].line}")
            else:
                self.syntax_errors.append(f"Syntax error: Expected '(' in line {self.tokens[0].line}")
        else:
            self.syntax_errors.append(f"Syntax error: Expected 'save' in line {self.tokens[0].line}")

    def recover_from_error(self):
        while self.tokens[0].type != TokenTypes.TK_EOF:
            self.tokens.pop(0)
            if self.tokens[0].type == TokenTypes.TK_SEMICOLON:
                self.tokens.pop(0)
                break
