import pyupbit
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

ui = uic.loadUiType("4-19.ui")[0]

access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
upbit = pyupbit.Upbit(access, secret)


class MyWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ticker = "KRW-BTC"

        self.getPriceButton.clicked.connect(self.getPrice)
        self.buyButton.clicked.connect(self.buyMarketPrice)
        self.sellButton.clicked.connect(self.sellMarketPrice)

    def getPrice(self):
        """
        시세 조회하기: upbit API
        self.getPriceTextEdit update
        :return: 
        """
        currentPrice = str(pyupbit.get_current_price())
        self.getPriceTextEdit.setText(currentPrice)
        return

    def buyMarketPrice(self):
        """
        시장가 매수하기: self.buyTextEdit에 있는 데이터 가져오기 validation
        upbit 시장가 매수 API 호출
        :return: 
        """
        buyPrice = self.buyTextEdit.toPlainText()

        if not self.isNumber(buyPrice):
            self.popup("숫자만 입력해주세요.")
            return False

        buyResult = upbit.buy_market_order(self.ticker, 5000)
        if (not buyResult) or "error" in buyResult:
            self.popup("조회 API 에러")
            return False

    def sellMarketPrice(self):
        """
        시장가 매도하기: self.sellTextEdit에 있는 데이터 가져오기 validation
        upbit 시장가 매도 API 호출
        :return: 
        """

    def popup(self, message):
        QMessageBox.information(self, "QMessageBox", message)

    def isNumber(self, num):
        try:
            tmp = float(num)
            return True
        except ValueError:
            return False


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
