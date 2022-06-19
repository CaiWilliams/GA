import git
from git import Repo
import pandas as pd
import requests
import csv
import time
import os
from ast import literal_eval
from Experiment import *
from Graph import Intra


class Jobs:

    def __init__(self, file_name,):
        self.file_name = file_name
        self.git_dir = os.path.join(os.getcwd(),'Experiment_Status','Experiment-Status')
        print(os.path.isdir(self.git_dir))
        if os.path.isdir(self.git_dir) == False:
            self.clone_remote()
        self.experiments = self.get_experiment_que()
        self.save_experiment_que()
        self.completed = self.get_completed_experiments()
        while True:
            self.pull_remote()
            if self.experiments.empty == True:
                time.sleep(1)
                self.pull_remote()
                if self.test_new_experiments() == False:
                    break
            experiment = self.load_experiment()
            if experiment != None:
                self.start_time = time.time()
                Experiment(**experiment)
                self.end_time = time.time()
                self.time_to_complete = (self.end_time - self.start_time)/60/60
                self.Graph()
                self.completed_experiments()
                time.sleep(0.1)
                self.push_completed()


    def get_experiment_que(self):
        experiments = pd.read_csv(os.path.join(self.git_dir,self.file_name), index_col=None)
        return experiments

    def save_experiment_que(self):
        os.path.join(os.getcwd(), 'Experiment_Status', 'Experiment-Status')
        self.experiments.to_csv(os.path.join(self.git_dir,self.file_name), index=False)
        return

    def load_experiment(self):
        of = {'PCE': PCE,'PCE_COST': PCE_COST}
        if self.experiments.empty == False:
            experiment = self.experiments.iloc[[0]]
        else:
            print("All experiments complete!")
            return
        experiment = experiment.dropna(axis=1)
        experiment = experiment.to_dict('records')[0]
        self.experiment_name = experiment['experiment_name']
        for param in experiment.items():
            key = param[0]
            value = param[1]
            if '[' in str(value):
                value = literal_eval(value)
                experiment[key] = value
            elif 'objective_function' == key:
                experiment[key] = of[value]
        return experiment

    def get_completed_experiments(self):
        self.completed = pd.read_csv(os.path.join(self.git_dir,'Completed_Experiments.csv'), index_col=None)

    def completed_experiments(self):
        self.completed = pd.concat([self.completed, self.experiments.iloc[[0]]])
        self.experiments = self.experiments.drop(axis=0, index=self.experiments.index[0])
        self.completed.to_csv(os.path.join(self.git_dir,'Completed_Experiments.csv'),index=False)
        self.save_experiment_que()

    def test_new_experiments(self):
        existing = self.experiments['experiment_name'].isin(self.completed['experiment_name']).astype(int)
        existing = np.sum(existing.to_numpy())
        if existing != 0:
            print('Experiments have already been completed!')
            return 0
        else:
            return 1

    def Graph(self):
        Intra.graph_optimisation(self.git_dir, os.path.join(self.git_dir, str(self.experiment_name)+'.exp'))
        return

    def clone_remote(self):
        Repo.clone_from('https://github.com/CaiWilliamsDurham/Experiment-Status.git', self.git_dir)

    def pull_remote(self):
        repo = git.Repo(self.git_dir)
        o = repo.remotes.origin
        o.pull()

    def push_completed(self):
        #try:
        repo = Repo(self.git_dir)
        #files = ['C:\\GA\\Experiment_Status\\Experiment-Status\Completed_Experiments.csv','C:\\GA\Experiment_Status\\Experiment-Status\Queued_Experiments.csv']
        files = os.listdir(self.git_dir)[1:]
        files = [os.path.join(self.git_dir, file) for file in files]
        commit_message = 'Experiment complete it %.2f hrs' % (self.time_to_complete)
        repo.index.add(files)
        repo.index.commit(commit_message)
        repo.git.push('origin','main')
        #except:
        #    print(' Some error occurred! :( ')
        return

Jobs('Queued_Experiments.csv')