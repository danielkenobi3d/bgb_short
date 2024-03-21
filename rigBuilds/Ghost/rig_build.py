from bgb_short.rigBuilds.Ghost.rig_ghost import rig_body
import importlib
import pymel.core as pm
importlib.reload(rig_body)

def custom_rig():
    rig_biped = rig_body.RigByped()
    rig_biped.build()

    pm.rename('GHOST_grp', 'GHOST_GEO_GRP')
    pm.parent('GHOST_GEO_GRP', 'rig')
    pm.parent('environment', 'rig')
