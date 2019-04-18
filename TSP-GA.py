import math, random, pip as np

class City:
    nc = 0 ## number of cities
    def __init__(self, x, y, id):
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
    
def generateCities():
    cities = []
    nCities = 7 + int(random.random() * 18) ## range is 7-25 cities

    for i in range(0,nCities):
        newx = int (random.random() * 1000) 
        newy = int (random.random() * 1000)
        newid = i
        cities.append(City(newx,newy,newid))

    return cities

def generateRoute(cities):
    route = random.sample(cities,len(cities))

    return route

class Individual:
    def __init__(self,route): 
        self.route = route
        self.totalDistance = 0
        self.fitness = 0
    
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
        self.individuals = []
        self.individuals.append(newGen)


def generateIndividual(cities): 
    newRoute = generateRoute(cities)
    newIndividual = Individual(newRoute)
    newIndividual.getDistance()

    return newIndividual

def generateInitialPopulation(n,cities):
    population = []
    for i in range(n):
        population.append(generateIndividual(cities))

    return population

def getMean(population):
    sum = 0
    popLen = len(population)

    for i in range(popLen):
        sum += population[i].totalDistance
    result = sum / popLen

    return result

def getStandardDeviation(population):
    popLen = len(population)
    mean = getMean(population)
    sum = 0

    for i in range(popLen): 
        sum += (population[i].totalDistance - mean) ** 2
    result = math.sqrt(sum)/(popLen - 1)

    return result

def selectPool(population): ## ones below (mean - standardDeviation) will be selected as elite
    good_rate = 70          ## ones below mean have 70% chance of selection
    bad_rate = 40           ## ones above or equal to mean have only 40% chance of selection
    selectedPool = []
    elite_pool = []
    good_pool = []
    bad_pool = []
    mean = getMean(population)
    stDev = getStandardDeviation(population)
    popLen = len(population)

    for i in range(popLen):
        if (population[i].totalDistance < mean-stDev):
            elite_pool.append(population[i])
        elif (population[i].totalDistance < mean):
            if (random.random() * 100 < good_rate):
                good_pool.append(population[i])
        else:
            if (random.random() * 100 < bad_rate):
                bad_pool.append(population[i])

    """ print("ELITE:",end = ' ') ## testing of selection pool
    elite = [c.totalDistance for c in elite_pool]
    print(elite) 
    print("GOOD:",end = ' ')
    elite = [c.totalDistance for c in good_pool]
    print(elite) 
    print("BAD:",end = ' ')
    elite = [c.totalDistance for c in bad_pool]
    print(elite)  """

    selectedPool.append(elite_pool)
    selectedPool.append(good_pool)
    selectedPool.append(bad_pool)

    return selectedPool

def nextGeneration(pool):
    newGen = []
    newGen.extend(pool[0]) ## add elites to next gen
    pool_array = []
    pool_array.extend(pool[0])
    pool_array.extend(pool[1])
    pool_array.extend(pool[2])
    poolLen = len(pool_array)
    pool_array = random.sample(pool_array,poolLen)
    
    for i in range(poolLen): ## use nMax as loop index max
        j = int(random.random() * poolLen)
        child = pool_array[i].breed(pool_array[j])
        child.getDistance()
        newGen.append(child) 

    return newGen

def loopGens(nGen,nInitial,cities):
    gen_book = []
    pool_book = []
    gen_1 = generateInitialPopulation(nInitial,cities)
    gen_book.append(gen_1)
    
    for i in range(nGen):
        new_pool = selectPool(gen_book[i])
        pool_book.append(new_pool)
        new_gen = nextGeneration(pool_book[i])
        gen_book.append(new_gen)
    
    result = []
    result.append(gen_book)
    result.append(pool_book)
    return result
    


## for testing purposes

cities = generateCities()
nCities = len(cities)
""" for i in range(0,nCities): ## test cities
    print("ID ",i," X:",cities[i].x," Y:" , cities[i].y) """

""" ind_1 = generateIndividual(cities) ## test distance calculations
for i in range(0,len(ind_1.route)):
    print(ind_1.route[i].id, end = ' ')
    if (i + 1 < len(ind_1.route)):
        print("ID ",i," X:",ind_1.route[i].x," Y:" , ind_1.route[i].y," Distance to next:",ind_1.route[i].distance(ind_1.route[i+1]))
 """

""" ind_1 = generateIndividual(cities) ## test breeding
ind_2 = generateIndividual(cities)
ind_3 = ind_1.genNext(ind_2)
for i in range(0,len(ind_1.route)):
    print(ind_1.route[i].id,end = ' ')
print()
for i in range(0,len(ind_2.route)):
    print(ind_2.route[i].id,end = ' ')
print()
for i in range(0,len(ind_3.route)):
    print(ind_3.route[i].id,end = ' ') """

""" gen_1 = generateInitialPopulation(40,cities) ## initial population test
dis = []
for i in range(len(gen_1)):
    dis.append(gen_1[i].getDistance()) """
##print(dis)
 
""" gen_1_mean = getMean(gen_1) ## test gen_2 generation
gen_1_stDev = getStandardDeviation(gen_1)
print (gen_1_mean)
print (gen_1_stDev)
pool_1 = selectPool(gen_1)
gen_2 = nextGeneration(pool_1)
print(len(gen_2)) """

res = loopGens(20,15,cities)

print(len(res[0][0]))
print("NEXT",'\n')
print(len(res[0][19]))

## end testing      

    


