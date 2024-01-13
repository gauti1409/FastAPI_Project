def add_num(num1: int, num2: int):
    return num1 + num2


def subtract_num(num1: int, num2: int):
    return num1 - num2


def multiply_num(num1: int, num2: int):
    return num1 * num2


def divide_num(num1: int, num2: int):
    return num1 / num2


"""TESTING CLASSES"""


class Insufficient_funds(Exception):
    pass


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise Insufficient_funds("Insufficient funds in account. ")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
