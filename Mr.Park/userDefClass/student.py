from abc import *

class Student(metaclass=ABCMeta):
    def __init__(self, name="", midterm=0, final=0):
        self._name = name
        self._midterm = midterm
        self._final = final
      
    def setName(self, name):
        self._name = name

    def setMidterm(self, midterm):
        self._midterm = midterm

    def setFinal(self, final):
        self._final = final

    def getName(self):
        return self._name

    # 여기를 반드시 구현해야지만 사용 가능하게 바꾸고 싶음
    @abstractmethod #decorator
    def calcSemGrade(self):
        pass
        # return ''
        # raise NotImplementedError("You must implement this function") # raise 어떤 exception을 발생시킨다. 내가 발생시킨 것, exception은 던져

    @staticmethod #decorator(@)
    def do_something():
        print('Hello world!')
        
    def __str__(self):
        return self._name + "\t" + self.calcSemGrade()
     
class LGstudent(Student):

    SECRETNUMBER = 486
    
    def calcSemGrade(self):
        average = round((self._midterm + self._final) / 2)
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"

class PFstudent(Student):
        
    def calcSemGrade(self):
        average = round((self._midterm + self._final) / 2)
        if average >= 60:
            return "Pass"
        else:
            return "Fail"


