from Architecture import *
from Objective_Functions import *
from GA import *
from GPVDM import *
import time
import pandas

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

def Experiment(name = "OnGoing_Experiment", mutation_rate = 0.01, population_size = 100, keep_best = 0.01, remove_worst = 0.01):
    Pop = np.zeros(10000000,dtype=Population)
    A = Architecture(4)
    A.set_y([10e-9,10e-9,10e-9,10e-9], [10e-9,10e-9,10e-9,10e-9], [300e-9,300e-9,300e-9,300e-9])
    CO = [A.y[0], A.y[1], A.y[2], A.y[3]]
    chromosones_needed = len(CO)
    P = Population(population_size, mutation_rate)
    P.fill_population(chromosones_needed)
    P.set_limits(0, A.y_limits[0, 0], A.y_limits[0, 1])
    P.set_limits(1, A.y_limits[1, 0], A.y_limits[1, 1])
    P.set_limits(2, A.y_limits[2, 0], A.y_limits[2, 1])
    P.set_limits(3, A.y_limits[3, 0], A.y_limits[3, 1])
    Target_PCE = Objective_Function(100, PCE)
    Gen = 0
    prevbest = 0

    start_time = time.time()
    while P.Exit < 5:
        print(Gen)
        print(P.Exit)
        P.rank_population(prevbest,Target_PCE)
        Pop[Gen] = copy.deepcopy(P)
        P.best_in_population(int(population_size * keep_best))
        P.worst_in_population(int(population_size * remove_worst))
        P.next_generation()
        if prevbest < P.result[np.argsort(P.result[:,0] - 100)[0],0]:
            prevbest = P.result[np.argsort(P.result[:,0] - 100)[0],0]
        Gen = Gen + 1

        with open(name +'.exp', 'wb') as handle:
            pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)
 
    #P.save('Last_Generation.gen')
    #with open('20220523PM6Y6125.exp', 'wb') as handle:
    #    pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)

    Execution_time = time.time() - start_time
    print(Execution_time)
    et = pd.DataFrame()
    et.loc['0','Execution time(s)'] = Execution_time
    et.to_csv(name + ".csv")

# Experiment("M0P10B0W0",0,10,0,0)
# Experiment("M0P20B0W0",0,20,0,0)
# Experiment("M0P40B0W0",0,40,0,0)
# Experiment("M0P60B0W0",0,60,0,0)
# Experiment("M0P80B0W0",0,80,0,0)
# Experiment("M0P100B0W0",0,100,0,0)
# Experiment("M0P200B0W0",0,200,0,0)
# Experiment("M0P400B0W0",0,400,0,0)
# Experiment("M0P600B0W0",0,600,0,0)
# Experiment("M0P800B0W0",0,800,0,0)
# Experiment("M0P1000B0W0",0,1000,0,0)

# Experiment("M001P10B0W0",0.01,10,0,0)
# Experiment("M002P10B0W0",0.02,10,0,0)
# Experiment("M004P10B0W0",0.04,10,0,0)
# Experiment("M006P10B0W0",0.06,10,0,0)
# Experiment("M008P10B0W0",0.08,10,0,0)
# Experiment("M01P10B0W0",0.1,10,0,0)
# Experiment("M02P10B0W0",0.2,10,0,0)
# Experiment("M04P10B0W0",0.4,10,0,0)
# Experiment("M06P10B0W0",0.6,10,0,0)
# Experiment("M08P10B0W0",0.8,10,0,0)


# Experiment("M001P20B0W0",0.01,20,0,0)
# Experiment("M002P20B0W0",0.02,20,0,0)
# Experiment("M004P20B0W0",0.04,20,0,0)
# Experiment("M006P20B0W0",0.06,20,0,0)
# Experiment("M008P20B0W0",0.08,20,0,0)
# Experiment("M01P20B0W0",0.1,20,0,0)
# Experiment("M02P20B0W0",0.2,20,0,0)
# Experiment("M04P20B0W0",0.4,20,0,0)
# Experiment("M06P20B0W0",0.6,20,0,0)
# Experiment("M08P20B0W0",0.8,20,0,0)

# Experiment("M001P40B0W0",0.01,40,0,0)
# Experiment("M002P40B0W0",0.02,40,0,0)
# Experiment("M004P40B0W0",0.04,40,0,0)
# Experiment("M006P40B0W0",0.06,40,0,0)
# Experiment("M008P40B0W0",0.08,40,0,0)
# Experiment("M01P40B0W0",0.1,40,0,0)
# Experiment("M02P40B0W0",0.2,40,0,0)
# Experiment("M04P40B0W0",0.4,40,0,0)
# Experiment("M06P40B0W0",0.6,40,0,0)
# Experiment("M08P40B0W0",0.8,40,0,0)

# Experiment("M001P60B0W0",0.01,60,0,0)
# Experiment("M002P60B0W0",0.02,60,0,0)
# Experiment("M004P60B0W0",0.04,60,0,0)
# Experiment("M006P60B0W0",0.06,60,0,0)
# Experiment("M008P60B0W0",0.08,60,0,0)
# Experiment("M01P60B0W0",0.1,60,0,0)
# Experiment("M02P60B0W0",0.2,60,0,0)
# Experiment("M04P60B0W0",0.4,60,0,0)
# Experiment("M06P60B0W0",0.6,60,0,0)
# Experiment("M08P60B0W0",0.8,60,0,0)

# Experiment("M001P80B0W0",0.01,80,0,0)
# Experiment("M002P80B0W0",0.02,80,0,0)
# Experiment("M004P80B0W0",0.04,80,0,0)
# Experiment("M006P80B0W0",0.06,80,0,0)
# Experiment("M008P80B0W0",0.08,80,0,0)
# Experiment("M01P80B0W0",0.1,80,0,0)
# Experiment("M02P80B0W0",0.2,80,0,0)
# Experiment("M04P80B0W0",0.4,80,0,0)
# Experiment("M06P80B0W0",0.6,80,0,0)
# Experiment("M08P80B0W0",0.8,80,0,0)

Experiment("M001P100B0W0",0.01,100,0,0)
Experiment("M002P100B0W0",0.02,100,0,0)
Experiment("M004P100B0W0",0.04,100,0,0)
Experiment("M006P100B0W0",0.06,100,0,0)
# Experiment("M008P100B0W0",0.08,100,0,0)
# Experiment("M01P100B0W0",0.1,100,0,0)
# Experiment("M02P100B0W0",0.2,100,0,0)
# Experiment("M04P100B0W0",0.4,100,0,0)
# Experiment("M06P100B0W0",0.6,100,0,0)
# Experiment("M08P100B0W0",0.8,100,0,0)


Experiment("M001P200B0W0",0.01,200,0,0)
Experiment("M002P200B0W0",0.02,200,0,0)
Experiment("M004P200B0W0",0.04,200,0,0)
Experiment("M006P200B0W0",0.06,200,0,0)
# Experiment("M008P200B0W0",0.08,200,0,0)
# Experiment("M01P200B0W0",0.1,200,0,0)
# Experiment("M02P200B0W0",0.2,200,0,0)
# Experiment("M04P200B0W0",0.4,200,0,0)
# Experiment("M06P200B0W0",0.6,200,0,0)
# Experiment("M08P200B0W0",0.8,200,0,0)

Experiment("M001P400B0W0",0.01,400,0,0)
Experiment("M002P400B0W0",0.02,400,0,0)
Experiment("M004P400B0W0",0.04,400,0,0)
Experiment("M006P400B0W0",0.06,400,0,0)
# Experiment("M008P400B0W0",0.08,400,0,0)
# Experiment("M01P400B0W0",0.1,400,0,0)
# Experiment("M02P400B0W0",0.2,400,0,0)
# Experiment("M04P400B0W0",0.4,400,0,0)
# Experiment("M06P400B0W0",0.6,400,0,0)
# Experiment("M08P400B0W0",0.8,400,0,0)

Experiment("M001P600B0W0",0.01,600,0,0)
Experiment("M002P600B0W0",0.02,600,0,0)
Experiment("M004P600B0W0",0.04,600,0,0)
Experiment("M006P600B0W0",0.06,600,0,0)
# Experiment("M008P600B0W0",0.08,600,0,0)
# Experiment("M01P600B0W0",0.1,600,0,0)
# Experiment("M02P600B0W0",0.2,600,0,0)
# Experiment("M04P600B0W0",0.4,600,0,0)
# Experiment("M06P600B0W0",0.6,600,0,0)
# Experiment("M08P600B0W0",0.8,600,0,0)

Experiment("M001P800B0W0",0.01,800,0,0)
Experiment("M002P800B0W0",0.02,800,0,0)
Experiment("M004P800B0W0",0.04,800,0,0)
Experiment("M006P800B0W0",0.06,800,0,0)
# Experiment("M008P800B0W0",0.08,800,0,0)
# Experiment("M01P800B0W0",0.1,800,0,0)
# Experiment("M02P800B0W0",0.2,800,0,0)
# Experiment("M04P800B0W0",0.4,800,0,0)
# Experiment("M06P800B0W0",0.6,800,0,0)
# Experiment("M08P800B0W0",0.8,800,0,0)

Experiment("M001P1000B0W0",0.01,1000,0,0)
Experiment("M002P1000B0W0",0.02,1000,0,0)
Experiment("M004P1000B0W0",0.04,1000,0,0)
Experiment("M006P1000B0W0",0.06,1000,0,0)
# Experiment("M008P1000B0W0",0.08,1000,0,0)
# Experiment("M01P1000B0W0",0.1,1000,0,0)
# Experiment("M02P1000B0W0",0.2,1000,0,0)
# Experiment("M04P1000B0W0",0.4,1000,0,0)
# Experiment("M06P1000B0W0",0.6,1000,0,0)
# Experiment("M08P1000B0W0",0.8,1000,0,0)