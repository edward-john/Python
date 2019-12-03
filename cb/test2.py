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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Test Window'
        # self.setGeometry(200,200,500,500)
        self.layout = QGridLayout()

        self.setLayout(self.layout)
        # self.resize(500,500)
        self.button = QPushButton('Test')
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.layout.addWidget(self.button,50,10)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
    