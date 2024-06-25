from src.Backend.Lexer.lexer import Lexer
from src.Backend.Parser.parser import Parser


class Analyzer:

    def __init__(self, text_entry):
        self.text_entry = text_entry
        self.tokens = []
        self.syntax_errors = []

    def analyze(self):
        lexic_errors_found = False
        self.analyze_tokens()
        print("**********************************")
        print("Found tokens:")
        for token in self.tokens:
            print(token)
        print("**********************************")
        for token in self.tokens:
            if token.type == 'TK_ERROR':
                lexic_errors_found = True
        if not lexic_errors_found:
            self.analyze_syntax()
            print("**********************************")
            print("Syntax analysis completed")
            if len(self.syntax_errors) == 0:
                print("No syntax errors found")
            else:
                print("Syntax errors found:")
                for error in self.syntax_errors:
                    print(error)
        else:
            self.syntax_errors.append("Se encontraron errores léxicos, no se puede realizar el análisis sintáctico")
            print("Se encontraron errores léxicos, no se puede realizar el análisis sintáctico")

    def analyze_tokens(self):
        lexer = Lexer(self.text_entry)
        lexer.analyze()
        self.tokens = lexer.tokens

    def analyze_syntax(self):
        parser = Parser(self.tokens)
        parser.parse()
        self.syntax_errors = parser.syntax_errors

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

miArray.save("ruta/del/archivo/csv");

miArray2.sort(asc=FALSE);
miArray2.save("ruta/del/archivo/csv");

Array Prueba3 = new Array [ 15, 80, 68, 55, 48.13, 12.25 ];
miArray3.sort(asc=TRUE);
miArray3.save("ruta/del/archivo/csv");

Array Prueba4 = new Array [ "12", "mundo", "como", "estas" ];
miArray4.save("ruta/del/archivo/csv");
"""
analyzer = Analyzer(content2)
analyzer.analyze()
