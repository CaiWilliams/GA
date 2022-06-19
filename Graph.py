import matplotlib.pyplot as plt
import numpy as np
import pickle

class Intra:
    def graph_optimisation(dir, exp_name):
        with open(exp_name, 'rb') as handle:
            just_name = exp_name.split('\\')[-1]
            just_name = just_name.split('.')[0]
            print(just_name)
            data = pickle.load(handle)
            data = data[data != 0]

            results_num = len(np.shape(data[0].result))
            if results_num > 1:
                results_num = np.shape(data[0].result)[1]

            if results_num == 1:
                average = np.asarray([np.average(i.result[:]) for i in data])
                std = np.asarray([np.std(i.result[:]) for i in data])
                plt.plot(average)
                print(average-std)
                plt.fill_between(range(len(data)), average-std, average+std, alpha=0.2)
                plt.xlabel('Generations')
                plt.ylabel('Result 0')
                plt.savefig(dir + '\\' + just_name + 'Result0.svg')
                plt.clf()
            else:
                for i in range(results_num):
                    average = np.asarray([np.average(j.result[:, i]) for j in data])
                    std = np.asarray([np.std(j.result[:, i]) for j in data])
                    plt.plot(average)
                    plt.fill_between(range(len(data)), average - std, average + std, alpha=0.2)
                    plt.xlabel('Generations')
                    plt.ylabel('Result ' + str(i))
                    plt.savefig(dir + '\\' + just_name + 'Result' + str(i) + '.svg')
                    plt.clf()

            layer_num = len(data[0].population[0].chromosomes)
            for i in range(layer_num):
                average = np.asarray([np.average([m.chromosomes[i] for m in j.population]) for j in data])
                std = np.asarray([np.std([m.chromosomes[i] for m in j.population]) for j in data])
                plt.plot(average)
                plt.fill_between(range(len(data)), average - std, average + std, alpha=0.2)
                plt.xlabel('Generations')
                plt.ylabel('Layer ' + str(i) + ' Thickness (m)')
                plt.savefig(dir + '\\' + just_name + 'Layer' + str(i) + '.svg')
                plt.clf()
        return