import pickle

with open('PreviousRun5.gap', 'rb') as handle:
    data = pickle.load(handle)
    for i in data:
        for m in i:
            print(m.chromosomes)