##############################################################
### This module provides UI for Ocean Record (c) program
### for logging data mainly in NMEA format from  various
### data sources.
### Also provides specific elements for controlling 
### TUV "Videomodule" data recording and managing.
####
#### Version 0.0
#### Updated 11.04.2022
##############################################################

import sys
from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc
from PySide2 import QtGui as qtg

class MainWindow(qtw.QMainWindow):
    """
    This is main window of Ocean Record.
    The init function configures all GUI elements.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set main widget
        self.dataField = qtw.QTextBrowser(text='Hello')
        self.setCentralWidget(self.dataField)

        # Set menu bar
        menubar = self.menuBar()
        options_menu = menubar.addMenu('Options')
        options_menu.addAction('Settings')
        options_menu.addSeparator()
        options_menu.addAction('Quit', self.close)

        # Set status bar
        self.statusBar().showMessage('Launching Ocean Record v. 0.0', 5000)

        # Set Toolbar
        topToolbar = self.addToolBar('Edit')
        topToolbar.addAction('Connect')
        topToolbar.addAction('Start')
        topToolbar.addAction('Reset Track')
        topToolbar.addAction('Set Depth 0')
        topToolbar.addAction('Cam control')

        # Set Docked camera widget
        camWidgetDock = qtw.QDockWidget("Cam control")
        camWidget = CameraWidget()
        camWidgetDock.setWidget(camWidget)
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, camWidgetDock)

        self.show()

class CameraWidget(qtw.QWidget):
    """
    This is widget contatining
    camera settings
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        camConnectButton = qtw.QPushButton("Connect cam")
        camRecFolderButton = qtw.QPushButton("Set rec folder")
        camSyncTimeButton = qtw.QPushButton("Sync camera time")
        camRecButton = qtw.QPushButton("Start SD rec")
        camFormatButton = qtw.QPushButton("Format SD")
        camDownloadsButton = qtw.QPushButton("Downloads")

        # self.setLayout(qtw.QVBoxLayout)
        cam_wgt_layout = qtw.QVBoxLayout(self)
        cam_wgt_layout.addWidget(camConnectButton)
        cam_wgt_layout.addWidget(camRecFolderButton)
        cam_wgt_layout.addWidget(camSyncTimeButton)
        cam_wgt_layout.addWidget(camRecButton)
        cam_wgt_layout.addWidget(camFormatButton)
        cam_wgt_layout.addWidget(camDownloadsButton)

        self.setLayout(cam_wgt_layout)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow(windowTitle = "Ocean Record")
    sys.exit(app.exec_())