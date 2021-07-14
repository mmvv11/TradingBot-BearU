# import pyupbit
#
# # 시세조회 API
# btcPrice = pyupbit.get_current_price("KRW-BTC")
# print(f"비트코인 시세: {btcPrice}")
#
# # 시장가 매수, 매도 API 호출
# access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
# secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
# upbit = pyupbit.Upbit(access, secret)
#
# ticker = "KRW-BTC"
# buyPrice = 5000
# sellPrice = 6000
#
# buyResult = upbit.buy_market_order(ticker, buyPrice)
# sellResult = upbit.sell_market_order(ticker, sellPrice)
#
# print(buyResult)
# print(sellResult)
#

a = None

if not a:
    print(1)