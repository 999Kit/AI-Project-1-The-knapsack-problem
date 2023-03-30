import random
import copy
import os

def population_generator(problem, n):
    population = []
    for _ in range(n):
        individual = [0] * len(problem.w)
        for t in problem.typeList:
            value = random.randrange(1, max(1, (1 << (len(t) - 1))))
            for i in range(len(t)):
                if(value % 2 != 0):
                    individual[t[i]] = 1
                value >>= 1
        population.append(individual)
    return population

def reproduce(x, y):
    child1 = copy.deepcopy(x)
    child2 = copy.deepcopy(y)
    l = random.randrange(0, len(x))
    child1 = child1[:l] + child2[l:]
    child2 = child2[:l] + child1[l:]
    return child1, child2
    
def mutate(problem, x, mr):
    p = random.uniform(0, 1)
    if p <= mr:
        return x
    while 1:
        t = random.randrange(0, problem.m)
        if(len(problem.typeList[t]) > 1):
            break
    l, r = random.sample(range(len(problem.typeList[t])), 2)
    l = problem.typeList[t][l]
    r = problem.typeList[t][r]

    # Bad individual
    if(problem.fitness(x) == 0):
        if x[l] == 1: x[l] = 0
        if x[r] == 1: x[r] = 0
    else:
        x[l] ^= 1
        # Double mutation
        q = random.uniform(0, 1)
        if(2 * q <= mr):
            x[r] ^= 1

    return x

def select_one(population):
    selectingFactor = 5
    index = len(population) * (random.uniform(0, 1) ** selectingFactor)
    return population[int(index)]


def weighted_random_choice(population, np):
    return (select_one(population) for _ in range(np))

def genetic_algorithm(problem, population, itr_threshold):
    mr = 0.4
    itr = itr_threshold
    pop_len = len(population)
    fittest_generation = []
    while itr:
        population2 = []
        population.sort(key=problem.fitness, reverse=True)
        for i in range(pop_len // 2):
            parent1, parent2 = weighted_random_choice(population, 2)
            child1, child2 = reproduce(parent1, parent2)
            child1, child2 = mutate(problem, child1, mr), mutate(problem, child2, mr)
            population2.append(child1)
            population2.append(child2)
        fittest_individual = max(population, key = problem.fitness)
        fittest_value = problem.fitness(fittest_individual)
        fittest_generation = max(fittest_generation, fittest_individual, key = problem.fitness)
        population = population2
        itr -= 1
    return fittest_generation, problem.fitness(fittest_generation)

