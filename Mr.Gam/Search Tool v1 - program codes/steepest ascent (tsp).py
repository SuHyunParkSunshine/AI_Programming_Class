import random as rd
import math

NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, table(-> 직선거리 미리계산))
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)
    
def createProblem():
    ## Read in a TSP (# of cities, locatioins) from a file.
    ## Then, create a problem instance and return it.
    fileName = input("Enter the file name of a TSP: ")
    fileName = f"C:\K-Digital3\AI_Programming\Mr.Gam\Search Tool v1 - program codes\problem\{fileName}.txt" 
    infile = open(fileName, 'r')
    # First line is number of cities
    numCities = int(infile.readline()) #첫번째 라인: 도시수
    locations = []
    line = infile.readline()  # The rest of the lines are locations
    while line != '': #라인이 끝날때까지
        locations.append(eval(line)) # Make a tuple and append eval(line) -> string으로 들어감
        line = infile.readline()
    infile.close()
    table = calcDistanceTable(numCities, locations)
    return numCities, locations, table #이렇게 return 하면 tuple화 됨.


def calcDistanceTable(numCities, locations): ###
    table = [] #2d
    for i in range(numCities):
        row = []
        for j in range(numCities):
            dx = locations[i][0] - locations[j][0]
            dy = locations[i][1] - locations[j][1]
            d = round(math.sqrt(dx**2 + dy**2), 1) #거리 계산 후 소수 첫째자리까지 표시!!
            row.append(d)
        table.append(row)

    #table 각각 도시 간의 거리
    return table # A symmetric matrix of pairwise distances


def steepestAscent(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def randomInit(p):   # Return a random initial tour
    n = p[0] #도시 수
    init = list(range(n)) #0~n-1까지의 리스트가 만들어짐
    rd.shuffle(init)
    return init


def evaluate(current, p): ###
    global NumEval
    NumEval += 1
    n = p[0]
    table = p[2]
    cost = 0 #인접한 도시들의 거리를 더한 것
    # 되기는 하는데 이해는 못하는 내가 짠 코드
    # numCities, _, table = p
    # for i in range(numCities - 1):
    #    r = current[i]
    #    rr = current[i + 1]
    #    cost += table[r][rr]
    ## Calculate the tour cost of 'current'
    ## 'p' is a Problem instance
    ## 'current' is a list of city ids
    for i in range(n-1):
        locFrom = current[i]
        locTo = current[i+1]
        cost += table[locFrom][locTo]
    cost += table[current[n-1]][current[0]] #맨 마지막에 돌아가야 하기 때문에 처음으로 돌아가는 거리를 더해쥼.
    return cost


def mutants(current, p): # Apply inversion
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = [] #비교해서 같은 값이 있는지 없는지 체크용
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([rd.randrange(n) for _ in range(2)]) #random 하게 2개 값을 뽑아냄
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j) #뽑은 구간을 inversion한다.뒤집기 고고
            count += 1
            neighbors.append(curCopy)
    return neighbors #n개의 후보를 뽑게 됨

def inversion(current, i, j):  ## Perform inversion
    curCopy = current[:]
    while i < j:
        curCopy[i], curCopy[j] = curCopy[j], curCopy[i] #i번째 j번째 해당하는 값 한번에 바꿔버리기
        i += 1
        j -= 1
        ##-- 양쪽에서 좁혀오면서 양쪽끝단들을 서로 바꿔치기 하는 중
    return curCopy #뽑아내서 inversion 한 변경된current(curCopy) 그잡채를 return 함, current 자체를 변경하여 업데이트 해버리면 원 데이터를 잃어버릴수 있음으로 curCopy에 저장

def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(best, p)

    for i in range(1, len(neighbors)):
        newValue = evaluate(neighbors[i], p)
        if newValue < bestValue:
            best = neighbors[i]
            bestValue = newValue

    return best, bestValue

def describeProblem(p):
    print()
    n = p[0]
    print("Number of cities:", n)
    print("City locations:")
    locations = p[1]
    for i in range(n):
        print("{0:>12}".format(str(locations[i])), end = '')
        if i % 5 == 4:
            print()

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

def displayResult(solution, minimum):
    print()
    print("Best order of visits:")
    tenPerRow(solution)       # Print 10 cities per row
    print("Minimum tour cost: {0:,}".format(round(minimum)))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def tenPerRow(solution):
    for i in range(len(solution)):
        print("{0:>5}".format(solution[i]), end='')
        if i % 10 == 9:
            print()

main()
