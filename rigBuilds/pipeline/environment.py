import os
from pathlib import Path
class Environment(object):
    def __init__(self, asset_name):
        "Z:\06-CLASSE ANIMATION M2\Projects\bgb24\04-ASSETS\Characters\bgb24_A_Grandma\bgb24_A_Grandma_Mod\bgb24_A_Grandma_Mod.mb"
        self.project_path = 'Z:/06-CLASSE ANIMATION M2/Projects/bgb24/04-ASSETS'
        self.task = {'model': '/bgb24_A_Grandma_Mod',
                     'rig': '/005_RIG/01_CHARACTER',
                     }
        self.asset_path = {'granny': '/Characters/bgb24_A_Grandma'}
        self.data_path = '/data'
        if asset_name in self.asset_path.keys():
            self.asset_name = asset_name
        else:
            raise(InterruptedError(f'not valid asset name {asset_name}'))

    @property
    def model(self):
        return "{}{}{}".format(self.project_path, self.task['model'], self.asset_path[ self.asset_name])
    @property
    def rig(self):
        return "{}{}{}".format(self.project_path, self.task['rig'], self.asset_path[self.asset_name])
    @property
    def data(self):
        return "{}{}{}{}".format(self.project_path, self.task['rig'], self.asset_path[self.asset_name], self.data_path)


if __name__ == '__main__':
    granny = Environment('granny')
    print(os.listdir(granny.rig))





