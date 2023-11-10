from REF.asset.babyK import facial_rig_definition
from RMPY.rig import rigFacial
from RMPY.rig import rigBlendShapeControls
import pymel.core as pm
from RMPY.rig import rigHierarchy
from RMPY.rig import rigStaticLayer
from RMPY.rig.switches import rigFloatSwitch
from RMPY.core import rig_core
from RMPY.creators import blendShape
reload(facial_rig_definition)


def build():
    create_facial_rig()
    create_jaw_layers()


def create_facial_rig():
    facial_controls = rigBlendShapeControls.RigBlendShapeControls(root='C_facialControls_reference_pnt')
    rigFacial.RigFacial(facial_rig_definition.definition, prefix_geometry_list=['lowRez', 'LeyeWet', 'ReyeWet', 'caruncle'])
    rigFacial.RigFacial(facial_rig_definition.eyes_dict, prefix_geometry_list=['lowRez', 'LeyeWet', 'ReyeWet', 'caruncle'])
    rigFacial.RigFacial(facial_rig_definition.correctives_dict)
    pm.parentConstraint('C_joint00_head_sknjnt', facial_controls.rig_system.controls, mo=True)
    pm.scaleConstraint('C_joint00_head_sknjnt', facial_controls.rig_system.controls, mo=True)
    pm.setAttr('character.visibility', False)
    static_connection('character', 'BabyK_body_lvl2')
    static_connection('lowRez', 'BabyK_body_lvl1')
    static_connection('LeyeWet', 'L_EyeWet')
    static_connection('ReyeWet', 'R_EyeWet')
    static_connection('caruncle', 'CaruncleCombined_lvl3')

def static_connection(source, destination):
    destination_bs = blendShape.BlendShape.by_node(destination)
    destination_bs.add_as_target(source)

    rig_hierarchy = rigHierarchy.RigHierarchy()
    pm.parent(source, rig_hierarchy.geometry)
    pm.setAttr('{}.visibility'.format(source), False)


def create_jaw_layers():
    geometries = [u'character', u'lowRez', u'Teeth', u'Dentine', u'Tongue', u'Gums']
    static_layer = rigStaticLayer.StaticLayer(*geometries, name='mouthOpen')
    mouth_close = rigStaticLayer.StaticLayer(*geometries, name='mouthClosed', rig_system=static_layer.rig_system)

    float_switch = rigFloatSwitch.FloatSwitch(control='C_joint00_jaw_ctr', attribute_name='lipSeal')

    for index, each_geo in enumerate(geometries):
        blend_shape = rig_core.BlendShape.by_node(each_geo)
        float_switch.attribute_output >> pm.Attribute('{}.{}'.format(blend_shape.node, static_layer.static_geometries[index]))
        float_switch.attribute_output_false >> pm.Attribute('{}.{}'.format(blend_shape.node, mouth_close.static_geometries[index]))


if __name__ == '__main__':
    # build()
    rigFacial.RigFacial(facial_rig_definition.definition, prefix_geometry_list=['lowRez', 'LeyeWet', 'ReyeWet'])
    # create_facial_rig()
    # float_switch = rigFloatSwitch.FloatSwitch(control='C_joint00_jaw_ctr', attribute_name='lipSeal')
    # float_switch.attribute_output >> pm.Attribute('blendShape1.{}'.format('C_character00_mouthOpen_msh'))
    # float_switch.attribute_output_false >> pm.Attribute('blendShape1.{}'.format('C_character00_mouthClosed_msh'))
    # rigFacial.RigFacial(facial_rig_definition.eyes_dict)

