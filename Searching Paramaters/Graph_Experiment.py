import matplotlib.pyplot as plt
import numpy
import json
import pickle
import numpy as np


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


        G.save_job()

    G.run()

    results = np.zeros(len(population))
    for idx,m in enumerate(population):
        with open('C:\\Users\dszm31\GA-Main\GPVDM\Temp'+str(idx)+'\sim_info.dat','r') as R:
            r = json.load(R)
            results[idx] = r['pce']
    return results

def PCE_COST(population):
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

        Al_resistivity = 2.65e-8
        ITO_resistivity = 7.5e-6
        Cell_area = 6.00005025e-6
        Serise_resistance = ((ITO_resistivity * args[0]) / Cell_area) + ((Al_resistivity * args[3]) / Cell_area)
        pritn(Serise_resistance)
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
        P3HTPCBM_CostPerg = 974.5
        Al_CostPerg = 0.233

        ITO_Cost = ITO_CostPerg * ITO_mass
        PEDOTPSS_Cost = PEDOTPSS_CostPerg * PEDOTPSS_mass
        P3HTPCBM_Cost = P3HTPCBM_CostPerg * P3HTPCBM_mass
        Al_Cost = Al_CostPerg * Al_mass
        Cost = float(ITO_Cost + PEDOTPSS_Cost + P3HTPCBM_Cost + Al_Cost)


        G.save_job()

    G.run()

    results = np.zeros(len(population))
    for idx, m in enumerate(population):
        with open('C:\\Users\dszm31\GA-Main\GPVDM\Temp' + str(idx) + '\sim_info.dat', 'r') as R:
            r = json.load(R)
            res = float(r['pce'])
            results[idx] = res/Cost
    return results

def Calc_Cost(args):
    Cell_area = 6.00005025e-6
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
    P3HTPCBM_CostPerg = 668.902#173.4191#74.32255#8.2581#297.3#111.49#49.5485#18.58065#97.45
    Al_CostPerg = 0.233

    ITO_Cost = ITO_CostPerg * ITO_mass
    PEDOTPSS_Cost = PEDOTPSS_CostPerg * PEDOTPSS_mass
    P3HTPCBM_Cost = P3HTPCBM_CostPerg * P3HTPCBM_mass
    Al_Cost = Al_CostPerg * Al_mass

    Cost = float(ITO_Cost + PEDOTPSS_Cost + P3HTPCBM_Cost + Al_Cost)
    print("ITO Cost: " + str(ITO_Cost/Cost) + " %")
    print("PEDOT:PSS Cost: " + str(PEDOTPSS_Cost / Cost) + " %")
    print("P3HT:PCBM Cost: " + str(P3HTPCBM_Cost / Cost) + " %")
    print("Al Cost: " + str(Al_Cost / Cost) + " %")
    return Cost

#print(Calc_Cost([2.121e-8,1.835e-8,7.874e-8,4.166e-7]))
#print(Calc_Cost([1.7587377602472335e-08,3.2032514438528925e-08,7.647646435027887e-08,5.6413959090831547e-08]))
#print(Calc_Cost([1e-7,1e-7,2.2e-7,1e-7]))
with open('M001P40B0W0.exp', 'rb') as handle:
    data = pickle.load(handle)
    data = data[data != 0]

    average = [np.average(i.result[:,0]) for i in data]
    min = [np.min(i.result[:,0]) for i in data]
    max = [np.max(i.result[:,0]) for i in data]
    #print(np.argmax(data[-1].result))
    plt.plot(average)
    plt.fill_between(range(len(data)), min, max, alpha=0.2)
    plt.xlabel('Generations')
    plt.ylabel('LCOE ($/kWh)')
    plt.show()

    average = [np.average(i.result[:,1]) for i in data]
    min = [np.min(i.result[:,1]) for i in data]
    max = [np.max(i.result[:,1]) for i in data]
    plt.plot(average)
    plt.fill_between(range(len(data)), min, max, alpha=0.2)
    plt.xlabel('Generations')
    plt.ylabel('Yeild (W)')
    plt.show()

    average = [np.average(i.result[:, 2]) for i in data]
    min = [np.min(i.result[:, 2]) for i in data]
    max = [np.max(i.result[:, 2]) for i in data]
    plt.plot(average)
    plt.fill_between(range(len(data)), min, max, alpha=0.2)
    plt.xlabel('Generations')
    plt.ylabel('Cost (£)')
    plt.show()

    average = [np.average(i.result[:, 3]) for i in data]
    min = [np.min(i.result[:, 3]) for i in data]
    max = [np.max(i.result[:, 3]) for i in data]
    plt.plot(average)
    plt.fill_between(range(len(data)), min, max, alpha=0.2)
    plt.xlabel('Generations')
    plt.ylabel('PCE (%)')
    plt.show()

    average = [np.average([m.chromosomes[0] for m in i.population]) for i in data]
    std = [np.std([m.chromosomes[0] for m in i.population]) for i in data]
    print("ITO Thickness: " + str(average[-1]) + " m")
    min = [np.min([m.chromosomes[0] for m in i.population]) for i in data]
    max = [np.max([m.chromosomes[0] for m in i.population]) for i in data]
    plt.plot(average)
    #plt.fill_between(range(len(data)),min,max,alpha=0.2)
    plt.xlabel('Generations')
    plt.ylabel('ITO Thickness (m)')
    #plt.yscale('log')
    #plt.show()

    average = [np.average([m.chromosomes[1] for m in i.population]) for i in data]
    print("PEDOT:PSS Thickness: " + str(average[-1]) + " m")
    min = [np.min([m.chromosomes[1] for m in i.population]) for i in data]
    max = [np.max([m.chromosomes[1] for m in i.population]) for i in data]
    plt.plot(average)
    #plt.fill_between(range(len(data)), min, max, alpha=0.2)
    plt.xlabel('Generations')
    plt.ylabel('PEDOT:PSS Thickness (m)')
    #plt.yscale('log')
    #plt.show()

    average = [np.average([m.chromosomes[2] for m in i.population]) for i in data]
    print("P3HT:PCBM Thickness: " + str(average[-1]) + " m")
    min = [np.min([m.chromosomes[2] for m in i.population]) for i in data]
    max = [np.max([m.chromosomes[2] for m in i.population]) for i in data]
    plt.plot(average)
    #plt.fill_between(range(len(data)), min, max, alpha=0.2)
    plt.xlabel('Generations')
    plt.ylabel('P3HT:PCBM Thickness (m)')
    #plt.yscale('log')
    #plt.show()

    average = [np.average([m.chromosomes[3] for m in i.population]) for i in data]
    print("Al Thickness: " + str(average[-1]) + " m")
    min = [np.min([m.chromosomes[3] for m in i.population]) for i in data]
    max = [np.max([m.chromosomes[3] for m in i.population]) for i in data]
    plt.plot(average)
    #plt.fill_between(range(len(data)), min, max, alpha=0.2)
    plt.xlabel('Generations')
    #plt.ylabel('Al Thickness (m)')
    plt.ylabel('Layer Thickness (m)')
    plt.show()

    # PCE = [np.average([m.chromosomes[4] for m in i.population]) for i in data[:100]]
    # plt.plot(PCE)
    # PCE = [np.average([m.chromosomes[5] for m in i.population]) for i in data[:100]]
    #plt.plot(PCE)