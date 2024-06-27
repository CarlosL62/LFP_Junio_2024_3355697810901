from src.Backend.Lexer.lexer import Lexer
from src.Backend.Parser.parser import Parser
from src.Backend.Lexer.token_types import TokenTypes
from src.Backend.Parser.declaration import Declaration
from src.Backend.Files.file import File
from tkinter import messagebox


class Analyzer:

    def __init__(self, text_entry):
        self.text_entry = text_entry
        self.tokens = []
        self.tokens_bkp = []
        self.syntax_errors = []
        self.statements = []

    def analyze(self):
        lexic_errors_found = False
        self.analyze_tokens()
        self.tokens_bkp = self.tokens.copy()
        print("**********************************")
        print("Tokens found:")
        for token in self.tokens:
            if token.type != TokenTypes.TK_ERROR:
                print(token)
        print ("Lexic errors found:")
        for token in self.tokens:
            if token.type == TokenTypes.TK_ERROR:
                lexic_errors_found = True
                print(token)
        print("**********************************")
        self.analyze_syntax()
        print("**********************************")
        print("Syntax analysis completed")
        if len(self.syntax_errors) == 0:
            print("No syntax errors found")
        else:
            print("Syntax errors found:")
            for error in self.syntax_errors:
                print(error)
        print("**********************************")
        if lexic_errors_found and len(self.syntax_errors) > 0:
            messagebox.showerror("Error", "Se encontraron errores léxicos y sintácticos" + "\n" + "Genera el reporte de errores para más información")
        elif lexic_errors_found:
            messagebox.showerror("Error", "Se encontraron errores léxicos" + "\n" + "Genera el reporte de errores para más información")
        elif len(self.syntax_errors) > 0:
            messagebox.showerror("Error", "Se encontraron errores sintácticos" + "\n" + "Genera el reporte de errores para más información")
        else:
            messagebox.showinfo("Éxito", "Análisis completado con éxito")
            self.execute_statements()

    def analyze_tokens(self):
        lexer = Lexer(self.text_entry)
        lexer.analyze()
        self.tokens = lexer.tokens

    def analyze_syntax(self):
        parser = Parser(self.tokens)
        parser.parse()
        self.statements = parser.symbol_table
        self.syntax_errors = parser.syntax_errors

    def execute_statements(self):
        declarations = []  # List to store the declarations only
        print('############################################')
        print('Executing statements')
        for statement in self.statements:
            if statement.instruction_type == 'declaration':
                declaration = Declaration()
                declaration.identifier = statement.identifier.lexeme
                print("Declaration found")
                print("Identifier: " + declaration.identifier)
                print("Values: ")
                for value in statement.values:
                    try:
                        # Try to convert the value to a number
                        number = float(value.lexeme.replace('"', ''))
                        declaration.values.append(number)
                    except ValueError:
                        # If the value is not a number, it is considered a string
                        declaration.values.append(value.lexeme.replace('"', ''))
                for value in declaration.values:
                    print(value)
                declarations.append(declaration)
            if statement.instruction_type == 'sort_function':
                print("Sort function found")
                print("Array name: " + statement.identifier.lexeme)
                print("Sort function parameters: " + statement.boolean.lexeme)
                if statement.boolean.lexeme == 'TRUE':
                    print("Sorting in ascending order")
                    for declaration in declarations:
                        if declaration.identifier == statement.identifier.lexeme:
                            declaration.values = self.sort_elements(declaration.values, 'TRUE')
                            for value in declaration.values:
                                print(value)
                elif statement.boolean.lexeme == 'FALSE':
                    print("Sorting in descending order")
                    for declaration in declarations:
                        if declaration.identifier == statement.identifier.lexeme:
                            declaration.values = self.sort_elements(declaration.values, 'FALSE')
                            for value in declaration.values:
                                print(value)
            if statement.instruction_type == 'save_function':
                print("Save function found")
                print("Array name: " + statement.identifier.lexeme)
                print("Save function parameters: " + statement.route.lexeme)
                for declaration in declarations:
                    if declaration.identifier == statement.identifier.lexeme:
                        file_manager = File()
                        print("Saving array " + declaration.identifier + " in " + statement.route.lexeme)
                        # Here the array is saved in the specified route
                        file_manager.content = 'data\n'
                        for value in declaration.values:
                            file_manager.content += f'{value}\n'
                        file_manager.save_as_file(statement.route.lexeme.replace('"', ''))

    def sort_elements(self, elements, asc):
        n = len(elements)
        for i in range(n):
            for j in range(0, n - i - 1):
                if asc == 'TRUE':
                    if elements[j] > elements[j + 1]:
                        elements[j], elements[j + 1] = elements[j + 1], elements[j]
                elif asc == 'FALSE':
                    if elements[j] < elements[j + 1]:
                        elements[j], elements[j + 1] = elements[j + 1], elements[j]
        return elements
