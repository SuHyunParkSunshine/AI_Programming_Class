from problem.problem import Numeric

def main():
    p = Numeric()    
    p.setVariables()   # 'p': (expr, domain) #튜플은 값 변환이 안됨
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting(p)
    # Report results
    p.report()
    
def steepestAscent(p):     
    current = p.randomInit() 
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = bestOf(neighbors, p) 
        if valueS >= valueC:
            break 
        else:
            current = successor
            valueC = valueS
    return current, valueC

def bestOf(neighbors, p): 
    best = neighbors[0]
    bestValue = p.evaluate(best)

    for i in range(1, len(neighbors)):
        newValue = p.evaluate(neighbors[i])
        if newValue < bestValue:
            best = neighbors[i]
            bestValue = newValue

    return best, bestValue

def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())

main()
