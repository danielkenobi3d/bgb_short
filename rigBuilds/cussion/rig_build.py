from RMPY.rig import rigSingleJoint


def custom_rig():
    Lcreation_points = ['L_cussion00_reference_pnt', 'L_cussion01_reference_pnt', 'L_cussion02_reference_pnt']
    Ccreation_points = ['C_cussion00_reference_pnt', 'C_cussion01_reference_pnt', 'C_cussion02_reference_pnt']
    Rcreation_points = ['R_cussion00_reference_pnt', 'R_cussion01_reference_pnt', 'R_cussion02_reference_pnt']
    rig_bits = rigSingleJoint.RigSingleJoint()
    rig_bits.create_point_base(*Ccreation_points, type='circular', size=.5)
    rig_bits.create_point_base(*Lcreation_points, type='circular', size=.5)
    rig_bits.create_point_base(*Rcreation_points, type='circular', size=.5)

    main_rig = rigSingleJoint.RigSingleJoint()
    main_rig.create_point_base('C_mainCussion_reference_pnt', centered=True, size=4)
    rig_bits.set_parent(main_rig)

