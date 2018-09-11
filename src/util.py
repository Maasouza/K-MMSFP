import math
def local_search(trees, g):
    costs = []
    leafs = set()
    nodes = [None]*g.V
    for idx, tree in enumerate(trees):
        costs.append([idx, tree.cost])
        for leaf in tree.getLeafs():
            leafs.add(leaf)
        for v in tree.vertex:
            nodes[v] = idx
        nodes[tree.root] = idx
    max_index, max_cost = max_set(costs)
    max_sum = sum(map(lambda x:x[1],costs))
    improve = True
    while improve :

        improve = False
        v = leafs.pop()
        cost_edge_v = 0
        for edge in trees[nodes[v]].edges:
            if v in edge:
                cost_edge_v = g.edges[edge]
                new_leaf = edge[0] if v == edge[1] else edge[1]
                break
        for u, w in g.adj_list[v].items():
            if(nodes[v] != nodes[u]):
                if(nodes[v] == max_index):
                    if(costs[nodes[u]][1] + w <= max_cost):
                        costs[nodes[u]][1] += w
                        costs[nodes[v]][1] -= cost_edge_v
                        max_index, max_cost = (nodes[u], costs[nodes[u]][1]) if (costs[nodes[u]][1]>costs[nodes[v]][1]) else (max_index, max_cost)
                        nodes[v] = nodes[u]
                        improve = True
                        leafs.add(v)
                        leafs.add(new_leaf)
                        leafs.discard(u)
                else:
                    if(costs[nodes[u]][1] + w <= max_cost):
                        costs[nodes[u]][1] += w
                        costs[nodes[v]][1] -= cost_edge_v
                        if(sum(map(lambda x:x[1],costs))<= max_sum):
                            max_index, max_cost = (nodes[u], costs[nodes[u]][1]) if (costs[nodes[u]][1]>costs[nodes[v]][1]) else (max_index, max_cost)
                            nodes[v] = nodes[u]
                            improve = True
                            leafs.add(v)
                            leafs.add(new_leaf)
                            leafs.discard(u)
                        else:
                            costs[nodes[u]][1] -= w
                            costs[nodes[v]][1] += cost_edge_v
            if improve:
                break

    return max(list(map(lambda x:x[1],costs)))

def min_set(s):
    ret = [math.inf, math.inf]
    for key, value in s:
        if(value <= ret[1]):
            ret = [key, value]
    return tuple(ret)

def max_set(s):
    ret = [0, 0]
    for key, value in s:
        if(value >= ret[1]):
            ret = [key, value]
    return ret

def generate():
    outfile = open("../resultados.csv","w")
    infile = open("../artigo.csv",'r')
    infile.readline()
    outfile.write('file, bub, time, status, r1, r2, h1, t, h2, t, h3, t, h1l, t, h2l, t, h3l, t, mh, t, sa, t, isa, t'+'\n')
    t_s = time.time()
    for line in infile:
        file, bub, _time, status, r1, r2 = line.split(",")
        r2 = str(int(r2))
        outfile.write(file+' ,'+bub+' ,'+_time+' ,'+status+' ,'+r1+' ,'+r2+' ,')
        g = Graph("../data/"+file)
        roots = [int(r1)-1,int(r2)-1]
        print(file,r1,r2)
        #Heuristica 1 
        start = time.time()
        r_trees, _ = g.rooted_trees(roots)
        end = time.time()
        trees = []
        for root in  roots:
            trees.append( Tree(root, r_trees[root]['edges'], r_trees[root]['cost'] ))
        resp = max(trees).cost
        outfile.write(str(resp)+' ,'+str(round(end-start,6))+' ,')
        #Heuristica 2
        start = time.time()
        r_trees = g.greedy_random_sf(roots)
        end = time.time()
        trees = []
        for root in  roots:
            trees.append( Tree(root, r_trees[root]['edges'], r_trees[root]['cost'] ))
        resp = max(trees).cost
        outfile.write(str(resp)+' ,'+str(round(end-start,6))+' ,')
        #Heuristica 3
        start = time.time()
        r_trees = g.improved_random_sf(roots)
        end = time.time()
        trees = []
        for root in  roots:
            trees.append( Tree(root, r_trees[root]['edges'], r_trees[root]['cost'] ))
        resp = max(trees).cost
        outfile.write(str(resp)+' ,'+str(round(end-start,6))+' ,')

        #Heuristica 1 LS
        start = time.time()
        r_trees, _ = g.rooted_trees(roots)
        end = time.time()
        trees = []
        for root in  roots:
            trees.append( Tree(root, r_trees[root]['edges'], r_trees[root]['cost'] ))
        resp = local_search(trees,g)
        outfile.write(str(resp)+' ,'+str(round(end-start,6))+' ,')
        #Heuristica 2LS
        start = time.time()
        r_trees = g.greedy_random_sf(roots)
        end = time.time()
        trees = []
        for root in  roots:
            trees.append( Tree(root, r_trees[root]['edges'], r_trees[root]['cost'] ))
        resp = local_search(trees,g)
        outfile.write(str(resp)+' ,'+str(round(end-start,6))+' ,')
        #Heuristica 3LS
        start = time.time()
        r_trees = g.improved_random_sf(roots)
        end = time.time()
        trees = []
        for root in  roots:
            trees.append( Tree(root, r_trees[root]['edges'], r_trees[root]['cost'] ))
        resp = local_search(trees,g)
        outfile.write(str(resp)+' ,'+str(round(end-start,6))+' ,')

        #================================ -
        s = Simulation(g,roots,10**3,0)

        start = time.time()
        _, resp = s.metropolisHasting()
        end = time.time()
        outfile.write(str(resp[-1])+' ,'+str(round(end-start,6))+' ,')

        start = time.time()
        _, resp = s.simulatedAnnealing(10**3, 10**-6, s.linearCoolingStrategy, 0.999)
        end = time.time()
        outfile.write(str(resp[-1])+' ,'+str(round(end-start,6))+' ,')

        start = time.time()
        _, resp = s.simulatedAnnealingRepeated(10**3, 10**-6, s.linearCoolingStrategy, 0.999)
        end = time.time()
        outfile.write(str(resp[-1])+' ,'+str(round(end-start,6)))


        outfile.write('\n')

    print("Total Time", str(time.time() - t_s))

dict_sum = lambda x: sum([i[1] for i in x.items()])
sum_if = lambda x,y: sum([1 for i in x if i==y])
