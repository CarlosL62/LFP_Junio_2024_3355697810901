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
            if len(self.syntax_errors) == 0:
                print("Syntax analysis completed successfully")
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
analyzer = Analyzer('''//Editor de código fuente

//Comentario de una línea

/*
Comentario
multilínea
*/

Array miArray new Array[15, 80, 68, 55, 48];
miArray.sort(asc=FALSE);
miArray.save("ruta/del/archivo.csv");
''')
analyzer.analyze()
