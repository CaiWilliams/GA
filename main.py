import numpy as np


class Population:

    def __init__(self, popultaion_number):
        self.population_number = popultaion_number + 1
        self.population = np.zeros(popultaion_number,dtype=object)

    def add_members(self, members):
        if type(members) != list:
            members = [members]
        adding_index = np.where(self.population == 0)[0]
        members_index = np.arange(0,len(members))
        adding_index = adding_index[members_index]
        self.population[adding_index] = members

    def fill_population(self, chromosome_length):
        self.population[:] = [Member(chromosome_length) for idx in self.population]
        for m in self.population:
            m.set_chromosome_random(range(chromosome_length),1,0)

    def rank_population(self, objective_funciton):
        self.result = [np.abs(objective_funciton.function(m.chromosomes) - objective_funciton.target) for m in self.population]
        self.rank = np.argsort(self.result)

    def best_in_population(self, n):
        self.best_n_idx = np.argsort(self.rank)[0:n]

    def worst_in_population(self, n):
        self.worst_n_idx = np.argsort(self.rank)[-n-1:-1]
        print(self.worst_n_idx)

    def breed(self, n):
        breeding_pool = np.delete(self.population, self.worst_n_idx)
        breeding_pool_rank = np.delete(self.rank, self.worst_n_idx)
        print(breeding_pool_rank)
        breeding_pool_weight = np.linspace(1,0,)
        print(breeding_pool_weight)
        print(np.sum(breeding_pool_weight))
        mothers = np.random.choice

    def next_generation(self, bn):
        TNG = np.zeros(self.population_number, dtype=object)
        TNG[0:bn] = self.best_in_population(bn)
        TNG[bn+1:-1] = self.breed(self.population_number - bn)




class Member:

    def __init__(self, chromosomes_length):
        self.chromosomes_length = chromosomes_length
        self.chromosomes = np.zeros(self.chromosomes_length)

    def set_chromosome_random(self, chromo_num, min, max):
        if type(chromo_num) != list:
            chromo_num = [chromo_num]
        if np.max(chromo_num) > self.chromosomes_length-1:
            return print("Chromosome outside of defined length")
        else:
            self.chromosomes[chromo_num] = np.random.uniform(min,max,len(chromo_num))


class Objective_Function:

    def __init__(self, target, function):
        self.target = target
        self.function = function


Pop = Population(50)
Pop.fill_population(5)
Sum = Objective_Function(1,np.sum)
Pop.rank_population(Sum)
Pop.best_in_population(10)
Pop.worst_in_population(10)
Pop.next_generation(10)

