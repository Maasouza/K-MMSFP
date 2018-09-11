class Tree:
    vertex = None
    root = None
    edges = None
    leafs = None
    cost = 0

    def __init__(self, root, edges, cost):
        self.root = root
        self.edges = edges
        self.cost = cost
        self.getVertex()
        self.getLeafs()

    def getVertex(self):
        if(self.vertex == None):
            self.vertex = set()
            for u,v in self.edges:
                self.vertex.add(u)
                self.vertex.add(v)
        return self.vertex

    def getLeafs(self):
        neighbors = {}
        if(self.leafs == None):
            self.leafs = set()
            for u,v in self.edges:
                neighbors[u] = neighbors.setdefault(u,0) + 1
                neighbors[v] = neighbors.setdefault(v,0) + 1

            for key, value in neighbors.items():
                if value == 1:
                    self.leafs.add(key)

        return self.leafs

    def __eq__(self, other):
        return self.cost == other.cost

    def __gt__(self, other):
        return self.cost > other.cost
