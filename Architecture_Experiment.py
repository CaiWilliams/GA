#!/usr/bin/env python3
from Architecture import *
from Objective_Functions import *
from GA import *
from GPVDM import *
import time
import pandas
import shutil
import itertools
from multiprocessing import Pool, Lock
import copy
import mgzip

def define_population(N, chromosones_order, mutation_chance):
    chromosones_needed = len(chromosones_order)
    P = Population(N, mutation_chance)
    P.fill_population(chromosones_needed)
    #P.set_limits(0, A.x_limits[0], A.x_limits[1])
    #P.set_limits(1, A.z_limits[0], A.z_limits[1])
    P.set_limits(0, A.y_limits[0, 0], A.y_limits[0, 1])
    P.set_limits(1, A.y_limits[1, 0], A.y_limits[1, 1])
    P.set_limits(2, A.y_limits[2, 0], A.y_limits[2, 1])
    P.set_limits(3, A.y_limits[3, 0], A.y_limits[3, 1])
    return P


def init(l):
    global lock
    lock = l

def Experiment(experiment_name,d,prng):

    name = d[5]
    print(name)
    mutation_rate = d[0]
    population_size = d[1]
    keep_best = d[2]
    remove_worst = d[3]
    active_material = d[4]

    Pop = np.zeros(10000000,dtype=Population)
    A = Architecture(3)
    A.set_y([20e-9,20e-9,20e-9], [20e-9,20e-9,20e-9], [500e-9,1000e-9,500e-9])
    CO = [A.y[0], A.y[1], A.y[2]]
    P = Population(population_size, prng, mutation_rate)
    P.fill_population(len(CO))

    P.set_limits(0, A.y_limits[0, 0], A.y_limits[0, 1])
    P.set_limits(1, A.y_limits[1, 0], A.y_limits[1, 1])
    P.set_limits(2, A.y_limits[2, 0], A.y_limits[2, 1])
    P.set_chromosome_map([1,3,4])
    Target_PCE = Objective_Function(100, PCE, name, P)
    Gen = 0
    prevbest = 0

    start_time = time.time()
    while P.Exit < 5:
        P.rank_population(prevbest, Target_PCE)
        Pop[Gen] = copy.deepcopy(P)
        P.best_in_population(int(population_size * keep_best))
        P.worst_in_population(int(population_size * remove_worst))
        P.next_generation()
        if prevbest < P.result[np.argsort(P.result[:,0] - 100)[0],0]:
            prevbest = P.result[np.argsort(P.result[:,0] - 100)[0],0]
        Gen = Gen + 1

    try:
        with mgzip.open(os.path.join(os.getcwd(),'Results',experiment_name,name +'.exp'), 'wb') as handle:
            pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        if os.path.exists(os.path.join(os.getcwd(),'Results',experiment_name)) == False:
            os.mkdir(os.path.join(os.getcwd(),'Results',experiment_name))

        if os.path.exists(os.path.join(os.getcwd(),'Results',experiment_name)) == False:
            os.mkdir(os.path.join(os.getcwd(),'Results',experiment_name))

        with mgzip.open(os.path.join(os.getcwd(),'Results',experiment_name,name +'.exp'), 'wb') as handle:
            pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)
 
    #P.save('Last_Generation.gen')
    #with open('20220523PM6Y6125.exp', 'wb') as handle:
    #    pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)

    Execution_time = time.time() - start_time
    #print(Execution_time)
    et = pd.DataFrame()
    et.loc['0','Execution time(s)'] = Execution_time
    et.to_csv(os.path.join(os.getcwd(),'Results',experiment_name,name +'.csv'))


def material_names(base_material,shift):
    name = base_material + '_' + str(int(np.around(shift * 100,decimals=0))) + 'pct'
    #if shift > 0:
    #     name = base_material + '_' + 'p' + str(int(np.around(shift,decimals=0))) + 'nm' 
    #elif shift < 0:
    #     name = base_material + '_m' + str(int(abs(np.around(shift,decimals=0)))) + 'nm'
    #else:
    #     name = base_material + '_0'
    return name

def runrange(experiment_name):
    #shifts = np.linspace(0,5,200)
    #variations = [material_names('p',s) for s in shifts]
    material = ['pm6y6'] #+ variations
    mutation = [0.025]
    population = [200]
    best = [0.2]
    worst = [0.2]
    perms = list(itertools.product(mutation, population, best, worst, material))
    perms = [list(p) for p in perms]
    prng = np.random.RandomState()
    name = ['M'+str(p[0])+"P"+str(p[1])+"B"+str(p[2])+"W"+str(p[3])+"MAT"+str(p[4])+"N" for p in perms]
    for i in range(len(perms)):
        perms[i].append(name[i])
    for i in perms:
        Experiment(experiment_name,i,prng)

if __name__ == '__main__':
    experiment_name = "chemnitz0"
    runrange(experiment_name)

    experiment_name = "chemnitz1"
    runrange(experiment_name)

    experiment_name = "chemnitz2"
    runrange(experiment_name)

    experiment_name = "chemnitz3"
    runrange(experiment_name)

    experiment_name = "chemnitz4"
    runrange(experiment_name)

