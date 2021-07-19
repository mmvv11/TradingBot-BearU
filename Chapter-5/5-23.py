import pandas as pd
import pyupbit
import matplotlib.pyplot as plt

# 업비트 4시간봉 기준 데이터 가져오기
data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240")

# data
data['middle'] = data['close'].rolling(20).mean()
data['upper'] = data['close'].rolling(20).mean() + data['close'].rolling(20).std() * 2
data['lower'] = data['close'].rolling(20).mean() - data['close'].rolling(20).std() * 2
data['selling'] = data['middle'] + (data['upper'] - data['middle']) * (2 / 3)

# csv파일로 저장
# data.to_csv("bollinger-band.csv")

# 시각화
ax = plt.gca()

data.plot(kind="line", y="middle", ax=ax)
data.plot(kind="line", y="upper", ax=ax)
data.plot(kind="line", y="lower", ax=ax)
data.plot(kind="line", y="selling", ax=ax)

plt.show()
