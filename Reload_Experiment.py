from Architecture import *
from Objective_Functions import *
from GA import *
from GPVDM import *

# def define_population(N, chromosones_order, mutation_chance):
#     chromosones_needed = len(chromosones_order)
#     P = Population(N, mutation_chance)
#     P.fill_population(chromosones_needed)
#     #P.set_limits(0, A.x_limits[0], A.x_limits[1])
#     #P.set_limits(1, A.z_limits[0], A.z_limits[1])
#     P.set_limits(0, A.y_limits[0, 0], A.y_limits[0, 1])
#     P.set_limits(1, A.y_limits[1, 0], A.y_limits[1, 1])
#     P.set_limits(2, A.y_limits[2, 0], A.y_limits[2, 1])
#     P.set_limits(3, A.y_limits[3, 0], A.y_limits[3, 1])
#     return P

Pop = np.zeros(10000000,dtype=Population)
A = Architecture(4)
A.set_y([2e-7,2e-7,4.4e-7,2e-7], [10e-9,10e-9,10e-9,10e-9], [1e-6,1e-6,1e-6,1e-6])
CO = [A.y[0], A.y[1], A.y[2], A.y[3]]
M = 0.1
population_size = 100
#P = define_population(population_size , CO, M)
P = Population(population_size, M)
P = P.load('OnGoing_Experiment.exp')
print(P)
Target_PCE = Objective_Function(0, LCOE)
Gen = 0


while Gen <= 50:
    P.rank_population(Target_PCE)
    #Pop[Gen] = copy.deepcopy(P)
    #P.best_in_population(int(population_size * 0.1))
    #P.worst_in_population(int(population_size * 0.2))
    #P.next_generation()
    #Gen = Gen + 1