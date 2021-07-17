import pyupbit
import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.1f}'.format
access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
upbit = pyupbit.Upbit(access, secret)

period = 20
multiplier = 2

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60")
df['middleBand'] = df['close'].rolling(period).mean()
df['upperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier

"""
천장-n% 계산 컬럼, 매수조건 부합, 매도조건 부합, 
"""
df['sellingPrice'] = df['upperBand'] * 0.995
# 현재봉 고가가 이전봉 ma20이상 and 이전봉 고가는 이전봉 ma20아래에 있을 것
# buyingCondition = (df['middleBand'].shift(1) <= df['high']) and (df['high'].shift(1) < df['middleBand'].shift(1))
df['matchForBuying'] = np.where((df['middleBand'].shift(1) <= df['high']) & (df['high'].shift(1) < df['middleBand'].shift(1)), "buy", "")
# 현재봉 고가가 이전봉 sellingPrice 이상.
# sellingCondition = df['high'] >= df['sellingPrice'].shift(1)
df['matchForSelling'] = np.where(df['high'] >= df['sellingPrice'].shift(1), "sell", "")

df = df[['high', 'close', 'middleBand', 'upperBand', 'sellingPrice', 'matchForBuying', 'matchForSelling']]

df.to_csv("data.csv", encoding='utf-8')
