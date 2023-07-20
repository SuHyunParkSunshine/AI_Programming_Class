from multiprocessing import Pool
import time

def work(x):
    for _ in range(10):
        y = x**2

if __name__ == "__main__":
    pool = Pool(4) # 일꾼 4명이 동시에 일 처리를 하는 중이라 순서가 뒤죽박죽으로 나온다.
    data = range(1, 100)
    t0 = time.time_ns()
    pool.map(work, data)
    t1 = time.time_ns()

    print(f'Time: {t1-t0} (ns)')
