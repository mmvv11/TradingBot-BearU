import pyupbit
from apscheduler.schedulers.background import BackgroundScheduler

# access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
access = "gXP6ewHuDQQbGp925ieK83APklqExT6BUx4oHXYa"
# secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
secret = "oCqRyS1tTexJZTxRSDywYndGkxQEmr78pXV2k11l"
upbit = pyupbit.Upbit(access, secret)

a = 1


def t():
    print(a)


t()

# schedule = BackgroundScheduler()
#
# def a():
#     print(1)
#
# schedule.add_job(a, 'cron', second="*/3", id="job")
#
# schedule.start()
#
# print("hi1")
#
# schedule.remove_job("job")
#
# schedule.add_job(a, 'cron', second="*/3", id="job")
#
# schedule.start()
#
# print("hi222")
#


import pyupbit
import pandas as pd
import matplotlib.pyplot as plt

df = pyupbit.get_ohlcv("KRW-PLA", interval="minute1")

multiplier = 2
period = 20  # 일이 아니라 갯수

df['MiddleBand'] = df['close'].rolling(period).mean()
df['UpperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier
df['LowerBand'] = df['close'].rolling(period).mean() - df['close'].rolling(period).std() * multiplier
print(df)
# df['sellingPrice'] = df['MiddleBand'] + (df['UpperBand'] - df['MiddleBand'])*(2/3)
#
# ax = plt.gca()
#
# df.plot(kind="line", y='MiddleBand', ax=ax)
# df.plot(kind="line", y='UpperBand', ax=ax)
# df.plot(kind="line", y='LowerBand', ax=ax)
# df.plot(kind="line", y='sellingPrice', ax=ax)
#
# plt.show()
#
# plt.savefig('fig1.png', dpi=300)

access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
# access = "gXP6ewHuDQQbGp925ieK83APklqExT6BUx4oHXYa"
secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
# secret = "oCqRyS1tTexJZTxRSDywYndGkxQEmr78pXV2k11l"

upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance())