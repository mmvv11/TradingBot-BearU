"""
매매전략

n초 간격으로 현재가 감시,
상승장 매수 구간, 상승장 매도구간 도달시 매매 이벤트 발생
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
    """
    GUI를 구성하는 메인클래스
    기준봉을 설정하고 봇을 실행, 중지
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        """
        봇 객체
        """
        self.bot = Bot()
        """
        봇 실행
        """
        self.pushButtonStart.clicked.connect(self.startBot)
        """
        봇 중지
        """
        self.pushButtonStop.clicked.connect(self.stopBot)

    def getInterval(self):
        """
        기준봉 값 확인
        :return:
        """
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

        if not interval:
            return False

        return interval

    def startBot(self):
        """
        봇 실행 메서드
        1. 봇이 이미 실행중인지 확인
        2. 기준봉이 설정되어있는지 확인
        3. 봇이 꺼져있다면 실행
        :return:
        """

        if self.bot.isRunning:
            return self.popup("봇이 이미 실행중입니다.")

        interval = self.getInterval()
        if not interval:
            return self.popup("설정값을 확인하세요.")

        self.bot.firstSetting(interval)
        self.bot.start()

    def stopBot(self):
        """
        봇 종료 메서드

        1. 봇이 실행중인지 확인
        2. 봇 종료
        :return:
        """
        if not self.bot.isRunning:
            return self.popup("실행 상태가 아닙니다.")

        self.bot.stopBot()
        return self.popup("봇을 종료합니다.")

    def popup(self, message):
        """
        팝업박스
        :param message:
        :return:
        """
        QMessageBox.information(self, "알림", message)


class Bot(QThread):
    """
    Bot 클래스는 Main 클래스로부터 설정값을 받아온다.
    스레드 형태로 대상 코인 시세를 1초 단위로 감시하며 매매로직을 수행한다.

    매매 로직은 다음과 같다.

    매수: 이전 봉 고가가 중앙선 아래에 있고, 현재 가격이 20선을 돌파한 경우
    매도: 현재 가격이 상단 밴드와 중앙선 2/3지점을 돌파한 경우
    """

    def __init__(self):
        super(Bot, self).__init__()
        """
        실행상태를 관리할 수 있는 속성
        """
        self.isRunning = False
        """
        기준봉에 따라 데이터를 업데이트하기 위한 스케줄러
        """
        self.schedule = BlockingScheduler()
        """
        Private API를 요청하기 위한 객체 생성
        """
        access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
        secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
        self.upbit = pyupbit.Upbit(access, secret)

    def run(self):
        """
        봇 실행
        """
        self.startBot()

    def firstSetting(self, interval):
        """
        초기값 세팅

        기준봉 : interval
        대상코인 : ticker
        초기 데이터: 상단밴드, 중앙밴드, 이전고가 데이터
        스케줄 : 기준봉에 따라 상단밴드, 중앙밴드, 이전고가 데이터 업데이트
        """
        self.interval = interval
        self.ticker = "KRW-BTC"
        self.getPriceInfomation()

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

    def getPriceInfomation(self):
        """
        기준봉에 따라 상단밴드, 중앙선, 이전 고가 데이터를 가져오는 메서드
        """
        df = pyupbit.get_ohlcv("KRW-BTC", interval=self.interval)
        period = 20  # 일이 아니라 갯수
        multiplier = 2

        df['middleBand'] = df['close'].rolling(period).mean()
        df['upperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier

        self.MA20 = df.iloc[-1]['middleBand']
        self.ceiling = df.iloc[-1]['upperBand']
        self.previousHighPrice = df.iloc[-1]['high']

    def startBot(self):
        """
        봇 실행

        1초 단위로 가격을 감시하고 매매타이밍을 포착
        """
        if not self.isRunning:
            self.isRunning = True

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        while self.isRunning:
            self.currentPrice = pyupbit.get_current_price(self.ticker) # 가격 조회
            status = self.getStatus(self.currentPrice) # 가격 상태 조회
            self.tradingLogic(status) # 가격 상태에 따른 로직 수행
            sleep(1)

    def stopBot(self):
        """
        봇 실행 종료 메서드
        
        isRunning => false
        스케줄러 취소하기
        """
        if self.isRunning:
            self.isRunning = False
            self.schedule.remove_job("job")
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def getStatus(self, price):
        """
        현재 가격 상태 반환

        매수 타이밍 => buy
        매도 타이밍 => sell
        나머지 => None
        """
        minSellingRange = self.MA20 + (self.ceiling - self.MA20) * (2 / 3)

        buyingCondition = (self.MA20 <= price) and (self.previousHighPrice < self.MA20)
        sellingCondition = minSellingRange <= price

        if buyingCondition:
            return "buy"
        if sellingCondition:
            return "sell"
        return None

    def tradingLogic(self, status):
        """
        매매로직 수행
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

            # if (not buyResult) or ("error" in buyResult):
            #     logger.error(f"매수 API 에러 {buyResult}")
            #     return False
            #
            # logger.info(f"매수 주문 {buyResult}")

        if status == "sell":
            """
            매도
            """
            volume = self.upbit.get_balance(self.ticker)
            tickerBalacne = volume * self.currentPrice

            if tickerBalacne < 5000:
                return

            sellResult = self.upbit.sell_market_order(self.ticker, volume)

            # if (not sellResult) or ("error" in sellResult):
            #     logger.error(f"매도 API 에러 {sellResult}")
            #     return False
            #
            # logger.info(f"매도 주문 {sellResult}")


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
