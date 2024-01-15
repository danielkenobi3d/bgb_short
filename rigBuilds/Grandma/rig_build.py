from RMPY.rig import rigSingleJoint
import pymel.core as pm

def custom_rig():
    zipper = rigSingleJoint.RigSingleJoint()
    zipper.create_point_base('C_zipper_reference_pnt')
    zipper.set_parent('neck_C0_1_jnt')

    boobs = rigSingleJoint.RigSingleJoint()
    boobs.create_point_base('L_boob_reference_pnt', 'R_boob_reference_pnt')
    boobs.set_parent('spine_C0_4_jnt')

    belt_root_point = pm.ls('c_belt_points_grp')[0]
    belt = rigSingleJoint.RigSingleJoint()
    belt.create_point_base(*belt_root_point.getChildren())
    belt.set_parent('spine_C0_0_jnt')



def custom_finalize():
    pass


if __name__ == '__main__':
    custom_rig()



