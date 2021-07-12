# 조건문을 이용. 매수, 매도 조건 판단

averagePrice = {"BTC": 200, "ETH": 100}
currentPrice = {"BTC": 300, "ETH": 80}

# 매도, 익절, 손절
    # 익절, 20% 이상 수익률
    # 손절, 5% 이상 손해

avgBTC = averagePrice["BTC"]
avgETH = averagePrice["ETH"]

currentBTC = currentPrice["BTC"]
currentETH = currentPrice["ETH"]

# BTC 목표가, 손절가 설정
targetBTC = avgBTC * 1.2
stopLossBTC = avgBTC * 0.95

# ETH 목표가, 손절가 설정
targetETH = avgETH * 1.2
stopLossETH = avgETH * 0.95

# 비트코인 매도 판단
# 익절의 경우
if currentBTC >= targetBTC:
    print("BTC 목표가 달성!")
# 손절의 경우
elif currentBTC <= stopLossBTC:
    print("BTC 손절")

# 이더리움 매도판단
if currentETH >= targetETH:
    print("ETH 목표가 달성!")
# 손절의 경우
elif currentETH <= stopLossETH:
    print("ETH 손절")