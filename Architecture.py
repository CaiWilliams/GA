import copy
import pickle
import numpy as np
import keyboard

from GA import *
from GPVDM import *



class Architecture:

    def __init__(self,layers):
        self.layers = layers

        self.x = np.nan
        self.x_limits = np.empty(2)

        self.z = np.nan
        self.z_limits = np.empty(2)

        self.y = np.empty(layers)
        self.y[:] = np.nan
        self.y_limits = np.empty((layers,2))

    def set_x(self, x, x_min, x_max):
        self.x = x
        self.x_limits[0] = x_min
        self.z = z
        self.z_limits[0] = z_min
        self.x_limits[1] = x_max

    def set_z(self, z, z_min, z_max):
        self.z_limits[1] = z_max

    def set_y(self, y, y_min, y_max):
        self.y[:] = y
        self.y_limits[:,0] = y_min
        self.y_limits[:,1] = y_max


def define_population(N, chromosones_order):
    chromosones_needed = len(chromosones_order)
    P = Population(N, 0.025)
    P.fill_population(chromosones_needed)
    #P.set_limits(0, A.x_limits[0], A.x_limits[1])
    #P.set_limits(1, A.z_limits[0], A.z_limits[1])
    P.set_limits(0, A.y_limits[0, 0], A.y_limits[0, 1])
    P.set_limits(1, A.y_limits[1, 0], A.y_limits[1, 1])
    P.set_limits(2, A.y_limits[2, 0], A.y_limits[2, 1])
    P.set_limits(3, A.y_limits[3, 0], A.y_limits[3, 1])
    return P


def PCE(population):
    G = gpvdm()
    for idx,m in enumerate(population):
        args = m.chromosomes
        G.create_job("Temp"+str(idx))

        # G.modify_pm("dx", category=["epitaxy"], layer_name="layers", layer_number=0, value=float(args[0]))
        # G.modify_pm("dx", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(args[0]))
        # G.modify_pm("dx", category=["epitaxy"], layer_name="layers", layer_number=2, value=float(args[0]))
        # G.modify_pm("dx", category=["epitaxy"], layer_name="layers", layer_number=3, value=float(args[0]))
        # G.modify_pm("len", category=["mesh", "mesh_x"], layer_name="segments", layer_number=0, value=float(args[0]))
        # #G.modify_pm("dx", category="epi", layer_name="layers", layer_number=4, value=args[0])
        #
        # G.modify_pm("dz", category=["epitaxy"], layer_name="layers", layer_number=0, value=float(args[1]))
        # G.modify_pm("dz", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(args[1]))
        # G.modify_pm("dz", category=["epitaxy"], layer_name="layers", layer_number=2, value=float(args[1]))
        # G.modify_pm("dz", category=["epitaxy"], layer_name="layers", layer_number=3, value=float(args[1]))
        # G.modify_pm("len", category=["mesh", "mesh_z"], layer_name="segments", layer_number=0, value=float(args[1]))
       # G.modify_pm("dz", category="epi", layer_name="layers", layer_number=4, value=args[1])

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=0, value=float(args[0]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(args[1]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(args[0]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=2, value=float(args[2]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=2, value=float(args[0] + args[1]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=3, value=float(args[3]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=3, value=float(args[0] + args[1] + args[2]))


        G.modify_pm("len", category=["mesh", "mesh_y"], layer_name="segments", layer_number=0, value=float(args[2]))


        G.save_job()

    G.run()

    results = np.zeros(len(population))
    for idx,m in enumerate(population):
        with open('C:\GA\GPVDM\Temp'+str(idx)+'\sim_info.dat','r') as R:
            r = json.load(R)
            results[idx] = r['pce']
    return results

Pop = np.zeros(1000000,dtype=Population)
A = Architecture(4)
#A.set_x(0.0024495,0.000024495,0.0024495)
#A.set_z(0.0024495,0.000024495,0.0024495)
A.set_y([1e-7,1e-7,2.2e-7,1e-7],[1e-9,1e-9,1e-9,1e-9], [1e-7,1e-7,2.2e-7,1e-7])
CO = [A.y[0], A.y[1], A.y[2], A.y[3]]
P = define_population(250, CO)
Target_PCE = Objective_Function(100,PCE)
Gen = 0

try:
    while Gen <= 1:
        P.rank_population(Target_PCE)
        Pop[Gen] = copy.deepcopy(P)
        P.best_in_population(5)
        P.worst_in_population(5)
        P.next_generation(5)
        Gen = Gen + 1

    P.save('Last_Generation.gen')
    with open('Previous_Experiment.exp', 'wb') as handle:
        pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)

finally:

    P.save('Last_Generation.gen')
    with open('Previous_Experiment.exp', 'wb') as handle:
        pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('PreviousRun.gap', 'rb') as handle:
#     data = pickle.load(handle)
#     #PCE = [np.average(i.result) for i in data[:100]]
#     PCE = [np.average([m.chromosomes[5] for m in i.population]) * 1e+9 for i in data[:100]]\
#     #plt.plot(PCE)
#     #PCE = [np.average([m.chromosomes[1] for m in i.population]) for i in data[:100]]
#     #PCE = PCE[:] * 1e-3
#     plt.plot(PCE)
#     plt.xlabel('Generations')
#     plt.ylabel('Al Thickness (nm)')
#     # PCE = [np.average([m.chromosomes[4] for m in i.population]) for i in data[:100]]
#     # plt.plot(PCE)
#     # PCE = [np.average([m.chromosomes[5] for m in i.population]) for i in data[:100]]
#     # plt.plot(PCE)
#     plt.show()
