import math, random, sys, numpy, matplotlib.pyplot as plt

class City: 
    nc = 0 ## number of city instances
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = City.nc ## self-generated with static variable nc
        self.name = "City" + str(City.nc)
        City.nc += 1
    
    def distance(self,nextCity): ## calculates distance between two cities 
        x_difference = self.x - nextCity.x
        y_difference = self.y - nextCity.y 
        result = math.sqrt(x_difference**2 + y_difference**2)

        return result

    def __repr__(self):
        return repr([self.name,self.x,self.y])

def generateRoute(cities): ## generate a random route using cities
    route = random.sample(cities,len(cities))

    return route

def readCityFile(f): ## read file with cities
    fi = open(default_parameters[6],"r")
    cities = []

    for line in fi:
        currentLine = line.split()
        currentCity = City(int(currentLine[1]),int(currentLine[2]))
        currentCity.name = currentLine[0]
        cities.append(currentCity)

    fi.close()
    return cities


class Individual: ## individual with a route
    count = 0

    def __init__(self,route): 
        self.route = route
        self.totalDistance = 0
        self.totalDistance = self.getDistance()
        ## fitness is equal to one over the total distance of the individual's route
        self.fitness = float(1 / self.totalDistance) 
        self.id = Individual.count ## self-generated with variable count
        Individual.count += 1
    
    def getDistance(self): ## return total distance of route
        routeLength = len(self.route)
        dist = 0
        for i in range(0,routeLength):
            currentCity = self.route[i]
            if (i<routeLength-1):    
                nextCity = self.route[i+1]
                dist += currentCity.distance(nextCity)
            else:
                nextCity = self.route[0]
                dist += currentCity.distance(nextCity)

        return dist
    
    def breed(self,parent2): ## "breeds" self with parent2 
        gene1 = [] # inherited from self
        gene2 = [] # inherited from parent2
        l = len(self.route)

        n1 = int(random.random() * l) 
        n2 = int(random.random() * l)
        start = min(n1,n2) 
        end = max(n1,n2)

        for i in range(start,end): ## the subroute [start,end] is retained from first parent
            gene1.append(self.route[i])

        ## take cities from parent2 that have not been retained from parent1
        gene2 = [c for c in parent2.route if c not in gene1] 
        res = gene1 + gene2 ## questionable
        child = Individual(res)

        ### FIX THIS ###
        ##for i in range(len(gene1)):
        ##    gene2.insert(start+i,gene1[i])
        ##child = Individual(gene2)

        return child

    def __repr__(self):
        return repr(self.route)

class generation(): ## generation consists of a list of individuals
    gen_id = 0

    def __init__(self,newGen): ## newGen is list of individuals
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
    def selectPool(self): ## select individuals that will procreate

        self.selected = []
        self.elite = []
        sortedPool = self.population
        sortedPool.sort(key=lambda x: x.fitness, reverse=True) ## sort by fitness (deacresing)
        sortedFitness = [c.fitness for c in sortedPool] ## list of fitness values
        ## following lines generate a weight distribution for individuals
        weights = numpy.cumsum(sortedFitness) 
        totalFitness = sum(sortedFitness)
        percentages = [((c*100)/totalFitness) for c in weights]
        ####

        total_l = len(self.population)
        elite_l = int(total_l * (default_parameters[8] / 100)) ## use input eliteSize 

        for i in range(elite_l): ## add elites to new gen
            self.elite.append(sortedPool[i])
            self.selected.append(sortedPool[i])

        leftToBreed = len(self.population) - len(self.elite) ## subtract the length of elites
        
        for _ in range(leftToBreed):
            irand = random.random() * 100 ## use weights to determine who gets selected
            for i in range(elite_l,total_l):
                if irand <= percentages[i]:
                    self.selected.append(sortedPool[i])
                    break
        return self.selected 

    def mutate(self,gen): 
        mutation_chance = default_parameters[7] ## use input mutation chance
        total_l = len(gen.population)

        for i in range(total_l):
            if (int(random.random() * 100) < mutation_chance):
                iMax = len(gen.population[i].route)
                a = int(random.random() * iMax)
                b = int(random.random() * iMax)
                ## swap two cities in the route
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
            ## select two random individuals from selected pool to breed
            i = int(random.random() * total_l)
            j = int(random.random() * total_l)
            newInd = pool[i].breed(pool[j])
            newPop.append(newInd)

        newGen = generation(newPop)
        self.mutate(newGen)
        return newGen
    
    def __repr__(self):
        return repr(self.population) 

class genBook(): ## contains list of generations, cities, and some statistical data
    gen_book = []
    gen_book_mins = []

    def __init__(self,nInitial,nCities,nGen):
        self.nInitial = nInitial
        self.nCities = nCities
        self.nGen = nGen
        self.genCount = 0
        if (default_parameters[6]=="AUTO"):
            self.cities = self.generateCities()
        else:
            self.cities = readCityFile(default_parameters[6])

        self.gen_book.append(self.generateInitialPopulation())

        for _ in range(nGen-1):
            self.gen_book_mins.append(self.gen_book[self.genCount].getMin())
            self.breedNext()

    def generateCities(self): ## generates random cities in the coordinate system and appends it to cities
        self.cities = []

        for _ in range(0,self.nCities):
            newx = int (random.random() * default_parameters[4]) 
            newy = int (random.random() * default_parameters[5])
            self.cities.append(City(newx,newy))

        return self.cities 

    def generateIndividual(self): ## generates random individual
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

    def breedNext(self): ## breeds next generation using the current one
        self.gen_book.append(self.gen_book[self.genCount].nextGeneration(self.nInitial))
        self.genCount += 1

    def plotDistanceGraph(self): ## plots the progress of minimal distances over the generations
        q = plt.plot(self.gen_book_mins)
        plt.savefig("DistanceGraph.png")
        plt.close()

    def plotRoute(self,ind,gen):
        cities_x = [] 
        cities_y = []
        city_labels = [c.name for c in self.cities]
        cities_x = [c.x for c in genBook1.cities]
        cities_y = [c.y for c in genBook1.cities]
        q = plt.plot(cities_x,cities_y,'go',linewidth=0.5)
        plt.plot(ind.route[0].x,ind.route[0].y,'ro')
        citiesLen = len(city_labels)
        for i in range(citiesLen):
            plt.annotate(city_labels[i],(cities_x[i],cities_y[i]))
        for i in range(citiesLen-1):
            currentDistance = ind.route[i].distance(ind.route[i+1])
            plt.arrow(ind.route[i].x, ind.route[i].y, (ind.route[i+1].x - ind.route[i].x), (ind.route[i+1].y-ind.route[i].y), head_width=15, head_length=50, length_includes_head = True, label = str(currentDistance))
        plt.arrow(ind.route[-1].x, ind.route[-1].y, (ind.route[0].x - ind.route[-1].x), (ind.route[0].y-ind.route[-1].y), head_width=15, head_length=50, length_includes_head = True)        
        plt.ylabel('Y')
        plt.xlabel('X')
        t = "Total distance: " + str(ind.totalDistance)
        plt.title(t)
        filename = "Gen" + str(gen.gen_id) + " route" + str(ind.id) +".png"
        plt.savefig(filename)
        plt.close()

## parameters in the following order:
## [0] ==> args[0] is reserved for script name, so the indexing starts with 1
## [1] nInitial ==> quantity of individuals in initial generation
## [2] nCities ==> number of cities, only used for auto-generated cities (in conjunction with "AUTO" in param 9)
## [3] nGen ==> number of generations to be bred
## [4] XWidth ==> width of x-coordinate of the map
## [5] YWidth ==> width of y-coordinate of the map
## [6] citiesPath ==> path to the file that contains cities 
##     file formatting should be one city per line ==> [Cityname][whitespace][x-coordinate][whitespace][y-coordinate][endline] 
##     input the word "AUTO" to generate random cities
## [7] mRate ==> mutationRate (Percent)
## [8] eliteSize ==> size of elite population (top percentage)

## to skip a certain parameter, input 0 and that one will be defaulted
parameter_names = ["placeholder_name","nInitial","nCities","nGen","XWidth","YWidth","citiesPath","mRate","eliteSize"]
default_parameters = ["placeholder.py",100, 15, 100, 1000, 1000, "TSP-GA-cities.txt", 10, 10]

## parse console input
## sample input: python TSP-GA.py 25 20 30 1500 1500 "TSP-GA-cities.txt" 20 20
argCount = len(sys.argv)
if (argCount < 2):
    print("All parameters set to default values.")
    print()
if (argCount > len(default_parameters)):
    argCount = len(default_parameters)

for i in range(1,argCount):
    if (sys.argv[i] != "0"):
        if (i==6):
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
genBook1.plotDistanceGraph()
genBook1.plotRoute(genBook.gen_book[0].population[0],genBook1.gen_book[0])
genBook1.plotRoute(genBook.gen_book[0].population[default_parameters[1]-1],genBook1.gen_book[0])
genBook1.plotRoute(genBook1.gen_book[default_parameters[3]-1].population[0],genBook1.gen_book[default_parameters[3]-1])
genBook1.plotRoute(genBook1.gen_book[default_parameters[3]-1].population[default_parameters[1]-1],genBook1.gen_book[default_parameters[3]-1])
