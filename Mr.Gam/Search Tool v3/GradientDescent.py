## Gradient Descent
# 수치문제에만 사용 가능하고, 조합의 문제에서는 사용할 수 없음

from problem.problem import Numeric

def main():
    p = Numeric()    
    p.setVariables()   # 'p': (expr, domain) #튜플은 값 변환이 안됨
    # Call the search algorithm
    solution, minimum = gradientDescent(p)
    # Show the problem and algorithm settings
    p.storeResult(solution, minimum)
    p.describe()
    displaySetting(p)
    # Report results
    p.report()
    
def gradientDescent(p):     
    current = p.randomInit() 
    valueC = p.evaluate(current)
    while True:
        successor = p.takeStep(current, valueC)
        valueS = p.evaluate(successor)
        if valueS >= valueC:
            break 
        else:
            current = successor
            valueC = valueS
    return current, valueC

def displaySetting(p):
    print()
    print("Search algorithm: Gradient-descent Hill Climbing")
    print()
    print("Mutation step size:", p.getAlpha())

main()
