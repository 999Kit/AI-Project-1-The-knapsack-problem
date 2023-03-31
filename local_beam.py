from utils import *
import sys
sys.set_int_max_str_digits(0)
from random import randint


def local_beam(problem):

    def generate_state():
        model = 0
        for i in range(len(problem.w)):
            flip = randint(0, 1)
            model |= (flip << i)
        return (problem.evaluation_function(model) ,model)

    beam_width = 5
    def generate_k_states():
        return [generate_state() for _ in range(beam_width)]
    
    

    def solve(problem):
        beam_depth = 100
        states = generate_k_states()

        while beam_depth:
            for i in range(len(problem.w)):
                for j in range(len(problem.w)):
                    successor = states[i][1]
                    successor ^= (1 << j)
                    states.append((problem.evaluation_function(successor), successor))

            states.sort(reverse=True)
            states = states[:beam_width]
            beam_depth -= 1

        return states[0][1], states[0][0]
    return solve(problem)
