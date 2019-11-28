import sys
import os

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSizeGrip
from ui import main

import qdarkstyle


class Window(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setupUi(self)
        self.populate()
        self.title = 'Client File Browser'
        # self.model.itemDoubleClicked.connect(self.open_file)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        vbox = QVBoxLayout()
        sizegrip = QSizeGrip(self)
        vbox.addWidget(sizegrip)

        self.setLayout(vbox)
        self.show()

    
    def populate(self):
        path = f'{os.environ["USERPROFILE"]}\\Desktop'
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)


    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction('Open')
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())
    

    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        os.startfile(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = Window()
    print((QtCore.QDir.rootPath()))
    sys.exit(app.exec_())
