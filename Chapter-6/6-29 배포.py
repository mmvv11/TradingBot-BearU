import os
import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyupbit
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger


def resourcePath(relativePath):
    basePath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(basePath, relativePath)


uiPath = resourcePath('ui.ui')
ui = uic.loadUiType(uiPath)[0]


class Main(QMainWindow, ui):
    """
    GUI를 구성합니다.

    기준봉을 설정하고, 봇을 실행, 중지
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

    def startBot(self):
        """
        봇 실행 메서드

        1. 봇이 이미 실행 중인가 확인
        2. 기준봉이 설정되어 있는가 확인
        3. 봇이 꺼져있으면 실행시킨다.
        """

        if self.bot.isRunning:
            return self.popup("봇이 이미 실행 중입니다.")

        interval = self.getInterval()

        if not interval:
            return self.popup("기준봉을 설정해주세요.")

        isValidStart = self.bot.firstSetting(interval)

        if not isValidStart:
            return self.popup("유효한 API키가 아닙니다.")

        self.bot.start()

    def stopBot(self):
        """
        봇 종료 메서드

        1. 봇이 실행중인지 검사
        2. 봇 종료
        """
        if not self.bot.isRunning:
            return self.popup("실행 상태가 아닙니다.")

        self.bot.stopBot()
        return self.popup("봇을 종료합니다.")

    def getInterval(self):
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

        # 아무것도 체크하지 않은 경우
        if not interval:
            return False

        return interval

    def popup(self, message):
        QMessageBox.information(self, "알림", message)


class Bot(QThread):
    """
    1. Main 클래스로부터 interval 값 가져오기 (기준봉)
    2. 필요한 데이터 요청하고 계산하기 (상단 밴드, 중간 밴드, 매도 가격) -> 스케줄러 사용
    3. 봇 실행
        - 현재 가격 조회
        - 가격 상태 판단
        - 매매 수행
    4. 봇 중지
        - 봇 중지
        - 스케줄러 중지
    """

    def __init__(self):
        super(Bot, self).__init__()
        self.isRunning = False

        """
        private API 객체
        """
        access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
        # access = "gXP6ewHuDQQbGp925ieK83APklqExT6BUx4oHXYa"
        secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
        # secret = "oCqRyS1tTexJZTxRSDywYndGkxQEmr78pXV2k11l"
        self.upbit = pyupbit.Upbit(access, secret)

        """
        대상 코인
        """
        self.ticker = "KRW-BTC"

    def run(self):
        self.startBot()

    def firstSetting(self, interval):
        isValidAPI = self.upbit.get_balance()

        if not isValidAPI:
            return False

        self.interval = interval
        self.updatePriceInfo()

        """
        기준봉에 따라 데이터를 주기적으로 갱신하는 스케줄러
        """
        self.scheduler = BackgroundScheduler()

        if self.interval == "minute1":
            trigger = OrTrigger([CronTrigger(minute="*", second="2")])
        if self.interval == "minute3":
            trigger = OrTrigger([CronTrigger(minute="*/3", second="2")])
        if self.interval == "minute5":
            trigger = OrTrigger([CronTrigger(minute="*/5", second="2")])
        if self.interval == "minute10":
            trigger = OrTrigger([CronTrigger(minute="*/10", second="2")])
        if self.interval == "minute15":
            trigger = OrTrigger([CronTrigger(minute="*/15", second="2")])
        if self.interval == "minute30":
            trigger = OrTrigger([CronTrigger(minute="*/30", second="2")])
        if self.interval == "minute60":
            trigger = OrTrigger([CronTrigger(hour="*", second="2")])
        if self.interval == "minute240":
            trigger = OrTrigger([CronTrigger(hour="*/4", second="2")])
        if self.interval == "day":
            trigger = OrTrigger([CronTrigger(day="*", hour="0", minute="0", second="2")])

        self.scheduler.add_job(self.updatePriceInfo, trigger, id="job")
        self.scheduler.start()

        return True

    def updatePriceInfo(self):

        data = pyupbit.get_ohlcv(self.ticker, interval=self.interval)

        period = 20
        multiplier = 2

        data['middle'] = data['close'].rolling(period).mean()
        data['upper'] = data['close'].rolling(period).mean() + data['close'].rolling(period).std() * multiplier

        self.MA20 = data.iloc[-1]['middle']
        self.upper = data.iloc[-1]['upper']
        self.previousHighPrice = data.iloc[-1]['high']

    def startBot(self):
        """
        봇 실행

        1초 단위로 가격을 감시하고 매매타이밍 포착
        """

        if not self.isRunning:
            self.isRunning = True

        while self.isRunning:
            self.currentPrice = pyupbit.get_current_price(self.ticker)  # 현재 가격 조회
            status = self.getStatus(self.currentPrice)  # 현재 가격 상태 조회
            self.tradingLogic(status)  # 매매 로직 수행하기
            sleep(1)

    def getStatus(self, currentPrice):
        """
        현재 가격 상태 반환 메서드

        매수: 이전봉 고가는 20선 아래에 있고, 현재 가격이 20선을 돌파한 경우
        매도: 상단밴드와 중간밴드의 2/3지점을 돌파

        매수 타이밍 : buy
        매도 타이밍: sell
        나머지: None
        """

        minSellingPrice = self.MA20 + (self.upper - self.MA20)

        buyingCondition = (self.MA20 <= currentPrice) and (self.previousHighPrice < self.MA20)
        sellingCondition = currentPrice >= minSellingPrice

        print(f"MA20:{self.MA20}, upper:{self.upper}, prevHigh: {self.previousHighPrice}")

        if buyingCondition:
            print("buy")
            return "buy"
        if sellingCondition:
            print("sell")
            return "sell"
        print("none")
        return None

    def tradingLogic(self, status):
        if not status:
            return

        if status == "buy":
            balance = self.upbit.get_balance()
            if balance < 5000:
                return

            # 수수료를 감안하여 balance에 0.99를 곱함
            buyResult = self.upbit.buy_market_order(self.ticker, balance * 0.99)

        if status == "sell":
            volume = self.upbit.get_balance(self.ticker)
            balance = volume * self.currentPrice
            if balance < 5000:
                return

            sellReult = self.upbit.sell_market_order(self.ticker, volume)

    def stopBot(self):
        """
        - 봇 중지
        - 스케줄러 중지
        """
        if self.isRunning:
            self.isRunning = False
            self.scheduler.remove_job("job")


app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()
