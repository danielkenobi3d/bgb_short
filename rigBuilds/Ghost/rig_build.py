from bgb_short.rigBuilds.Ghost.rig_ghost import rig_body
import importlib
import pymel.core as pm
importlib.reload(rig_body)
from bgb_short.pipeline import environment
from RMPY.creators import blendShape
from RMPY.rig import rigFacial
from RMPY.rig import rigHierarchy
def create_facial_rig():
    env = environment.Environment()
    facial_definition = env.get_variables_from_path(environment.pipe_config.facial_definition)
    rigFacial.RigFacial(facial_definition.definition,
                        prefix_geometry_list=facial_definition.prefix_geometry_list)

    for each in facial_definition.direct_blendshape:
        static_connection(each, facial_definition.direct_blendshape[each])


def static_connection(source, destination):
    destination_bs = blendShape.BlendShape.by_node(destination)
    destination_bs.add_as_target(source)
    rig_hierarchy = rigHierarchy.RigHierarchy()
    pm.parent(source, rig_hierarchy.geometry)
    pm.setAttr('{}.visibility'.format(source), False)

def custom_rig():
    rig_biped = rig_body.RigByped()
    rig_biped.build()
    create_facial_rig()
    pm.rename('GHOST_grp', 'GHOST_GEO_GRP')
    pm.parent('GHOST_GEO_GRP', 'rig')
    pm.parent('environment', 'rig')
