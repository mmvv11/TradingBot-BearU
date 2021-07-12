# 파이썬 문법 - variable, data type.. etc

"""
변수
"""

# 변수명 = 변수에 넣고 싶은 데이터

a = 1
# print(a)


"""
Data Type
"""

# 1. 숫자

# 숫자 사칙연산
num = 2
num2 = 3

# print(num + num2) # 더하기
# print(num - num2) # 빼기
# print(num * num2) # 곱하기
# print(num / num2) # 나누기
# print(num // num2) # 몫
# print(num % num2) # 나머지

# int, float type

# print(type(3)) # int
# print(type(3.1)) # float


# 2. 문자열

# 선언

str = "안녕하세요"
str2= '안녕하세요-2'


# 문자 인덱싱, 슬라이싱
# print(str[0]) # 인덱싱
# print(str[0:2]) # 슬라이싱


# 3. bool

# 선언
True
False


# 비교연산 ==, !=, >, <=

# print(1 == 1) # True
# print(1 != 1) # False
# print(3 < 1) # False
# print(3 <= 4) # True


# 4. 리스트

# CRUD

# create
# arr = ["a", "b", "c", 1, 3]
# print(arr)
#
# # read
# print(arr[0:3])
#
# # update
# arr[0] = "A"
# print(arr)
#
# # delete
# del arr[0]
# print(arr)


# 5. 딕셔너리

# CRUD

# create
userList = {"김철수": 123, "박민수": 345}

# read
print(userList["박민수"])

# update
userList["김철수"] = "a123123"
print(userList)

# delete
del userList['김철수']
print(userList)
