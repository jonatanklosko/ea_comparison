from leap_ec.algorithm import generational_ea
from leap_ec import ops, decoder, representation
from leap_ec.real_rep.problems import RastriginProblem
from leap_ec.real_rep.initializers import create_real_vector

import numpy as np
from toolz import curry
from leap_ec.ops import iteriter_op

import sys
import time

if len(sys.argv) != 4:
    print("Usage: python rastrigin.py [population_size] [problem_size] [generations]")
    exit(1)

population_size, problem_size, generations = map(int, sys.argv[1:])

@curry
@iteriter_op
def mutate_randomreal(next_individual, bounds, probability):
    while True:
        try:
            individual = next(next_individual)
        except StopIteration:
            return

        bounds = np.array(bounds)
        individual.genome = np.random.uniform(bounds[:, 0], bounds[:, 1])
        individual.fitness = None  # invalidate fitness since we have new genome

        yield individual

bounds = [(-5.12, 5.12)] * problem_size

ea = generational_ea(max_generations=generations, pop_size=population_size,
                    problem=RastriginProblem(a=10.0),

                    representation=representation.Representation(
                        decoder=decoder.IdentityDecoder(),
                        initialize=create_real_vector(bounds)
                    ),

                    pipeline=[
                        ops.tournament_selection,
                        ops.clone,
                        ops.uniform_crossover(p_swap=0.5),
                        mutate_randomreal(bounds=bounds, probability=0.001),
                        ops.evaluate,
                        ops.pool(size=population_size)
                    ])

start = time.time()

for i, best in ea:
    if i == generations:
        print("final fitness:", best.fitness)

print("time [s]:", time.time() - start)
