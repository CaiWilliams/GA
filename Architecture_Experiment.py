import numpy as np

from Architecture import *

def define_population(N, chromosones_order, mutation_chance,A):
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

def PCE(population):
    G = gpvdm()
    for idx,m in enumerate(population):
        args = m.chromosomes
        G.create_job("Temp"+str(idx))
        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=0, value=float(args[0]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(args[1]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(args[0]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=2, value=float(args[2]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=2, value=float(args[0] + args[1]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=3, value=float(args[3]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=3, value=float(args[0] + args[1] + args[2]))


        G.modify_pm("len", category=["mesh", "mesh_y"], layer_name="segments", layer_number=0, value=float(args[2]))

        Al_resistivity = 1.59e-8
        ITO_resistivity = 7.5e-6
        Cell_area = 6.00005025e-6
        Serise_resistance = (ITO_resistivity * (args[0] / Cell_area)) + (Al_resistivity * (args[3] / Cell_area))
        G.modify_pm("Rcontact",category=["parasitic"],value=float(Serise_resistance))

        G.save_job()

    G.run()

    results = np.zeros(len(population))
    for idx,m in enumerate(population):
        with open('C:\\User\\dszm31\\GA-Main\\GPVDM\\Temp'+str(idx)+'\\sim_info.dat','r') as R:
            r = json.load(R)
            results[idx] = r['pce']
    return results


def PCE_COST(population):
    G = gpvdm()
    Cost = np.zeros(len(population))
    for idx,m in enumerate(population):
        args = m.chromosomes
        G.create_job("Temp"+str(idx))
        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=0, value=float(args[0]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(args[1]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(args[0]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=2, value=float(args[2]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=2, value=float(args[0] + args[1]))

        G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=3, value=float(args[3]))
        G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=3, value=float(args[0] + args[1] + args[2]))


        G.modify_pm("len", category=["mesh", "mesh_y"], layer_name="segments", layer_number=0, value=float(args[2]))

        Al_resistivity = 2.65e-8
        ITO_resistivity = 1e-4
        Cell_area = 6.00005025e-6
        Serise_resistance = ((ITO_resistivity * args[0]) / Cell_area) + ((Al_resistivity * args[3]) / Cell_area)
        G.modify_pm("Rcontact",category=["parasitic"],value=float(Serise_resistance))

        ITO_Desnity = 7.14 * 100
        PEDOTPSS_Density = 1.011 * 100
        P3HTPCBM_Density = 1.3 * 100
        Al_Density = 2.7 * 100

        ITO_Volume = Cell_area * args[0]
        PEDOTPSS_Volume = Cell_area * args[1]
        P3HTPCBM_Volume = Cell_area * args[2]
        Al_Volume = Cell_area * args[3]

        ITO_mass = ITO_Volume * ITO_Desnity
        PEDOTPSS_mass = PEDOTPSS_Volume * PEDOTPSS_Density
        P3HTPCBM_mass = P3HTPCBM_Volume * P3HTPCBM_Density
        Al_mass = Al_Volume * Al_Density

        ITO_CostPerg = 28.68
        PEDOTPSS_CostPerg = 7.08
        P3HTPCBM_CostPerg = np.loadtxt('ActiveLayer.cost')[0]
        Al_CostPerg = 0.233

        ITO_Cost = ITO_CostPerg * ITO_mass
        PEDOTPSS_Cost = PEDOTPSS_CostPerg * PEDOTPSS_mass
        P3HTPCBM_Cost = P3HTPCBM_CostPerg * P3HTPCBM_mass
        Al_Cost = Al_CostPerg * Al_mass
        Cost[idx] = ITO_Cost + PEDOTPSS_Cost + P3HTPCBM_Cost + Al_Cost


        G.save_job()
    G.run()
    results = np.zeros((len(population),3))
    for idx, m in enumerate(population):
        with open('C:\\Users\\dszm31\\GA-Main\\GPVDM\\Temp' + str(idx) + '\\sim_info.dat', 'r') as R:
            r = json.load(R)
            res = float(r['pce'])
            results[idx, 0] = res / Cost[idx]
            results[idx, 1] = res
            results[idx, 2] = Cost[idx]
    return results


def exp(active_later_cost):
    C = np.ones(2) * active_later_cost
    np.savetxt('ActiveLayer.cost',C)
    Pop = np.zeros(10000000,dtype=Population)
    A = Architecture(4)
    #A.set_x(0.0024495,0.000024495,0.0024495)
    #A.set_z(0.0024495,0.000024495,0.0024495)
    A.set_y([1e-7,1e-7,2.2e-7,1e-7], [10e-9,10e-9,10e-9,10e-9], [1e-6,1e-6,1e-6,1e-6])
    CO = [A.y[0], A.y[1], A.y[2], A.y[3]]
    M = 0.30
    P = define_population(125, CO, M,A)
    Target_PCE = Objective_Function(10000000000000000,PCE_COST)
    Gen = 0

    try:
        while Gen <= 75:
            P.rank_population(Target_PCE)
            Pop[Gen] = copy.deepcopy(P)
            P.best_in_population(12)
            P.worst_in_population(25)
            P.next_generation(25)
            Gen = Gen + 1

            with open('OnGoing_Experiment'+'_'+str(active_later_cost)+'.exp', 'wb') as handle:
                pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)

        P.save('Last_Generation.gen')
        with open('20220523PM6Y6125.exp', 'wb') as handle:
            pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)

    finally:

        P.save('Last_Generation.gen')
        with open('20220523PM6Y6125.exp', 'wb') as handle:
            pickle.dump(Pop, handle, protocol=pickle.HIGHEST_PROTOCOL)

# exp(1)
# exp(2)
# exp(4)
# exp(6)
# exp(8)
# exp(10)
# exp(20)
# exp(40)
# exp(60)
# exp(80)
# exp(100)
# exp(200)
# exp(400)
# exp(600)
# exp(800)
exp(1000)