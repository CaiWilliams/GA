from GA import *


class Experiment:
    def __init__(self, population_members, mutation_chance, *chromosomes):
        chromosomes_needed = len(chromosomes)
        P = Population(population_members,mutation_chance)
        P.fill_population(chromosomes_needed)
        for idx,chromo in chromosomes:
            P.set_limits(idx,chromo.limits[0],chromo.limits[1])
        print(chromosomes_needed)

Experiment(200,0.025,'A','B','C','D')