class State():

    items = None    # list indicating the presence of items in the state
    objFunction = None
    costs = None
    roots = None

    def __init__(self):
        self.items = []
        self.roots = []
        self.costs = []
        self.edges = []
        self.alter =[]

    def update(self, g):
        self.edges = []
        for idx, root in enumerate(self.roots):
            if(self.alter[idx]):
                used = [0 if root == item else 1 for item in self.items]
                mst = g.mst(root, marked = used)
                self.costs[idx] = (mst['cost'])
                self.edges.extend(list(mst['edges'])[:])
                self.alter[idx] = False
        self.objFunction = max(self.costs)

    def copy(self):
        obj_copy = State()
        obj_copy.items = self.items[:]
        obj_copy.roots = self.roots[:]
        obj_copy.objFunction = self.objFunction
        obj_copy.costs = self.costs[:]
        obj_copy.edges = self.edges[:]
        obj_copy.alter = self.alter[:]
        return obj_copy

    def __repr__(self):
        return str(self.items)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return self.items == other.items

    def __gt__(self, other):
        return self.objFunction > other.objFunction