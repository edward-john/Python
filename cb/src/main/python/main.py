import os
import sys
import qdarkstyle
import xlwings as xw
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
        self.settingsbox = Settings()
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
        self.wpfolder = 'Annual Workpapers'
        self.prevpath = []
        self.listyear = []
        self.clientname = ''
        self.backbutton.setEnabled(False)
        self.toggle_year(False)
        self.count = 0
        self.counter = 0

        # Context Menu
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        # Set instance of window app
        self.show()

    # TODO: Error message on tree view if no folder found         // ETA: 30 Minutes
    # TODO: Tax year to read only available folders               // ETA: 2 Hours
    # TODO: Extract information from latest workpapers            // ETA: 4 Hours
    # TODO: For future update > Add XPM Links                     // ETA: 10 Hours
    # TODO: Context Menu > Add New  > Workpapers / Folder         // ETA: 30 Minutes
    # TODO: Add double click event to open files in tree view     // ETA: 50 Minutes
    # TODO: Add images for close and minimize button              // ETA: 20 Minutes
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

        # Declaring variables from config file
        if self.settings['clientdir']:
            self.clientdir = self.settings['clientdir']
        else:
            self.clientdir = f'{os.environ["USERPROFILE"]}'

        self.completer_pref = int(self.settings['autocomplete'])
        self.yearpref = self.settings['yearprefix']
        self.year = str(datetime.now().year)
        self.diryear = f'{self.yearpref}{self.year}'

    def select_client(self, event):
        """Hide label and show line edit"""
        self.clientlabel.hide()
        self.lineEdit.show()

    def client_selected(self):
        """Show label, hide line edit and update label"""
        self.lineEdit.hide()
        self.clientlabel.show()
        self.clientname = self.lineEdit.text()
        self.folder(opt='selected')

    def folder(self, opt=None):
        """Changing folder function, all of them passed here"""

        # Detect how folder function is initialized
        if opt == 'selected':
            self.path = os.path.join(self.clientdir, self.clientname,
                                     self.diryear)
        elif opt == 'back':
            self.path = self.prevpath[self.counter-1]
        elif opt == 'manual':
            self.path = self.file_path
        elif opt == 'up':
            self.path = os.path.dirname(self.path)
        elif opt == 'switch':
            print(self.path)
            self.path = self.path.replace(self.curryear, self.newyear)
            print(self.path)
            print(len(self.curryear), len(self.newyear))

        self.treeView.setRootIndex(self.model.index(self.path)) #Run folder

        #Detect year and declare year variables
        if len(self.path.split('\\')) >= 4:
            if self.yearpref in self.path.split('\\')[3]:
                self.toggle_year(True)
                currfolder = os.path.basename(self.path)
                index = self.treeView.model()
                index = index.index(1,0)
                self.treeView.expand(index)
                self.yearline.setText(currfolder.strip(self.yearpref))
        else:
            self.toggle_year(False)

        #Detect if current index is inside client
        if self.path == self.clientdir:
            self.clientlabel.setText('Select a client...')
            self.lineEdit.setText('')
            self.lineEdit.hide()
            self.clientlabel.show()
        elif len(self.path.split('\\')) >= 3:  # Detect if on second level
            self.prevclient = self.clientname
            self.clientname = self.path.split('\\')[2]
            self.clientfolder = '\\'.join(self.path.split('\\')[0:3])
            self.clientlabel.setText(self.clientname)
            self.lineEdit.setText(self.clientname)
            self.lineEdit.hide()
            self.clientlabel.show()
            if self.prevclient != self.clientname:
                self.years(self.clientfolder, clear=True)
                print(self.listyear)

        # Storing paths to a list
        if not opt == 'back':
            self.counter += 1  # Usage Counter
            if self.counter == 1:
                self.prevpath.append(self.clientdir)
            else:
                self.prevpath.append(self.path)

        # Toggle year widget if current index contains year pref
        self.windowspath = self.path.replace('/', '\\')
        self.addressbar.setText(self.windowspath)
        self.backbutton.setEnabled(True)

    def years(self, folderthree, clear=None):
        """Create a list of years from folder structure"""
        if clear:
            self.listyear = []
            self.index = 0

        folders = os.listdir(folderthree)
        for folder in folders:
            if self.yearpref in folder:
                year = folder.lstrip(self.yearpref)
                self.listyear.append(year)

    def goback(self):
        self.folder(opt='back')

    def go_up(self):
        self.folder(opt='up')

    def toggle_year(self, boolean):
        self.rightarrow.setEnabled(boolean)
        self.leftarrow.setEnabled(boolean)
        self.yearline.setEnabled(boolean)

    def addyear(self):
        """Add one year on yearline"""
        currfolder = os.path.basename(self.path)
        self.curryear = currfolder.strip(self.yearpref)
        self.index = self.listyear.index(self.curryear)
        self.index = self.index + 1
        self.newyear = self.listyear[self.index]
        self.yearline.setText(self.newyear)
        self.folder(opt='switch')

    def lessyear(self):
        """Less 1 year on yearline"""
        currfolder = os.path.basename(self.path)
        self.curryear = currfolder.strip(self.yearpref)
        self.yearline.setText(self.curryear)
        self.index = self.listyear.index(self.curryear)
        self.index = self.index - 1
        self.newyear = self.listyear[self.index]
        self.yearline.setText(self.newyear)
        self.folder(opt='switch')

    def actions(self):
        """All actions for buttons"""
        self.closebutton.clicked.connect(self.close)
        self.minimizebutton.clicked.connect(self.showMinimized)
        self.completer.activated.connect(self.client_selected)
        self.settingsbutton.clicked.connect(self.open_settings)
        self.rightarrow.clicked.connect(self.addyear)
        self.leftarrow.clicked.connect(self.lessyear)
        self.clientlabel.mousePressEvent = self.select_client
        self.backbutton.clicked.connect(self.goback)
        self.settingsbox.buttonBox.accepted.connect(self.save_settings)
        self.treeView.mouseDoubleClickEvent = self.open_file
        self.upper.clicked.connect(self.go_up)
        self.lineEdit.returnPressed.connect(self.client_selected)

    def save_settings(self):
        self.settingsbox.writer()
        self.load_settings()
        self.setEnabled(True)
        self.client_names()
        self.actions()

    def open_settings(self):
        """Open settings dialog box"""
        self.settingsbox.show()
        self.settingsbox.exec_()

    def populate(self):
        """Load file browser model on tree view"""
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 350)
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

    def open_file(self, *event):
        """Open Function"""
        index = self.treeView.currentIndex()
        self.file_path = self.model.filePath(index)
        self.file_path = self.file_path.replace('/', '\\')
        if os.path.isdir(self.file_path):
            self.folder(opt='manual')
        else:
            os.startfile(self.file_path)

    """ Event Handling """

    def keyPressEvent(self, event):
        """Key press events"""
        if event.key() == QtCore.Qt.Key_Backspace:  # Go back on previous folder
            self.folder(opt='back')

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

        # Initiate
        self.reader()  # Apply displays to input widgets

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
