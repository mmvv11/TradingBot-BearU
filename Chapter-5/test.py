import pyupbit

access = "8eIUpONfW2eGzRFrcmcSWVU4CBLzvJ9f8rfiPCh8"
secret = "FZatuQ65in9k1rmd8DOIxmzAiLGAvxR6E1dwL3p5"
upbit = pyupbit.Upbit(access, secret)

v = upbit.get_balance("KRW-BTC")

p = pyupbit.get_current_price()

vv = 5000/p

print(vv)
