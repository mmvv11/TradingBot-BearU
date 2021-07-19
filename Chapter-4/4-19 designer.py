import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyupbit

ui = uic.loadUiType("custum.ui")[0]


class Main(QMainWindow, ui):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)

        self.ticker = "KRW-BTC"

        self.pushButtonPrice.clicked.connect(self.getPrice)  # 비트코인 가격을 가져와서, textEditPrice에 넣어주기
        self.pushButtonBuy.clicked.connect(self.buyMarketPrice)  # textEditBuy에 있는 숫자를 가져와서, 시장가 매수 API 호출
        self.pushButtonSell.clicked.connect(self.sellMarketPrice)  # textEditSell에 있는 숫자를 가져와서, 시장가 매도 API 호출

        """
        pricevat API
        """
        access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
        secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
        self.upbit = pyupbit.Upbit(access, secret)

    def getPrice(self):
        """
        비트코인 가격을 가져와서, textEditPrice에 넣어주기
        :return:
        """
        currentPrice = str(pyupbit.get_current_price(self.ticker))
        self.textEditPrice.setText(currentPrice)
        return

    def buyMarketPrice(self):
        """
        textEditBuy에 있는 숫자를 가져와서, 시장가 매수 API 호출
        :return:
        """
        buyPrice = self.textEditBuy.toPlainText()
        buyPrice = self.isNumber(buyPrice)
        # buyPrice가 숫자인지 아닌지 검사
        if not buyPrice:
            # 팝업 메세지 생성하기
            self.popup("숫자가 아닙니다.")
            return False

        buyResult = self.upbit.buy_market_order(self.ticker, buyPrice)
        if (not buyResult) or "error" in buyResult:
            self.popup(f"매수 API 에러: {buyResult}")
            return False
        self.popup(f"매수주문 완료, {buyPrice}원")

    def isNumber(self, num):
        try:
            num = float(num)
            return num
        except:
            return False

    def popup(self, message):
        QMessageBox.information(self, "알림", message)

    def sellMarketPrice(self):
        """
        textEditSell에 있는 숫자를 가져와서, 시장가 매도 API호출
        :return:
        """
        sellPrice = self.textEditSell.toPlainText()
        sellPrice = self.isNumber(sellPrice)

        if not sellPrice:
            self.popup("숫자가 아닙니다.")
            return False

        askPrice = pyupbit.get_orderbook(self.ticker)[0]['orderbook_units'][0]['bid_price']
        volume = sellPrice / askPrice


        sellResult = self.upbit.sell_market_order(self.ticker, volume)
        if (not sellResult) or "error" in sellResult:
            self.popup(f"매도 API 에러: {sellResult}")
            return False
        self.popup(f"매도주문 완료: {sellPrice}원")


app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()
