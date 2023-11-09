import importlib

import maya.cmds as cmds
import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from shiboken2 import wrapInstance
from bgb_short.pipeline.tools.UI import buildForm
import maya.mel as mel
from bgb_short.pipeline.mgear import io
importlib.reload(buildForm)

# import os
# import sys
# sys.path.append(os.path.dirname(__file__))


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.ui = buildForm.Ui_Form()
        print(self.__class__)
        self.ui.setupUi(self)
        self.setWindowTitle('bgb Short Pipe')
        self.ui.save_rig_button.clicked.connect(io.export_template)

    def JointDrawStyle(self):
        mel.eval("source RMJointDisplay.mel;RMChangeJointDrawStyle();")

if __name__ == '__main__':
    w = Main()
    w.show()
