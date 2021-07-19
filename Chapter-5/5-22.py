import pandas as pd
import pyupbit

# 업비트 데이터 가져오기
data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240")
data['movingAverage20'] = data['close'].rolling(20).mean()
data.to_csv("upbitData.csv")

# 종가를 기준으로 이동평균 구하기