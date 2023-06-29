import random as rd
import math

#problem/Convex.txt
#problem/Ackley.txt
#problem/Griewank.txt

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain) #튜플은 값 변환이 안됨
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def createProblem(): ###
    ## Read in an expression and its domain from a file.
    fileName = input("Enter the filename of a fuction: ")
    # fileName = f"C:/K-Digital3/AI_Programming/Mr.Gam/Search Tool v1 - program codes/problem/{fileName}.txt"   
    fileName = f"C:/K-Digital3/AI_Programming/Mr.Gam/Search Tool v1 - program codes/problem/{fileName}.txt"    
     
    infile = open(fileName, 'r')
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.    
    ## 'expression' is a string.
    expression = infile.readline().strip()
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    varNames = []
    ## 'low' is a list of lower bounds of the varaibles.
    low = []    
    ## 'up' is a list of upper bounds of the varaibles.
    up = []

    line = infile.readline().strip()
    while line != '':
        data = line.split(',')
        varNames.append(data[0])
        low.append(float(data[1])) #Convert to float
        up.append(float(data[2])) #Convert to float
        line = infile.readline().strip()
    

    domain = [varNames, low, up]
    infile.close()
    return expression, domain


def steepestAscent(p):
    current = randomInit(p) # 'current' is a list of values, 계속 업데이트되는 파트/ randomInit()-> 시작점을 모르기 떄매 random하게 넣어쥼
    valueC = evaluate(current, p) #valueC 시작점에 해당하는 함수값
    while True:
        neighbors = mutants(current, p)
        successor, valueS = bestOf(neighbors, p) #successor(제일 좋은 변수), valueS(제일 좋은 함수값)
        if valueS >= valueC: #현재보다 좋은지 비교(후보값: valueS)
            break #후보값이 더 크면 나빠진 것임으로 탈출
        else:
            current = successor
            valueC = valueS
    return current, valueC


def randomInit(p): ###
    domain = p[1]
    low = domain[1]
    up = domain[2]
    
    init = []
    for i in range(len(low)):
        r = rd.uniform(low[i], up[i]) #uniform low bound, upper bound 에서 수를 랜덤하게 뽑아냄
        init.append(r)
    
    return init    # Return a random initial point
                   # as a list of values

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval #함수 내부에서 값이 바뀔때는 global 선언을 해주어야 한다. 
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    # domain = p[1] # p[1] is domain
    # varNames = domain[0]  
    varNames = p[1][0]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i]) #ex. 'x1 = 3.2' 이런식으로 들어감
        exec(assignment) #exec함수: statement 계산 (String 값) -> 문자열로 표현된 식을 exec함수가 계산 가능한 함수로 인식
    return eval(expr) 
    #eval함수: expression 계산 (String 값) -> 문자열로 표현된 식을 exec함수가 계산 가능한 함수로 인식

def mutants(current, p): ###
    neighbors = []
    for i in range(len(current)):
        mutant = mutate(current, i, DELTA, p)
        neighbors.append(mutant)
        mutant = mutate(current, i, -DELTA, p)
        neighbors.append(mutant)

    return neighbors     # Return a set of successors


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(best, p)

    # for successor in range(1, len(neighbors)):
    #     successorVal = evaluate(successor, p)
    #     if successorVal < bestValue:
    #         best = successor
    #         bestValue = successorVal     

    for i in range(1, len(neighbors)):
        newValue = evaluate(neighbors[i], p)
        if newValue < bestValue:
            best = neighbors[i]
            bestValue = newValue

    return best, bestValue

def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple


main()
