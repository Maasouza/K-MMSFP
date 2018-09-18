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
                print("Itt - ",t," - ",temperature,' - ', self.currentSolution.objFunction)

            ret.append(self.bestSolution.objFunction)
            found_time.append(time.time()-start)
            if currentChanged and self.isBetterSolution(self.currentSolution):
                print("Itt - ",t," - ",temperature,' - ', self.currentSolution.objFunction)
            elif(random.random()<0.005):
                continue
            temperature = coolingStrategy(initialT, beta, t, delta, temperature)
        return name, ret, found_time