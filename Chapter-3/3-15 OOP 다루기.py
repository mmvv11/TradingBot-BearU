# 클래스 선언
# 속성과 생성자
# 메서드
# 객체생성
# 상속

# class AirPlain:
#     def __init__(self, departure, arrival):
#         self.departure = departure
#         self.arrival = arrival
#
#     def broadcast(self):
#         print(f"이 비행기의 출발지는 {self.departure}입니다. 도착지는 {self.arrival}입니다.")
#
#
# class CombatAirPlain(AirPlain):
#     def __init__(self, departure, arrival, missile):
#         super().__init__(departure, arrival)
#         self.missile = missile
#
#     def attack(self):
#         print("공격 기능을 수행합니다.")
#
#
# a = CombatAirPlain("서울", "부산", 1)
#
# a.attack()



class User:
    def __init__(self, name, phone, age):
        self.name = name
        self.phone = phone
        self.age = age

    def basicInfo(self):
        print(f"""
        이름: {self.name}
        휴대폰: {self.phone}
        나이: {self.age}
        """)


# 실행예시

man = User("홍길동", "010-1234-1234", 30)
man.basicInfo()

# 결과
# 이름: 홍길동
# 휴대폰: 010-1234-1234
# 나이: 30