"""
매매전략

n초 간격으로 현재가 감시, 
상승장 매수 구간, 상승장 매도구간 도달시 매매 이벤트 발생

상승장 매수: 이전 봉 종가 20선 아래에 있을 때, 20선 +n% 범위에서 매수
상승장 매도: 천장 +-n% 범위에서 매도
"""
import pyupbit
from time import sleep
import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5 import uic

ui = uic.loadUiType("5-20.ui")[0]


class Main(QMainWindow, ui):
    def __init__(self):
        """
        20선, 천장, 바닥 가격을 속성으로 가지고 있어야함
        +-n% 범위를 속성으로 가지고 있어야함
        """
        super().__init__()
        self.setupUi(self)
        self.MA20 = 1
        self.ceiling = 1
        self.bottom = 1
        self.tradingRange = 1
        self.previousClosePrice = 1

        """
        API key
        """
        self.access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
        self.secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
        self.upbit = pyupbit.Upbit(self.access, self.secret)

        """
        봇 실행
        """
        self.pushButtonStart.clicked.connect(self.startBot)
        """
        봇 중지
        """
        self.pushButtonStop.clicked.connect(self.stopBot)

    def popup(self, message):
        """
        팝업박스
        :param message:
        :return:
        """
        QMessageBox.information(self, "알림", message)

    def checkSetting(self):
        """
        설정값 확인
        :return:
        """
        tradingRange = self.textEditTradingRange.toPlainText() if True else False
        bongs = [self.radioButton1, self.radioButton3, self.radioButton5, self.radioButton10, self.radioButton15,
                 self.radioButton30, self.radioButton60, self.radioButton240, self.radioButtonDay]
        self.selectedBong = None
        for bong in bongs:
            if bong.isChecked():
                self.selectedBong = bong

        return tradingRange and self.selectedBong

    def startBot(self):
        if not self.checkSetting():
            return self.popup("설정값을 확인해주세요.")
        if not self.isRunning:
            self.isRunning = True

        while self.isRunning:
            currentPrice = pyupbit.get_current_price()
            status = self.getStatus(currentPrice)
            print(status)
            self.tradingLogic(status)
            sleep(1)

    def stopBot(self):
        if self.isRunning:
            self.isRunning = False

    def getStatus(self, price):
        """
        현재 가격 상태 반환
        :param price:
        :return:
        """
        maxBuyingRange = self.MA20 * (1 + self.tradingRange)
        minSellingRange = self.ceiling * (1 - self.tradingRange)

        buyingCondition = (self.MA20 <= price <= maxBuyingRange) and (self.previousClosePrice < self.MA20)
        sellingCondition = minSellingRange <= price

        if buyingCondition:
            return "buy"
        if sellingCondition:
            return "sell"
        return None

    def tradingLogic(self, status):
        """
        매매로직 수행행
       :param status:
        :return:
        """
        if not status:
            return
        if status == "buy":
            """
            풀매수
            """
            pass
        if status == "sell":
            """
            풀매도
            """
            pass

class Bot(QThread):
    def __init__(self):
        super(Bot, self).__init__()

    def run(self):



app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()

# import pyupbit
# import pandas as pd
# import matplotlib.pyplot as plt
#
# access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
# secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
# upbit = pyupbit.Upbit(access, secret)
# pd.options.display.float_format = '{:.1f}'.format
#
#
# def isBullMarket(interval):
#     df = pyupbit.get_ohlcv("KRW-BTC", interval=interval)
#     period = 20  # 일이 아니라 갯수
#     df['MiddleBand'] = df['close'].rolling(period).mean()
#     MA20 = df.iloc[-1]['MiddleBand']
#     currentPrice = pyupbit.get_current_price()
#
#     if currentPrice > MA20:
#         return True
#     else:
#         return False
#
#
# """
# 시각화 예시
# """
# df = pyupbit.get_ohlcv("KRW-BTC", interval="minute240")
#
# multiplier = 2
# period = 20  # 일이 아니라 갯수
#
# df['MiddleBand'] = df['close'].rolling(period).mean()
# df['UpperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier
# df['LowerBand'] = df['close'].rolling(period).mean() - df['close'].rolling(period).std() * multiplier
#
# ax = plt.gca()
#
# df.plot(kind="line", y='MiddleBand', ax=ax)
# df.plot(kind="line", y='UpperBand', ax=ax)
# df.plot(kind="line", y='LowerBand', ax=ax)
#
# plt.show()
