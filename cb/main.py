import os
import sys

import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QBasicTimer, QCoreApplication, QPoint
from PyQt5.QtGui import QFont, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QDesktopWidget,
                             QDialog, QFrame, QGridLayout, QLabel, QLineEdit,
                             QMainWindow, QMenu, QMenuBar, QMessageBox,
                             QProgressBar, QPushButton, QStatusBar, QTextEdit,
                             QToolBar, QToolTip, QVBoxLayout, QWidget, qApp)

from ui import main


class Window(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        """Window Object"""
        super(Window, self).__init__()

        self.setupUi(self) #Initialize UI
        self.populate() #Run FileSystem Model
        self.title = 'Client File Browser' #Set Window Title

        # Set Flags (Frameless)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

        #Context Menu
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        self.oldPos = self.pos()

        #Show Window
        self.show()


    def populate(self):
        """Load file browser model on tree view"""
        path = f'{os.environ["USERPROFILE"]}\\Desktop'
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)


    def context_menu(self):
        """Right Click Menu: [OPEN]"""
        menu = QtWidgets.QMenu()
        open = menu.addAction('Open')
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


    def open_file(self):
        """Open Function"""
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        os.startfile(file_path)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()


    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) #Dark Theme
    window = Window()
    sys.exit(app.exec_())
