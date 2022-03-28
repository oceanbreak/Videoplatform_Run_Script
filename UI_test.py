from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle('Ocean test')
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText('This is label')
        self.label.move(50,50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('Click')
        self.b1.clicked.connect(self.onButtonPush)

    def onButtonPush(self):
        self.label.setText('You clicked me')

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()
