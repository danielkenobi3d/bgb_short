from bgb_short.rigBuilds.Ghost.rig_ghost import rig_body
import importlib
importlib.reload(rig_body)

def custom_rig():
    rig_biped = rig_body.RigByped()
    rig_biped.build()
