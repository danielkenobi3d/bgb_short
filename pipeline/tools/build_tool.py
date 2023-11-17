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

import importlib
from bgb_short.pipeline import pipe_config
from bgb_short.pipeline import environment
import os
import pkgutil
from pathlib import Path
importlib.reload(io)
importlib.reload(pipe_config)
importlib.reload(environment)


class BuildStep(QListWidgetItem):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.evaluate = None

    def toggle_item(self):
        if int(self.flags() & Qt.ItemIsEnabled):
            self.setFlags(self.flags() & ~Qt.ItemIsEnabled)
        else:
            self.setFlags(self.flags() | Qt.ItemIsEnabled)

    @property
    def is_enabled(self):
        if int(self.flags() & Qt.ItemIsEnabled):
            return True
        else:
            return False

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.build_step_list = []
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
        self.add_build_steps()
        self.ui.listWidget.itemDoubleClicked.connect(self.build_clicked)

    def update_env(self):
        print(f'the index changed {self.ui.comboBox.currentIndex()}')
        print(self.env.asset_list[self.ui.comboBox.currentIndex()])
        self.env.asset = self.env.asset_list[self.ui.comboBox.currentIndex()]

    def build_clicked(self):
        index = 0
        run_till = self.ui.listWidget.currentItem()
        if run_till.is_enabled:
            if run_till.evaluate is not None:
                index = self.ui.listWidget.currentRow()
        else:
            return

        for each_widget in self.build_step_list[:index+1]:
            if each_widget.is_enabled:
                if each_widget.evaluate:
                    each_widget.evaluate()
                each_widget.toggle_item()

    def import_base_modules(self):
        env = environment.Environment()
        asset_module = importlib.import_module(f'{pipe_config.modules_path}.{env.asset}')

        if 'inherit' in vars(asset_module):
            inherit_module = importlib.import_module(f'{pipe_config.modules_path}.{asset_module.inherit}')
        else:
            inherit_module = importlib.import_module(f'{pipe_config.modules_path}.{pipe_config.default_module}')

        importlib.reload(asset_module)
        importlib.reload(inherit_module)

        build_config_file = None
        for each in pkgutil.iter_modules(inherit_module.__path__):
            if not each.ispkg:
                if each.name.split('_')[-1] == 'config':
                    print(inherit_module.__class__)
                    print(Path(f'{inherit_module.__name__}.{each.name}'))
                    build_config_file = importlib.import_module(f'{inherit_module.__name__}.{each.name}')
        return asset_module, inherit_module, build_config_file

    def add_build_steps(self):
        asset_module, inherit_module, build_config_file = self.import_base_modules()
        if build_config_file:
            for each in build_config_file.build_order:
                self.build_step_list[-1].evaluate = self.build_step_list.append(BuildStep(each))
                for step_text, step_function in build_config_file.build[each]:
                    self.build_step_list.append(BuildStep(f'    {step_text}'))
                    self.build_step_list[-1].evaluate = env.get_variables_from_path(step_function)

        for each in self.build_step_list:
            self.ui.listWidget.addItem(each)







if __name__ == '__main__':
    w = Main()
    w.show()
