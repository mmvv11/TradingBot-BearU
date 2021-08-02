import pyupbit
import pandas as pd
import matplotlib.pyplot as plt

df = pyupbit.get_ohlcv("KRW-PLA", interval="minute1")

multiplier = 2
period = 20  # 일이 아니라 갯수
ratio = 2/3

df['MiddleBand'] = df['close'].rolling(period).mean()
df['UpperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier
df['LowerBand'] = df['close'].rolling(period).mean() - df['close'].rolling(period).std() * multiplier
df['sellingPrice'] = df['MiddleBand'] + (df['UpperBand'] - df['MiddleBand'])* ratio

ax = plt.gca()

df.plot(kind="line", y='MiddleBand', ax=ax)
df.plot(kind="line", y='UpperBand', ax=ax)
df.plot(kind="line", y='LowerBand', ax=ax)
df.plot(kind="line", y='sellingPrice', ax=ax)

plt.show()

