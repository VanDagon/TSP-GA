import math, random, sys, numpy, matplotlib.pyplot as plt

class City:
    nc = 0 ## number of city instances
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = City.nc
        self.name = "City" + str(City.nc)
        City.nc += 1
    
    def distance(self,nextCity):
        x_difference = self.x - nextCity.x
        y_difference = self.y - nextCity.y 
        result = math.sqrt(x_difference**2 + y_difference**2)

        return result

    def __repr__(self):
        return repr([self.name,self.x,self.y])

def generateRoute(cities):
    route = random.sample(cities,len(cities))

    return route

def readCityFile(f):
    fi = open(default_parameters[9],"r")
    cities = []

    for line in fi:
        currentLine = line.split()
        currentCity = City(int(currentLine[1]),int(currentLine[2]))
        currentCity.name = currentLine[0]
        cities.append(currentCity)

    fi.close()
    return cities


class Individual:
    def __init__(self,route): 
        self.route = route
        self.totalDistance = 0
        self.totalDistance = self.getDistance()
        self.fitness = float(1 / self.totalDistance)
    
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
        mean = self.getMean() 
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

    ### use sort instead of standard Deviation
    def selectPool(self): 

        self.selected = []
        self.elite = []
        sortedPool = self.population
        sortedPool.sort(key=lambda x: x.fitness, reverse=True)
        sortedFitness = [c.fitness for c in sortedPool]
        weights = numpy.cumsum(sortedFitness)
        totalFitness = sum(sortedFitness)
        percentages = [((c*100)/totalFitness) for c in weights]
        total_l = len(self.population)
        elite_l = int(total_l * 0.20) ## take top 20% as elite 

        for i in range(elite_l): ## add elites to new gen
            self.elite.append(sortedPool[i])
            self.selected.append(sortedPool[i])

        leftToBreed = len(self.population) - len(self.elite)
        
        for _ in range(leftToBreed):
            irand = random.random() * 100
            for i in range(elite_l,total_l):
                if irand <= percentages[i]:
                    self.selected.append(sortedPool[i])
                    break
        return self.selected 

    def mutate(self,gen):
        mutation_chance = 15
        total_l = len(gen.population)

        for i in range(total_l):
            if (int(random.random() * 100) < mutation_chance):
                iMax = len(gen.population[i].route)
                a = int(random.random() * iMax)
                b = int(random.random() * iMax)
                gen.population[i].route[a], gen.population[i].route[b] = gen.population[i].route[b], gen.population[i].route[a]
        return gen
    
    def nextGeneration(self,nNext): ## breeds new generation from selected pool
        
        newPop = []
        left = nNext
        pool = self.selected
        total_l = len(pool)
        elite_l = len(self.elite)
        newPop.extend(self.elite)
        left = left - elite_l

        for _ in range(left):
            i = int(random.random() * total_l)
            j = int(random.random() * total_l)
            newInd = pool[i].breed(pool[j])
            newPop.append(newInd)

        newGen = generation(newPop)
        self.mutate(newGen)
        return newGen
    
    def __repr__(self):
        return repr(self.population) 

class genBook():
    gen_book = []

    def __init__(self,nInitial,nCities,nGen):
        self.nInitial = nInitial
        self.nCities = nCities
        self.nGen = nGen
        if (default_parameters[9]=="AUTO"):
            self.cities = self.generateCities()
        else:
            self.cities = readCityFile(default_parameters[9])

        self.gen_book.append(self.generateInitialPopulation())

        for _ in range(nGen-1):
            self.breedNext()

    def generateCities(self):
        self.cities = []

        for _ in range(0,self.nCities):
            newx = int (random.random() * default_parameters[4]) 
            newy = int (random.random() * default_parameters[5])
            self.cities.append(City(newx,newy))

        return self.cities 

    def generateIndividual(self): 
        newRoute = generateRoute(self.cities)
        newIndividual = Individual(newRoute)
        newIndividual.getDistance()

        return newIndividual

    def generateInitialPopulation(self):
        population = []
        for _ in range(self.nInitial):
            population.append(self.generateIndividual())

        gen_0 = generation(population)
        self.genCount = 0
        return gen_0

    def breedNext(self):
        self.gen_book.append(self.gen_book[self.genCount].nextGeneration(self.nInitial))
        ##print(self.gen_book[self.genCount].population)
        print(self.gen_book[self.genCount].getMin())
        self.genCount += 1


## parameters in the following order:
## (Caution: args[0] is reserved for script name, so the indexing starts with 1)
## [1] nInitial ==> quantity of individuals in initial generation
## [2] nCities ==> number of cities, only used for auto-generated cities (in conjunction with "AUTO" in param 9)
## [3] nGen ==> number of generations to be bred
## [4] XWidth ==> width of x-coordinate of the map
## [5] YWidth ==> width of y-coordinate of the map
## [6] goodRate ==> percent chance that a 'good' individual (with below mean totalDistance) will be selected
## [7] badRate ==> percent chance that a 'bad' individual (with above mean totalDistance) will be selected
## [8] popMax ==> the hard cap on quantity of individuals in every generation ## not implemented yet
## [9] citiesPath ==> path to the file that contains cities 
##     file formatting should be one city per line ==> [Cityname][whitespace][x-coordinate][whitespace][y-coordinate][endline] 
##     input the word "AUTO" to generate random cities
## [10] popMaxSwitch ==> switch for hard cap on population (for parameter 9), has value 0 or 1

## to skip a certain parameter, input 0 and that one will be defaulted
parameter_names = ["placeholder_name","nInitial","nCities","nGen","XWidth","YWidth","goodRate","badRate","popMax","citiesPath","popMaxSwitch"]
default_parameters = ["placeholder.py",50, 15, 50, 1000, 1000, 70, 40, 50, "TSP-GA-cities.txt", 0]

## parse console input
## sample input: python TSP-GA.py 25 20 30 1500 1500 75 45 50 "TSP-GA-cities.txt" 0
argCount = len(sys.argv)
if (argCount < 2):
    print("All parameters set to default values.")
    print()
if (argCount > len(default_parameters)):
    argCount = len(default_parameters)

for i in range(1,argCount):
    if (sys.argv[i] != "0"):
        if (i==9):
            default_parameters[i] = sys.argv[i]
            print("parameter",i,":",parameter_names[i],"set to",sys.argv[i])
        else:
            n = int(sys.argv[i])
            if (n>=0):
                default_parameters[i] = int(sys.argv[i])
                print("parameter",i,":",parameter_names[i],"set to",sys.argv[i])
            else:
                print("parameter",i,":",parameter_names[i],"is negative. This parameter will take the default value of:",default_parameters[i])
print(default_parameters)

## main:
genBook1 = genBook(default_parameters[1],default_parameters[2],default_parameters[3])
print(genBook1.gen_book[0].population)
gen1 = [c.totalDistance for c in genBook1.gen_book[0].population]
gen_final = [c.totalDistance for c in genBook1.gen_book[genBook1.genCount].population]
plt.plot(gen1,'go',linewidth=2)
plt.ylabel('some numbers')
plt.show()
plt.plot(gen_final,'ro',linewidth=1)
plt.ylabel('some numbers')
plt.show()
""" for i in range(default_parameters[3]):
    print(i,genBook1.gen_book[i])
    print() """
