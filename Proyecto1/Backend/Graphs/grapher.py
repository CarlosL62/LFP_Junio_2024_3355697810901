from graphviz import Digraph
from Backend.Lexer.tokenTypes import TokenTypes
from Backend.Graphs.graph import Graph


class Grapher:

    graphes = []  # list of graphs

    def __init__(self, validTokens, errorTokens):
        self.validTokens = validTokens
        self.errorTokens = errorTokens

    def graphExtraxtor(self):
        global graph
        print("Extrayendo grafos...")

        if self.errorTokens.__len__() > 0:
            print("Hay errores léxicos, no se puede generar el grafo")
            for error in self.errorTokens:
                print(f"Error: {error.lexeme} en la línea {error.line}, columna {error.column}")
        else:
            print("No hay errores léxicos, generando grafos...")
            for i in range(self.validTokens.__len__()):
                if self.validTokens[i].type == TokenTypes.NAME:
                    graph = Graph()
                    graph.name = self.validTokens[i + 2].lexeme.replace("'", "")
                    print(f"Graph: {graph.name}")
                elif self.validTokens[i].type == TokenTypes.NODES:
                    aux = i
                    firstString = True
                    for aux in range(i, self.validTokens.__len__()):
                        if self.validTokens[aux].type == TokenTypes.STRING and firstString:
                            graph.addNode(self.validTokens[aux].lexeme.replace("'", ""), self.validTokens[aux + 2].lexeme.replace("'", ""))
                            firstString = False
                        elif self.validTokens[aux].type == TokenTypes.STRING and not firstString:
                            firstString = True
                        elif self.validTokens[aux].type == TokenTypes.RBRAKET:
                            break
                elif self.validTokens[i].type == TokenTypes.CONECTIONS:
                    aux = i
                    firstString = True
                    for aux in range(i, self.validTokens.__len__()):
                        if self.validTokens[aux].type == TokenTypes.STRING and firstString:
                            graph.addConnection(self.validTokens[aux].lexeme.replace("'", ""), self.validTokens[aux + 2].lexeme.replace("'", ""))
                            firstString = False
                        elif self.validTokens[aux].type == TokenTypes.STRING and not firstString:
                            firstString = True
                        elif self.validTokens[aux].type == TokenTypes.RBRAKET:
                            break
                    self.graphes.append(graph)
                i += 1
            print("Grafos generados correctamente")
        for graph in self.graphes:
            print(f"Graph: {graph.name}")
            for node in graph.nodes:
                print(f"Node: {node[0]} Text: {node[1]}")
            for connection in graph.connections:
                print(f"Connection: {connection[0]} -> {connection[1]}")

    def generateGraph(self, index):
        graph = self.graphes[index]
        dot = Digraph(comment=graph.name)  # name of the graph
        dot.attr(label=graph.name, labelloc='t', fontsize='20')  # graph label
        # add nodes
        for node in graph.nodes:
            dot.node(node[0], node[1])
        # add connections
        for connection in graph.connections:
            dot.edge(connection[0], connection[1])
        # save and render the graph in a PNG file
        dot.render(f'output/generatedGraph', format='png', cleanup=True)
