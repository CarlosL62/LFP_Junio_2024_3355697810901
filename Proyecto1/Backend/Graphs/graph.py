class Graph:

    def __init__(self):
        self.name = None
        self.nodes = []
        self.connections = []

    def addNode(self, node, text):
        self.nodes.append([node, text])

    def addConnection(self, nodeA, nodeB):
        self.connections.append([nodeA, nodeB])