from leap_ec.algorithm import generational_ea
from leap_ec import ops, decoder, representation
from leap_ec.binary_rep.problems import MaxOnes
from leap_ec.binary_rep.initializers import create_binary_sequence
from leap_ec.binary_rep.ops import mutate_bitflip

import sys
import time

if len(sys.argv) != 4:
    print("Usage: python one_max.py [population_size] [problem_size] [generations]")
    exit(1)

population_size, problem_size, generations = map(int, sys.argv[1:])

ea = generational_ea(generations, pop_size=population_size,
                    problem=MaxOnes(),

                    representation=representation.Representation(
                        decoder=decoder.IdentityDecoder(),
                        initialize=create_binary_sequence(length=problem_size)
                    ),

                    pipeline=[
                        ops.tournament_selection,
                        ops.clone,
                        ops.uniform_crossover(p_swap=0.5),
                        mutate_bitflip(probability=0.001),
                        ops.evaluate,
                        ops.pool(size=population_size)
                    ])

start = time.time()

for i, best in ea:
    if i == generations:
        print("final fitness:", best.fitness)

print("time [s]:", time.time() - start)
