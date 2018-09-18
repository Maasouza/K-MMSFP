from grafo import *
import time
from tree import *
from simulation import *
from graph_plot import *
from genetico import *
import numpy as np


from os import listdir
from os.path import isfile, join
path = '../data/'
files = [f for f in listdir(path) if isfile(join(path, f))]
out = open('../3k.csv','w')
out.write('file #nodes r1 r2 value time')
for file in files:
    print(file)
    g = Graph(path+file)
    roots = [random.randint(0,6),random.randint(7,13),random.randint(14,19)]
    g.make_complete()
    s = Simulation(g,roots,10**4,0)
    t_s = time.time()
    _, resp, _ = s.simulatedAnnealingSubtree((10**3), 10**-3, s.linearCoolingStrategy, 0.9)
    t_f = time.time()
    out.write(file+' '+str(g.V)+' '+str(roots[0])+' '+str(roots[1])+' '+str(roots[2])+' '+str(resp[-1])+' '+str(t_f - t_s)+'\n')