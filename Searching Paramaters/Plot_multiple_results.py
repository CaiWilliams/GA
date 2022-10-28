import matplotlib.pyplot as plt
import numpy
import json
import pickle
import numpy as np



def  plot_resuts(*args):
    for file_name in args:
        with open(file_name, 'rb') as handle:
            print(file_name)
            data = pickle.load(handle)
            data = data[data != 0]
            best = np.max(data[0].result[:,0])
            e = 0
            while e < 5:
                for idx,i in enumerate(data):
                    if best < np.max(i.result[:,0]):
                        best = np.max(i.result[:,0])
                        e = 0
                    else:
                        e = e + 1
                    if e >= 5:
                        break
                    print(e)
            print(len(data))
            data = data[:idx]
                
                

            average = [np.average(i.result[:,0]) for i in data]
            min = [np.min(i.result[:,0]) for i in data]
            max = [np.max(i.result[:,0]) for i in data]
            plt.plot(max)
            #plt.fill_between(range(len(data)), min, max, alpha=0.2)
    plt.xlabel('Generations')
    plt.ylabel('LCOE ($/kWh)')
    plt.show()

#plot_resuts('M08P10B0W0.exp','M08P20B0W0.exp','M08P40B0W0.exp','M08P60B0W0.exp')
plot_resuts('M0P10B0W0.exp','M0P20B0W0.exp','M0P40B0W0.exp','M0P60B0W0.exp','M0P80B0W0.exp','M0P100B0W0.exp','M0P200B0W0.exp','M0P400B0W0.exp','M0P600B0W0.exp','M0P800B0W0.exp','M0P1000B0W0.exp')
#plot_resuts("M001P40B0W0.exp","M002P40B0W0.exp","M004P40B0W0.exp","M006P40B0W0.exp","M008P40B0W0.exp","M01P40B0W0.exp")
#plot_resuts("M0P100B0W0.exp","M001P100B0W0.exp","M002P100B0W0.exp","M004P100B0W0.exp","M006P100B0W0.exp","M008P100B0W0.exp","M01P100B0W0.exp","M02P100B0W0.exp","M04P100B0W0.exp","M06P100B0W0.exp","M08P100B0W0.exp")