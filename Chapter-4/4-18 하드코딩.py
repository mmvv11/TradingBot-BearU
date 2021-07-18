import sys
from PyQt5.QtWidgets import *


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setGeometry(100, 100, 300, 500)
        self.setWindowTitle("워밍업 프로그램")

        # 시세조회
        self.getPriceLabel = QLabel("현재가격", self)
        self.getPriceTextEdit = QTextEdit(self)
        self.getPriceTextEdit.move(0, 30)
        self.getPriceButton = QPushButton("조회", self)
        self.getPriceButton.move(120, 30)

        # 매수
        self.buyLabel = QLabel("매수금액", self)
        self.buyLabel.move(0, 60)
        self.buyTextEdit = QTextEdit(self)
        self.buyTextEdit.move(0, 90)
        self.buyButton = QPushButton("매수", self)
        self.buyButton.move(120, 90)

        # 매도
        self.sellLabel = QLabel("매도금액", self)
        self.sellLabel.move(0, 120)
        self.sellTextEdit = QTextEdit(self)
        self.sellTextEdit.move(0, 150)
        self.sellButton = QPushButton("매도", self)
        self.sellButton.move(120, 150)



app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()
