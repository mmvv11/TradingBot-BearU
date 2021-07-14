import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

ui = uic.loadUiType("4-19.ui")[0]


class MyWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()