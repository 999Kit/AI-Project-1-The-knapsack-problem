from utils import *
import sys

sys.set_int_max_str_digits(0)
from random import randint
import heapq


def local_beam(problem, beam_width=100, beam_depth=1):
    if beam_width > len(problem.w): 
        beam_width = len(problem.w)

    def generate_state():
        model = 0
        for i in range(len(problem.w)):
            flip = randint(0, 1)
            model |= (flip << i)
        return (problem.eval_lb(model)*-1, model)

    def generate_k_states_randomly():
        return [generate_state() for _ in range(beam_width)]

    def generate_k_states_greedily():
        # Generate good set of partial assignments using Dantzig's greedy approximation algorithm
        # Sort the items by the value to weight ratio in non-increasing order
        sorted_items = sorted(range(len(problem.w)), key=lambda k: problem.v[k]/problem.w[k], reverse=True)
        
        # Initialize an empty list for each class
        class_lists = [[] for _ in range(problem.m)]

        # Add each item to its corresponding class list
        for item in sorted_items:
            class_lists[problem.c[item]-1].append(item)

        # Pick the next item from each class with the maximum value to weight ratio
        k_states = []
        for _ in range(beam_width):
            model = 0
            total_weight = 0
            while 1:
                old_weight = total_weight
                for class_list in class_lists:
                    if class_list:
                        # Get the item from the class with the maximum value to weight ratio
                        item = class_list[0]
                        # Add the item to the model
                        if total_weight + problem.w[item] <= problem.W:
                            model |= (1 << item)
                            total_weight += problem.w[item]
                            class_list.pop(0)
                if total_weight == old_weight:
                    break
            value = problem.evaluation_function(model)
            k_states.append((value*-1, model))
        return k_states

    def generate_successors(parent, pq, map):
        for i in range(len(problem.w)):
            successor = parent ^ (1 << i)
            value = 0
            value = problem.eval_lb(successor) * -1
            heapq.heappush(pq, (value, successor))

    def solve(beam_width, beam_depth):
        # initialize k greedily generated states
        pq = generate_k_states_greedily()
        while beam_depth:
            # generate all successors of each state
            for i in range(beam_width):
                generate_successors(pq[i][1], pq, map)

            # select k best successors
            select = [heapq.heappop(pq) for _ in range(beam_width)]
            print(select)
            pq = select

            beam_depth -= 1
        value = pq[0][0]
        if value > 0:
            value = 0
        else:
            value *= -1

        return pq[0][1], value

    return solve(beam_width, beam_depth)