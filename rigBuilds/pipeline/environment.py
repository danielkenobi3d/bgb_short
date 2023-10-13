import os
from pathlib import Path
class Environment(object):
    def __init__(self):

        self.project_path = 'Z:\\06-CLASSE ANIMATION M2\\PROJET-BGB'
        self.asset_path = '\\01_CHARACTER\\002_GRANNY'
        self.model_path = '\\003_MODEL\\01_CHARACTER'
        self.rig_path = '\\005_RIG'
        self.data_paht = '\\data'

    @property
    def model(self):
        return Path("{}{}{}".format(self.project_path, self.asset_path, self.model_path))

if __name__=='__main__':
    granny = Environment()
    print(os.listdir(granny.model))





