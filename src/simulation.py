import random
import queue as Q
import numpy as np
from datetime import datetime
from state import *
from math import exp, log
from tree import *
from util import sum_if
from util import dict_sum
import time

class Simulation():

    graph = None
    bestSolution = None         # State of the best solution found so far
    currentSolution = None      # State of the current algorithm solution (except Hill Climbing)
    initialSolution = None      # State of the initial solution generated on object constructor
    transitionProb = {}         # dictionary with uniform transition probability coming out of the key state
    executions = 1              # number of iterations for the algorithms (except Simulated Annealing)
    roots = None                # List of Forest's roots
    savedStates = None
    def __init__(self, graph, roots, executions = 1, start_random = True):
        random.seed(datetime.now())
        self.roots = roots 
        self.executions = executions
        self.graph = graph
        self.transitionProb = None
        self.transitionProb = {}
        self.initialSolution = State()
        self.currentSolution = State()
        self.savedStates = {}
        items = [None]*self.graph.V
        if(start_random):
            self.graph.make_complete() # Tornar todas as soluçoes viaveis
            for i in range(self.graph.V):
                self.currentSolution.items.append(np.random.choice(self.roots))
                if(i in self.roots):
                    self.currentSolution.items[i] = i
        else:
            r_trees = self.graph.improved_random_sf(roots)
            trees = []
            for root in roots:
                trees.append( Tree(root, r_trees[root]['edges'], r_trees[root]['cost'] ))
            for idx, tree in enumerate(trees):
                for v in tree.vertex:
                    items[v] = tree.root
            self.currentSolution.items = items[:]
            self.graph.make_complete()

        self.currentSolution.alter = [True]*len(self.roots)
        self.currentSolution.costs = [None]*len(self.roots)
        self.currentSolution.roots = self.roots[:]
        self.currentSolution.update(self.graph)
        self.savedStates[self.currentSolution] = self.currentSolution.copy()
        self.initialSolution = self.currentSolution.copy()

    def restartInstance(self):
        self.currentSolution = self.initialSolution.copy()
        self.bestSolution = self.initialSolution.copy()

    def isBetterSolution(self, solution):
        if (solution.objFunction < self.bestSolution.objFunction) or (solution.objFunction == self.bestSolution.objFunction and sum(solution.costs) < sum(self.bestSolution.costs)):
            self.bestSolution = solution.copy()
            return True
        return False

    def allNewStates(self, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()

        possibleStates = []
        for i in range(self.graph.V):
            for root in self.roots:
                new = State()
                new = self.newStateFor(i, root, state)
                if len(new.items) != 0:
                    possibleStates.append(new.copy())
        return possibleStates[:]

    def transitionProbFrom(self, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()

        pij = self.transitionProb.setdefault(state, None)
        if pij == None:
            pij = 1 / len(self.allNewStates(state.copy()))
            self.transitionProb[self.currentSolution] = pij
        return pij

    def newStateFor(self, i, root, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()

        state_i = State()
        state_i = state.copy()
        if(i not in self.roots) and (state_i.items[i] != root):
            old_root = state_i.items[i]
            state_i.items[i] = root
            state_i.alter[self.roots.index(old_root)] = True 
            state_i.alter[self.roots.index(root)] = True
            return state_i
        return State()

    def probNewStateFor(self, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()
        prob_select_root, prob_change_for_root = self.calc_p_root(state.costs)
        prob_tree = self.calc_p_index(state.items)
        prob_index = []
        for i in state.items:
            prob_index.append( prob_tree[i]*prob_select_root[state.roots.index(i)])
        newState = State()
        while len(newState.items) == 0:
            idx = np.random.choice(len(state.items),1, p= prob_index)[0]
            root = np.random.choice(len(state.roots),1, p= prob_change_for_root)[0]
            pij = prob_index[idx]*prob_change_for_root[root]
            newState = self.newStateFor(idx,state.roots[root]).copy()

        pji = self.calc_pji(newState,idx, state.items[idx])
        return newState.copy(), pij, pji

    def calc_pji(self, state, item, old_root):
        pji = None
        prob_select_root, prob_change_for_root = self.calc_p_root(state.costs)
        prob_tree = self.calc_p_index(state.items)
        prob_index = []
        for i in state.items:
            prob_index.append( prob_tree[i]*prob_select_root[state.roots.index(i)])
        root = state.roots.index(old_root)
        pji = prob_index[item]*prob_change_for_root[root]
        return pji

    def calc_p_root(self, cost):
        p = cost[:]
        ret = {
            'h': [],
            'l': []
        }
        sum_p = sum(p)
        n = len(p)-1 if len(p)>1 else 1
        for idx, _ in enumerate(p):
            ret['h'].append(p[idx]/sum_p)
            ret['l'].append((sum_p - p[idx])/(n*sum_p))
        return ret['h'], ret['l']

    def calc_p_index(self, items):
        ret = {}
        for root in self.roots:
            ret[root] = 1/sum_if(items, root)
        return ret

    def newStateForSubtree(self, i, root, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()
        state_i = State()
        state_i = state.copy()
        if(i not in self.roots) and (state_i.items[i] != root):
            old_root = state_i.items[i]
            state_i.items[i] = root
            state_i.alter[self.roots.index(old_root)] = True
            state_i.alter[self.roots.index(root)] = True
            vertices = self.subtree(i, state_i.edges)
            for v in vertices:
                state_i.items[v] = root
            return state_i
        return State()

    def subtree(self, vertex, edges):
        q = Q.Queue()
        ret = []
        q.put(vertex)
        while not q.empty():
            v = q.get()
            ret.append(v)
            for i, j in edges:
                if(v==i):
                    q.put(j)
        return ret

    def randomWalk(self, p):
        self.restartInstance()
        print("Start optimal value:", self.bestSolution.objFunction)
        name = 'Random Walk p = ' + str(p)
        t = 0   # steps
        ret = [self.currentSolution.objFunction]
        while t < self.executions:
            t += 1
            unif = random.random()
            if unif < p:
                possibleStates = self.allNewStates()
                index = random.randint(0, len(possibleStates)-1)
                newState = State()
                newState = possibleStates[index].copy()
                self.currentSolution = newState.copy()
                self.currentSolution.update(self.graph)
                if self.isBetterSolution(self.currentSolution):
                    print("Itt - ",t," - ", self.currentSolution.objFunction)
            ret.append(self.bestSolution.objFunction)
        return name, ret

    def accept(self, newState, pij, pji):
        unif = random.random()
        alfa = (self.currentSolution.objFunction * pji) / (newState.objFunction * pij)
        if unif < alfa:
            return True
        return False

    def calculeteP(self, states):
        p = []
        p_ii = 1
        currentV = self.currentSolution.v
        for state in states:
            p_ij = min(1, state.v / currentV) / len(states)
            p.append(p_ij)
            p_ii -= p_ij
            if p_ij < 0:
                print(state, len(state.items), self.n)
        p.append(p_ii)
        return p[:]

    def metropolisHasting(self):
        self.restartInstance()
        print("Start optimal value:", self.bestSolution.objFunction)
        name = 'Metropolis Hasting'
        t = 0   # steps
        ret = [self.currentSolution.objFunction]
        while t < self.executions:
            t += 1
            currentChanged = False
            newState = State()
            while len(newState.items) == 0:
                index = random.randint(0, self.graph.V-1)
                root = np.random.choice(self.roots)
                newState = self.newStateFor(index,root).copy()

            newState.update(self.graph)
            delta = newState.objFunction - self.currentSolution.objFunction
            if delta < 0:
                # accept = 1
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                if self.accept(newState, 1, 1):
                    self.currentSolution = newState.copy()
                    currentChanged = True

            if currentChanged and self.isBetterSolution(self.currentSolution):
                print("Itt - ",t," - ", self.currentSolution.objFunction)

            ret.append(self.bestSolution.objFunction)
        return name, ret

    def hillClimbing(self):
        self.restartInstance()
        # bestSolution is always currentSolution
        name = 'Hill Climbing'
        t = 0   # steps
        ret = [self.bestSolution.objFunction]

        while 1:
            t += 1
            newState = State()
            newState = min(self.allNewStates(self.bestSolution))
            newState.update(self.graph)
            if self.isBetterSolution(newState):
                ret.append(self.bestSolution.objFunction)
            else:
                ret.append(self.bestSolution.objFunction)
                break
        return name, ret

    def boltzman(self, deltaV, t, pij, pji):
        return exp((-deltaV-(10**(-10)))/t) * (pji / pij)

    def simulatedAnnealing(self, initialT, epsilon, coolingStrategy, beta):
        self.restartInstance()
        def format_e(n):
            #format large number in scientific notation
            a = '%E' % n
            return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]
        print("Start optimal value:", self.bestSolution.objFunction)
        name = 'Simulated Annealing T = ' + str(format_e(initialT)) + ' b = ' + str(beta) + ' ' + coolingStrategy.__name__
        temperature = initialT
        t = 0   # steps
        start = time.time()
        found_time = [0]
        ret = [self.currentSolution.objFunction]
        while temperature > epsilon:
            t += 1
            currentChanged = False
            newState = State()
            while len(newState.items) == 0:
                index = random.randint(0, self.graph.V-1)
                root = np.random.choice(self.roots)
                newState = self.newStateFor(index, root).copy()

            if(newState in self.savedStates):
                newState = self.savedStates[newState].copy()
            else:
                newState.update(self.graph)
                self.savedStates[newState] = newState.copy()

            delta = newState.objFunction-self.currentSolution.objFunction
            if delta < 0:
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                if random.random() < self.boltzman(delta, temperature, 1, 1):
                    self.currentSolution = newState.copy()
                    currentChanged = True

            if currentChanged and self.isBetterSolution(self.currentSolution):
                print("Itt - ",t," - ", self.currentSolution.objFunction)

            ret.append(self.bestSolution.objFunction)
            found_time.append(time.time() - start)
            temperature = coolingStrategy(initialT, beta, t, delta, temperature)
        return name, ret, found_time

    def simulatedAnnealingRepeated(self, initialT, epsilon, coolingStrategy, beta):
        self.restartInstance()
        def format_e(n):
            #format large number in scientific notation
            a = '%E' % n
            return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]
        print("Start optimal value:", self.bestSolution.objFunction)
        name = 'Simulated Annealing T = ' + str(format_e(initialT)) + ' b = ' + str(beta) + ' ' + coolingStrategy.__name__
        temperature = initialT
        t = 0   # steps
        ret = [self.currentSolution.objFunction]
        found_time = [0]
        start = time.time()
        while temperature > epsilon:
            t += 1
            currentChanged = False
            newState = State()
            while len(newState.items) == 0:
                index = random.randint(0, self.graph.V-1)
                root = np.random.choice(self.roots)
                newState = self.newStateFor(index, root).copy()
            if(newState in self.savedStates):
                newState = self.savedStates[newState].copy()
            else:
                newState.update(self.graph)
                self.savedStates[newState] = newState.copy()

            delta = newState.objFunction-self.currentSolution.objFunction
            if delta < 0:
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                if random.random() < self.boltzman(delta, temperature, 1, 1):
                    self.currentSolution = newState.copy()
                    currentChanged = True

            ret.append(self.bestSolution.objFunction)
            found_time.append(time.time() - start)
            if currentChanged and self.isBetterSolution(self.currentSolution):
                print("Itt - ",t," - ", self.currentSolution.objFunction)
            elif(random.random()<0.01):
                continue
            temperature = coolingStrategy(initialT, beta, t, delta, temperature)
        return name, ret, found_time

    def improvedSimulatedAnnealing(self, initialT, epsilon, coolingStrategy, beta):
        self.restartInstance()
        def format_e(n):
            #format large number in scientific notation
            a = '%E' % n
            return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]
        print("Start optimal value:", self.bestSolution.objFunction)
        name = 'Simulated Annealing T = ' + str(format_e(initialT)) + ' b = ' + str(beta) + ' ' + coolingStrategy.__name__
        temperature = initialT
        t = 0   # steps
        ret = [self.currentSolution.objFunction]
        found_time = [0]
        start = time.time()
        while temperature > epsilon:
            t += 1
            currentChanged = False

            index = random.randint(0, self.graph.V-1)
            root = np.random.choice(self.roots)
            newState, pij, pji = self.probNewStateFor()
            if(newState in self.savedStates):
                newState = self.savedStates[newState].copy()
            else:
                newState.update(self.graph)
                self.savedStates[newState] = newState.copy()
            delta = newState.objFunction-self.currentSolution.objFunction
            if delta < 0:
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                if random.random() < self.boltzman(delta, temperature, pij, pji ):
                    self.currentSolution = newState.copy()
                    currentChanged = True

            ret.append(self.bestSolution.objFunction)
            found_time.append(time.time()-start)

            if currentChanged and self.isBetterSolution(self.currentSolution):
                print("Itt - ",t," - ", self.currentSolution.objFunction)
            elif(random.random()<0.01):
                continue
            temperature = coolingStrategy(initialT, beta, t, delta, temperature)
        return name, ret, found_time

    def simulatedAnnealingSubtree(self, initialT, epsilon, coolingStrategy, beta):
        self.restartInstance()
        def format_e(n):
            #format large number in scientific notation
            a = '%E' % n
            return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]
        print("Start optimal value:", self.bestSolution.objFunction)
        name = 'Simulated Annealing T = ' + str(format_e(initialT)) + ' b = ' + str(beta) + ' ' + coolingStrategy.__name__
        temperature = initialT
        t = 0   # steps
        start = time.time()
        ret = [self.currentSolution.objFunction]
        found_time = [0]
        while temperature > epsilon:
            t += 1
            currentChanged = False
            newState = State()
            while len(newState.items) == 0:
                index = random.randint(0, self.graph.V-1)
                root = np.random.choice(self.roots)
                newState = self.newStateForSubtree(index, root).copy()

            if(newState in self.savedStates):
                newState = self.savedStates[newState].copy()
            else:
                newState.update(self.graph)
                self.savedStates[newState] = newState.copy()
            delta = newState.objFunction-self.currentSolution.objFunction

            if delta < 0:
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                if random.random() < self.boltzman(delta, temperature, 1, 1):
                    self.currentSolution = newState.copy()
                    currentChanged = True

            if currentChanged and self.isBetterSolution(self.currentSolution):
                print("Itt - ",t," - ", self.currentSolution.objFunction)

            ret.append(self.bestSolution.objFunction)
            found_time.append(time.time()-start)
            if currentChanged and self.isBetterSolution(self.currentSolution):
                print("Itt - ",t," - ", self.currentSolution.objFunction)
            elif(random.random()<0.005):
                continue
            temperature = coolingStrategy(initialT, beta, t, delta, temperature)
        return name, ret, found_time

    def linearCoolingStrategy(self, initialT, beta, t, delta, temperature):
        return initialT - beta * t

    def expCoolingStrategy(self, initialT, beta, t, delta, temperature):
        return initialT * (beta ** t)

    def dynamicCoolingStrategy(self, initialT, beta, t, delta, temperature):
        if(delta == 0):
            return initialT - beta * t 
        return initialT - beta * t + (log(abs(delta)) / delta) * t

    def geometricCoolingStrategy(self, initialT, beta, t, delta, temperature):
        return temperature*beta