from src.Backend.Files.file import File
from src.Backend.Reports.graph import Graph
from graphviz import Digraph
from tkinter import messagebox

class ReportMaker:

    def __init__(self):
        self.tokens = []
        self.syntax_errors = []
        self.graph = Graph()

    file_manager = File()

    def make_report_tokens(self, path):
        self.file_manager.content = ('''
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reporte de Tokens</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }

                    h1 {
                        color: #333;
                        text-align: center;
                    }

                    table {
                        width: 80%;
                        margin: 20px auto;
                        border-collapse: collapse;
                    }

                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background-color: #f2f2f2;
                    }

                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }

                    tr:hover {
                        background-color: #ddd;
                    }
                </style>
            </head>
            <body>
                <h1>Reporte de Tokens</h1>
                <table>
                    <tr>
                        <th>Token</th>
                        <th>Lexema</th>
                        <th>Linea</th>
                        <th>Columna</th>
                    </tr>
        ''')

        for token in self.tokens:
            if token.type.name != 'TK_ERROR':
                self.file_manager.content += ('''
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                '''.format(token.type.name, token.lexeme, token.line, token.column))

        self.file_manager.content += ('''
                    </table>
                </body>
                </html>
            ''')

        self.file_manager.save_as_file(path)

    def make_report_errors(self, path):
        self.file_manager.content = ('''
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reporte de Errores</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }
    
                    h1 {
                        color: #333;
                        text-align: center;
                    }
                    
                    h2 {
                        color: #333;
                        text-align: center;
                    }
    
                    table {
                        width: 80%;
                        margin: 20px auto;
                        border-collapse: collapse;
                    }
    
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
    
                    th {
                        background-color: #f2f2f2;
                    }
    
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
    
                    tr:hover {
                        background-color: #ddd;
                    }
    
                    ul {
                        list-style-type: none;
                        padding: 0;
                        margin: 0;
                        text-align: center;
                    }
    
                    li {
                        padding: 8px;
                        border: 1px solid #ddd;
                        margin-bottom: 10px;
                    }
                </style>
            </head>
            <body>
                <h1>Reporte de Errores</h1>
                <h2>Reporte de Errores Léxicos</h2>
                <table>
                    <tr>
                        <th>Lexema</th>
                        <th>Linea</th>
                        <th>Columna</th>
                    </tr>
        ''')

        for token in self.tokens:
            if token.type.name == 'TK_ERROR':
                self.file_manager.content += ('''
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                '''.format(token.lexeme, token.line, token.column))

        self.file_manager.content += ('''
                    </table>
                    <h2>Errores Sintácticos</h2>
                    <ul>
        ''')

        for error in self.syntax_errors:
            self.file_manager.content += ('''
                <li>{}</li>
            '''.format(error))

        self.file_manager.content += ('''
                    </ul>
                </body>
                </html>
            ''')

        self.file_manager.save_as_file(path)

    def make_report_derivation_tree(self, path, statements):
        # This report is made with graphviz and the dot language
        self.graph_extractor(statements)
        self.grapher(path)

    def graph_extractor(self, statements):
        print("Graph Extractor")
        # Not errors found verified before calling this method
        # The graph will be made with the following initial structure:
        self.graph.addNode("Statements", "Statements")
        self.graph.addNode("Declarations", "Declarations")
        self.graph.addNode("Function_calls", "Function calls")
        self.graph.addConnection("Statements", "Declarations")
        self.graph.addConnection("Statements", "Function_calls")
        # The next nodes are added to the graph
        aux = 0  # Auxiliar variable to store the index of the statement, it will work to save different names
        for statement in statements:
            # If the statement is a declaration
            if statement.instruction_type == 'declaration':
                # The declaration info is declared and added to the graph
                node_text = f'Array {statement.identifier.lexeme} = new Array['
                for i in range(statement.values.__len__()):
                    if i == statement.values.__len__() - 1:
                        node_text += statement.values[i].lexeme
                    else:
                        node_text += statement.values[i].lexeme + ', '
                node_text += '];'
                self.graph.addNode(statement.identifier.lexeme+aux.__str__(), node_text)
                self.graph.addConnection('Declarations', statement.identifier.lexeme+aux.__str__())
            # If the statement is a function call
            elif statement.instruction_type == 'sort_function':
                # The function call info is declared and added to the graph
                node_text = f'{statement.identifier.lexeme}.sort(asc={statement.boolean.lexeme});'
                self.graph.addNode(statement.identifier.lexeme+aux.__str__(), node_text)
                self.graph.addConnection('Function_calls', statement.identifier.lexeme+aux.__str__())
            elif statement.instruction_type == 'save_function':
                # The function call info is declared and added to the graph
                node_text = f'{statement.identifier.lexeme}.save(route={statement.route.lexeme});'
                self.graph.addNode(statement.identifier.lexeme+aux.__str__(), node_text)
                self.graph.addConnection('Function_calls', statement.identifier.lexeme+aux.__str__())
            aux += 1

    def grapher(self, path):
        # The graph is generated with the graphviz library
        dot = Digraph(comment='Derivation Tree')  # Name of the graph
        dot.attr(label='Derivation Tree', labelloc='t', fontsize='20')  # Graph label
        # Add nodes to the graph
        for node in self.graph.nodes:
            dot.node(node[0], node[1])
        # Add connections to the graph
        for connection in self.graph.connections:
            dot.edge(connection[0], connection[1])
        # Save and render the graph in an SVG file
        pathn = path.replace('.svg', '')
        dot.render(pathn, format='svg', cleanup=True)
        messagebox.showinfo("Reporte generado", "El reporte del árbol de derivación se ha generado correctamente.")
