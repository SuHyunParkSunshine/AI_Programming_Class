import random as rd
import math

DELTA = 0.01   # Mutation step size
LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def createProblem(): ###
    ## Read in an expression and its domain from a file.
    fileName = input("Enter the filename of a fuction: ")
    fileName = f"C:/K-Digital3/AI_Programming/Mr.Gam/Search Tool v1 - program codes/problem/{fileName}.txt"    
    # fileName = f"C:/K-Digital3/AI_Programming/Mr.Gam/Search Tool v1 - program codes/problem/{fileName}.txt"
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


def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of values
    valueC = evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
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
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)


def randomMutant(current, p): ###
    i = rd.randint(0, len(current) - 1) #우리는 0,1,2,3,4를 뽑아내야대기 때문에 '-1'해줘야한다.
    # d = rd.uniform(-DELTA, DELTA)
    if rd.uniform(0,1) > 0.5:
        d = DELTA
    else:
        d = -DELTA
    return mutate(current, i, d, p) # Return a random successor


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

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
    print("Search algorithm: First-Choice Hill Climbing")
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

#first-choice: 단순, 제일 좋진 않아도 좋으면 고!! 따라서, steepest ascent보다 짧게 걸린다.
#steepest ascent: 제일 좋은 걸 찾아서 고!!