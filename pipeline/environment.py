import os
from pathlib import Path
import pymel.core as pm
import importlib
import pkgutil

try:
    import pipe_config
except:
    from bgb_short.pipeline import pipe_config

importlib.reload(pipe_config)
def filter_right_file(file_list):
    """
    finds the correct file path to import it will import the smallest in length maya file
    :return:
    """
    return_file = None
    file_name_len = 0
    for each in file_list:
        if each.split('.')[-1] in ['mb', 'ma']:
            if return_file is None:
                return_file = each
                file_name_len = len(each)
            else:
                if len(each) < file_name_len:
                    return_file = each
                    file_name_len = len(each)
    return return_file


class ModuleSplit(object):
    # A very simple class to split the mudles and the function on a path.
    # it accepts a full path for example rig_build.character.build_rig
    # and splits this in to module: rig_build.character
    # and function: build_rig
    def __init__(self, name_function):
        self.tokens = name_function.split('.')

    @property
    def modules(self):
        return '.'.join(self.tokens[:-1])

    @property
    def variable(self):
        return self.tokens[-1]


class Environment(object):
    asset_module = None
    inherit_module = None
    build_config_file = None

    def __init__(self):
        super().__init__()
        self.asset_list = pipe_config.asset_list
        self._env_node = None
        self._asset = None
        self._project_path = pipe_config.project_path
        self._asset_path = pipe_config.asset_path
        self._model_path = pipe_config.model_path
        self._rig_path = pipe_config.rig_path
        self._publish_folder = pipe_config.publish_folder
        self._data_path = pipe_config.data_path



    @property
    def model(self):
        return Path("{}{}{}".format(self._project_path, self._asset_path.format(self.asset), self._model_path.format(self.asset)))

    @property
    def rig(self):
        return Path("{}{}{}".format(self._project_path, self._asset_path.format(self.asset), self._rig_path.format(self.asset)))

    @property
    def data(self):
        return Path("{}{}{}{}".format(self._project_path, self._asset_path.format(self.asset), self._rig_path.format(self.asset), self._data_path))

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
        return self.env_node.asset.get()

    @asset.setter
    def asset(self, asset_value):
        if asset_value in self.asset_list:
           self._asset = asset_value
           self.env_node.asset.set(asset_value)
        else:
            print(f'not  valid asset {asset_value}, needs to be inside {self.asset_list}')

    def get_latest_version(self, modelling=False, rigging=False):
        if modelling == True:
            list_of_publish_dir = os.listdir(f'{self.model}{self._publish_folder}')
        elif rigging == True:
            list_of_publish_dir = os.listdir(f'{self.rig}{self._publish_folder}')
        else:
            list_of_publish_dir = os.listdir(f'{self.model}{self._publish_folder}')
        print(f'loading {list_of_publish_dir}')
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
        files_list = os.listdir(f'{self.model}{self._publish_folder}/{latest_version_folder}')
        return Path(f'{self.model}{self._publish_folder}/{latest_version_folder}/{filter_right_file(files_list)}')
    
    def import_environment_modules(self):
        self.asset_module = importlib.import_module(f'{pipe_config.modules_path}.{self.asset}')

        if 'inherit' in vars(self.asset_module):
            self.inherit_module = importlib.import_module(f'{pipe_config.modules_path}.{self.asset_module.inherit}')
        else:
            self.inherit_module = importlib.import_module(f'{pipe_config.modules_path}.{pipe_config.default_module}')

        importlib.reload(self.asset_module)
        importlib.reload(self.inherit_module)
        self.build_config_file = None
        for each in pkgutil.iter_modules(self.asset_module.__path__):
            if not each.ispkg:
                if each.name.split('_')[-1] == 'config':
                    self.build_config_file = importlib.import_module(f'{self.asset_module.__name__}.{each.name}')
        if not self.build_config_file:
            for each in pkgutil.iter_modules(self.inherit_module.__path__):
                if not each.ispkg:
                    if each.name.split('_')[-1] == 'config':
                        self.build_config_file = importlib.import_module(f'{self.inherit_module.__name__}.{each.name}')

        importlib.reload(self.build_config_file)
        return self.asset_module, self.inherit_module, self.build_config_file

    def get_variables_from_path(self, step_function):
        # gets variables from path accepts a string in the form of a path and it is going to return the corresponding variable(function)
        # from the path provided in Context
        self.import_environment_modules()
        function_path = ModuleSplit(step_function)
        print(function_path.modules)
        if function_path.modules:
            try:
                new_module = importlib.import_module(f'{self.asset_module.__name__}.{function_path.modules}')
            except ModuleNotFoundError as e:
                print(f'module not found {e}')
                new_module = importlib.import_module(f'{self.inherit_module.__name__}.{function_path.modules}')
        else:
            try:
                new_module = importlib.import_module(f'{self.asset_module.__name__}.{function_path.variable}')
                return new_module
            except ModuleNotFoundError as e:
                new_module = importlib.import_module(f'{self.inherit_module.__name__}.{function_path.variable}')
                return new_module

        importlib.reload(new_module)
        if function_path.variable in dir(new_module):
            return getattr(new_module, function_path.variable)
        else:
            new_module = importlib.import_module(f'{self.inherit_module.__name__}.{function_path.modules}')
            importlib.reload(new_module)
            if function_path.variable in dir(new_module):
                return getattr(new_module, function_path.variable)
            else:
                print(f'couldnt import function  {function_path.variable}\n'
                      f'from any of this paths {self.asset_module.__name__} {self.inherit_module.__name__}')
                print(dir(self.inherit_module))


if __name__ == '__main__':
    granny = Environment()
    facial_definition = granny.get_variables_from_path('facial_definition')
    print(facial_definition.definition)




