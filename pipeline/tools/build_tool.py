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
from bgb_short.pipeline import environment
from RMPY.core import data_save_load
# import os
# import sys
# sys.path.append(os.path.dirname(__file__))
importlib.reload(buildForm)
importlib.reload(environment)

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.env = environment.Environment()
        self.ui = buildForm.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('bgb Short Pipe')
        self.ui.save_guides_button.clicked.connect(io.export_template)
        self.ui.save_skin_button.clicked.connect(data_save_load.save_skin_cluster)
        self.ui.save_shapes_button.clicked.connect(data_save_load.save_curve)

        for index, each in enumerate(self.env.asset_list):
            self.ui.comboBox.insertItem(index, each)
        self.ui.comboBox.currentIndexChanged.connect(self.update_env)


    def update_env(self):
        print(f'the index changed {self.ui.comboBox.currentIndex()}')
        print(self.env.asset_list[self.ui.comboBox.currentIndex()])
        self.env.asset = self.env.asset_list[self.ui.comboBox.currentIndex()]


if __name__ == '__main__':
    w = Main()
    w.show()
