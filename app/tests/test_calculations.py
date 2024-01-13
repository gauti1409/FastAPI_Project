from app.calculations import add_num, subtract_num, multiply_num, divide_num, BankAccount, Insufficient_funds
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def initial_balance_bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected_value",
                         [(3, 2, 5), (4, 2, 6), (9, 10, 19), (12, 14, 26)])
def test_add(num1, num2, expected_value):
    print("testing add function")
    assert add_num(num1, num2) == expected_value


def test_subtract():
    assert subtract_num(5, 3) == 2


def test_multiply():
    assert multiply_num(5, 3) == 15


def test_divide():
    assert divide_num(4, 2) == 2


"""The fixture here calls the function zero_bank_Account before it runs the test case. So it calls the function and then whatever we return in 
the fixture above will get passed into the variable called zero_bank_account in the function test_bank_default_amount. So in this way,
we don't have to create an instance for the BankAccount class everytime we define a new function for testing. """


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_set_initial_amount(initial_balance_bank_account):
    assert initial_balance_bank_account.balance == 50


def test_bank_withdraw(initial_balance_bank_account):
    initial_balance_bank_account.withdraw(20)
    assert initial_balance_bank_account.balance == 30


def test_bank_deposit(initial_balance_bank_account):
    initial_balance_bank_account.deposit(100)
    assert initial_balance_bank_account.balance == 150


def test_bank_interest_amount(initial_balance_bank_account):
    initial_balance_bank_account.collect_interest()
    assert initial_balance_bank_account.balance == 50*1.1


@pytest.mark.parametrize("deposited, withdrew, expected_value",
                         [(200, 100, 100), (50, 10, 40), (1200, 200, 1000)])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected_value):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected_value


def test_insufficient_funds(initial_balance_bank_account):
    with pytest.raises(Exception):
        initial_balance_bank_account.withdraw(300)


def test_insufficient_funds_2(initial_balance_bank_account):
    with pytest.raises(Insufficient_funds):
        initial_balance_bank_account.withdraw(300)
