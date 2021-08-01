import pyupbit
import pandas as pd

period = 20
multiplier = 2

"""
백테스트에 필요한 데이터 가져오기
"""
df = pyupbit.get_ohlcv("KRW-PLA", interval="minute30")
df['middle'] = df['close'].rolling(period).mean()  # 중간밴드
df['upper'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier  # 상단밴드
df['sellingPrice'] = df['middle'] + (df['upper'] - df['middle']) * 1  # 목표가 밴드

"""
비교를 쉽게하기 위해 같은 행에 이전 데이터 값을 불러오기
"""
df['prevHigh'] = df['high'].shift(1)
df['prevMiddle'] = df['middle'].shift(1)
df['prevClose'] = df['close'].shift(1)
df['prevSellingPrice'] = df['sellingPrice'].shift(1)

"""
매수, 매도 조건 판단
"""
df['isBuying'] = (df['prevMiddle'] <= df['high']) & (df['prevHigh'] < df['prevMiddle'])
df['isSelling'] = df['high'] >= df['prevSellingPrice']

# df.to_csv("data.csv")

isValidBuy = True
isValidSell = False

def getROR(row):
    global isValidBuy, isValidSell, buyingPrice, sellingPrice

    # 매수
    if (row['prevMiddle'] <= row['high']) & (row['prevHigh'] < row['prevMiddle']) & isValidBuy:
        isValidBuy = False
        isValidSell = True
        buyingPrice = row['prevMiddle']
    # 매도
    if (row['high'] >= row['prevSellingPrice']) & isValidSell:
        isValidBuy = True
        isValidSell = False
        sellingPrice = row['prevSellingPrice']
        return sellingPrice/buyingPrice

    return 1


df['ror'] = df.apply(getROR, axis=1)

# df.to_csv("data2.csv")

ror = df['ror'].cumprod()[-1]

print(ror)