import numpy as np
import pandas as pd
import itertools
import copy

from GPVDM import *


class yeild:

    def __init__(self, experiment_name, population_N):
        self.experiment_name = experiment_name
        sim_dirs = ['Temp' + str(n) for n in range(population_N)]
        irradiance_range = np.asarray([1.1, 1, 0.8, 0.6, 0.4, 0.2, 0.1])
        temperature_range = np.asarray([288.15, 298.15, 323.15, 348.15])
        yeild_frame = pd.DataFrame(columns=temperature_range - 273.15, index= irradiance_range * 1000).to_dict()
        results = []
        for sim in sim_dirs:
            results.append(yeild_frame)
        combinations = [list(tup) for tup in itertools.product(irradiance_range,temperature_range)]
        for comb in combinations:
            irr,temp = comb
            temp = temp - 273.15
            irr = irr * 1000
            result = self.calc_power(sim_dirs, *comb)
            for idx in range(len(results)):
                dict = copy.deepcopy(results[idx])
                dict[temp][irr] = result[idx]
                results[idx] = dict
        for idx,r in enumerate(results):
            df = pd.DataFrame(r)
            df.to_csv('Yeild_Table_'+str(sim_dirs[idx])+'.csv')


    def calc_power(self, sim_dirs, irradiance, temperature):
        G = gpvdm()
        for dir in sim_dirs:
            G.load_job(dir)
            G.modify_temperature(temperature)
            G.modify_irradiance(irradiance)
            G.save_job()
        G.run()
        results = np.zeros(len(sim_dirs))
        for idx in range(len(sim_dirs)):
            with open(os.path.join(os.getcwd(), "GPVDM", "Temp" + str(idx), 'sim_info.dat'), 'r') as R:
                r = json.load(R)
                results[idx] = r['Pmax']
        for dir in sim_dirs:
            G.load_job(dir)
            G.modify_temperature(300)
            G.modify_irradiance(1)
            G.save_job()
        return results

yeild('test',1)