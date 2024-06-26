from src.Backend.Files.file import File


class ReportMaker:

    def __init__(self):
        self.tokens = []
        self.syntax_errors = []

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
