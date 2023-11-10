import os
from pathlib import Path
import pymel.core as pm


def filter_right_file(file_list):
    """
    finds the correct file path to import it will import the smallest in length maya file
    :return:
    """
    return_file = None
    file_name_len = 0
    for each in file_list:
        if each.split('.')[-1] in ['mb', 'ma']:
            if return_file == None:
                return_file = each
                file_name_len = len(each)
            else:
                if len(each) < file_name_len:
                    return_file = each
                    file_name_len = len(each)
    return return_file


class Environment(object):
    def __init__(self):
        self.asset_list = ['Grandma', 'Ghost', 'Guardian', 'Rick']
        self._env_node = None
        self._asset = None
        print(f'current_asset: {self.env_node.asset.get()}')
        self._project_path = 'Z:/06-CLASSE ANIMATION M2/Projects/bgb24/04-ASSETS/Characters'
        # 'C:/Users/danie/OneDrive/rubika/shortFilm/assets/'
        self._asset_path = '/bgb24_A_{}'
        self._model_path = '/bgb24_A_{}_Mod'
        self._rig_path = '/bgb24_A_{}_Rig'
        self._data_path = '/data'

    @property
    def model(self):
        return Path("{}{}{}".format(self._project_path, self._asset_path.format(self._asset), self._model_path.format(self._asset)))

    @property
    def rig(self):
        return Path("{}{}{}".format(self._project_path, self._asset_path.format(self._asset), self._rig_path.format(self._asset)))

    @property
    def data(self):
        return Path("{}{}{}{}".format(self._project_path, self._asset_path.format(self._asset), self._rig_path.format(self._asset), self._data_path))
    @property
    def env_node(self):
        if pm.ls('environment'):
            self._env_node = pm.ls('environment')[0]
            self._asset = self._env_node.asset.get()
        else:
            self._env_node = pm.group(empty=True, name='environment')
            pm.addAttr(self._env_node, ln='asset', type='string')
            if not self._asset:
                self._asset = self.asset_list[0]
            self._env_node.asset.set(self._asset, type='string')
        return self._env_node

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, asset_value):
        if asset_value in self.asset_list:
           self._asset = asset_value
           self.env_node.asset.set(asset_value)
        else:
            print(f'not  valid asset {asset_value}, needs to be inside {self.asset_list}')
    def get_latest_version(self, modelling=False, rigging=False):
        if modelling == True:
            list_of_publish_dir = os.listdir(f'{self.model}/_published')
        elif rigging == True:
            list_of_publish_dir = os.listdir(f'{self.rig}/_published')
        else:
            list_of_publish_dir = os.listdir(f'{self.model}/_published')

        latest_version_folder = None
        index = 0
        for each in list_of_publish_dir:
            if not latest_version_folder:
                latest_version_folder = each
                index = int(each[0:3])
            else:
                current_index = int(each[0:3])
                if current_index > index:
                    index = current_index
                    latest_version_folder = each
        files_list = os.listdir(f'{self.model}/_published/{latest_version_folder}')
        return Path(f'{self.model}/_published/{latest_version_folder}/{filter_right_file(files_list)}')


if __name__ == '__main__':
    granny = Environment()
    print(granny.data)
    print(granny.model)
    print(granny.rig)
    print(granny.get_latest_version(modelling=True))




