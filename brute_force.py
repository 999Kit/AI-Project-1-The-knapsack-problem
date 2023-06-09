import sys
from utils import *
import time
sys.set_int_max_str_digits(0)
sys.setrecursionlimit(2000)

def brute_force(problem):
    begTime = time.time()
    def solve(problem, state, curIndex):
        if(time.time() - begTime > 2):
            return state, int(1e9)
        if curIndex < 0:
            evaluation_value = problem.evaluation_function(state)
            return state, evaluation_value
        return max(solve(problem, state, curIndex - 1), solve(problem, state | (1 << curIndex), curIndex - 1),
                   key=lambda x: x[1])
    return solve(problem, 0, len(problem.w) - 1)