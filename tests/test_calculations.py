import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount(0)

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (5, 3, 8),
    (9, 4, 13)
])
def test_add(num1,num2,expected):
    print("testing add function")
    assert add(num1, num2) == expected

def test_subtract():
    print("testing subtract function")
    assert subtract(9, 4) == 5

def test_multiply():
    print("testing multiply function")
    assert multiply(5, 3) == 15

def test_divide():
    print("testing divide function")
    assert divide(15, 3) == 5

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    print("testing bank account")
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(100)
    assert bank_account.balance == 150

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)

# test_add()
test_subtract()
test_multiply()
test_divide()