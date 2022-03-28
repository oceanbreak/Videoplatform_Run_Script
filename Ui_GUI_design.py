# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Coding\Videoplatform_Run_Script\GUI_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(471, 466)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(20, 10, 75, 61))
        self.connectButton.setObjectName("connectButton")
        self.startLogButton = QtWidgets.QPushButton(self.centralwidget)
        self.startLogButton.setGeometry(QtCore.QRect(110, 10, 75, 61))
        self.startLogButton.setObjectName("startLogButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 90, 431, 331))
        self.textBrowser.setObjectName("textBrowser")
        self.resetTrackButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetTrackButton.setGeometry(QtCore.QRect(200, 10, 75, 61))
        self.resetTrackButton.setObjectName("resetTrackButton")
        self.setDepthZeroButton = QtWidgets.QPushButton(self.centralwidget)
        self.setDepthZeroButton.setGeometry(QtCore.QRect(290, 10, 75, 61))
        self.setDepthZeroButton.setAutoDefault(False)
        self.setDepthZeroButton.setObjectName("setDepthZeroButton")
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(380, 10, 75, 61))
        self.settingsButton.setAutoDefault(False)
        self.settingsButton.setObjectName("settingsButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 471, 21))
        self.menubar.setObjectName("menubar")
        self.menuOcean_Record = QtWidgets.QMenu(self.menubar)
        self.menuOcean_Record.setObjectName("menuOcean_Record")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuOcean_Record.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ocean Record"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.startLogButton.setText(_translate("MainWindow", "Start"))
        self.resetTrackButton.setText(_translate("MainWindow", "Reset track"))
        self.setDepthZeroButton.setText(_translate("MainWindow", "Set depth 0"))
        self.settingsButton.setText(_translate("MainWindow", "Settings"))
        self.menuOcean_Record.setTitle(_translate("MainWindow", "About"))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())