# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\\main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 70, 801, 521))
        self.groupBox.setObjectName("groupBox")
        self.treeView = QtWidgets.QTreeView(self.groupBox)
        self.treeView.setGeometry(QtCore.QRect(220, 20, 571, 461))
        self.treeView.setObjectName("treeView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 26))
        self.menubar.setObjectName("menubar")
        self.menuClient_File_Browser = QtWidgets.QMenu(self.menubar)
        self.menuClient_File_Browser.setObjectName("menuClient_File_Browser")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuSettings.addSeparator()
        self.menubar.addAction(self.menuClient_File_Browser.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Navigate"))
        self.menuClient_File_Browser.setTitle(_translate("MainWindow", "Client File Browser"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
