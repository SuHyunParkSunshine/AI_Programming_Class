import math
import random

#interface
class Problem:
    def __init__(self): #생성자(Constructor) '__init__': initialise
        self._solution = [] #'_' 외부에 보여주기 싫은 클래스 변수임을 나타냄.
        self._value = 0 #python 'self'는 java의 'this'
        self._numEval = 0

    def setVariables(self): #createProblem
        pass #numeric 이랑 tsp에서 따로 overriding 해서 만들어 줘야 함.

    def randomInit(self):
        pass

    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self):
        pass

    def describe(self): #describeProblem: 어떤 문제를 풀었는지 출력해주는 함수
        pass

    def storeResult(self, solution, value): #최종 솔루션을 저장하는 항수
        self._solution = solution
        self._value = value

    def report(self):
        #numEval 출력해주는 것
        print()
        print("Total number of evaluations: {0:,}".format(self._numEval))

class Numeric(Problem): # Problem에서 상속을 받겠다.
    def __init__(self):
        Problem.__init__(self) #problem에 있는 initialisation도 사용하겟다이? super class의 initialise한 걸 쓰겟다.
        self._expression = ''
        self._domain = []
        self._delta = 0.01    

        # Gradient Descent에 사용할 변수
        self._alpha = 0.01
        self._dx = 10 ** (-4)    

    def getDelta(self):
        return self._delta    

    def getAlpha(self):
        return self._alpha

    def getDx(self):
        return self._dx

    def setVariables(self): #createProblem        
        fileName = input("Enter the filename of a fuction: ")
        fileName = f"C:/K-Digital3/AI_Programming/Mr.Gam/Search Tool v1 - program codes/problem/{fileName}.txt"        
        infile = open(fileName, 'r')        
        self._expression = infile.readline().strip()
        
        varNames = []        
        low = []        
        up = []

        line = infile.readline().strip()
        while line != '':
            data = line.split(',')
            varNames.append(data[0])
            low.append(float(data[1])) #Convert to float
            up.append(float(data[2])) #Convert to float
            line = infile.readline().strip()    

        self._domain = [varNames, low, up]
        infile.close()
        # 이미 변수에 저장이 되었기 때문에 굳이 return 필요 없음

    def takeStep(self, x, v):
        # x: 현재 변수 값/ y: 함수 값
        grad = self.gradient(x, v)
        xCopy = x[:]

        for i in range(len(x)):
            xCopy[i] -= self._alpha * grad[i]
        
        if self.isLegal(xCopy):
            return xCopy # domain 범위 내면 업데이트
        else:
            return x # domain 범위 밖이면 그대로
        
    def isLegal(self, x):
        domain = self._domain
        low, up = domain[1], domain[2]
        for i in range(len(low)):
            l, u = low[i], up[i]
            if l <= x[i] <= u:
                pass
            else:
                return False
        return True

    def gradient(self, x, v):
        grad = []

        for i in range(len(x)):
            xCopy = x[:]
            xCopy[i] += self._dx

            df = self.evaluate(xCopy) - v
            g = df / self._dx

            grad.append(g)
        return grad

    def randomInit(self):
        domain = self._domain
        low = domain[1]
        up = domain[2]
    
        init = []
        for i in range(len(low)):
            r = random.uniform(low[i], up[i]) #uniform low bound, upper bound 에서 수를 랜덤하게 뽑아냄
            init.append(r)

        return init    # Return a random initial point
                   # as a list of values

    def evaluate(self, current):
                   
        self._numEval += 1
        expr = self._expression       
        varNames = self._domain[0] ##check later!!
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i]) 
            exec(assignment) 
        return eval(expr) 

    def mutants(self, current):
        neighbors = []
        for i in range(len(current)):
            mutant = self.mutate(current, i, self._delta)
            neighbors.append(mutant)
            mutant = self.mutate(current, i, -self._delta)
            neighbors.append(mutant)

        return neighbors
     
    def mutate(self, current, i, d): 
        curCopy = current[:]
        domain = self._domain      
        l = domain[1][i]   
        u = domain[2][i]   
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def randomMutant(self, current):
        i = random.randint(0, len(current) - 1) 
        if random.uniform(0,1) > 0.5:
            d = self._delta
        else:
            d = -self._delta
        return self.mutate(current, i, d) 

    def describe(self): #describeProblem: 어떤 문제를 풀었는지 출력해주는 함수
        print()
        print("Objective function:")
        print(self._domain[0])   # Expression
        print("Search space:")
        varNames = self._domain[0] # p[1] is domain: [VarNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i])) 

    def report(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._value)) #self._value는 minimum을 의미
        
        #Problem class의 report를 가져다 쓰겟다.
        Problem.report(self) #super().report
    
    def coordinate(self):
        c = [round(value, 3) for value in self._solution] #self._solution의 각각의 값을 value
        return tuple(c)  # Convert the list to a tuple

class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []
        self._distanceTable = []

    def setVariables(self): #createProblem
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = input("Enter the file name of a TSP: ")
        fileName = f"C:\K-Digital3\AI_Programming\Mr.Gam\Search Tool v1 - program codes\problem\{fileName}.txt" 
        infile = open(fileName, 'r')        
        self._numCities = int(infile.readline())         
        line = infile.readline()  
        while line != '': 
            self._locations.append(eval(line)) 
            line = infile.readline()
        infile.close()
        self._distanceTable = self.calcDistanceTable()
            
    def calcDistanceTable(self): ###
        table = [] #2d
        locations = self._locations
        for i in range(self._numCities):
            row = []
            for j in range(self._numCities):
                dx = locations[i][0] - locations[j][0]
                dy = locations[i][1] - locations[j][1]
                d = round(math.sqrt(dx**2 + dy**2), 1) #거리 계산 후 소수 첫째자리까지 표시!!
                row.append(d)
            table.append(row)   
        return table # A symmetric matrix of pairwise distances

    def randomInit(self):
        n = self._numCities #도시 수
        init = list(range(n)) #0~n-1까지의 리스트가 만들어짐
        random.shuffle(init)
        return init

    def evaluate(self, current):
        self._numEval += 1
        n = self._numCities
        table = self._distanceTable
        cost = 0 
        for i in range(n-1):
            locFrom = current[i]
            locTo = current[i+1]
            cost += table[locFrom][locTo]
        cost += table[current[n-1]][current[0]]
        return cost

    def mutants(self, current):
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n: 
            i, j = sorted([random.randrange(n) for _ in range(2)]) 
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j) 
                count += 1
                neighbors.append(curCopy)
        return neighbors 
    
    def inversion(self, current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i] #i번째 j번째 해당하는 값 한번에 바꿔버리기
            i += 1
            j -= 1
            ##-- 양쪽에서 좁혀오면서 양쪽끝단들을 서로 바꿔치기 하는 중
        return curCopy

    def randomMutant(self, current):
        while True:
            i, j = sorted([random.randrange(self._numCities)
                        for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def describe(self): #describeProblem: 어떤 문제를 풀었는지 출력해주는 함수
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def report(self):
        #Overriding
        print()
        print("Best order of visits:")
        self.tenPerRow()       # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        
        Problem.report(self)

    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()