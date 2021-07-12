"""
함수
"""


# 선언
# y = 2x+1

# def y(x):
#     result = 2*x+1
#     return result
#
# print(y(3))
# print(y(1))

# return

# def return_test(number):
#     for i in range(1, number+1):
#         print(i)
#         if i >= 10:
#             return
#
# return_test(50)


# BMI 지수 계산
# bmi = 체중(kg) / 신장*신장(m)

def BMIIndex(weight, height):
    height = height / 100  # m단위 변환
    bmi = weight / (height*height)
    
    if bmi < 18.5:
        return "저체중"
    elif 18.5 <= bmi < 23:
        return "정상"
    elif 23 <= bmi < 25:
        return "과체중"
    elif 25 <= bmi < 30:
        return "경도비만"
    elif bmi >= 30:
        return "고도비만"

result = BMIIndex(78, 150)
print(result)