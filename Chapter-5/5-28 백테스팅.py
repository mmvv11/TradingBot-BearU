import pyupbit
import pandas as pd

pd.options.display.float_format = '{:.1f}'.format
access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
upbit = pyupbit.Upbit(access, secret)

period = 20
multiplier = 2
ratio = 1

isValidBuy = True
isValidSell = False

"""
백테스트에 필요한 데이터 가져오기. 4시간봉
"""
df = pyupbit.get_ohlcv("KRW-BTC", interval="minute240")
df['middleBand'] = df['close'].rolling(period).mean()  # 중간 밴드
df['upperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier  # 상단 밴드
df['sellingPrice'] = df['middleBand'] + (df['upperBand'] - df['middleBand']) * ratio  # 목표가 밴드

"""
비교를 쉽게하기 위해 같은 행에 이전 데이터 값을 불러오기
"""
df['prevHigh'] = df['high'].shift(1)
df['prevMiddle'] = df['middleBand'].shift(1)
df['prevClose'] = df['close'].shift(1)
df['prevSellingPrice'] = df['sellingPrice'].shift(1)

df['isBuying'] = (df['prevMiddle'] <= df['high']) & (df['prevHigh'] < df['prevMiddle'])
df['isSelling'] = df['high'] >= df['prevSellingPrice']


# df.to_csv("show.csv")  # csv 파일로 만들기


def getROR(row):
    """
    기대 수익률 계산 함수
    """
    global isValidBuy, isValidSell, buyingPrice, sellingPrice

    # 매수
    if (row['prevMiddle'] <= row['high']) & (row['prevHigh'] < row['prevMiddle']) & isValidBuy:
        isValidBuy = False
        isValidSell = True
        buyingPrice = row['prevMiddle']  # 매수가격은 이전 중간밴드

    # 매도
    if (row['high'] >= row['prevSellingPrice']) & isValidSell:
        isValidBuy = True
        isValidSell = False
        sellingPrice = row['prevSellingPrice']  # 매도 가격은 이전 판매 목표가

        return sellingPrice / buyingPrice  # 수익률 = 매도가/매수가

    return 1  # 매도가 일어나지 않은 경우엔 1


# dataframe의 apply 메서드를 적용하면 각 행의 값을
df['ror'] = df.apply(getROR, axis=1)

# 열의 모든 값을 곱하는 cumprod 메서드
ror = df['ror'].cumprod()[-1]

# 백테스팅 수익률 계산 결과
print(ror)
