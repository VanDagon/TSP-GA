import math, random, pip as np

class City:
    nc = 0 ## number of cities
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = City.nc
        City.nc += 1
    
    def distance(self,nextCity):
        x_difference = self.x - nextCity.x
        y_difference = self.y - nextCity.y 
        result = math.sqrt(x_difference**2 + y_difference**2)

        return result

    def __repr__(self):
        return repr(self.id)

def generateRoute(cities):
    route = random.sample(cities,len(cities))

    return route

class Individual:
    def __init__(self,route): 
        self.route = route
        self.totalDistance = 0
        ##self.fitness = 0 ## not implemented yet
        self.totalDistance = self.getDistance()
    
    def getDistance(self):
        routeLength = len(self.route)

        for i in range(0,routeLength):
            currentCity = self.route[i]
            if (i<routeLength-1):    
                nextCity = self.route[i+1]
                self.totalDistance += currentCity.distance(nextCity)
            else:
                nextCity = self.route[0]
                self.totalDistance += currentCity.distance(nextCity)

        return self.totalDistance
    
    def breed(self,parent2):
        gene1 = [] # inherited from self
        gene2 = [] # inherited from parent2
        l = len(self.route)

        n1 = int(random.random() * l) 
        n2 = int(random.random() * l)

        start = min(n1,n2)
        end = max(n1,n2)

        for i in range(start,end):
            gene1.append(self.route[i])
        gene2 = [c for c in parent2.route if c not in gene1]

        for i in range(len(gene1)):
            gene2.insert(start+i,gene1[i])
        child = Individual(gene2)

        return child

    def __repr__(self):
        return repr(self.totalDistance)

class generation():
    gen_id = 0

    def __init__(self,newGen):
        self.gen_id = generation.gen_id
        generation.gen_id = generation.gen_id + 1
        self.population = []
        self.population.extend(newGen)
        self.getMean()
        self.getStandardDeviation()
        self.getMin()
        self.selectPool()

    def getMean(self):
        sum = 0
        popLen = len(self.population)

        for i in range(popLen):
            sum += self.population[i].totalDistance
        self.mean = sum / popLen

        return self.mean

    def getStandardDeviation(self):
        popLen = len(self.population)
        mean = self.getMean() ## :@ :@ :@
        sum = 0

        for i in range(popLen): 
            sum += (self.population[i].totalDistance - mean) ** 2
        result = math.sqrt(sum)/(popLen - 1)
        self.standardDeviation = result
        return result

    def getMin(self):
        distances = [d.totalDistance for d in self.population]
        self.minimum = min(distances)
        return self.minimum

    def selectPool(self): ## ones below (mean - standardDeviation) will be selected as elite
        good_rate = 70          ## ones below mean have 70% chance of selection
        bad_rate = 40           ## ones above or equal to mean have only 40% chance of selection
        selectedPool = []
        elite_pool = []
        good_pool = []
        bad_pool = []
        mean = self.getMean()
        stDev = self.getStandardDeviation()
        popLen = len(self.population)

        for i in range(popLen):
            if (self.population[i].totalDistance < mean-stDev):
                elite_pool.append(self.population[i])
            elif (self.population[i].totalDistance < mean):
                if (random.random() * 100 < good_rate):
                    good_pool.append(self.population[i])
            else:
                if (random.random() * 100 < bad_rate):
                    bad_pool.append(self.population[i])

        selectedPool.append(elite_pool)
        selectedPool.append(good_pool)
        selectedPool.append(bad_pool)
        self.selected = selectedPool
        return self.selected

    def nextGeneration(self,nNext): ## breeds new generation from selected pool
        newPop = []
        newPop.extend(self.selected[0]) ## add elites to new population
        pool_array = []
        pool_array.extend(self.selected[0])
        pool_array.extend(self.selected[1])
        pool_array.extend(self.selected[2])
        poolLen = len(pool_array)
        eliteLen = len(newPop)

        if (eliteLen >= nNext):
            newGen = generation(newPop)
            return newGen
        else:
            nNext = nNext - eliteLen

        for i in range(nNext):
            j = int(random.random() * poolLen) % nNext
            newInd = pool_array[i%poolLen].breed(pool_array[j])
            newPop.append(newInd)

        newGen = generation(newPop)
        return newGen
    
    def __repr__(self):
        return repr(self.population)

class genBook():
    gen_book = []

    def __init__(self,nInitial,nCities,nGen):
        self.nInitial = nInitial
        self.nCities = nCities
        self.nGen = nGen
        self.cities = self.generateCities()   
        self.gen_book.append(self.generateInitialPopulation())

        for i in range(nGen-1):
            self.breedNext()

    def generateCities(self):
        self.cities = []

        for i in range(0,self.nCities):
            newx = int (random.random() * 1000) 
            newy = int (random.random() * 1000)
            self.cities.append(City(newx,newy))

        return self.cities 

    def generateIndividual(self): 
        newRoute = generateRoute(self.cities)
        newIndividual = Individual(newRoute)
        newIndividual.getDistance()

        return newIndividual

    def generateInitialPopulation(self):
        population = []
        for i in range(self.nInitial):
            population.append(self.generateIndividual())

        gen_0 = generation(population)
        self.genCount = 0
        return gen_0

    def breedNext(self):
        self.gen_book.append(self.gen_book[self.genCount].nextGeneration(self.nInitial))
        self.genCount += 1


## main()
genBook1 = genBook(25,35,100)
""" for i in range(100): ## test
    print(i,' --- ',genBook1.gen_book[i].standardDeviation,' --- ',genBook1.gen_book[i].minimum) """
