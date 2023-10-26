from RMPY.rig import rigPistonLace
import pymel.core as pm
build_points = pm.ls('C_grapplinHook*_reference_pnt')
rig_grapplinhook = rigPistonLace.RigPistonLace()
rig_grapplinhook.create_point_base(*build_points, create_piston_controls=True, controls_number = 10, joint_number=30)