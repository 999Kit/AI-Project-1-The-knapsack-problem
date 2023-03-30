import sys
from utils import *
sys.set_int_max_str_digits(0)

def brute_force(problem):
    def evaluation_function(problem, model):
        classes_chosen = 0
        total_weight = 0
        total_value = 0

        for idx in range(len(problem.w)):
            if (model >> idx) & 1 == 1:
                total_weight += problem.w[idx]

                if total_weight > problem.W:
                    return 0

                total_value += problem.v[idx]
                classes_chosen |= 1 << (problem.c[idx] - 1)

        if classes_chosen + 1 != 1 << problem.m:
            return 0

        return total_value

    def solve(problem, state, curIndex):
        if curIndex < 0:
            evaluation_value = evaluation_function(problem, state)
            return state, evaluation_value
        return max(solve(problem, state, curIndex - 1), solve(problem, state | (1 << curIndex), curIndex - 1), key = lambda x : x[1])
    
    return solve(problem, 0, len(problem.w) - 1)
