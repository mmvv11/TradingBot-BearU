"""
매매전략

n초 간격으로 현재가 감시,
상승장 매수 구간, 상승장 매도구간 도달시 매매 이벤트 발생

상승장 매수: 이전 봉 종가 20선 아래에 있을 때, 20선 +n% 범위에서 매수
상승장 매도: 천장 +-n% 범위에서 매도
"""
from datetime import datetime

import pyupbit
from time import sleep
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

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
        self.bot = Bot()

        """
        봇 실행
        """
        self.pushButtonStart.clicked.connect(self.startBot)
        """
        봇 중지
        """
        self.pushButtonStop.clicked.connect(self.stopBot)

    def checkSetting(self):
        """
        설정값 확인 및 초기세팅
        :return:
        """
        tradingRange = self.textEditTradingRange.toPlainText()
        try:
            tradingRange = float(tradingRange) / 100
        except:
            tradingRange = False

        interval = None

        if self.radioButton1.isChecked():
            interval = "minute1"
        elif self.radioButton3.isChecked():
            interval = "minute3"
        elif self.radioButton5.isChecked():
            interval = "minute5"
        elif self.radioButton10.isChecked():
            interval = "minute10"
        elif self.radioButton15.isChecked():
            interval = "minute15"
        elif self.radioButton30.isChecked():
            interval = "minute30"
        elif self.radioButton60.isChecked():
            interval = "minute60"
        elif self.radioButton240.isChecked():
            interval = "minute240"
        elif self.radioButtonDay.isChecked():
            interval = "day"

        if tradingRange and interval:
            self.bot.firstSetting(tradingRange, interval)
            return True
        else:
            return False

    def startBot(self):
        if not self.checkSetting():
            self.popup("설정값을 확인하세요.")
            return

        if not self.bot.isRunning:
            self.bot.start()

    def stopBot(self):
        self.bot.stopBot()
        self.popup("봇 종료")

    def popup(self, message):
        """
        팝업박스
        :param message:
        :return:
        """
        QMessageBox.information(self, "알림", message)


class Bot(QThread):
    def __init__(self):
        super(Bot, self).__init__()
        self.isRunning = False
        self.schedule = BlockingScheduler()

        """
        API key
        """
        self.access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
        self.secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
        self.upbit = pyupbit.Upbit(self.access, self.secret)

    def run(self):
        """
        봇 실행
        :return:
        """
        if self.interval == "minute1":
            self.schedule.add_job(self.getPriceInfomation, 'cron', minute="*/1", second="2", id='job')
        if self.interval == "minute3":
            self.schedule.add_job(self.getPriceInfomation, 'cron', minute="*/3", second="2", id='job')
        if self.interval == "minute5":
            self.schedule.add_job(self.getPriceInfomation, 'cron', minute="*/5", second="2", id='job')
        if self.interval == "minute10":
            self.schedule.add_job(self.getPriceInfomation, 'cron', minute="*/10", second="2", id='job')
        if self.interval == "minute15":
            self.schedule.add_job(self.getPriceInfomation, 'cron', minute="*/15", second="2", id='job')
        if self.interval == "minute30":
            self.schedule.add_job(self.getPriceInfomation, 'cron', minute="*/30", second="2", id='job')
        if self.interval == "minute60":
            self.schedule.add_job(self.getPriceInfomation, 'cron', hour="*", second="2", id="job")
        if self.interval == "minute240":
            self.schedule.add_job(self.getPriceInfomation, 'cron', hour="*/4", second="2", id="job")
        if self.interval == "day":
            self.schedule.add_job(self.getPriceInfomation, 'cron', day="*", hour="0", minute="0", second="2", id="job")
        self.schedule.start()

        self.startBot()

    def firstSetting(self, tradingRange, interval):
        self.tradingRange = tradingRange
        self.interval = interval
        self.ticker = "KRW-BTC"
        self.getPriceInfomation()

    def getPriceInfomation(self):
        df = pyupbit.get_ohlcv("KRW-BTC", interval=self.interval)
        period = 20  # 일이 아니라 갯수
        multiplier = 2

        df['MiddleBand'] = df['close'].rolling(period).mean()
        df['UpperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier
        df['LowerBand'] = df['close'].rolling(period).mean() - df['close'].rolling(period).std() * multiplier

        self.MA20 = df.iloc[-1]['MiddleBand']
        self.ceiling = df.iloc[-1]['UpperBand']
        self.bottom = df.iloc[-1]['LowerBand']
        self.previousHighPrice = df.iloc[-1]['high']

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def startBot(self):
        if not self.isRunning:
            self.isRunning = True

        while self.isRunning:
            self.currentPrice = pyupbit.get_current_price(self.ticker)
            status = self.getStatus(self.currentPrice)
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

        buyingCondition = (self.MA20 <= price <= maxBuyingRange) and (self.previousHighPrice < self.MA20)
        sellingCondition = minSellingRange <= price

        print(self.ceiling, minSellingRange, price)

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
            매수
            """
            krwBalance = self.upbit.get_balance()
            if krwBalance < 5000:
                return

            buyResult = self.upbit.buy_market_order(self.ticker, 5000)

        if status == "sell":
            """
            매도
            """
            volume = self.upbit.get_balance(self.ticker)
            tickerBalacne = volume * self.currentPrice

            if tickerBalacne < 5000:
                return

            sellResult = self.upbit.sell_market_order(self.ticker, volume)

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
