import copy
import pickle
import numpy as np
import time

from GA import Population,Member,ObjectiveFunction
from Architecture import Architecture
from Objective_Functions import PCE, PCE_COST




class Experiment:

    def __init__(self, experiment_name = "Ongoing_Experiment", population_N = 500, chromosomes_N = 4, chromosomes_min = [10e-9, 10e-9, 10e-9, 10e-9], chromosomes_max = [1e-6, 1e-6, 1e-6, 1e-6], chromosomes_start = [1e-7, 1e-7, 2.2e-7, 1e-7], mutation_chance= 0.2, best_frac = 0.1, worst_frac = 0.2, max_generations = 100, objective_function = PCE, target = 100,  **objective_function_arguments):
        self.start_time = time.time()
        self.results = np.zeros(max_generations+1, dtype=Population)

        self.population_N = population_N
        self.chromosomes_N = chromosomes_N
        self.mutation_chance = mutation_chance

        self.architecture = Architecture(chromosomes_N)
        self.architecture.set_y(chromosomes_start,chromosomes_min,chromosomes_max)
        self.chromosomes_order = [self.architecture.y[i] for i in range(chromosomes_N)]
        population = self.define_population()
        OF = ObjectiveFunction(target, objective_function, **objective_function_arguments)
        self.generation = 0

        while self.generation <= max_generations:
            population.rank_population(OF)
            self.results[self.generation] = copy.deepcopy(population)
            population.best_in_population(int(self.population_N * best_frac))
            population.worst_in_population(int(self.population_N * worst_frac))
            population.next_generation(int(self.population_N * worst_frac))
            self.generation = self.generation + 1

            with open(experiment_name + '.exp','wb') as f:
                pickle.dump(self.results, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.end_time = time.time()
        self.experiment_name = experiment_name


    def define_population(self):
        P = Population(self.population_N, self.mutation_chance)
        P.fill_population(self.chromosomes_N)
        for i in range(self.chromosomes_N):
            P.set_limits(i, self.architecture.y_limits[i,0], self.architecture.y_limits[i,1])
        return P



Experiment(population_N=10,max_generations=0,objective_function=PCE_COST, cost_per_g = [0,0,1,0])