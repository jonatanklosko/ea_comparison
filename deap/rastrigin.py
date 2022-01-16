import random
from deap import creator, base, tools, algorithms
import math

import sys
import time

if len(sys.argv) != 4:
    print("Usage: python rastrigin.py [population_size] [problem_size] [generations]")
    exit(1)

population_size, problem_size, generations = map(int, sys.argv[1:])

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("x", random.uniform, -5.12, 5.12)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.x, n=problem_size)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    s = sum(10 + x * x - 10 * math.cos(x * 2 * math.pi) for x in individual)
    return (-s, )

def mutUniformReal(individual, low, up, indpb):
    """
    Mutate an individual by replacing attributes, with probability *indpb*,
    by a float uniformly drawn between *low* and *up*.

    Based on `tools.mutUniformInt`.
    """

    size = len(individual)

    for i in range(size):
        if random.random() < indpb:
            individual[i] = random.uniform(low, up)

    return (individual,)

toolbox.register("evaluate", evaluate)
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", mutUniformReal, indpb=0.001, low=-5.12, up=5.12)

population = toolbox.population(n=population_size)

start = time.time()
final_population, _ = algorithms.eaSimple(population, toolbox, cxpb=1.0, mutpb=1.0, ngen=generations, verbose=False)
end = time.time()

final_fitness = list(map(toolbox.evaluate, final_population))

print("final fitness:", max(final_fitness))
print("time [s]:", end - start)
