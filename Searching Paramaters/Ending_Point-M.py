import os 
import matplotlib.pyplot as plt
import numpy as np
import natsort
import pickle

files = np.asarray(natsort.natsorted([_ for _ in os.listdir() if _.endswith('.exp')]))
Mutation = np.asarray([float(f.split("P")[0].strip("M")[:1] + "." + f.split("P")[0].strip("M")[1:]) for f in files ])
Population = np.asarray([int(f.split("P")[1].split("B")[0].strip("P")) for f in files])
P_lim_idx = np.argwhere(Population > 1000)
files = np.delete(files,P_lim_idx)
Mutation = np.delete(Mutation,P_lim_idx)
print(Mutation)
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
        best = np.max(data[0].result[:,0])
        e = 0
        while e < 5:
                for jdx,i in enumerate(data):
                    if best < np.max(i.result[:,0]):
                        best = np.max(i.result[:,0])
                        e = 0
                    else:
                        e = e + 1
                    if e >= 5:
                        break
        data = data[:jdx]
        start_average[idx] = np.average(data[-1].result[:,0])
        start_std[idx] = np.std(data[-1].result[:,0])
        start_max[idx] = np.max(data[-1].result[:,0])

P = [10,20,40,60,80,100,200]
M = np.asarray([0, 0.01, 0.02, 0.04, 0.06])
P_where = [np.argwhere(Mutation == p) for p in M]
average = np.zeros(len(M))
a_std = np.zeros(len(M))
max = np.zeros(len(M))
m_std = np.zeros(len(M))

for idx in range(len(M)):
    average[idx] = np.average(start_average[P_where[idx]])
    a_std[idx] = np.std(start_average[P_where[idx]])
    max[idx] = np.average(start_max[P_where[idx]])
    m_std[idx] = np.std(start_max[P_where[idx]])

#plt.errorbar(M*100, average, yerr=a_std,fmt="o")
plt.errorbar(M*100, max, yerr=m_std,fmt="o",c="tab:orange")
#plt.xlim(left = 0, right = 210)
plt.xlabel("Mutation Rate (%)")
plt.ylabel("PCE (%)")
plt.savefig("Ending_Point_Mutation_Max.png", dpi=600)