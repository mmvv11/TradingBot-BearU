"""
반복문
"""

# for

# for i in [1, 2, 3]:
#     print(i)
#
# for i in "가나다라":
#     print(i)
#
# for i in {"a": 1, "b": 2}:
#     print(i)

# empty = []
#
# for i in range(1, 11):
#     empty.append(i)
#
# print(empty)

# while

# num = 1  # 초기조건
# while num < 11:  # 종료조건
#     print(num)
#     num = num + 1  # 증감조건

# empty = []
#
# num = 1
#
# while num < 11:
#     empty.append(num)
#     num += 1
#
# print(empty)

# 1. break: 반복문 탈출
# 2. continue: 해당 반복 스킵

num = 1

while num < 11:
    print(1)
    if num == 5:
        print(1)
        continue

    print(num)
    print(1)
    num += 1
    print(1)