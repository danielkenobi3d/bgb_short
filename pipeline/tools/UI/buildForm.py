# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'build_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(247, 437)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.AssetGroupBox = QtWidgets.QGroupBox(Form)
        self.AssetGroupBox.setObjectName("AssetGroupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.AssetGroupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.comboBox = QtWidgets.QComboBox(self.AssetGroupBox)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_5.addWidget(self.comboBox)
        self.verticalLayout_3.addWidget(self.AssetGroupBox)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_4.addWidget(self.listWidget)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.save_rig_button = QtWidgets.QPushButton(self.tab_2)
        self.save_rig_button.setObjectName("save_rig_button")
        self.verticalLayout.addWidget(self.save_rig_button)
        self.save_shapes_button = QtWidgets.QPushButton(self.tab_2)
        self.save_shapes_button.setObjectName("save_shapes_button")
        self.verticalLayout.addWidget(self.save_shapes_button)
        self.save_skin_button = QtWidgets.QPushButton(self.tab_2)
        self.save_skin_button.setObjectName("save_skin_button")
        self.verticalLayout.addWidget(self.save_skin_button)
        self.save_reference_points = QtWidgets.QPushButton(self.tab_2)
        self.save_reference_points.setObjectName("save_reference_points")
        self.verticalLayout.addWidget(self.save_reference_points)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_3.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.AssetGroupBox.setTitle(_translate("Form", "Asset build"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "build steps"))
        self.save_rig_button.setText(_translate("Form", "save rig"))
        self.save_shapes_button.setText(_translate("Form", "save shapes"))
        self.save_skin_button.setText(_translate("Form", "save skinning"))
        self.save_reference_points.setText(_translate("Form", "save reference points"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "save data"))
