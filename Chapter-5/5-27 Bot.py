import sys
from apscheduler.schedulers.background import BackgroundScheduler
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyupbit

from time import sleep

ui = uic.loadUiType("5-25.ui")[0]


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
        - 현재 가격을 조회
        - 가격 상태 판단
        - 매매 수행
    4. 봇 중지
        - 봇 중지
        - 스케줄러 중지
    """

    def __init__(self):
        super().__init__()
        self.isRunning = False

        """
        private API 객체
        """
        access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
        secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
        self.upbit = pyupbit.Upbit(access, secret)

        """
        기준 코인
        """
        self.ticker = "KRW-BTC"

    def run(self):
        self.startBot()

    def firstSetting(self, interval):
        isValidAPI = self.upbit.get_balance()

        if not isValidAPI:
            return False

        # 1. Main 클래스로부터 interval 값 가져오기 (기준봉)
        self.interval = interval
        self.updatePriceInfo()

        """
        updatePriceInfo 메서드를 호출하는 스케줄러
        """
        self.scheduler = BackgroundScheduler()

        if self.interval == "minute1":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*", second="2", id="job")
        if self.interval == "minute3":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/3", second="2", id="job")
        if self.interval == "minute5":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/5", second="2", id="job")
        if self.interval == "minute10":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/10", second="2", id="job")
        if self.interval == "minute15":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/15", second="2", id="job")
        if self.interval == "minute30":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/30", second="2", id="job")
        if self.interval == "minute60":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', hour="*", second="2", id="job")
        if self.interval == "minute240":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', hour="1-23/4", second="2", id="job")
        if self.interval == "day":
            self.scheduler.add_job(self.updatePriceInfo, 'cron', day="*", hour="0", minute="0", second="2", id="job")

        self.scheduler.start()

        return True

    def updatePriceInfo(self):
        # 2. 필요한 데이터 요청하고 계산하기 (상단 밴드, 중간 밴드, 매도 가격) -> 스케줄러 사용
        data = pyupbit.get_ohlcv(self.ticker, interval=self.interval)

        period = 20
        multiplier = 2

        data['middle'] = data['close'].rolling(period).mean()  # 중간밴드
        data['upper'] = data['close'].rolling(period).mean() + data['close'].rolling(20).std() * multiplier  # 상단밴드

        self.middle = data.iloc[-2]['middle']  # 이전봉 중간밴드 값
        self.upper = data.iloc[-2]['upper']  # 이전봉 상단밴드 값
        self.prevHighPrice = data.iloc[-2]['high']  # 이전봉 종가

    def startBot(self):
        """
        3. 봇 실행
        - 현재 가격을 조회
        - 가격 상태 판단
        - 매매 수행
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
        현재 가격 상태 반환

        매수: 이전봉 고가는 중간밴드 아래, 현재가격이 중간밴드를 돌파
        매도: 상단밴드와 중간밴드의 2/3 돌파

        매수 타이밍: buy
        매도 타이밍: sell
        나머지: None
        """

        targetPrice = self.middle + (self.upper - self.middle) * 2 / 3

        buyingCondition = (currentPrice > self.middle) and (self.prevHighPrice < self.middle)
        sellingCondition = currentPrice >= targetPrice

        if buyingCondition:
            return "buy"
        if sellingCondition:
            return "sell"

        return None

    def tradingLogic(self, status):
        if not status:
            return

        if status == "buy":
            # 매수
            balance = self.upbit.get_balance()

            if balance < 5000:
                return

            self.upbit.buy_market_order(self.ticker, balance * 0.99)

        if status == "sell":
            # 매도
            volume = self.upbit.get_balance(self.ticker)
            balance = volume * self.currentPrice

            if balance < 5000:
                return

            self.upbit.sell_market_order(self.ticker, volume)

    def stopBot(self):
        """
        봇 중지

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
