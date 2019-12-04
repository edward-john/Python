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
                             QCompleter, QFileDialog)

from ui import main, settings


class Window(main.Ui_MainWindow, QMainWindow, ApplicationContext):
    def __init__(self):
        """Window Object"""
        super(Window, self).__init__()

        # Inherit from UI file
        self.setupUi(self)

        # Load settings
        self.load_settings()

        # Class Variables
        self.oldPos = self.pos()  # variable for dragging frameless window

        # Set Flags (Frameless)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

        # Initialize widget defaults
        self.populate()
        self.client_names()
        self.actions()  # loading all actions
        self.lineEdit.hide()
        self.yearline.setText(self.year)
        self.treeView.setRootIndex(self.model.index(self.clientdir))

        # Context Menu
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        # Set instance of window app
        self.show()

    # TODO: Go up one level folder                                // ETA: 15 Minutes
    # TODO: Error message on tree view if no folder found         // ETA: 30 Minutes
    # TODO: Click event on clientlabel to show lineedit           // ETA: 1-3 Hours
    # TODO: Settings configuration >> Custom folder structure     // ETA: 45 Minutes
    # TODO: Tax year to read only available folders               // ETA: 2 Hours
    # TODO: Extract information from latest workpapers            // ETA: 4 Hours
    # TODO: For future update > Add XPM Links                     // ETA: 10 Hours
    # TODO: Context Menu > Add New  > Workpapers / Folder         // ETA: 30 Minutes
    # TODO: Add double click event to open files in tree view     // ETA: 50 Minutes
    # TODO: Add images for close and minimize button              // ETA: 20 Minutes
    # TODO: Add address bar                                       // ETA: 30 Minutes
    # TODO: Dynamic font size, dependent of len()                 // ETA: 15 Minutes

    def load_settings(self):
        """Load settings from config file"""

        # Settings File
        self.configpath = f'{os.environ["USERPROFILE"]}\\Client Browser'
        self.configfile = f'{self.configpath}\\config.txt'
        self.configparam = ['clientdir', 'autocomplete', 'yearprefix']

        if not os.path.exists(self.configpath):
            os.mkdir(self.configpath)
        if not os.path.exists(self.configfile):
            with open(self.configfile, 'w+') as f:
                separator = '=\n'
                f.write(separator.join(self.configparam) + '=')
                f.close

        # Read config file
        configuration = open(self.configfile, 'r')
        self.settings = {}
        for lines in configuration.readlines():
            line = lines.strip('\n').split('=')
            self.settings[line[0]] = line[1]

        # Declaring variables
        if self.settings['clientdir']:
            self.clientdir = self.settings['clientdir']
        else:
            self.clientdir = f'{os.environ["USERPROFILE"]}'

        self.completer_pref = int(self.settings['autocomplete'])
        self.yearpref = self.settings['yearprefix']
        self.year = str(datetime.now().year)
        self.diryear = f'{self.yearpref}{self.year}'
        self.wpfolder = 'Annual Workpapers'
        self.prevpath = []

    def select_client(self):
        """Hide label and show line edit"""
        self.clientlabel.hide()
        self.lineEdit.show()

    def client_selected(self):
        """Show label, hide line edit and update label"""
        self.clientlabel.show()
        self.lineEdit.hide()
        self.clientname = self.lineEdit.text()
        self.clientlabel.setText(self.clientname)
        self.folder()

    def folder(self):
        self.path = os.path.join(self.clientdir, self.clientname,
                                self.diryear, self.wpfolder)
        self.treeView.setRootIndex(self.model.index(self.path))
        self.prevpath.append(self.path) #Attaching variable to store paths
        self.addressbar.setText(self.path)
        print(self.prevpath)

    def addyear(self):
        """Add one year on yearline"""
        self.year = str(int(self.year) + 1)
        self.diryear = f'{self.yearpref}{self.year}'
        self.yearline.setText(self.year)
        self.folder()

    def lessyear(self):
        """Less 1 year on yearline"""
        self.year = str(int(self.year) - 1)
        self.diryear = f'{self.yearpref}{self.year}'
        self.yearline.setText(self.year)
        self.folder()

    def actions(self):
        """All actions for buttons"""
        self.closebutton.clicked.connect(self.close)
        self.minimizebutton.clicked.connect(self.showMinimized)
        self.completer.activated.connect(self.client_selected)
        self.settingsbutton.clicked.connect(self.open_settings)
        self.File.clicked.connect(self.select_client)
        self.rightarrow.clicked.connect(self.addyear)
        self.leftarrow.clicked.connect(self.lessyear)

    def open_settings(self):
        """Open settings dialog box"""
        self.settingsbox = Settings()
        self.settingsbox.exec_()

    def populate(self):
        """Load file browser model on tree view"""
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setSortingEnabled(1)

    def client_names(self):
        """Auto complete list of entries"""
        self.clients = os.listdir(self.clientdir)
        self.completer = QCompleter(self.clients)
        self.completer.setCaseSensitivity(0)
        self.completer.setMaxVisibleItems(10)
        self.completer.setCompletionMode(self.completer_pref)
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

    """ Event Handling """

    def keyPressEvent(self, event):
        """Key press events"""
        if event.key() == QtCore.Qt.Key_Backspace:  # Go back on previous folder
            if self.prevfolder:
                self.treeView.setRootIndex(self.model.index(self.clientdir))

    def mousePressEvent(self, event):
        """Record the position when mouse is pressed"""
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        """Updating positions as we drag"""
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class Settings(settings.Ui_Dialog, QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.setupUi(self)

        # Config File
        self.configpath = f'{os.environ["USERPROFILE"]}\\Client Browser'
        self.configfile = f'{self.configpath}\\config.txt'

        # Combo box set up
        self.cmodes = ['Popup', 'Unfiltered Popup', 'Inline']
        self.autocomplete.addItems(self.cmodes)
        self.browse_button.clicked.connect(self.getClientpath)
        self.buttonBox.accepted.connect(self.writer)

        #Initiate
        self.reader()  # Apply displays to input widgets
        self.show()

    def reader(self):
        self.settings = {}
        configuration = open(self.configfile, 'r')
        for lines in configuration.readlines():
            line = lines.strip('\n').split('=')
            self.settings[line[0]] = line[1]
        if self.settings['clientdir']:
            self.clientdir = self.settings['clientdir']
        else:
            self.clientdir = f'{os.environ["USERPROFILE"]}'

        self.clientpath.setText(self.clientdir)
        if self.settings['autocomplete'] == '':
            self.autocomplete.setCurrentIndex(0)
        else:
            index = int(self.settings['autocomplete'])
            self.autocomplete.setCurrentIndex(index)
        self.yearprefix.setText(self.settings['yearprefix'])

    def writer(self):
        self.config = {'clientdir': '', 'autocomplete': '', 'yearprefix': ''}
        self.config['clientdir'] = self.clientpath.text()
        self.config['yearprefix'] = self.yearprefix.text()
        item_index = int(self.autocomplete.currentIndex())
        self.config['autocomplete'] = item_index
        textdump = ''

        for keys in self.config:
            textdump += f'{keys}={self.config[keys]}\n'

        with open(self.configfile, 'w+') as f:
            f.write(textdump)
            f.close

    def getClientpath(self):
        filedialog = QFileDialog()
        filedialog.setFileMode(QFileDialog.DirectoryOnly)
        filename = filedialog.getExistingDirectory(self, 'Select Directory')
        filename = filename.replace('/', '\\')
        self.clientpath.setText(filename)

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
