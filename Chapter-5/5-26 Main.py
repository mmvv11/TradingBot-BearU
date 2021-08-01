import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

ui = uic.loadUiType("ui.ui")[0]


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

        # TODO 봇 실행 메서드 호출하기, interval 값 넘기기

    def stopBot(self):
        """
        봇 종료 메서드

        1. 봇이 실행중인지 검사
        2. 봇 종료
        """
        if not self.bot.isRunning:
            return self.popup("실행 상태가 아닙니다.")

        # TODO 봇 종료 메서드 호출하기.
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


class Bot():
    def __init__(self):
        self.isRunning = False


app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()
