import os
import sys
import qdarkstyle
from datetime import datetime

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QBasicTimer, QCoreApplication, QPoint
from PyQt5.QtGui import QFont, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QDesktopWidget,
                             QDialog, QFrame, QGridLayout, QLabel, QLineEdit,
                             QMainWindow, QMenu, QMenuBar, QMessageBox,
                             QProgressBar, QPushButton, QStatusBar, QTextEdit,
                             QToolBar, QToolTip, QVBoxLayout, QWidget, qApp,
                             QCompleter)

from ui import main, settings

print(sys.path)

class Window(main.Ui_MainWindow, QMainWindow, ApplicationContext):
    def __init__(self):
        """Window Object"""
        super(Window, self).__init__()

        #Inherit from UI file
        self.setupUi(self)  # Initialize UI
        self.clientdir = os.environ['USERPROFILE']  # Client Default Directory

        # Settings Initialization
        self.configpath = f'{os.environ["USERPROFILE"]}\\Client Browser'
        self.configfile = f'{self.configpath}\\config.txt'

        if not os.path.exists(self.configpath):
            os.mkdir(self.configpath)
        if not os.path.exists(self.configfile):
            with open(self.configfile, 'w+') as f:
                f.write('clientdir:\nautocomplete:\nlastclient:\nlastyear:')
                f.close

        # Class Variables
        self.year = str(datetime.today().year)
        self.diryear = f'31 March {self.year}'
        self.oldPos = self.pos()  # variable for dragging frameless window

         # Set Flags (Frameless)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

        # Context Menu
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        #Initialize widget defaults
        self.populate()
        self.client_names()  # autocomplete parameters
        self.actions()  # loading all actions
        self.lineEdit.hide()
        self.yearline.setText(self.year)

        # Set instance of window app
        self.show()


    def show_hide(self):
        """Hide label and show line edit"""
        self.clientlabel.hide()
        self.lineEdit.show()


    def hide_show(self):
        """Show label, hide line edit and update label"""
        self.clientlabel.show()
        self.lineEdit.hide()
        self.loadclientname()


    def loadclientname(self):
        """Update client label from auto complete text"""
        self.clientname = self.lineEdit.text()
        self.clientlabel.setText(self.clientname)
        self.clientpath = os.path.join(self.clientdir, self.clientname,
                                       self.diryear, )
        self.treeView.setRootIndex(self.model.index(self.clientpath))


    def addyear(self):
        """Add one year on yearline"""
        self.year = str(int(self.year) + 1)
        self.diryear = f'31 March {self.year}'
        self.yearline.setText(self.year)
        self.loadclientname()


    def lessyear(self):
        """Less 1 year on yearline"""
        self.year = str(int(self.year) - 1)
        self.diryear = f'31 March {self.year}'
        self.yearline.setText(self.year)
        self.loadclientname()


    def actions(self):
        """All actions for buttons"""
        self.closebutton.clicked.connect(self.close)
        self.minimizebutton.clicked.connect(self.showMinimized)
        self.completer.activated.connect(self.hide_show)
        self.settingsbutton.clicked.connect(self.settings)
        self.File.clicked.connect(self.show_hide)
        self.rightarrow.clicked.connect(self.addyear)
        self.leftarrow.clicked.connect(self.lessyear)


    def settings(self):
        """Open settings dialog box"""
        self.settingsbox = Settings()
        self.settingsbox.exec_()


    def populate(self):
        """Load file browser model on tree view"""
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(self.clientdir))
        self.treeView.setSortingEnabled(1)


    def client_names(self):
        """Auto complete list of entries"""
        self.clients = os.listdir(self.clientdir)
        self.completer = QCompleter(self.clients)
        self.completer.setCaseSensitivity(0)
        self.completer.setMaxVisibleItems(10)
        self.lineEdit.setCompleter(self.completer)


    def context_menu(self):
        """Right Click Menu: [OPEN]"""
        menu = QtWidgets.QMenu()

        # Actions
        open = menu.addAction('Open')
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


    def open_file(self):
        """Open Function"""
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        os.startfile(file_path)


    def mousePressEvent(self, event):
        """Record the position when mouse is pressed"""
        self.oldPos = event.globalPos()
        # print(QLabel.mousePressEvent(self.clientlabel, event))


    def mouseMoveEvent(self, event):
        """Updating positions as we drag"""
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class Settings(settings.Ui_Dialog, QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.setupUi(self)
        self.show()


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()


    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


if __name__ == '__main__':
    my_app = ApplicationContext()
    my_app.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())  # Dark Theme
    exit_code = Window()
    my_app.app.exec_()
