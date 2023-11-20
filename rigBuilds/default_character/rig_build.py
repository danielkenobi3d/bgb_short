from bgb_short.pipeline import environment
from bgb_short.pipeline.mgear import io
from RMPY.core import data_save_load
from RMPY.core import search_hierarchy
import pymel.core as pm
import importlib
from pathlib import Path
from bgb_short.rigBuilds.default_character import rig_facial


def import_geometry():
    env = environment.Environment()
    pm.importFile(env.get_latest_version(modelling=True))


def import_guides():
    io.import_template()


def import_reference_points():
    for each in data_save_load.available_maya_files():
        data_save_load.import_maya_file(each)


def facial_rig():
    rig_facial.build()


def build_rig():
    io.build_template()


def custom_rig():
    pass


def load_skinning_data():
    env = environment.Environment()
    root_node = pm.ls('*_GEO_GRP')[0]
    print(root_node)
    list_of_objects = search_hierarchy.shape_type_in_hierarchy(root_node)
    for each in list_of_objects:
        if Path(f'{env.data}/skinClusters/{each}.json').exists():
            data_save_load.load_skin_cluster(each)


def load_shapes_data():
    env = environment.Environment()
    controls = pm.ls('*_ctl')
    for each in controls:
        if Path(f'{env.data}/nurbsCurves/{each}.json').exists():
            data_save_load.load_curves(*controls)


def cleanup():
    pass


def custom_finalize():
    pass


if __name__ == '__main__':
    import_reference_points()


