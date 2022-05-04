import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

sys.path.append("C:\\Users\\Cai Williams\\Desktop\\modules")

from gpvdm_api import gpvdm_api
from gpvdm_json import gpvdm_data

api = gpvdm_api(verbose=False)

script_name = os.path.basename(__file__).split('.')[0]
scan_dir = os.path.join(os.getcwd(), script_name)



api.mkdir(scan_dir)
api.server.server_base_init(scan_dir)

for mue in [1e-5, 1e-6, 1e-7, 1e-8]:
    for muh in [1e-5, 1e-6, 1e-7, 1e-9]:

        sim_path = os.path.join(scan_dir, "{:.2e}".format(mue), "{:.2e}".format(muh))
        api.mkdir(sim_path)
        api.clone(sim_path, os.getcwd())

        data = gpvdm_data()
        data.load(os.path.join(sim_path, "sim.json"))
        data.epi.layers[2].shape_dos.mue_y = mue
        data.epi.layers[2].shape_dos.muh_y = muh
        data.save()
        api.add_job(path=sim_path)

api.server.simple_run()
api.build_multiplot(scan_dir, gnuplot=True)


PCE = np.zeros(4)
i = 0
for mue in [1e-5, 1e-6, 1e-7, 1e-8]:
    for muh in [1e-5, 1e-6, 1e-7, 1e-9]:

        sim_path = os.path.join(scan_dir, "{:.2e}".format(mue), "{:.2e}".format(muh))
        with open(sim_path + "\sim_info.dat") as f:
            X = json.loads(f.read())
            PCE[i] = X['pce']
            i = i + 1
    plt.plot(PCE)
    i=0
plt.show()
