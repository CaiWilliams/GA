#import copy

from unicodedata import category
import matplotlib.pyplot as plt

import yield_calc
from GPVDM import *
import device_fitting
from device_fitting import *
from yield_calc import *
import numpy as np
import pandas as pd
import itertools
import os
import time

def calc_series_resistance(args, cell_area, top_electrode_resistivity, bottom_electrode_resistivity):
    cell_width = np.sqrt(cell_area)
    cell_mid = cell_width / 2
    top_electrode_area = args[0] * cell_width
    bottom_electrode_area = args[-1] * cell_width
    series_resistance = ((top_electrode_resistivity * cell_mid) / top_electrode_area) + ((bottom_electrode_resistivity * cell_mid) / bottom_electrode_area)
    return float(series_resistance)

def calc_series_resistance2(args, cell_area, top_electrode_resistivity, bottom_electrode_resistivity):
    cell_width = np.sqrt(cell_area)
    cell_mid = cell_width / 2
    top_electrode_series_resistance = (top_electrode_resistivity / args[0]) * (cell_mid/cell_width)
    bottom_electrode_series_resistance = (bottom_electrode_resistivity / args[-1]) * (cell_mid/cell_width)
    series_resistance = top_electrode_series_resistance + bottom_electrode_series_resistance
    return float(series_resistance)

def calc_series_resistance3(args, cell_area, top_electrode_resistivity, bottom_electrode_resistivity):
    cell_width = np.sqrt(cell_area)
    cell_mid = cell_width / 2
    top_electrode_series_resistance = top_electrode_resistivity * ((cell_mid)/(cell_width*args[0])) #/ args[0]) * (cell_mid/cell_width)
    bottom_electrode_series_resistance = bottom_electrode_resistivity * ((cell_mid)/(cell_width*args[1])) #(bottom_electrode_resistivity / args[-1]) * (cell_mid/cell_width)
    series_resistance = top_electrode_series_resistance + bottom_electrode_series_resistance
    return float(series_resistance)

def calc_cost(args, cell_area, density, cost_per_g):
    cost = 0
    for idx,layer in enumerate(args):
        volume = cell_area * layer
        mass = volume * (density[idx] * 100)
        cost = cost + (mass * cost_per_g[idx])
    return cost

def read_pce(population,name):
    results = np.zeros(len(population))
    for idx, m in enumerate(population):
        with open(os.path.join(os.getcwd(), "GPVDM", "Temp" + name +str(idx), 'sim_info.dat'), 'r') as R:
            r = json.load(R)
            results[idx] = r['pce']
    return results

def read_Pmax(population,name):
    results = np.zeros(len(population))
    for idx, m in enumerate(population):
        with open(os.path.join(os.getcwd(), "GPVDM", "Temp" + name +str(idx), 'sim_info.dat'), 'r') as R:
            r = json.load(R)
            results[idx] = r['Pmax']
    return results

def layer_thicknses(G,population):
    for idx, m in enumerate(population):
        args = m.chromosomes
        y0 = 0
        G.load_job("Temp" + str(idx))
        for arg in args:
            G.modify_pm("dy", category=["epitaxy"], layer_name="layer", layer_number=0, value=float(arg))
            G.modify_pm("y0", category=["epitaxy"], layer_name="layer", layer_number=1, value=float(y0))
            y0 = y0 + arg
            #G.save_job()
    return G


def layer_thicknses2(G,name,population,pop):
    print(pop)
    material = name.split('MAT')[1][:-1]
    material_base = material.split('_')[0]
    map = pop.chromosome_map
    for idx, m in enumerate(population):
        args = m.chromosomes
        y0 = 0
        G.create_job_json("Temp" + name + str(idx), material_base)
        if 'pm6y6' in material:
            G.modify_pm_json("optical_material",category=['epitaxy'],layer_name='layer',layer_number=3,value='chemnitz/active_fresh')
        else:
            G.modify_pm_json("optical_material",category=['epitaxy'],layer_name='layer',layer_number=3,value='blends/'+str(material))
        for idx,arg in enumerate(args):
            if idx < len(args):
                G.modify_pm_json("dy", category=["epitaxy"], layer_name="layer", layer_number=map[idx], value=float(arg))
                G.modify_pm_json("y0", category=["epitaxy"], layer_name="layer", layer_number=map[idx]+1, value=float(y0))
            else:
                G.modify_pm_json("dy", category=["epitaxy"], layer_name="layer", layer_number=map[idx]+1, value=float(arg))
            y0 = y0 + arg
        update_mesh2(G,args)
        update_series_resistance2(G,args)
        
        G.save_job()
    return G

def update_mesh(G,population):
    for idx, m in enumerate(population):
        args = m.chromosomes
        y0 = 0
        G.load_job("Temp" + str(idx))
        G.modify_pm("len", category=["mesh", "mesh_y"], layer_name="segments", layer_number=0, value=float(args[2]))
        #G.save_job()
    return G

def update_mesh2(G,args):
    G.modify_pm_json("len", category=["mesh", "mesh_y"], layer_name="segment", layer_number=0, value=float(args[2]))
    return G

def update_series_resistance(G,population,cell_area,top_electrode_resitivity,bottom_electrode_resistivity):
    for idx, m in enumerate(population):
        args = m.chromosomes
        y0 = 0
        G.load_job("Temp" + str(idx))
        G.modify_pm_json("Rcontact",category=["parasitic"],value=calc_series_resistance2(args, cell_area, top_electrode_resitivity, bottom_electrode_resistivity))
        #G.save_job()
    return G

def update_series_resistance2(G,args, top_electrode_resitivity = 2.65e-8, bottom_electrode_resistivity = 1e-4, cell_area = 6.00005025e-6):
    G.modify_pm_json("Rcontact",category=["parasitic"],value=calc_series_resistance2(args, cell_area, top_electrode_resitivity, bottom_electrode_resistivity))
    return G

def calculate_cost(G, population, cell_area, density, cost_per_g):
    Cost = np.zeros(len(population))
    for idx, m in enumerate(population):
        args = m.chromosomes
        Cost[idx] = calc_cost(args, cell_area, density, cost_per_g)
    return Cost

def PCE(population, pop, top_electrode_resistivity = 1e-4, bottom_electrode_resistivity = 2.65e-8, cell_area = 6.00005025e-6, name="NoName"):

    G = gpvdm()
    G = layer_thicknses2(G,name,population,pop)

    G.run()

    pce = read_pce(population,name)
    results = np.zeros((len(population), 4))
    results[:,0] = pce
    return results

def PCE_COST(population, top_electrode_resistivity = 2.65e-8, bottom_electrode_resistivity = 1e-4, cell_area = 6.00005025e-6,  density = [7.14,1.011,1.3,2.7], cost_per_g = [28.68,7.08,1,0.233]):
    G = gpvdm()
    for idx,m in enumerate(population):
        G.create_job("Temp" + str(idx))

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

def modify_temperature_irradiance(temperature,irradiance,population):
    G = gpvdm()
    for idx in range(len(population)):
        G.load_job("Temp" + str(idx))
        G.modify_temperature(temperature)
        G.modify_irradiance(irradiance)
        G = G.save_job()
    G.run()
    return

def LCOE(population, location='Portsmouth', top_electrode_resistivity = 2.65e-8, bottom_electrode_resistivity = 1e-4, cell_area = 6.00005025e-6,  density = [7.14,1.011,1.3,2.7], cost_per_g = [28.68,7.08,472,0.233]):
    #p3ht:PCBM cost per g: £472
    #pm6:y6 cost per g: £1630
    G = gpvdm()
    for idx, m in enumerate(population):
        G.create_job("Temp" + str(idx))

    G = layer_thicknses2(G, population)
    Cost = calculate_cost(G, population, 1.6, density, cost_per_g)
    results = np.zeros((len(population), 4))
    results[:,2] = Cost
    print(results[:,2])

    G.run()



    irradiance_range = np.asarray([1.1, 1, 0.8, 0.6, 0.4, 0.2, 0.1])
    temperature_range = np.asarray([288.15, 298.15, 323.15, 348.15])
    yield_frame = pd.DataFrame(columns=temperature_range-273.15, index=irradiance_range*1000).to_dict()
    yield_tables = []
    for p in population:
        yield_tables.append(yield_frame)
    combinations = [list(tup) for tup in itertools.product(irradiance_range, temperature_range)]
    for comb in combinations:
        irr, temp = comb
        temp = temp
        G = modify_temperature_irradiance(temp,irr,population)
        Pmax = read_Pmax(population)
        if irr == 1 and temp == 298.15:
            PCE = read_pce(population)
            results[:,3] = PCE
        for idx in range(len(yield_tables)):
            #dict = copy.deepcopy(yield_tables[idx])
            dict[temp-273.15][irr*1000] = Pmax[idx]
            yield_tables[idx] = dict

    for idx,r in enumerate(yield_tables):
        df = pd.DataFrame(r)
        dir = os.path.join(os.getcwd(), 'Yield_Tables', 'Temp' + str(idx) + '.csv')
        df.to_csv(dir)
    for idx in range(len(population)):
        device_fitting.fit_device('Temp'+str(idx)+'.csv', 'Yield_Coefficients')
    loc = yield_calc.calulate_yield_setup(location)
    lcoe_tabel = pd.read_csv('Tabulated_LCOE_Main.csv')
    costs = lcoe_tabel['Unnamed: 0'].values
    power_gen = lcoe_tabel.columns.values[1:].astype('float')
    lcoe_tabel = lcoe_tabel.to_numpy()
    for idx in range(len(population)):
        dev_dir = os.path.join(os.getcwd(),'Yield_Coefficients','Temp'+str(idx)+'.csv')
        results[idx, 1] = np.sum(yield_calc.calculate_yield(loc,dev_dir))*20
        r_idx = (np.abs(costs - results[idx, 2])).argmin()
        r_jdx = (np.abs(power_gen - results[idx, 1])).argmin()
        results[idx, 0] = lcoe_tabel[r_idx, r_jdx]
        print(results[idx, 0])
    return results



def Rastrigin_Funcition(x):
    A = 10
    n = len(x)
    sum = 0
    for idx in x:
        sum = sum + (np.power(idx,2) - A * np.cos(2 * np.pi * idx))
    f = (A * n) + sum
    return f

def Rastrigin(population):
    results = np.zeros((len(population),1))
    for idx, i in enumerate(population):
        results[idx] = Rastrigin_Funcition(i.chromosomes)
    return results


if __name__ == '__main__':
    #top_electrode_resistivity = 2.65e-8
    #bottom_electrode_resistivity = 1e-4
    top_electrode_resistivity = 1e-4
    bottom_electrode_resistivity = 2.65e-8
    xy = np.linspace(0.0024495,0.24495,50)
    for XY in xy:
        cell_area = np.power(XY,2)
        print(cell_area)
        print(calc_series_resistance2([100e-9,100e-9,100e-9,100e-9],cell_area,top_electrode_resistivity,bottom_electrode_resistivity))
        print(calc_series_resistance2([500e-9,500e-9,500e-9,500e-9],cell_area,top_electrode_resistivity,bottom_electrode_resistivity))
        print(calc_series_resistance3([100e-9,100e-9,100e-9,100e-9],cell_area,top_electrode_resistivity,bottom_electrode_resistivity))
        print(calc_series_resistance3([500e-9,500e-9,500e-9,500e-9],cell_area,top_electrode_resistivity,bottom_electrode_resistivity))