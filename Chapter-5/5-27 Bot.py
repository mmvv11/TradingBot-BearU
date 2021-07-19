import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyupbit
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler

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

        print(1)
        self.bot.firstSetting(interval)
        self.bot.start()
        print(33)

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
    Bot 클래스는 Main 클래스로 부터 설정값(기준봉)을 받아옵니다.
    1초 단위로 대상 코인 시세를 감시하며 매매로직을 수행하겠습니다.

    매매로직

    매수: 이전봉 고가가 중앙선 아래에 있고, 현재 가격은 중앙선을 돌파한 경우
    매도: 현재 가격이 상단 밴드와 중앙선 2/3지점을 돌파하는 경우
    """

    def __init__(self):
        super(Bot, self).__init__()
        """
        실행 상태를 관리할 수 있는 속성
        """
        self.isRunning = False
        """
        private API 호출 객체
        """
        access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
        secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
        self.upbit = pyupbit.Upbit(access, secret)

        """
        대상 코인
        """
        self.ticker = "KRW-BTC"

        """
        스케줄러
        """
        self.scheduler = BackgroundScheduler()

    def run(self):
        self.startBot()

    def startBot(self):
        """
        봇 실행

        1초 단위로 현재 가격 감시, 매매 타이밍 포착
        """
        if not self.isRunning:
            self.isRunning = True

        while self.isRunning:
            self.currentPrice = pyupbit.get_current_price(self.ticker)  # 현재 가격 조회

            status = self.getStatus(self.currentPrice)  # 가격 상태 리턴

            self.tradingLogic(status)  # 가격 상태에 따른 로직 수행

            sleep(1)

    def stopBot(self):
        """
        봇 실행 종료 메서드

        self.isRunnig = False
        스케줄러 취소하기
        :return:
        """
        if self.isRunning:
            self.isRunning = False
            self.scheduler.remove_job("job")

    def getStatus(self, currentPrice):
        """
        현재 가격 상태를 반환합니다.

        매수 타이밍 : buy
        매도 타이밍: sell
        나머지: None
        """
        minSellingPrice = self.MA20 + (self.ceiling - self.MA20) * 2 / 3

        buyingCondition = (currentPrice >= self.MA20) and (self.previousHighPrice < self.MA20)
        sellingContion = currentPrice >= minSellingPrice

        if buyingCondition:
            return "buy"
        if sellingContion:
            return "sell"
        return None

    def tradingLogic(self, status):
        """
        매매로직 수행 메서드
        """
        if not status:
            return

        # 매수 로직 수행
        if status == "buy":
            krwBalance = self.upbit.get_balance()
            if krwBalance < 5000:
                return

            buyResult = self.upbit.buy_market_order(self.ticker, krwBalance)

        # 매도 로직 수행
        if status == "sell":
            volume = self.upbit.get_balance(self.ticker)
            tickerBalance = volume * self.currentPrice

            if tickerBalance < 5000:
                return

            sellReuslt = self.upbit.sell_market_order(self.ticker, volume)

    def firstSetting(self, interval):
        """
        초기값 셋팅

        기준봉: interval
        초기 데이터 계산: 상단밴드, 중앙밴드, 이전 고가 데이터
        스케줄: 기준봉에 따라 데이터를 업데이트
        """
        self.interval = interval
        print("여기?1")
        self.getPriceInfomation()
        print("여기?2")

        if self.interval == "minute1":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', minute="*/1", second="2", id="job")
        if self.interval == "minute3":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', minute="*/3", second="2", id="job")
        if self.interval == "minute5":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', minute="*/5", second="2", id="job")
        if self.interval == "minute10":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', minute="*/10", second="2", id="job")
        if self.interval == "minute15":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', minute="*/15", second="2", id="job")
        if self.interval == "minute30":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', minute="*/30", second="2", id="job")
        if self.interval == "minute60":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', hour="*", second="2", id="job")
        if self.interval == "minute240":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', hour="*/4", second="2", id="job")
        if self.interval == "day":
            self.scheduler.add_job(self.getPriceInfomation, 'cron', day="*", hour="0", minute="0", second="2", id="job")

        self.scheduler.start()


    def getPriceInfomation(self):
        """
        기준봉에 따라 데이터를 업데이트 하는 메서드
        :return:
        """
        data = pyupbit.get_ohlcv(self.ticker, interval=self.interval)

        period = 20
        multiplier = 2

        data['middle'] = data['close'].rolling(period).mean()
        data['upper'] = data['close'].rolling(period).mean() + data['close'].rolling(period).std() * multiplier

        self.MA20 = data.iloc[-1]['middle']
        self.ceiling = data.iloc[-1]['upper']
        self.previousHighPrice = data.iloc[-1]['high']


app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()
