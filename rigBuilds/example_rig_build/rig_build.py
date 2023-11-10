from RMPY.rig.biped import rigBiped
from RMPY.rig import rigHierarchy
from RMPY.core import controls
from RMPY.core import data_save_load
import pymel.core as pm
from RMPY.rig.switches import rigBoolSwitch
from RMPY.rig.switches import rigEnumSwitch
from REF.asset.babyK import rig_facial
from REF.asset.babyK import rig_correctives

from RMPY.core import rig_core
from REF.asset.babyK import rig_static
from RMPY.creators import blendShape


def build():
    load_sources()
    build_rig()
    hierarchy()
    load_data()
    finalize()


def load_sources():
    data_save_load.import_all_available_maya_files()


def build_rig():
    rig_biped = rigBiped.RigByped()
    rig_biped.build()
    rig_static.build()
    rig_facial.build()
    viz_switch_lods()
    visibility_switch()
    rig_correctives.build()
    controls.color_now_all_ctrls()
    lock_attributes()
    prepare_for_spaceswitch()


def hide_rigs():
    settings_rig_sistems = pm.ls('*_settings*_pnt')
    for each in settings_rig_sistems:
        each.visibility.set(False)


def hierarchy():
    # enum_switch = rigEnumSwitch.RigEnumSwitch(control='C_settings00_world_ctr', attribute_name='lock_geometry')
    # enum_switch.add_enum_names('Normal', 'Template','Reference',  attribute_name='sphereCube')
    rig_hierarchy = rigHierarchy.RigHierarchy()
    pm.parent('BabyK_GRP', rig_hierarchy.geometry)

    settings_ctr = pm.ls('C_settings00_world_ctr')[0]
    pm.addAttr('C_settings00_world_ctr', ln='geometry_display', at='enum', k=True, enumName=['Normal', 'Template','Reference'])
    rig_hierarchy.geometry.overrideEnabled.set(1)
    pm.connectAttr('C_settings00_world_ctr.geometry_display', rig_hierarchy.geometry.overrideDisplayType)
    settings_ctr.geometry_display.set(2)


def visibility_switch():
    # bool_switch = rigBoolSwitch.RigBoolSwitch(control='C_settings00_world_ctr', attribute_name='low_high_rez')
    # for each in pm.ls(u'BabyK_body_lvl1', u'CaruncleCombined_lvl2', u'nails_lvl1'):
    #     bool_switch.attribute_output >> each.visibility
    # for each in pm.ls(u'BabyK_body_lvl2', u'CaruncleCombined_lvl3', u'nails_lvl2'):
    #     bool_switch.attribute_output_false >> each.visibility

    secondary_controls_visibility = rigBoolSwitch.RigBoolSwitch(control='C_settings00_world_ctr',
                                                                attribute_name='secondaryControls')
    for each in {u'L_bendy00_shoulder_grp', u'L_bendy01_shoulder_grp', u'L_bendy02_shoulder_grp',
                 u'L_bendy03_shoulder_grp', u'L_bendy04_shoulder_grp', u'L_bendy05_shoulder_grp',
                 u'R_bendy00_shoulder_grp', u'R_bendy01_shoulder_grp', u'R_bendy02_shoulder_grp',
                 u'R_bendy03_shoulder_grp', u'R_bendy04_shoulder_grp', u'R_bendy05_shoulder_grp',
                 u'L_bendy00_leg_grp',
                 u'L_bendy01_leg_grp', u'L_bendy02_leg_grp', u'L_bendy03_leg_grp', u'L_bendy04_leg_grp',
                 u'L_bendy05_leg_grp', u'L_twistOrigin00_leg_grp', u'L_twistOrigin01_leg_grp',
                 u'R_twistOrigin00_leg_grp', u'R_bendy00_leg_grp', u'R_bendy01_leg_grp', u'R_bendy02_leg_grp',
                 u'R_twistOrigin01_leg_grp', u'R_bendy03_leg_grp', u'R_bendy04_leg_grp', u'R_bendy05_leg_grp',
                 u'R_twistOrigin00_clavicle_grp', u'R_twistOrigin00_shoulder_grp', u'L_twistOrigin00_clavicle_grp',
                 u'L_twistOrigin00_shoulder_grp'}:
        secondary_controls_visibility.attribute_output >> pm.ls(each)[0].visibility

    static_controls_visibility = rigBoolSwitch.RigBoolSwitch(control='C_settings00_world_ctr',
                                                             attribute_name='staticControls')

    for each in {'C_controls00_lowLip_grp', 'R_controls00_breastStatic_grp'}:
        static_controls_visibility.attribute_output >> pm.ls(each)[0].visibility



def load_data():
    controls_list = pm.ls('*ctr')
    data_save_load.load_curves(*controls_list)

    geometry = pm.ls(u'BabyK_body_lvl1', u'BabyK_body_lvl2', u'CaruncleCombined_lvl2', u'CaruncleCombined_lvl3',
                     u'L_EyeWet', u'R_EyeWet', u'Teeth', u'Dentine', u'Tongue', u'Gums', u'nails_lvll', u'nails_lvl2',
                     u'C_character00_mouthClosed_msh', u'C_character00_mouthOpen_msh',
                     u'L_Sclera_lvl1', u'L_Sclera_lvl2', u'L_pupill', u'L_Iris', u'R_sclera_lvl1', u'R_Sclera_lvl2',
                     u'R_pupill', u'R_Iris', u'L_caruncle', u'R_caruncle', u'toenails_lvl2',
                     u'C_lowRez00_mouthOpen_msh', u'C_Teeth00_mouthOpen_msh', u'C_Dentine00_mouthOpen_msh',
                     u'C_Tongue00_mouthOpen_msh', u'C_Gums00_mouthOpen_msh', u'C_lowRez00_mouthClosed_msh',
                     u'C_Teeth00_mouthClosed_msh', u'C_Dentine00_mouthClosed_msh', u'C_Tongue00_mouthClosed_msh',
                     u'C_Gums00_mouthClosed_msh', u'L_Tacco_15highHeels_msh', u'R_Tacco_15highHeels_msh',
                     u'C_character00_lipLayer_msh', u'C_lowRez00_lipLayer_msh', u'C_BabyK01_staticBreast_msh',
                     u'C_BabyK00_staticBreast_msh' u'C_cloth00_staticBreast_msh', u'C_shortDress_cloth_msh',
                     u'C_Tacco_12highHeels_msh', u'nails_lvl1'
                     )
    data_save_load.load_skin_cluster(*geometry)


def cleanup():
    delete_objects = []
    for each in pm.ls('|*'):
        if each.name() != 'rig':
            if each.getShape():
                if pm.objectType(each.getShape()) != 'camera':
                    delete_objects.append(each)
            else:
                delete_objects.append(each)
    pm.delete(delete_objects)


def finalize():
    cleanup()
    set_default_pose()
    hide_rigs()

    for source, destination in zip(['C_BabyKBreastsUP_low_BS', 'C_BabyKBreastsUP_high_BS',
                                    'C_BabyK_heels_Low_BS', 'C_BabyK_heels_high_BS',
                                    'C_BabyKToenails_high_BS'
                                    ],
                                   ['BabyK_body_lvl1', 'BabyK_body_lvl2',
                                    'BabyK_body_lvl1', 'BabyK_body_lvl2',
                                    'toenails_lvl2']):
        destination_bs = blendShape.BlendShape.by_node(destination)
        destination_bs.add_as_target(source)
    # pm.delete('C_reference_points_pnt')
    # pm.delete('measures_ref_grp')


def viz_switch_lods():
    rig_enum_names = rigEnumSwitch.RigEnumSwitch(control='C_settings00_world_ctr')
    rig_enum_names.add_enum_names('High', 'Low', attribute_name='geo_lod')
    for each in pm.ls(u'BabyK_body_lvl2', u'CaruncleCombined_lvl3', u'nails_lvl2'):
        rig_enum_names.switch['High'].attribute_output >> each.visibility
    for each in pm.ls(u'BabyK_body_lvl1', u'CaruncleCombined_lvl2', u'nails_lvl1'):
        rig_enum_names.switch['Low'].attribute_output >> each.visibility

    # pm.connectAttr('C_object01_mouthClosed_UDF.output', 'C_reverse105_rig_rvs.inputX')


def lock_attributes():
    only_rotate = {u'C_joint00_head_ctr', u'L_joint00_shoulder_ctr', u'L_joint01_shoulder_ctr',
                   u'R_joint00_shoulder_ctr', u'R_joint01_shoulder_ctr', u'R_object00_palm_ctr', u'L_object00_palm_ctr',
                   u'R_joint00_leg_ctr', u'R_joint01_leg_ctr', u'L_joint00_leg_ctr', u'L_joint01_leg_ctr',
                   u'R_joint00_ankleFeet_ctr', u'L_joint00_ankleFeet_ctr', u'L_joint01_ankleFeet_ctr',
                   u'R_joint01_ankleFeet_ctr'}
    rig_core.lock_and_hide_attributes(*only_rotate, bit_string='0001110000')
    nothing = [u'L_root00_shoulder_ctr', u'R_root00_shoulder_ctr', u'R_root00_leg_ctr', u'L_root00_leg_ctr']
    rig_core.lock_and_hide_attributes(*nothing, bit_string='0000000000')


def set_default_pose():
    pm.setAttr('L_object01_dynamicBreast_ctr.jiggle', 0.05)
    pm.setAttr('R_object01_dynamicBreast_ctr.jiggle', 0.05)
    pm.setAttr('C_joint00_jaw_ctr.cornersFollow', 0.5)
    pm.setAttr('C_joint00_jaw_ctr.lipSeal', 10)


def prepare_for_spaceswitch():
    for side in 'LR':
        ankle_fk = pm.ls('{}_joint00_ankleFeet_ctr'.format(side))[0]
        switch_locator = pm.spaceLocator(name='{}_jointIK00_leg_loc'.format(side))
        switch_locator.setParent(ankle_fk)
        pm.matchTransform(switch_locator, '{}_jointIK00_leg_ctr'.format(side))
        switch_locator.visibility.set(False)


if __name__ == '__main__':
    build()
    # load_sources()
    # build_rig()
    # hierarchy()
    # load_data()
    # finalize()
