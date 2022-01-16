import random
from deap import creator, base, tools, algorithms
import numpy as np

import sys
import time

if len(sys.argv) != 4:
    print("Usage: python one_max.py [population_size] [problem_size] [generations]")
    exit(1)

population_size, problem_size, generations = map(int, sys.argv[1:])

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("x", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.x, n=problem_size)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    s = np.sum(individual)
    return (s,)

toolbox.register("evaluate", evaluate)
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.001)

population = toolbox.population(n=population_size)

start = time.time()
final_population, _ = algorithms.eaSimple(population, toolbox, cxpb=1.0, mutpb=1.0, ngen=generations, verbose=False)
end = time.time()

final_fitness = list(map(toolbox.evaluate, final_population))

print("final fitness:", max(final_fitness))
print("time [s]:", end - start)
