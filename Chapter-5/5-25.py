import pyupbit
import pandas as pd
import matplotlib.pyplot as plt

access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
upbit = pyupbit.Upbit(access, secret)
pd.options.display.float_format = '{:.1f}'.format


def isBullMarket(interval):
    df = pyupbit.get_ohlcv("KRW-BTC", interval=interval)
    period = 20  # 일이 아니라 갯수
    df['MiddleBand'] = df['close'].rolling(period).mean()
    MA20 = df.iloc[-1]['MiddleBand']
    currentPrice = pyupbit.get_current_price()

    if currentPrice > MA20:
        return True
    else:
        return False


"""
시각화 예시
"""
df = pyupbit.get_ohlcv("KRW-BTC", interval="minute240")

multiplier = 2
period = 20  # 일이 아니라 갯수

df['MiddleBand'] = df['close'].rolling(period).mean()
df['UpperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier
df['LowerBand'] = df['close'].rolling(period).mean() - df['close'].rolling(period).std() * multiplier

ax = plt.gca()

df.plot(kind="line", y='MiddleBand', ax=ax)
df.plot(kind="line", y='UpperBand', ax=ax)
df.plot(kind="line", y='LowerBand', ax=ax)

plt.show()

"""
매매전략

n초 간격으로 현재가 감시, 
상승장 매수 구간, 상승장 매도구간 도달시 매매 이벤트 발생

상승장 매수: 이전 봉 종가 20선 아래에 있을 때, 20선 +n% 범위에서 매수
상승장 매도: 천장 +-n% 범위에서 매도
"""

from time import sleep


class Bot():
    def __init__(self):
        """
        20선, 천장, 바닥 가격을 속성으로 가지고 있어야함
        +-n% 범위를 속성으로 가지고 있어야함
        """
        self.MA20 = 1
        self.ceiling = 1
        self.bottom = 1
        self.tradingRange = 1
        self.previousClosePrice = 1

    def startBot(self):
        while True:
            currentPrice = pyupbit.get_current_price()
            status = self.getStatus(currentPrice)
            self.tradingLogic(status)
            sleep(1)

    def getStatus(self, price):
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
        if not status:
            return
        if status == "buy":
            """
            풀매수
            """
        if status == "sell":
            """
            풀매도
            """

        # def bullTradingLogic():
#     """
#     상승장 매매 전략
#     """
#
# def bearTradingLogic():
#     """
#     하락장 매매 전략
#     """
