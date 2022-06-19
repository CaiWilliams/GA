from GPVDM import *
import numpy as np

def calc_series_resistance(args, cell_area, top_electrode_resistivity, bottom_electrode_resistivity):
    cell_width = np.sqrt(cell_area)
    cell_mid = cell_width / 2
    top_electrode_area = args[0] * cell_width
    bottom_electrode_area = args[-1] * cell_width
    series_resistance = ((top_electrode_resistivity * cell_mid) / top_electrode_area) + ((bottom_electrode_resistivity * cell_mid) / bottom_electrode_area)
    return float(series_resistance)

def calc_cost(args, cell_area, density, cost_per_g):
    cost = 0
    for idx,layer in enumerate(args):
        volume = cell_area * layer
        mass = volume * (density[idx] * 100)
        cost = cost + (mass * cost_per_g[idx])
    return cost

def read_pce(population):
    results = np.zeros(len(population))
    for idx, m in enumerate(population):
        with open(os.path.join(os.getcwd(), "GPVDM", "Temp" + str(idx), 'sim_info.dat'), 'r') as R:
            r = json.load(R)
            results[idx] = r['pce']
    return results

def layer_thicknses(G,population):
    for idx, m in enumerate(population):
        args = m.chromosomes
        y0 = 0
        G.load_job("Temp" + str(idx))
        for arg in args:
            G.modify_pm("dy", category=["epitaxy"], layer_name="layers", layer_number=0, value=float(arg))
            G.modify_pm("y0", category=["epitaxy"], layer_name="layers", layer_number=1, value=float(y0))
            y0 = y0 + arg
            G.save_job()
    return G

def update_mesh(G,population):
    for idx, m in enumerate(population):
        args = m.chromosomes
        y0 = 0
        G.load_job("Temp" + str(idx))
        G.modify_pm("len", category=["mesh", "mesh_y"], layer_name="segments", layer_number=0, value=float(args[2]))
        G.save_job()
    return G

def update_series_resistance(G,population,cell_area,top_electrode_resitivity,bottom_electrode_resistivity):
    for idx, m in enumerate(population):
        args = m.chromosomes
        y0 = 0
        G.load_job("Temp" + str(idx))
        G.modify_pm("Rcontact",category=["parasitic"],value=calc_series_resistance(args, cell_area, top_electrode_resitivity, bottom_electrode_resistivity))
        G.save_job()
    return G

def PCE(base_experiment, population, top_electrode_resistivity = 2.65e-8, bottom_electrode_resistivity = 1e-4, cell_area = 6.00005025e-6):
    G = gpvdm()
    for idx,m in enumerate(population):
        G.create_job(base_experiment,"Temp" + str(idx))

    G = layer_thicknses(G,population)
    G = update_mesh(G,population)
    G = update_series_resistance(G, population, cell_area, top_electrode_resistivity, bottom_electrode_resistivity)

    G.run()
    pce = read_pce(population)
    return pce

def calculate_cost(G, population, cell_area, density, cost_per_g):
    Cost = np.zeros(len(population))
    for idx, m in enumerate(population):
        args = m.chromosomes
        Cost[idx] = calc_cost(args, cell_area, density, cost_per_g)
    return Cost


def PCE_COST(base_experiment, population, top_electrode_resistivity = 2.65e-8, bottom_electrode_resistivity = 1e-4, cell_area = 6.00005025e-6,  density = [7.14,1.011,1.3,2.7], cost_per_g = [28.68,7.08,1,0.233]):
    G = gpvdm()
    for idx,m in enumerate(population):
        G.create_job(base_experiment,"Temp" + str(idx))

    G = layer_thicknses(G,population)
    G = update_mesh(G,population)
    G = update_series_resistance(G, population, cell_area, top_electrode_resistivity, bottom_electrode_resistivity)
    Cost = calculate_cost(G, population, cell_area, density, cost_per_g)

    G.run()
    results = np.zeros((len(population), 3))
    pce = read_pce(population)

    for idx,c in enumerate(Cost):
        results[idx,0] = pce[idx]/c
        results[idx,1] = pce[idx]
        results[idx,2] = c
    return results
