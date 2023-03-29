from GA import *
from utils import *
if __name__ == '__main__':
    with open("INPUT_0.txt", "r") as f:
        W = int(f.readline())
        m = int(f.readline())
        w = list(map(int, f.readline().split(', ')))
        v = list(map(int, f.readline().split(', ')))
        c = list(map(int, f.readline().split(', ')))
        kp = KnapsackProblem(W, m, w, c, v)
        population = population_generator(kp, 100)
        fittest_individual = genetic_algorithm(kp, population, 50)
        print(kp.fitness(fittest_individual))
        print(fittest_individual)
