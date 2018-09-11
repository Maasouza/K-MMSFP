import queue as Q
import numpy as np
import math
from util import *

class Graph:
    def __init__(self, file = None, numVertex = 0):
        self.V = numVertex
        self.E = 0
        self.maxWeight = 0
        self.file = file
        self.edges = {}
        self.adj_matrix = [[0 for x in range(self.V)] for y in range(self.V)]
        self.adj_list = {}
        if(file != None):
            self.read_file(file)
        self.subtrees = {}

    def read_file(self, file):
        with open(file,'r') as file:
            self.V, self.E = map(int,file.readline().split())
            self.adj_matrix = [[0 for x in range(self.V)] for y in range(self.V)] 
            for i in range(self.E):
                i, j, c = map(int,file.readline().split())
                self.addEdge(i-1, j-1, c)
                self.addEdge(j-1, i-1, c)
                self.maxWeight += c

    def addEdge(self, i, j, c):
        '''Adiciona ou altera o valor da aresta i,j'''
        self.edges[(i,j)] = c
        self.edges[(j,i)] = c
        self.adj_list.setdefault(i,{})[j] = c
        self.adj_list.setdefault(j,{})[i] = c
        self.adj_matrix[i][j] = c
        self.adj_matrix[j][i] = c

    def removeEdge(self, i, j):
        self.edges.pop((i,j),None)
        self.edges.pop((j,i),None)
        self.adj_list[i].pop(j,None)
        self.adj_list[j].pop(i,None)
        self.adj_matrix[i][j] = 0
        self.adj_matrix[j][i] = 0

    def mst(self, v=0, roots=[], marked = None  ):
        st_root = v
        if(len(roots)>1):
            st_root = roots[0]
            v = roots[0]
        tree_cost = 0
        used = 0
        if(marked != None):
            inMST = marked
            used = sum(marked)
        else:
            inMST = [False]*self.V
        key = {}
        tree = {}
        heap = Q.PriorityQueue()
        for i in range(self.V):
            tree[i] = -1
            key[i] = math.inf
        key[v] = 0
        heap.put((key[v], v))
        while used != self.V:
            h = heap.get()
            u = h[1]
            w = h[0]
            if(inMST[u] == True):
                continue
            inMST[u] = True
            used += 1
            tree_cost+=w
            for adj in self.adj_list[u].items():
                v = adj[0]
                w = adj[1]
                if (inMST[v] == False) and (key[v]>w):
                    key[v] = w
                    heap.put((key[v],v))
                    tree[v] = u

        spanning_tree = {
            'root': st_root,
            'cost': tree_cost,
            'edges': set()
            }

        for v in roots:
            tree[v] = -1

        for edge in tree.items():
            if(edge[1]==-1):
                continue
            spanning_tree['edges'].add((edge[1],edge[0]))
        return spanning_tree

    def rooted_trees(self, roots):
        self.subtrees = {}
        rootEdges = []
        for i in range(len(roots)-1):
            for j in range(i+1,len(roots)):
                rootEdges.append((roots[i], roots[j]))
                rootEdges.append((roots[j], roots[i]))
                self.addEdge(roots[i], roots[j], 0)
        bottleneck_tree = self.mst(roots = roots)

        for root in roots:
            self.subtrees[root] = {
                'cost': 0,
                'edges': set(),
            }
            q = Q.Queue()
            q.put(root)
            while not q.empty():
                v = q.get()
                for edge in bottleneck_tree['edges']:
                    if(v in edge) and   (edge not in self.subtrees[root]['edges'] ):
                        self.subtrees[root]['edges'].add(edge)
                        self.subtrees[root]['cost'] += self.adj_matrix[edge[0]][edge[1]]
                        if(v == edge[0]):
                            q.put(edge[1])
                        else:
                            q.put(edge[0])
        for i in range(len(roots)-1):
            for j in range(i+1,len(roots)):
                self.removeEdge(roots[i], roots[j])
        return self.subtrees, bottleneck_tree

    def greedy_random_sf(self, roots):
        self.subtrees = {}
        heapDict = {}
        inST = [False]*self.V
        used = len(roots)
        key = {}
        cur_tree = roots[0]
        for root in roots:
            inST[root] = True
            key[root] = [math.inf]*self.V
            heapDict[root] = Q.PriorityQueue()
            self.subtrees[root] = {
                'cost':0,
                'edges': set()
            }
            for adj in self.adj_list[root].items():
                # item = (cost, (v, parent[v])
                key[root][adj[0]] = adj[1]
                item = (adj[1],(adj[0],root))
                heapDict[root].put(item)

        while used != self.V:
            item = heapDict[cur_tree].get()
            c = item[0]
            v,parent = item[1]
            if(inST[v]):
                continue
            inST[v] = True
            used+=1
            self.subtrees[cur_tree]['cost']+=c
            self.subtrees[cur_tree]['edges'].add((parent, v))
            for adj in self.adj_list[v].items():
                i =  adj[0]
                c = adj[1]
                if (not inST[i]) and (key[cur_tree][i]>c):
                    key[cur_tree][i] = c
                    item = (c,(i,v))
                    heapDict[cur_tree].put(item)
            for root in roots:
                cost = self.subtrees[root]['cost']
                if(cost<= self.subtrees[cur_tree]['cost']):
                    cur_tree = root
        return self.subtrees

    def improved_random_sf(self, roots):
        self.subtrees = {}
        heapDict = {}
        inST = [False]*self.V
        used = len(roots)
        key = {}
        cur_tree = roots[0]
        target = 0
        for root in roots:
            inST[root] = True
            key[root] = [math.inf]*self.V
            heapDict[root] = Q.PriorityQueue()
            self.subtrees[root] = {
                'cost':0,
                'edges': set()
            }
            for adj in self.adj_list[root].items():
                # item = (cost, (v, root))
                key[root][adj[0]] = adj[1]
                item = (adj[1],(adj[0],root))
                heapDict[root].put(item)
        #selecting first tree
        possible_trees = set()
        for root in roots:
            if(len(heapDict[root].queue) > 0):
                min_vertex = heapDict[root].queue[0]
                item = (root, min_vertex[0])
                possible_trees.add(item)
        cur_tree = min_set(possible_trees)[0]
        possible_trees.clear()
        while used != self.V:

            item = heapDict[cur_tree].get()
            c = item[0]
            v,parent = item[1]

            if(inST[v]):
                continue
            inST[v] = True
            used+=1

            self.subtrees[cur_tree]['cost']+=c
            self.subtrees[cur_tree]['edges'].add((parent, v))

            for adj in self.adj_list[v].items():
                i =  adj[0]
                c = adj[1]
                if (not inST[i]) and (key[cur_tree][i]>c):
                    key[cur_tree][i] = c
                    item = (c,(i,v))
                    heapDict[cur_tree].put(item)

            for root in roots:
                if(len(heapDict[root].queue) > 0):
                    min_vertex = heapDict[root].queue[0]
                    item = (root,self.subtrees[root]['cost']+min_vertex[0])
                    possible_trees.add(item)

            cur_tree = min_set(possible_trees)[0]
            possible_trees.clear()

        return self.subtrees

    def get_prob(self, roots):
        probs = []
        for i in range(self.V):
            dist_sum = 0
            prob = [0]*len(roots)
            if(i in roots):
                prob[roots.index(i)] = 1
                probs.append(prob)
                continue
            for idx, r in enumerate(roots):
                dist_sum +=  self.adj_list[i].setdefault(r,0)
                prob[idx] = self.adj_list[i].setdefault(r,0)

            for idx in range(len(prob)):
                if(prob[idx]!=0):
                    prob[idx] = (dist_sum - prob[idx])/((len(prob)-1)*dist_sum)
            probs.append(prob)
        return probs

    def mst_from_probs(self, roots, probs):
        vertex_list = {}
        spanning_tree = {}
        for root in roots:
            spanning_tree[root] = None
            vertex_list[root] = [True]*self.V

        for idx, prob in enumerate(probs):
            tree = np.random.choice(roots, p = prob)
            vertex_list[tree][idx] = False

        for root in roots:
            spanning_tree[root] = self.mst(root, marked = vertex_list[root])

        return spanning_tree

    def make_complete(self):
        for i in range(self.V-1):
            for j in range(i+1,self.V):
                if((i, j) not in self.edges and (j,i) not in self.edges):
                    self.addEdge(i, j, self.maxWeight+1)

    def make_uncomplete(self):
        for i in range(self.V-1):
            for j in range(i+1,self.V):
                if(self.adj_matrix[i][j]==self.maxWeight+1):
                    self.removeEdge(i, j)

    def __repr__(self):
        ret = 'Grafo\n\t |V| => '+str(self.V)+'\n\t |E| => '+str(self.E)+'\n Matrix de adjacencia\n'
        for i in  self.adj_matrix:
            ret += str(i)+'\n'
        return ret