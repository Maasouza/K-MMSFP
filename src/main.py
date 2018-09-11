from grafo import *
import time
from tree import *
from simulation import *
from graph_plot import *
from genetico import *
import numpy as np

test_file = '../data/ran-50-100-1.dat'
g = Graph(test_file)
roots = [0, 41]
# #################################### Genetico

# ag = AG(50,1000, 0.2,0.4, 0.05, g, roots)
# ag.run()

####################################
# g.make_uncomplete()
# r_trees = g.greedy_random_sf(roots)
# end = time.time()
# trees = []
# for root in  roots:
#     trees.append( Tree(root, r_trees[root]['edges'], r_trees[root]['cost'] ))
# resp = max(trees).cost
# print(resp)
# with open("../sol.txt",'w') as arq:
#     for tree in trees:
#         arq.write("\n"+str(tree.root)+"\n")
#         for u, v in tree.edges:
#             arq.write(str(u)+" "+str(v)+"\n")
######################################
# s = Simulation(g, roots, 10**4,0)
# _ , resp, t = s.simulatedAnnealingSubtree(5*(10**3), 10**-3, s.linearCoolingStrategy, 0.9)
# best = s.bestSolution.items
# print(resp[-1], t[resp.index(resp[-1])] , best)
# trees = []
# g.make_uncomplete()
# for root in roots:
#     used=[]
#     for v in best:
#         used.append( 0 if v == root else 1)
#     sol = g.mst(v=root,marked=used)
#     trees.append( Tree(root, sol['edges'], sol['cost'] ))
# for tree in trees:
#     x = 0
#     for u,v in tree.edges:
#         x+= g.adj_matrix[u][v]
# plot_viz(trees, roots,g)
#+=========================================================================================================
#outfile = open("../resultados-5501-6000.csv","w")
#outfile = open("../qlqr.csv","w")
infile = open("../new.csv",'r')
infile.readline()
n = 50
for idx, line in enumerate(infile):
    file, bub, r1, r2 = line.split(",")
    r2 = str(int(r2))
    bub = int(bub)
    outfile = open('../metric/'+r1+'-'+r2+file,'w')
    outfile2 = open('../tttplot/'+r1+'-'+r2+file,'w')
    outfile.write('file, r1, r2, meanttb, tmean, min, max, avg, std\n')
    outfile2.write('file, r1, r2, ttb, tt1%, tt5%\n')


    g = Graph("../data/"+file)
    roots = [int(r1)-1,int(r2)-1]
    s = Simulation(g,roots,10**4,0)

    res = []
    tb = []
    totalT = []

    for i in range(n):
        print(idx,'-' ,file,'- itt -',i)
        t_s = time.time()
        _, resp, t = s.simulatedAnnealingSubtree(5*(10**3), 10**-2, s.linearCoolingStrategy, 0.99)
        t_e = time.time()
        totalT.append(t_e - t_s)
        res.append(resp[-1])
        tb.append(round(t[resp.index(resp[-1])],6))
        ttb = None
        t1pc = None
        t5pc = None
        for idk, r in enumerate(resp):
            if( r <= bub and ttb == None):
                ttb = t[idk]
            elif( r <= bub*1.01 and t1pc == None):
                t1pc = t[idk]
            elif( r <= bub*1.05 and t5pc == None):
                t5pc = t[idk]
            if(ttb != None and t1pc!= None and t5pc != None):
                break
        if(ttb == None):
            ttb = 3600
        if(t1pc == None):
            t1pc = 3600
        if(t5pc == None):
            t5pc = 9999
        outfile2.write(file+','+str(r1)+','+str(r2)+','+str(ttb)+','+str(t1pc)+','+str(t5pc)+'\n')
    outfile.write(file+','+str(r1)+','+str(r2)+','+str(np.mean(tb))+','+str(np.mean(totalT))+','+str(min(res))+','+str(max(res))+','+str(np.mean(res))+','+str(np.std(res))+'\n')
    outfile.close()
    outfile2.close()
