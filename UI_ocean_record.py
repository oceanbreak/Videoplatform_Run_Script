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
    def __init__(self):
        super().__init__()


        # Set main widget
        self.dataField = qtw.QTextBrowser(text='Hello')
        self.setCentralWidget(self.dataField)



        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())