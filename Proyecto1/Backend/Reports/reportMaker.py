class ReportMaker:
    def __init__(self, validTokens, errorTokens):
        self.validTokens = validTokens
        self.errorTokens = errorTokens

    def makeReportTokens(self, path):
        with open(path, 'w', encoding='utf-8') as report:
            report.write('''
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

            for token in self.validTokens:
                report.write('''
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                '''.format(token.type.name, token.lexeme, token.line, token.column))

            report.write('''
                    </table>
                </body>
                </html>
            ''')

    def makeReportErrors(self, path):
        with open(path, 'w', encoding='utf-8') as report:
            report.write('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Reporte de errores</title>
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
                    <h1>Reporte de Errores</h1>
                    <table border="1">
                        <tr>
                            <th>Token</th>
                            <th>Lexema</th>
                            <th>Linea</th>
                            <th>Columna</th>
                        </tr>
            ''')

            for error in self.errorTokens:
                report.write('''
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                '''.format(error.type.name, error.lexeme, error.line, error.column))

            report.write('''
                    </table>
                </body>
                </html>
            ''')
