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
        self.statements = []
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
        # Clean the list of statements
        self.statements = []

    def sort_elements(self, elements, asc):
        if asc == 'TRUE':
            return sorted(elements)
        elif asc == 'FALSE':
            return sorted(elements, reverse=True)

#Example of use
content1 = ('''//Editor de código fuente

//Comentario de una línea

/*
Comentario
multilínea
*/

Array miArray1 = new Array[15, 80, 68, 55, 48];
Array miArray2 = new Array["hola", "mundo", "cruel"];
Array miArray3 = new Array["uno", 2, "tres", 4, "cinco"];
miArray1.sort(asc=FALSE);
miArray1.save("ruta/del/archivo.csv");
Array miArray4 = new Array[15, 80, 68, 55, 48];
Array miArray5 = new Array["hola", "mundo", "cruel"];
Array miArray6 = new Array["uno", 2, "tres", 4, "cinco"];
miArray2.sort(asc=TRUE);
miArray5.save("ruta/del/archivo.csv");
''')

content2 = """Array Prueb_a = new Array [ 15, 80, 68, 55, 48.13, 12.25 ];
Array Prueba_2 = new Array [ "hola", "mundo", "como", "estas" ];

miArray.save("ruta/del/archivo/1csv");

miArray2.sort(asc=FALSE);
miArray2.save("ruta/del/archivo/2csv");

Array Prueba3 = new Array [ 15, 80, 68, 55, 48.13, 12.25 ];
miArray3.sort(asc=TRUE);
miArray3.save("ruta/del/archivo/3csv");

Array Prueba4 = new Array [ "12", "mundo", "como", "estas" ];
miArray4.save("ruta/del/archivo/4csv");
"""

content3 = """Array test_numbers = new Array [ 15, 80, 68, 55, 48.13, 12.25 ];
test_numbers.sort(asc=FALSE);
Array testString = new Array [ "12", "mundo", "como", "estas" ];
testString.sort(asc=TRUE);
testString.save("4.csv");
test_numbers.save("1.csv");
"""

content4 = '''// Declaro mi nuevo array
Array array_basico = new Array [50, 48, 78, 69, 550, 7, 80];

//Lo ordeno de forma descendente
array_basico.sort( asc = FALSE );

/* Guardo el array en un csv para usarlo después */
array_basico.save("array1_ordenado_descendente.csv");'''
# analyzer = Analyzer(content4)
# analyzer.analyze()
#
# elements_test = analyzer.sort_elements([50, 48, 78, 69, 550, 7, 80], 'FALSE')
# print(elements_test)
