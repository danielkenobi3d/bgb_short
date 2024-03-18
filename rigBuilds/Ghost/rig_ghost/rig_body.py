from RMPY.rig.biped.rig import arm
from RMPY.rig.biped.rig import rigForwardBackwardFKSpine
from RMPY.rig.biped.rig import hand
from RMPY.rig import rigFK
from RMPY.rig.biped.rig import rig_jaw
from RMPY.rig import rigWorld
from RMPY.rig.biped.rig import neckHead
from RMPY.rig.biped.rig import rigIKFKLegFeet
from RMPY.rig import rigBase
from RMPY.rig import rigProp
from RMPY.rig.biped.rig import armSpaceSwitch
from RMPY.rig.biped.rig import legSpaceSwitch
from RMPY.rig.biped.rig import handSpaceSwitch
from RMPY.rig.biped.rig import rigEyesAim
from RMPY.rig.biped.rig import rigBreast
from RMPY.rig.biped.rig import rigToes
from RMPY.rig.biped.rig import neckHeadSpaceSwitch
from RMPY.rig.biped.rig import rigEyesSpaceSwitch
from RMPY.rig import rigSingleJoint
from bgb_short.rigBuilds.Ghost.rig_ghost import rigSpine
import importlib
importlib.reload(rigSpine)

class RigBypedModel(rigBase.BaseModel):
    def __init__(self, **kwargs):
        super(RigBypedModel, self).__init__(**kwargs)
        self.l_arm = arm.Arm()
        self.r_arm = arm.Arm()
        self.l_hand = hand.Hand()
        self.r_hand = hand.Hand()
        self.neck_head = neckHead.NeckHead()
        self.cog = rigProp.RigProp()
        self.rig_world = rigWorld.RigWorld()
        self.eyes = rigEyesAim.RigEyesAim()
        self.eye_space_switch = rigEyesSpaceSwitch.EyeSpaceSwitch()
        self.l_mustach = rigFK.RigFK()
        self.r_mustach = rigFK.RigFK()
        self.c_mustach = rigSingleJoint.RigSingleJoint()
        self.rig_spine = None

class RigByped(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigByped, self).__init__(*args, **kwargs)
        self._model = RigBypedModel()

        self.arm_root = [u'{}_clavicle01_reference_pnt', u'{}_shoulder01_reference_pnt', u'{}_elbow01_reference_pnt',
                         u'{}_palm01_reference_pnt']
        self.hip_root = ['C_COG_reference_pnt']
        self.hand_root = [u'{}_palm01_reference_pnt']
        self.neck_root = [u'C_neck00_reference_pnt', u'C_head00_reference_pnt', u'C_headTip00_reference_pnt']
        self.eyes_root = [u'R_eye_reference_pnt', u'L_eye_reference_pnt']
        self.mustach_root = ['{}_mustach00_reference_pnt', '{}_mustach01_reference_pnt', '{}_mustach02_reference_pnt', '{}_mustach03_reference_pnt']
        self.c_mustach_root = 'C_mustach00_reference_pnt'
    @property
    def neck_head(self):
        return self._model.neck_head

    @property
    def eyes(self):
        return self._model.eyes

    @property
    def l_arm(self):
        return self._model.l_arm

    @property
    def r_arm(self):
        return self._model.r_arm

    @property
    def l_hand(self):
        return self._model.l_hand

    @property
    def r_hand(self):
        return self._model.r_hand

    @property
    def cog(self):
        return self._model.cog
    @property
    def l_mustach(self):
        return self._model.l_mustach
    @property
    def r_mustach(self):
        return self._model.r_mustach
    @property
    def c_mustach(self):
        return self._model.c_mustach


    @property
    def rig_world(self):
        return self._model.rig_world

    @property
    def eye_space_switch(self):
        return self._model.eye_space_switch

    def build(self):
        # self.hip.create_point_base(*self.hip_root, name='hip')
        self.cog.create_point_base(self.hip_root[0], name='cog', depth=1)
        self.cog.custom_world_align(self.cog.reset_controls[0])

        self.l_arm.create_point_base(*[each.format('L') for each in self.arm_root])
        self.l_arm.set_parent(self.cog)
        self.r_arm.create_point_base(*[each.format('R') for each in self.arm_root])
        self.r_arm.set_parent(self.cog)

        self.l_hand.create_point_base(*[each.format('L') for each in self.hand_root])
        self.l_hand.set_parent(self.l_arm)

        self.r_hand.create_point_base(*[each.format('R') for each in self.hand_root])
        self.r_hand.set_parent(self.r_arm)

        self.neck_head.create_point_base(*self.neck_root)
        self.r_mustach.create_point_base(*[each.format('R') for each in self.mustach_root])
        self.l_mustach.create_point_base(*[each.format('L') for each in self.mustach_root])
        self.c_mustach.create_point_base(self.c_mustach_root)
        self.c_mustach.set_parent(self.neck_head)
        self.r_mustach.set_parent(self.c_mustach)
        self.l_mustach.set_parent(self.c_mustach)

        self.eyes.create_point_base(*self.eyes_root)
        self.eye_space_switch.build(self.eyes, self.neck_head, self.rig_world)
        self.neck_head.set_parent(self.cog)

        self.cog.set_parent(self.rig_world)
        self.eyes.set_parent(self.neck_head)
        self._model.rig_spine = rigSpine.RigSpine()
        self.rig_spine.set_parent(self.cog)
        # self.create.constraint.node_base(self.spine.backward_root, self.hip.root, point=True)
        # self.create.constraint.node_base(self.cog.tip, self.hip.root, orient=True, mo=True)

        # setup as skinned joints
        self.eyes.rename_as_skinned_joints(nub=False)
        self.l_arm.rename_as_skinned_joints()
        self.r_arm.rename_as_skinned_joints()
        self.l_hand.rename_as_skinned_joints()
        self.r_hand.rename_as_skinned_joints()
        self.neck_head.rename_as_skinned_joints()
        self.r_mustach.rename_as_skinned_joints()
        self.l_mustach.rename_as_skinned_joints()










