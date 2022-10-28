import os 
import matplotlib.pyplot as plt
import numpy as np
import natsort
import pickle

files = np.asarray(natsort.natsorted([_ for _ in os.listdir() if _.endswith('.exp')]))
Mutation = np.asarray([float(f.split("P")[0].strip("M")[:1] + "." + f.split("P")[0].strip("M")[1:]) for f in files ])
Population = np.asarray([int(f.split("P")[1].split("B")[0].strip("P")) for f in files])
P_lim_idx = np.argwhere(Population > 400)
files = np.delete(files,P_lim_idx)
Mutation = np.delete(Mutation,P_lim_idx)
Population = np.delete(Population,P_lim_idx)

print(Mutation)
print(Population)
print(files)

start_average = np.zeros(len(files))
start_std = np.zeros(len(files))
start_max = np.zeros(len(files))

for idx,file in enumerate(files):
    print(file)
    with open(file,'rb') as handle:
        data = pickle.load(handle)
        data = data[data != 0]
        start_average[idx] = np.average(data[0].result[:,0])
        start_std[idx] = np.std(data[0].result[:,0])
        start_max[idx] = np.max(data[0].result[:,0])

P = [10,20,40,60,80,100,200,400]
P_where = [np.argwhere(Population == p) for p in P]
average = np.zeros(len(P))
a_std = np.zeros(len(P))
max = np.zeros(len(P))
m_std = np.zeros(len(P))

for idx in range(len(P)):
    average[idx] = np.average(start_average[P_where[idx]])
    a_std[idx] = np.std(start_average[P_where[idx]])
    max[idx] = np.average(start_max[P_where[idx]])
    m_std[idx] = np.std(start_max[P_where[idx]])

#plt.errorbar(P, average, yerr=a_std,fmt="o")
plt.errorbar(P, max, yerr=m_std,fmt="o", c='tab:orange')
plt.xlim(left = 0, right = 410)
plt.xlabel("Population Size")
plt.ylabel("PCE (%)")
plt.savefig("Starting_Point_Max.png", dpi=600)