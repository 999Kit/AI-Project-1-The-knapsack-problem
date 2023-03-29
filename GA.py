import random
import copy
import os
def population_generator(n):
    population = []
    for _ in range(n):
        individual = [0] * len(w)
        for t in typeList:
            value = random.randrange(1, max(1, (1 << (len(t) - 1))))
            for i in range(len(t)):
                if(value % 2 != 0):
                    individual[t[i]] = 1
                value >>= 1
        population.append(individual)
    return population

def fitness(individual):
    total_weight = 0
    total_value = 0
    mask = 0
    for i in range(len(individual)):
        if individual[i]:
            total_weight += w[i]
            if(total_weight > W):
                return 0
            total_value += v[i]
            mask |= (1 << (c[i] - 1))
    if(mask == (1 << m) - 1):
        return total_value
    return 0
def reproduce(x, y):
    child1 = copy.deepcopy(x)
    child2 = copy.deepcopy(y)
    l = random.randrange(0, len(x))
    child1 = child1[:l] + child2[l:]
    child2 = child2[:l] + child1[l:]
    return child1, child2
    
def mutate(x, mr):
    p = random.uniform(0, 1)
    if p <= mr:
        return x
    while 1:
        t = random.randrange(0, m)
        if(len(typeList[t]) > 1):
            break
    l, r = random.sample(range(len(typeList[t])), 2)
    l = typeList[t][l]
    r = typeList[t][r]

    # Bad individual
    if(fitness(x) == 0):
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

def genetic_algorithm(population):
    mr = 0.4
    itr = 5000
    pop_len = len(population)
    fittest_generation = []
    f = open("data.bin", 'w')
    while itr:
        population2 = []
        population.sort(key=fitness, reverse=True)
        for i in range(pop_len // 2):
            parent1, parent2 = weighted_random_choice(population, 2)
            child1, child2 = reproduce(parent1, parent2)
            child1, child2 = mutate(child1, mr), mutate(child2, mr)
            population2.append(child1)
            population2.append(child2)
        fittest_individual = max(population, key = fitness)
        fittest_value = fitness(fittest_individual)
        # print(fittest_value)
        f.write(str(fittest_value) + '\n')
        fittest_generation = max(fittest_generation, fittest_individual, key = fitness)
        population = population2
        itr -= 1
    f.close()
    return fittest_generation

if __name__ == '__main__':
    with open("INPUT_0.txt", "r") as f:
        W = int(f.readline())
        m = int(f.readline())
        w = list(map(int, f.readline().split(', ')))
        v = list(map(int, f.readline().split(', ')))
        c = list(map(int, f.readline().split(', ')))
        typeList = [list() for _ in range(m)]
        for i, x in enumerate(c):
            typeList[x - 1].append(i)
        population = population_generator(100)
        fittest_individual = genetic_algorithm(population)
        print(fitness(fittest_individual))
        print(fittest_individual)


