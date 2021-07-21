from threading import Thread
from time import sleep

def example():
    while True:
        print("반복문")
        sleep(2)

"""
싱글 스레드 경우
"""
print("안녕")

example()

print("잘가")

"""
멀티 스레드를 사용한 경우
"""
print("안녕")

t = Thread(target=example)
t.start()

print("잘가")
