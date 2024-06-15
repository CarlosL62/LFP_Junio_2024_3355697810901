from graphviz import Digraph

class Grapher:

    def __init__(self):

        # Crear un grafo dirigido
        dot = Digraph(comment='Grafo Dirigido')

        # Añadir nodos
        dot.node('A', 'Nodo A')
        dot.node('B', 'Nodo B')
        dot.node('C', 'Nodo C')

        # Añadir aristas
        dot.edge('A', 'B', 'A a B')
        dot.edge('A', 'C', 'A a C')
        dot.edge('B', 'C', 'B a C')

        # Guardar y renderizar el grafo en un archivo PNG
        dot.render('output/grafo_dirigido', format='png', cleanup=True)

#ejemplo
graph = Grapher()