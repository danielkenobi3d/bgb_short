from RMPY.rig import rigSingleJoint
import pymel.core as pm


selection = pm.ls(selection=True)
rig_joint = rigSingleJoint.RigSingleJoint()
rig_joint.create_point_base(*selection)

