# 문법을 모두 활용해 지속적인 가격 감시

from time import sleep # 코드 진행 일시정지
from random import randrange # 랜덤 정수 생성

# 평균매수가격, 목표가격, 손절가격 설정
averagePrice = 105
targetPrice = 109
stopLossPrice = 101

# 함수 정의
def getRightTiming():
    """
    1. currentPrice에 100과 110 사이의 랜덤 정수를 할당할 것
    2. 현재가격(currentPrice)를 2초 단위로 갱신하며 감시할 것
    3. 현재가격과 목표가격, 손절가격을 비교하며 print문으로 매도 실행 여부를 표시할 것
    """
    while True:
        currentPrice = randrange(100, 110)
        if currentPrice >= targetPrice:
            print(f"현재 가격 {currentPrice} 목표가 달성 매도 실행")
        elif currentPrice <= stopLossPrice:
            print(f"현재 가격 {currentPrice} 손절가격 달성 매도 실행")
        else:
            print(f"현재 가격 {currentPrice}")
        sleep(2)

getRightTiming()





