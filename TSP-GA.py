import math, random, pip as np

class City:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
    
    def distance(self,nextCity):
        x_difference = self.x - nextCity.x
        y_difference = self.y - nextCity.y 
        result = math.sqrt(x_difference**2 + y_difference**2)

        return result
    
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
    
    def genNext(self,parent2):
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

def generateIndividual(cities): ## static int as id?!
    newIndividual = Individual(generateRoute(cities))

    return newIndividual

def generateInitialPopulation(n,cities):
    population = []
    for i in range(n):
        population.append(generateIndividual(cities))

    return population

def getMedian(population):
    sum = 0
    popLen = len(population)

    for i in range(popLen):
        sum += population[i].totalDistance
    result = sum / popLen

    return result

def getStandardDeviation(population):
    popLen = len(population)
    median = getMedian(population)
    sum = 0

    for i in range(popLen): 
        sum += (population.totalDistance - median) ** 2
    result = sqrt(sum)/popLen

    return result

def selectPool(population): ## ones below (median - standardDeviation) will be selected as elite
                            ## ones below median have 70% chance of selection
                            ## ones above median have only 30% chance of selection
    



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

gen_1 = generateInitialPopulation(10,cities) ## initial population test
dis = []
for i in range(len(gen_1)):
    dis.append(gen_1[i].getDistance())
## print(dis) 



## end testing      

    


