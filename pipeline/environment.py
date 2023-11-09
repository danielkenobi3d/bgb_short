import os
from pathlib import Path


class Environment(object):
    def __init__(self):
        self.asset_list = ['002_GRANNY']
        self._asset = self.asset_list[0]
        self.project_path = 'C:/Users/danie/OneDrive/rubika/shortFilm/assets/'
        # 'Z:\\06-CLASSE ANIMATION M2\\PROJET-BGB'
        self.asset_path = '\\01_CHARACTER\\{}'
        self.model_path = '\\003_MODEL'
        self.rig_path = '\\005_RIG'
        self.data_path = '\\data'

    @property
    def model(self):
        return Path("{}{}{}".format(self.project_path, self.asset_path, self.model_path))

    @property
    def rig(self):
        return "{}{}{}".format(self.project_path, self.asset_path, self.rig_path)

    @property
    def data(self):
        return Path("{}{}{}{}".format(self.project_path, self.asset_path.format(self._asset), self.rig_path, self.data_path))

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, asset_value):
        if asset_value in self.asset_list:
           self._asset = asset_value

        else:
            print(f'not  valid asset {asset_value}, needs to be inside {self.asset_list}')





if __name__ == '__main__':
    granny = Environment()
    print(os.listdir(granny.rig))





