import copy
import pickle
import numpy as np
#import keyboard

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



