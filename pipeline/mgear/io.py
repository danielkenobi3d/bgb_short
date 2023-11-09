from mgear.shifter import io
from bgb_short.pipeline import environment
import importlib
from mgear.shifter import guide_manager
import pymel.core as pm

importlib.reload(environment)


def export_template():
    pm.select('guide')
    granny = environment.Environment()
    io.export_guide_template(f'{granny.data}/guides.json')


def import_template():
    granny = environment.Environment()
    io.import_guide_template(f'{granny.data}/guides.json')


def build_from_data_guides():
    granny = environment.Environment()
    io.import_guide_template(f'{granny.data}/guides.json')


def build_template():
    # granny = environment.Environment()
    pm.select('guide')
    guide_manager.build_from_selection()



if __name__ == '__main__':
    import_template()
    build_template()