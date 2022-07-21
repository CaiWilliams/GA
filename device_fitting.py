import itertools
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import os


def Power(GT,P,k1,k2,k3,k4,k5,k6):
    G = GT[1, :]
    T = GT[0, :]
    return G * (P + (k1 * np.log(G)) + (k2 * np.power(np.log(G), 2)) + (k3 * T) + (k4 * T * np.log(G)) + (k5 * T * np.power(np.log(G), 2) + (k6 * np.power(T, 2))))


def Load_Device(dir):
    data = pd.read_csv(dir)
    Temperatures = data.columns.to_numpy()
    Temperatures = Temperatures[1:].astype(int)
    Irradiance = data['Unnamed: 0'].to_numpy()
    data = data.drop('Unnamed: 0', axis=1)
    Power = data.to_numpy().ravel()
    GT = [list(tup) for tup in itertools.product(Temperatures, Irradiance)]
    nans = np.argwhere(np.isnan(Power))
    Power = np.delete(Power,nans)
    GT = np.delete(GT, nans,axis=0).T
    return GT, Power

def fit_device(name,save_dir):
    GT, P = Load_Device(os.path.join(os.getcwd(),'Yield_Tables',name)
    popt, pcov = curve_fit(Power, GT, P)
    cols = ['k1','k2','k3','k4','k5','k6']
    data = pd.DataFrame(popt[:6],columns=cols,index=False)
    data.to_csv(os.path.join(os.getcwd(),save_dir,name))