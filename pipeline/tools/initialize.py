import importlib
from bgb_short.pipeline import pipe_config
from bgb_short.pipeline import environment
import os
import pkgutil
importlib.reload(pipe_config)
importlib.reload(environment)


asset_module = importlib.import_module(f'{pipe_config.modules_path}{environment.Environment().asset}')

if inherit in vars(asset_module):
    default_module = importlib.import_module(f'{pipe_config.modules_path}{asset_module.inherit}')
else:
    default_module = importlib.import_module(f'{pipe_config.modules_path}{pipe_config.default_module}')

print(os.listdir(default_module.__path__[0]))
print(pkgutil.iter_modules(default_module))
build_config_file = None
for each in pkgutil.iter_modules(default_module.__path__):
    if not each.ispkg:
        if each.name.split('_')[-1] == 'config':
            build_config_file = importlib.import_module(f'{default_module}{each}')

for each in build_config_file.build_order:
    build_config_file.build[each]












