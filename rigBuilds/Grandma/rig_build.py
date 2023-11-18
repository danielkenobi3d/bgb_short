from bgb_short.pipeline import environment
from bgb_short.pipeline.mgear import io
import pymel.core as pm
import importlib
importlib.reload(environment)
importlib.reload(io)


def import_geometry():
    env = environment.Environment()
    pm.importFile(env.get_latest_version(modelling=True))


def import_guides():
    io.import_template()


def build_rig():
    io.build_template()


def custom_rig():
    pass


def cleanup():
    pass


def custom_finalize():
    pass

if __name__ == '__main__':
    import_geometry()


