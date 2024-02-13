from RMPY.rig import rigLaceRing
from RMPY.rig import rigBase
from RMPY.rig import rigSplineIK
from RMPY.rig import rigFK
from RMPY.rig import rigSinFunction
import importlib
importlib.reload(rigSplineIK)
importlib.reload(rigLaceRing)
import pymel.core as pm


class RigSpineModel(rigBase.BaseModel):
    def __init__(self):
        self.rig_lace_base = None
        self.rig_spline_ik = None
        self.rig_sin = None
        self.rig_fk = None
        self.offset_groups_list = None


class RigSpine(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spine_points = pm.ls('C_spine00_reference_grp')[0].getChildren()
        self.spine_base_points = pm.ls('C_spineLace00_reference_grp')[0].getChildren()
        self.build()

    def build(self):
        self._model.rig_lace_base = rigLaceRing.LaceRing(self.rig_system)
        self.rig_lace_base.create_point_base(*self.spine_base_points, centered=True,
                                             create_path_surface=True,
                                             joint_number=0, nurbs_to_poly_output=True)

        self._model.rig_spline_ik = rigSplineIK.RigSplineIK(rig_system=self.rig_system)
        self.rig_spline_ik.create_curve_base(self.rig_lace_base.lace_rig.curve, equidistant_points=True,
                                             number_of_joints=40, create_up_vectors=True)
        pm.disconnectAttr(self.rig_spline_ik.reset_controls[0].rotateX)
        pm.disconnectAttr(self.rig_spline_ik.reset_controls[0].rotateY)
        pm.disconnectAttr(self.rig_spline_ik.reset_controls[0].rotateZ)
        pm.disconnectAttr(self.rig_spline_ik.reset_controls[1].rotateX)
        pm.disconnectAttr(self.rig_spline_ik.reset_controls[1].rotateY)
        pm.disconnectAttr(self.rig_spline_ik.reset_controls[1].rotateZ)
        self.rig_spline_ik.reset_controls[0].rotateX.set(90)
        self.rig_spline_ik.reset_controls[1].rotateX.set(90)

        self._model.rig_sin = rigSinFunction.RigSinFunction(rig_system=self.rig_system)
        self._model.offset_groups = self.create.group.point_base(*self.rig_lace_base.controls)
        self.rig_sin.create_point_base(*self.offset_groups)
        self._model.rig_fk = rigFK.RigFK()
        self.rig_fk.create_point_base(*self.spine_points, orient_type='point_orient')
        pm.skinCluster(self.rig_fk.joints, self.rig_lace_base.geometry_output)
        self.root = self.rig_fk.root
        pm.addAttr(self.rig_fk.controls[0], ln='amplitud', proxy=self.rig_spline_ik.rig_system.settings.amplitud)
        pm.addAttr(self.rig_fk.controls[0], ln='phase', proxy=self.rig_spline_ik.rig_system.settings.phase)
        pm.addAttr(self.rig_fk.controls[0], ln='wave_length', proxy=self.rig_spline_ik.rig_system.settings.wave_length)
        pm.addAttr(self.rig_fk.controls[0], ln='decay', proxy=self.rig_spline_ik.rig_system.settings.decay)
        pm.addAttr(self.rig_fk.controls[0], ln='decay_limit', proxy=self.rig_spline_ik.rig_system.settings.decay_limit)
        self.rig_fk.controls[0].amplitud.set(0)
        self.rig_fk.controls[0].phase.set(12)
        self.rig_fk.controls[0].wave_length.set(1.5)
        self.rig_fk.controls[0].decay.set(10)
        self.rig_fk.controls[0].decay_limit.set(4)




if __name__ == '__main__':
    RigSpine()




