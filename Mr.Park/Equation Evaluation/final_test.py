# 주어진 파일에서 수식과 변수 값을 읽어 함수 값을 계산하여 출력하는 클래스를 작성하세요.
# 이 때, decorator와 logging을 이용하여 값을 콘솔에 출력하세요.

import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def measure(func):
    """
        decorator function
        logging을 이용해 x값, y값, 계산값 을 출력할 수 있는 기능을 추가
    """
    logging.basicConfig(level=logging.INFO)

class Evaluator:
    def __init__(self, filename):
        """
            filename에 주어진 경로에서 읽기 전용으로 csv 파일을 읽어서
            각 줄에 있는 수식과 변수 값을 저장

            csv 파일은 수식,x값,y값 으로 구성되어 있음

            ex) equations.txt
            10*x + 2*y,2,5
            0.5*x - 1.8*y,7,3
        """
        # open 써서 차일 열과, for 문으로 줄을 읽어 온다.
        # split으로 csv 값 구분해서 저장    
        self.eq = []
        infile = open(filename, 'r')
        for line in infile:
            expression, xv, yv = line.strip().split(',')
            self.eq.append((expression, float(xv), float(yv)))
        infile.close()
        

    def solve(self, idx):
        """
            idx 번째 수식을 계산한 값을 반환

            ex)
            solve(1) 은 equations.txt 의 0.5*x - 1.8*y가
            x=7, y=3일 때 값을 계산하여 반환

            solve 내부에는 logging이나 print 사용하지 말 것
        """
        # 교수님 코드
        # exec('x=' + self.eq[1])
        # exec('y=' + self.eq[2])
        # eval(self.eq[0])

        #수현쓰 코드
        expression, xv, yv = self.eq[idx]
        result = eval(expression, {'x': xv, 'y': yv})        
        return result
    
def main():
    evaluator = Evaluator('equations.txt')
    assert np.allclose(evaluator.solve(0), 30)
    assert np.allclose(evaluator.solve(1), -1.9)

main()
