import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

ui = uic.loadUiType("5-25.ui")[0]

class Main(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()