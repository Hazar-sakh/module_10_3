from threading import Thread, Lock
from time import sleep
from random import randint


class Bank(Thread):

    def __init__(self):
        self.balance = 0
        self.lock = Lock()
        super().__init__()

    def deposit(self):
        for i in range(0, 100):
            depo_cash = randint(50, 500)
            self.balance += depo_cash
            if self.balance > 500 and self.lock.locked():
                self.lock.release()
            print(f'Пополнение: {depo_cash}. Баланс: {self.balance}')
            sleep(0.001)

    def take(self):
        for i in range(0, 100):
            take_cash = randint(50, 500)
            print(f'Запрос на {take_cash}')
            if take_cash > self.balance:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            else:
                self.balance -= take_cash
                print(f'Снятие: {take_cash}. Баланс: {self.balance}')


bk = Bank()

th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
