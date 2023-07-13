from problem.problem import *
from Optimizer import *

def main():
    p, pType = selectProblem() #sub function # pType(= 1(Numeric) or 2(Tsp))
    alg = selectAlgorithm(pType) #알고리즘 선택
    
    alg.run(p) # 실행    

    p.describe()
    alg.displaySetting()
    # Report results
    p.report()

def selectProblem():
    print("Select the problem type: ")
    print("1. Numeric")
    print("2. Tsp")

    pType = int(input("Enter the number: "))

    if pType == 1:
        p = Numeric()
    elif pType == 2:
        p = Tsp()
    else:
        print("Choose from the number given!!")

    p.setVariables()
    return p, pType

def selectAlgorithm(pType):
    print()
    print("Select Algorithm: ")
    print("1. Steepest Acent")
    print("2. First Choice")
    print("3. Gradient Decent")

    aType = int(input("Enter the number: "))

    # if문을 사용한 방법
    # if aType == 1:
    #     alg = SteepestAcent()
    # elif aType == 2:
    #     alg = FirstChoice()
    # elif aType == 3:
    #     alg = GradientDescent()
    # else:
    #     print("Choose from the number given!!")

    #dictionary를 사용한 방법 -> 다른 알고리즘 추후 추가 용이
    optimizers = {1 : 'SteepestAcent()', 2 : 'FirstChoice()', 3 : 'GradientDescent()'}
    
    alg = eval(optimizers[aType])
    alg.setVariables(pType)
    
    return alg

main()