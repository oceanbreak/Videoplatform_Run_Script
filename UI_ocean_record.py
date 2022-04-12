##############################################################
### This module provides UI for Ocean Record (c) program
### for logging data mainly in NMEA format from  various
### data sources.
### Also provides specific elements for controlling 
### TUV "Videomodule" data recording and managing.
####
#### Version 0.1
#### Updated 12.04.2022
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

        # Status flags
        self._cam_control = False

        # Set central data field
        self.dataField = qtw.QTextBrowser()
        self.dataField.setFontPointSize(12.0)
        self.dataField.setText('Setup your input channels in Options - Settings\n' \
                                        'and click "Connect" button to start')
        self.setCentralWidget(self.dataField)

        # Set menu bar
        menubar = self.menuBar()
        options_menu = menubar.addMenu('Options')
        options_menu.addAction('Settings')
        options_menu.addSeparator()
        options_menu.addAction('Quit', self.close)

        # Set status bar #####################################################
        self.statusBar().showMessage('Launching Ocean Record v. 0.0', 5000)

        # Set Toolbar ########################################################
        topToolbar = self.addToolBar('Edit')
        topToolbar.setMovable(False) # Hardly tie widget to main window

        # Main action that starts the whole program
        topToolbar.addAction('Connect')

        actStart = topToolbar.addAction('Start')
        actStart.setEnabled(False)

        actReset = topToolbar.addAction('Reset Track')
        actReset.setEnabled(False)

        actSetDepth0 = topToolbar.addAction('Set Depth 0')
        actSetDepth0.setEnabled(False)

        topToolbar.addSeparator()

        topToolbar.addAction('Cam control', self.toggleCamControl)

        # Set Docked camera widget (hidden by default) ##########################
        self.camWidgetDock = qtw.QDockWidget("Cam control")
        camWidget = CameraWidget()
        self.camWidgetDock.setWidget(camWidget)
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, self.camWidgetDock)
        self.camWidgetDock.hide()


        self.show()

    def toggleCamControl(self):
        if self._cam_control:
            self.camWidgetDock.hide()
            self._cam_control = False
        else:
            self.camWidgetDock.show()
            self._cam_control = True

class CameraWidget(qtw.QWidget):
    """
    This is widget contatining
    camera settings
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # Status flags
        self._cam_connected = False

        # Setup buttons
        self.camConnectButton = qtw.QPushButton("Connect cam")
        self.camRecFolderButton = qtw.QPushButton("Set rec folder", Enabled=False)
        self.camSyncTimeButton = qtw.QPushButton("Sync camera time", Enabled=False)
        self.camRecButton = qtw.QPushButton("Start SD rec", Enabled=False)
        self.camFormatButton = qtw.QPushButton("Format SD", Enabled=False)
        self.camDownloadsButton = qtw.QPushButton("Downloads", Enabled=False)

        self.camConnectButton.clicked.connect(self.connectCamera)

        # self.setLayout(qtw.QVBoxLayout)
        cam_wgt_layout = qtw.QVBoxLayout(self)
        cam_wgt_layout.addWidget(self.camConnectButton)
        cam_wgt_layout.addWidget(self.camRecFolderButton)
        cam_wgt_layout.addWidget(self.camSyncTimeButton)
        cam_wgt_layout.addWidget(self.camRecButton)
        cam_wgt_layout.addWidget(self.camFormatButton)
        cam_wgt_layout.addWidget(self.camDownloadsButton)
        self.setLayout(cam_wgt_layout)

    def connectCamera(self):
        if not self._cam_connected:
            self.camConnectButton.setText('Disconnect')
            self._cam_connected = True

            # Enable all buttons
            self.camRecFolderButton.setEnabled(True)
            self.camSyncTimeButton.setEnabled(True)
            self.camRecButton.setEnabled(True)
            self.camFormatButton.setEnabled(True)
            self.camDownloadsButton.setEnabled(True)

        else:
            self.camConnectButton.setText('Connect')
            self._cam_connected = False

            # Disable buttons
            self.camRecFolderButton.setEnabled(False)
            self.camSyncTimeButton.setEnabled(False)
            self.camRecButton.setEnabled(False)
            self.camFormatButton.setEnabled(False)
            self.camDownloadsButton.setEnabled(False)



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow(windowTitle = "Ocean Record")
    sys.exit(app.exec_())