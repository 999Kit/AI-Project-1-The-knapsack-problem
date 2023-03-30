from utils import *
import sys
sys.set_int_max_str_digits(0)
from random import randint


def local_beam(problem):

    def evaluation_function(model):
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

    def generate_state():
        model = 0
        for i in range(len(problem.w)):
            flip = randint(0, 1)
            model |= (flip << i)
        return (evaluation_function(model) ,model)

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
                    states.append((evaluation_function(successor), successor))

            states.sort(reverse=True)
            states = states[:beam_width]
            beam_depth -= 1

        return states[0][1], states[0][0]
    return solve(problem)
