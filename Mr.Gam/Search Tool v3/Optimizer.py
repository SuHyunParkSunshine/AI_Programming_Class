from Setup import Setup

class HillClimbing:
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0
        self._limitStock = 100

    def run(self):
        pass

    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Mutation step size: ", self._delta)                  
    
    def setVariables(self, pType):
        self._pType = pType


class SteepestAcent(HillClimbing):
    # 상속에 init 있기 때문에 따로 init 안 한 경우에는 parent꺼를 쓰게 된다. init이 없는게 아니라 HillClimbing의 init method를 쓰고 있는 즁
    def run(self, p):
        current = p.randomInit() 
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p) 
            if valueS >= valueC:
                break 
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)

    def bestOf(self, neighbors, p):
        best = neighbors[0]
        bestValue = p.evaluate(best)

        for i in range(1, len(neighbors)):
            newValue = p.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue = newValue

        return best, bestValue
    
    # Overriding
    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        HillClimbing.displaySetting(self)

class FirstChoice(HillClimbing):
    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStock:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)
    
    def displaySetting(self):
        print()
        print("Search algorithm: First Choice Hill Climbing")
        print()
        HillClimbing.displaySetting(self)
        print("Max evaluations with no improvement: {0:,} iterations".format(self._limitStock)) 

class GradientDescent(HillClimbing):
    def run(self, p):
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
        p.storeResult(current, valueC)

    def displaySetting(self):
        print()
        print("Search algorithm: Gradient-descent Hill Climbing")
        print()
        print("Update rate:", self._alpha)
        print("Increment for calculating dericatives: ")