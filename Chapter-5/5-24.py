import pyupbit
import pandas as pd


"""
이동평균선으로 상승장 판단하기

20 평균선을 기준으로 한다.
20선 위에 있다면 상승장 판단
20선 아래에 있다면 하락장 판단
"""

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


print(isBullMarket("month"))


