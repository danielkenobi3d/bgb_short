from REF.asset.babyK import facial_rig_definition
from RMPY.rig import rigFacial
from RMPY.rig import rigBlendShapeControls
import pymel.core as pm
from RMPY.rig import rigSingleJoint
from RMPY.rig import rigStaticLayer
from RMPY.rig.switches import rigFloatSwitch
from RMPY.core import rig_core
reload(rigSingleJoint)


def build():
    static_layer_face()
    static_body()


def static_layer_face():
    root_points = pm.ls('C_lip_static_grp')[0]
    single_joint_rig = rigSingleJoint.RigSingleJoint()
    for each in root_points.getChildren():
        single_joint_rig.create_point_base(each, static=True, type='circular')
        if 'upperLip' in str(each):
            single_joint_rig.create.constraint.node_base('C_joint00_head_sknjnt', single_joint_rig.reset_controls[-1],
                                                         mo=True)
        else:
            single_joint_rig.create.constraint.node_base('C_joint00_jaw_sknjnt', single_joint_rig.reset_controls[-1],
                                                         mo=True)
    single_joint_rig.zero_joint
    geometries = [u'character', u'lowRez']
    static_layer = rigStaticLayer.StaticLayer(*geometries, name='lipLayer')


def static_body():
    root_points = pm.ls('C_body00_reference_grp')[0]
    single_joint_rig = rigSingleJoint.RigSingleJoint()
    for each_root in root_points.getChildren():
        print (each_root.getChildren())
        single_joint_rig.create_point_base(*each_root.getChildren(), static=True, type='circular')
    single_joint_rig.zero_joint

    single_joint_rig.create.constraint.node_base('C_forwardFK03_Spine_jnt', single_joint_rig.rig_system.controls, mo=True)
    geometries = [u'BabyK_body_lvl1', u'BabyK_body_lvl2', u'C_shortDress_cloth_msh']
    rigStaticLayer.StaticLayer(*geometries, name='staticBreast')


if __name__ == '__main__':
    static_body()

