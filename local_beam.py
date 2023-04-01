from utils import *
import sys

sys.set_int_max_str_digits(0)
from random import randint
import heapq


def local_beam(problem, beam_width=5, beam_depth=100):
    def generate_state():
        model = 0
        for i in range(len(problem.w)):
            flip = randint(0, 1)
            model |= (flip << i)
        return (problem.evaluation_function(model), model)

    def generate_k_states():
        return [generate_state() for _ in range(beam_width)]

    def generate_successors(parent, index, pq):
        if index < 0:
            return
        heapq.heappush(pq, (problem.evaluation_function(parent) * -1, parent))
        generate_successors(parent ^ (1 << index), index - 1, pq)
        generate_successors(parent, index - 1, pq)

    def solve(beam_width, beam_depth):
        # initialize k randomly generated states
        pq = generate_k_states()

        while beam_depth:
            # generate all successors of each state
            for i in range(beam_width):
                generate_successors(pq[i][1], len(problem.w) - 1, pq)

            # select k best successors
            select = [heapq.heappop(pq) for _ in range(beam_width)]
            pq = select

            beam_depth -= 1

        return pq[0][1], pq[0][0] * -1

    return solve(beam_width, beam_depth)