from asyncio import protocols
import numpy as np
import pickle

class Population:

    def __init__(self, popultaion_number, prng, mutate=0.2):
        self.mutate = mutate
        self.population_number = popultaion_number
        self.population = np.zeros(popultaion_number, dtype=object)
        self.Exit = 0
        self.prng = prng

    def add_members(self, members):
        if type(members) != list:
            members = [members]
        adding_index = np.where(self.population == 0)[0]
        members_index = np.arange(0, len(members))
        adding_index = adding_index[members_index]
        self.population[adding_index] = members

    def fill_population(self, chromosome_length):
        self.chromosome_length = chromosome_length
        self.limits = np.empty((chromosome_length, 2))
        self.limits[:] = np.nan
        self.population[:] = [Member(chromosome_length,self.prng) for idx in self.population]
        for m in self.population:
            m.set_chromosome_random(range(chromosome_length), 0, 1)

    def set_limits(self, chromosome_number, min, max):
        self.limits[chromosome_number][0] = min
        self.limits[chromosome_number][1] = max
        for m in self.population:
            m.set_chromosome_random(chromosome_number, min, max)


    def rank_population(self, prevbest, objective_funciton):
        self.objective_funciton = objective_funciton
        self.result = objective_funciton.function(self.population, objective_funciton.population, name=objective_funciton.name)
        self.rank = np.zeros(len(self.result))
        self.rank[:] = np.argsort(np.abs(self.result[:, 0] - objective_funciton.target))
        self.best_n_idx = np.argsort(self.result[:,0] - objective_funciton.target)[0]
        best = self.result[self.best_n_idx,0]
        if best > prevbest:
            print("Improvment")
            self.Exit = 0
        else:
            print("Static")
            self.Exit = self.Exit + 1

    def set_chromosome_map(self,args):
        self.chromosome_map = args

    def best_in_population(self, n):
        self.best_n_idx = np.argsort(self.rank)[:n]
        return self.population[self.best_n_idx]

    def worst_in_population(self, n):
        if n == 0:
            self.worst_n_idx = np.asarray([])
        else:
            self.worst_n_idx = np.argsort(self.rank)[-n:]

    def breed(self, n):
        if len(self.worst_n_idx) == 0:
            breeding_pool = self.population
            breeding_pool_results = self.result[:,0]
        else:
            breeding_pool = np.delete(self.population, self.worst_n_idx)
            breeding_pool_results = np.delete(self.result[:, 0], self.worst_n_idx)
        breeding_pool_rank = np.argsort(np.abs(breeding_pool_results - self.objective_funciton.target))
        breeding_pool[:] = breeding_pool[breeding_pool_rank]
        breeding_pool_weight = np.linspace(1, 0, len(breeding_pool))
        breeding_pool_weight = breeding_pool_weight / sum(breeding_pool_weight)
        Children_n = n#len(breeding_pool) #- len(self.worst_n_idx)
        mothers = self.prng.choice(breeding_pool, Children_n, p=breeding_pool_weight)
        fathers = self.prng.choice(breeding_pool, Children_n, p=breeding_pool_weight)
        crossover_point = self.prng.randint(0, self.chromosome_length - 1, len(mothers))
        x = zip(mothers, fathers, crossover_point)
        next_generation = np.zeros(Children_n, dtype=object)
        for idx, x in enumerate(x):
            next_generation[idx] = Member(self.chromosome_length,self.prng).set_chromosome_parents(x[0], x[1], x[2])
            next_generation[idx] = next_generation[idx].mutate(self.mutate, self.limits)
        return next_generation

    def next_generation(self):
        TNG = np.zeros(self.population_number, dtype=object)
        TNG[:len(self.best_n_idx)] = self.best_in_population(len(self.best_n_idx))
        if len(self.best_n_idx) == 0:
            TNG = self.breed(self.population_number)
        else:
            TNG[:len(self.best_n_idx)] = self.best_in_population(len(self.best_n_idx))
            n  = self.population_number - len(self.best_n_idx)
            TNG[len(self.best_n_idx):] = self.breed(n)
        self.population = TNG

    def save(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self, filename):
        with open(filename, 'rb') as handle:
            data = pickle.load(handle)
            data = data[data != 0]
            self = data[-1]
            return self


class Member:

    def __init__(self, chromosomes_length,prng):
        self.chromosomes_length = chromosomes_length
        self.chromosomes = np.zeros(self.chromosomes_length, dtype=float)
        self.prng = prng

    def set_chromosome_random(self, chromo_num, min, max):
        if type(chromo_num) != list:
            chromo_num = [chromo_num]
        if np.max(chromo_num) > self.chromosomes_length - 1:
            return print("Chromosome outside of defined length")
        else:
            self.chromosomes[chromo_num] = self.prng.uniform(min, max, len(chromo_num))

    def set_chromosome_parents(self, mother, father, crossover):
        self.chromosomes[:crossover] = mother.chromosomes[:crossover]
        self.chromosomes[crossover:] = father.chromosomes[crossover:]
        self.chromosomes = self.chromosomes
        return self

    def mutate(self, p, limits):
        m_p = self.prng.uniform(0, 1)
        if p > m_p:
            m_c = self.prng.randint(0, self.chromosomes_length - 1)
            self.chromosomes[m_c] = self.prng.uniform(low=limits[m_c][0], high=limits[m_c][1])
        return self


class Objective_Function:

    def __init__(self, target, function, name, population):
        self.target = target
        self.function = function
        self.name = name
        self.population = population
