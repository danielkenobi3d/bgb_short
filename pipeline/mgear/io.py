from mgear.shifter import io
from bgb_short.pipeline import environment
import importlib
from mgear.shifter import guide_manager
import pymel.core as pm
from pathlib import Path

importlib.reload(environment)


def export_template():
    pm.select('guide')
    granny = environment.Environment()
    io.export_guide_template(f'{granny.data}/guides.json')


def import_template():
    granny = environment.Environment()
    file_path = Path(f'{granny.data}/guides.json')
    if file_path.exists():
        io.import_guide_template(f'{granny.data}/guides.json')
    else:
        print(f'no guides template found at path {file_path}')


def build_from_data_guides():
    granny = environment.Environment()
    file_path = Path(f'{granny.data}/guides.json')
    if file_path.exists():
        io.import_guide_template(f'{granny.data}/guides.json')
    else:
        print(f'no guides template found at path {file_path}')


def build_template():
    # granny = environment.Environment()
    if pm.ls('guide'):
        pm.select('guide')
        guide_manager.build_from_selection()
    else:
        print('no guide found on the scene')



if __name__ == '__main__':
    import_template()
    build_template()