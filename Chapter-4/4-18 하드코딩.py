import sys
from PyQt5.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 300, 500)  # 윈도우의 위치와 크기를 설정합니다.
        self.setWindowTitle("워밍업")  # 프로그램 상단에 표시될 타이틀을 설정합니다.

        # 시세조회
        getPriceLabel = QLabel("현재가격", self)
        getPriceTextEdit = QTextEdit(self)
        getPriceTextEdit.move(0, 30)
        getPriceButton = QPushButton("조회", self)
        getPriceButton.move(120, 30)
        getPriceErrorLabel = QLabel(self)
        getPriceErrorLabel.move(0, 40)

        # 매수
        buyLabel = QLabel("매수금액", self)
        buyLabel.move(0, 60)
        buyTextEdit = QTextEdit(self)
        buyTextEdit.move(0, 90)
        buyButton = QPushButton("매수", self)
        buyButton.move(120, 90)
        buyErrorLabel = QLabel(self)
        buyErrorLabel.move(0, 100)

        # 매도
        sellLabel = QLabel("매도금액", self)
        sellLabel.move(0, 120)
        sellTextEdit = QTextEdit(self)
        sellTextEdit.move(0, 150)
        sellButton = QPushButton("매도", self)
        sellButton.move(120, 150)
        sellErrorLabel = QLabel(self)
        sellErrorLabel.move(0, 160)


# 맨 처음 썻던 코드와 같은 패턴입니다. 달라진 것은 UI 구성을 객체지향적으로 했다는 것이겠죠.
app = QApplication(sys.argv)  # QApplication 객체를 생성하고
window = MyWindow()  # 보여주고 싶은 UI를 구성하여
window.show()  # show 메서드를 호출하고
app.exec_()  # 이벤트 루프를 실행시켜주면 됩니다!
