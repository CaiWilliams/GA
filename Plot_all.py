import matplotlib.pyplot as plt
import os
import pickle
import numpy as np

import re
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

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

experiment_dir = 'Failed PCBMP3HT\\'
files = sorted_alphanumeric(os.listdir(experiment_dir))
active_layer_cost = [int(f.split('_')[-1].split('.')[0]) for f in files]
files = [experiment_dir + f for f in files]


PCE_Cost_Mean = np.zeros(len(files))
PCE_Cost_Error = np.zeros(len(files))

PCE_Mean = np.zeros(len(files))
PCE_Error = np.zeros(len(files))

Cost_Mean = np.zeros(len(files))
Cost_Error = np.zeros(len(files))

Layer_0_Mean = np.zeros(len(files))
Leyer_0_Error = np.zeros(len(files))

Layer_1_Mean = np.zeros(len(files))
Leyer_1_Error = np.zeros(len(files))

Layer_2_Mean = np.zeros(len(files))
Leyer_2_Error = np.zeros(len(files))

Layer_3_Mean = np.zeros(len(files))
Leyer_3_Error = np.zeros(len(files))

for idx, f in enumerate(files):
    with open(f, 'rb') as handle:

        data = pickle.load(handle)
        data = data[data != 0]

        PCE_Cost_Mean[idx] = [np.average(i.result[:, 0]) for i in data][-1]
        PCE_Cost_Error[idx] = [np.std(i.result[:, 0]) for i in data][-1]/np.sqrt(125)

        PCE_Mean[idx] = [np.average(i.result[:, 1]) for i in data][-1]
        PCE_Error[idx] = [np.std(i.result[:, 1]) for i in data][-1] / np.sqrt(125)

        Cost_Mean[idx] = [np.average(i.result[:, 2]) for i in data][-1]
        Cost_Error[idx] = [np.std(i.result[:, 2]) for i in data][-1] / np.sqrt(125)

        Layer_0_Mean[idx] = [np.average([m.chromosomes[0] for m in i.population]) for i in data][-1]
        Leyer_0_Error[idx] = [np.std([m.chromosomes[0] for m in i.population]) for i in data][-1]/np.sqrt(125)

        Layer_1_Mean[idx] = [np.average([m.chromosomes[1] for m in i.population]) for i in data][-1]
        Leyer_1_Error[idx] = [np.std([m.chromosomes[1] for m in i.population]) for i in data][-1] / np.sqrt(125)

        Layer_2_Mean[idx] = [np.average([m.chromosomes[2] for m in i.population]) for i in data][-1]
        Leyer_2_Error[idx] = [np.std([m.chromosomes[2] for m in i.population]) for i in data][-1] / np.sqrt(125)

        Layer_3_Mean[idx] = [np.average([m.chromosomes[3] for m in i.population]) for i in data][-1]
        Leyer_3_Error[idx] = [np.std([m.chromosomes[3] for m in i.population]) for i in data][-1] / np.sqrt(125)


plt.errorbar(active_layer_cost, PCE_Cost_Mean, yerr=PCE_Cost_Error)
plt.ylabel('Cost Per Unit PCE (£/%)')
plt.xlabel('Active Layer Cost (£/g)')
plt.xscale('log')
plt.show()

plt.errorbar(active_layer_cost, PCE_Mean, yerr=PCE_Error)
plt.ylabel('Power Conversion Efficiency (£/%)')
plt.xlabel('Active Layer Cost (£/g)')
plt.xscale('log')
plt.show()

plt.errorbar(active_layer_cost, Cost_Mean, yerr=Cost_Error)
plt.ylabel('Device Cost (£)')
plt.xlabel('Active Layer Cost (£/g)')
plt.xscale('log')
plt.show()

plt.errorbar(active_layer_cost, Layer_0_Mean, yerr=Leyer_0_Error)
plt.ylabel('ITO Thickness (m)')
plt.xlabel('Active Layer Cost (£/g)')
plt.xscale('log')
plt.show()

plt.errorbar(active_layer_cost, Layer_1_Mean, yerr=Leyer_1_Error)
plt.ylabel('PEDOT:PSS Thickness (m)')
plt.xlabel('Active Layer Cost (£/g)')
plt.xscale('log')
plt.show()

plt.errorbar(active_layer_cost, Layer_2_Mean, yerr=Leyer_2_Error)
plt.ylabel('P3HT:PCBM Thickness (m)')
plt.xlabel('Active Layer Cost (£/g)')
plt.xscale('log')
plt.show()

plt.errorbar(active_layer_cost, Layer_3_Mean, yerr=Leyer_3_Error)
plt.ylabel('Al Thickness (m)')
plt.xlabel('Active Layer Cost (£/g)')
plt.xscale('log')
plt.show()