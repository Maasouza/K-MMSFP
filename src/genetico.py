import numpy as np
class AG:

    def __init__(self, population, generations, bornRate, deathRate, mutationRate, grafo, roots):
        self.roots = roots
        self.grafo = grafo
        self.grafo.make_complete()
        self.generations = generations
        self.bornRate = bornRate
        self.deathRate =deathRate
        # self.crossoverType = crossoverType
        self.prob = []
        self.all_cost = 0
        self.mutationRate = mutationRate
        self.population = []
        self.initialPop = population
        for _ in range(population):
            person = []
            for i in range(grafo.V):
                person.append(np.random.choice(roots))
            for root in roots:
                person[root] = root
            self.population.append([person,None,0])
        self.evaluate()

    def resetInstance(self):
        self.population = []
        for _ in range(self.initialPop):
            person = []
            for i in range(self.grafo.V):
                person.append(np.random.choice(self.roots))
            for root in self.roots:
                person[root] = root
            self.population.append([person,None,0])
        self.evaluate()

    def evaluate(self):
        self.prob = []
        self.all_cost = 0
        for idx, person in enumerate(self.population):
            cost = []
            objFunction = 0
            if(person[2]==0):
                for root in self.roots:
                    used = [0 if root == gene else 1 for gene in person[0]]
                    cost.append(self.grafo.mst(root, marked = used)['cost'])
                objFunction = max(cost)
            else:
                objFunction = person[1]
            self.population[idx][1] = objFunction
            self.population[idx][2] = 1
            self.prob.append(objFunction)
            self.all_cost += objFunction

        for idx, _ in enumerate(self.prob):
            self.prob[idx] =  (self.all_cost - self.prob[idx]) / (( len(self.prob)-1)*self.all_cost)

    def crossover(self):
        number_of_sons = round(self.initialPop*self.bornRate)
        number_of_deaths = round(self.initialPop*self.deathRate)
        filhos = []
        n_pais = len(self.roots)
        for _ in range(number_of_sons):
            pais = np.random.choice(len(self.population), 2 , p=self.prob)
            pais = [self.population[i] for i in pais]
            mutate = np.random.random()
            filho = []
            if(np.random.random() < self.bornRate):
                for i in range(self.grafo.V):
                    if(mutate < self.mutationRate and i not in self.roots):
                        filho.append(np.random.choice(self.roots))
                    else:
                        p = self.calc_prob(pais)
                        idx = np.random.choice(len(pais),p = p)
                        filho.append(pais[idx][0][i])
                filhos.append([filho,None,0])

        deaths = 0
        mean = self.all_cost/len(self.population)
        will_die = []
        for idx, person in enumerate(self.population):
            if(person[1] > mean):
                del self.population[idx]
                deaths+=1
                if(deaths == number_of_deaths):
                    break
        self.population.extend(filhos[:])
        delta = self.initialPop - len(self.population)
        for i in range(delta):
            self.population.append([self.create_random(), None, 0])

    def create_random(self):
        person = []
        for i in range(self.grafo.V):
            person.append(np.random.choice(self.roots))
        for root in self.roots:
            person[root] = root
        return person

    def calc_prob(self, v):
        cost = 0
        n = len(v)-1
        p = []
        for i in v:
            cost += i[1]
            p.append(i[1])
        for i,_ in enumerate(p):
            p[i] = (cost - p[i])/(n*cost)
        return p


    def bestSolution(self):
        return sorted(self.population, key = lambda x:x[1])[0]

    def run(self):
        t = 0
        self.resetInstance()
        while t<self.generations:
            t+=1
            self.crossover()
            self.evaluate()
        return self.bestSolution()[1]