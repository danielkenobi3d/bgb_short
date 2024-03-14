from RMPY.rig import rigSingleJoint
from RMPY.rig import rigProp
from RMPY.rig import rigStaticLayer
from RMPY.core import data_save_load
from RMPY.rig import rigUVPin
import importlib
import pymel.core as pm
importlib.reload(rigProp)

def build():

    main_backpack = rigProp.RigProp()
    main_backpack.create_point_base('C_backPack00_reference_pnt', centered=True, size=.5, static=True)
    main_backpack.zero_joint

    main_backpack_top = rigProp.RigProp()
    main_backpack_top.create_point_base('C_backPackTop00_reference_pnt', centered=True, size=.5, static=True)

    main_backpack_top.set_parent(main_backpack)
    pm.parentConstraint(main_backpack.joints[-1], main_backpack_top.reset_joints[0], mo=True)


    main_strap_backpack = rigSingleJoint.RigSingleJoint()
    main_strap_backpack.create_point_base('C_backpackSmallStrapMain00_reference_pnt', centered=True, size=.5, static=True)
    main_strap_backpack.set_parent(main_backpack_top)

    for each_child in pm.ls('C_smallStrap00_reference_grp')[0].getChildren():
        small_strap_rig = rigSingleJoint.RigSingleJoint(each_child)
        small_strap_rig.create_point_base(each_child, centered=True, size=.1, static=True)
        small_strap_rig.set_parent(main_strap_backpack)

    for each_strap in pm.ls('L_straps00_reference_grp', 'R_straps00_reference_grp'):
        start = 65
        for each_root_point in each_strap.getChildren():
            strap_rig = rigProp.RigProp()
            strap_rig.create_point_base(each_root_point,name=f'control{chr(start)}', centered=True, size=.3, static=True)
            uv_pin_rig = rigUVPin.RigUVPin(rig_system=strap_rig.rig_system)
            uv_pin_rig.create_point_base(strap_rig.reset_controls[0], geometry='C_shirt_001_HIGH')
            uv_pin_rig.clean_up()
            strap_rig.set_parent(uv_pin_rig)
            start += 1


    # 'C_shirt_001_HIGH'
    # creates the layer geometry rig
    static_geos = ['R_belt_001_HIGH', 'L_belt_001_HIGH', 'L_buckleB_001_HIGH', 'L_buckleA_001_HIGH',
                   'R_buckleA_001_HIGH', 'R_buckleB_001_HIGH', 'C_zipperBaseB_001_HIGH',
                   'C_zipperHandleB_001_HIGH', 'C_zipperBaseA_001_HIGH', 'C_zipperHandleA_001_HIGH',
                   'C_decoration_001_HIGH', 'C_strap_001_HIGH', 'C_bagB_001_HIGH',
                   'C_bagA_001_HIGH', 'C_zipperB_001_HIGH', 'C_zipperA_001_HIGH']
    static_geo_rig = rigStaticLayer.StaticLayer(*static_geos, name='fullBackpackStatic')
    try :
        data_save_load.load_skin_cluster(static_geo_rig.static_geometries)
    except:
        pass

    only_straps_geos = ['R_belt_001_HIGH', 'L_belt_001_HIGH', 'L_buckleB_001_HIGH', 'R_buckleB_001_HIGH']
    static_strap_geo_rig = rigStaticLayer.StaticLayer(*only_straps_geos, name='strapsStatic')
    try:
        data_save_load.load_skin_cluster(static_strap_geo_rig.static_geometries)
    except:
        pass


if __name__=='__main__':
    build()