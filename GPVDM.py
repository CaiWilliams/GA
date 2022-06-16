import os
import sys
import json

sys.path.append("C:\\Users\\dszm31\\modules")

from gpvdm_api import gpvdm_api
from gpvdm_json import gpvdm_data


class gpvdm:
    def __init__(self):

        self.api = gpvdm_api(verbose=False)

        self.script_name = os.path.basename(__file__).split('.')[0]
        self.scan_dir = os.path.join(os.getcwd(), self.script_name)

        self.api.mkdir(self.scan_dir)
        self.api.server.server_base_init(self.scan_dir)

    def create_job(self, sim_name):
        self.sim_path = os.path.join(self.scan_dir, sim_name)
        self.api.mkdir(self.sim_path)
        self.api.clone(self.sim_path, os.getcwd())

        self.data = gpvdm_data()
        self.data.load(os.path.join(self.sim_path, "sim.json"))
        return self

    def load_job(self, sim_name):
        self.sim_path = os.path.join(self.scan_dir, sim_name)
        #self.api.mkdir(self.sim_path)
        #self.api.clone(self.sim_path, os.getcwd())
        #self.data = gpvdm_data()
        self.data.load(os.path.join(self.sim_path, "sim.json"))
        return self

    def modify_parameter(self, category, layer_name, layer_value, subcategory, parameter, value):
        x = getattr(self.data, category)
        x = getattr(x, layer_name)
        x = getattr(x[layer_value], subcategory)
        setattr(x, parameter, value)
        return self

    def modify_pm(self, *args, category, layer_name=None, layer_number=None, value):
        x = getattr(self.data, category[0])
        try:
            for i in category[1:]:
                x = getattr(x, i)
        except:
            print("")
        try:
            x = getattr(x, layer_name)
        except:
            print("")
        if layer_number == None:
            x = x
        else:
            x = x[layer_number]
        for arg in args[:-1]:
            x = getattr(x, arg)
        setattr(x, args[-1], value)

    def remesh(self):

        self.data.mesh.config.remesh_x = "True"
        self.data.mesh.config.remesh_y = "True"
        self.data.mesh.config.remesh_z = "True"

    def save_job(self):
        self.data.save()
        self.api.add_job(path=self.sim_path)
        self.data.save()
        return self

    def run(self):
        self.api.server.simple_run()
        return self