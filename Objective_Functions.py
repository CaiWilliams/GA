import copy

import matplotlib.pyplot as plt

#from GPVDM import *
import device_fitting
from device_fitting import *
from yield_model import *
import numpy as np
import pandas as pd
import itertools
import os

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

def read_Pmax(population):
    results = np.zeros(len(population))
    for idx, m in enumerate(population):
        with open(os.path.join(os.getcwd(), "GPVDM", "Temp" + str(idx), 'sim_info.dat'), 'r') as R:
            r = json.load(R)
            results[idx] = r['Pmax']
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

def calculate_cost(G, population, cell_area, density, cost_per_g):
    Cost = np.zeros(len(population))
    for idx, m in enumerate(population):
        args = m.chromosomes
        Cost[idx] = calc_cost(args, cell_area, density, cost_per_g)
    return Cost

def PCE(population, top_electrode_resistivity = 2.65e-8, bottom_electrode_resistivity = 1e-4, cell_area = 6.00005025e-6):
    G = gpvdm()
    for idx,m in enumerate(population):
        G.create_job("Temp" + str(idx))

    G = layer_thicknses(G,population)
    G = update_mesh(G,population)
    G = update_series_resistance(G, population, cell_area, top_electrode_resistivity, bottom_electrode_resistivity)

    G.run()
    pce = read_pce(population)
    return pce


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

def modify_temperature(self, temperature):
    x = getattr(self.data, 'epitaxy')
    layers = getattr(x, 'layers')
    for layer in layers:
        DOS = getattr(layer, 'shape_dos')
        setattr(DOS, 'Tstart', float(temperature))
        setattr(DOS, 'Tstop', float(temperature + 5))
    return self

def modify_irradiance(self, irradiance):
    x = getattr(self.data, 'light')
    setattr(x, 'Psun', float(irradiance))
    return self

def modify_temperature_irradiance(G,temperature,irradiance,population):
    for idx, m in enumerate(population):
        args = m.chromosomes
        y0 = 0
        G.load_job("Temp" + str(idx))
        for arg in args:
            G.modify_temperature(temperature)
            G.modify_Irradiance(irradiance)
            G.save_job()
    return G

def LCOE(population, top_electrode_resistivity = 2.65e-8, bottom_electrode_resistivity = 1e-4, cell_area = 6.00005025e-6,  density = [7.14,1.011,1.3,2.7], cost_per_g = [28.68,7.08,1,0.233]):
    G = gpvdm()
    for idx, m in enumerate(population):
        G.create_job("Temp" + str(idx))

    G = layer_thicknses(G, population)
    G = update_mesh(G, population)
    G = update_series_resistance(G, population, cell_area, top_electrode_resistivity, bottom_electrode_resistivity)
    Cost = calculate_cost(G, population, cell_area, density, cost_per_g)
    G.run()
    results = np.zeros((len(population), 3))
    pce = read_pce(population)

    irradiance_range = np.asarray([1.1, 1, 0.8, 0.6, 0.4, 0.2, 0.1])
    temperature_range = np.asarray([288.15, 298.15, 323.15, 348.15])
    yield_frame = pd.DataFrame(columns=temperature_range - 273.15, index=irradiance_range * 1000).to_dict()
    yield_tables = []
    for p in population:
        yield_tables.append(yield_frame)
    combinations = [list(tup) for tup in itertools.product(irradiance_range, temperature_range)]

    for comb in combinations:
        irr, temp = comb
        temp = temp - 273.15
        irr = irr * 1000
        G = G.modify_temperature_irradiance(G,temp,irr)
        G.run()
        Pmax = read_Pmax(population)
        for idx in range(len(yield_tables)):
            dict = copy.deepcopy(yield_tables[idx])
            dict[temp][irr] = Pmax[idx]
            yield_tables[idx] = dict
    for idx,r in enumerate(yield_tables):
        df = pd.DataFrame(r)
        dir = os.path.join(os.getcwd(), 'Yield_Table', 'Temp'+str(idx)+'.csv')
        df.to_csv(dir)
    for idx in range(len(population)):
        device_fitting.fit_device('Temp'+str(idx)+'.csv', 'Yield_Coefficients')









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
