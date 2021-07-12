"""
연산자, 조건문
"""

# 논리 연산자

# or
# print((1==1) or (1 == 3)) # True
#
# # and
# print((1==1) and (1 == 3)) # False
#
# # not
# print(not(True))


# 조건문

# 단일 조건
existID = "a123"
existPassword = "qwer1234"

newID = "a12"
newPassword = "qwer124"

# if (existID == newID) and (existPassword == newPassword):
#     print("로그인 성공")

# 다중 조건

if (existID == newID) and (existPassword == newPassword):
    print("로그인 성공")
elif  (existID == newID) and (existPassword != newPassword):
    print("비밀번호를 잘못 입력 했습니다.")
else:
    print("존재하지 않는 아이디입니다.")

