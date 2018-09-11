import networkx as nx
test_file = '../data/ran-50-100-1.dat'
roots = [0,41]
trees = {}
best = [0, 41, 41, 41, 41, 0, 41, 0, 0, 41, 0, 0, 41, 41, 41, 0, 41, 0, 41, 0, 0, 0, 41, 0, 0, 41, 41, 0, 41, 0, 41, 0, 0, 0, 0, 0, 0, 41, 41, 0, 41, 41, 0, 0, 0, 0, 0, 41, 41, 41]

G = nx.Graph()
maxWeight = 0

f = lambda x:sum([a[2]['weight'] for a in x])

with open(test_file) as file:
    V, E = map(int,file.readline().split())
    for i in range(E):
        i, j, c = map(int,file.readline().split())
        G.add_edge(i-1, j-1, weight = c)
        maxWeight += c

for root in roots:
    trees[root] = []

for idx, v in enumerate(best):
    trees[v].append(idx)

g_trees = []
for idx, tree in trees.items():
    g_trees.append(G.subgraph(tree))



mst1 = nx.minimum_spanning_tree(g_trees[0])
print(len(mst1.edges()), f(mst1.edges(data=True)))

mst2 = nx.minimum_spanning_tree(g_trees[1])
print(len(mst2.edges()),f(mst2.edges(data=True)))

print(mst1.edges())