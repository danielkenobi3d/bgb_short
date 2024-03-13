from RMPY.rig import rigSingleJoint
from RMPY.rig import rigProp
from RMPY.rig import rigStaticLayer


simple_rig = rigSingleJoint.RigSingleJoint()
simple_rig.create_point_base('C_backpackSmallStrapMain00_reference_pnt', centered=True, size=.5, static=True)
simple_rig.zero_joint
simple_rig.set_parent('BP_strip_grp_ctrl')
static_geo_rig = rigStaticLayer.StaticLayer('R_belt_001_HIGH')
