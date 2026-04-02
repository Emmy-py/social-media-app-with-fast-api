from app.calculations import add, subtract, multiply, divide, Bank_Account
import pytest  

@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 5),
    (5, 2, 7),
    (4, 3, 7),
    (10, 2, 12)
])
def test_add(num1, num2, expected):
    print("Testing add function...")

    sum_result = add(num1, num2)
    assert sum_result == expected, f"Test failed: add({num1}, {num2}) should equal {expected}, got {sum_result}"
    print("All tests passed!")


def test_subtract():
    print('Testing subtract function...')
    difference_result = subtract(5, 2)
    assert difference_result == 3, f"test failed: subtract(5, 2) should equal 3, got {difference_result}"
    print("All tests passed!")


def test_multiply():
    print('Testing multiply function...')
    product_result = multiply(4, 3)
    assert product_result == 12, f"test failed: multiply(4, 3) should equal 12, got {product_result}"
    print("All tests passed!")


def test_divide():
    print('Testing divide function...')
    quotient_result = divide(10, 2)
    assert quotient_result == 5.0, f"test failed: divide(10, 2) should equal 5.0, got {quotient_result}"
    
    try:
        divide(10, 0)
        assert False, "test failed: divide(10, 0) should raise ValueError"
    except ValueError as e:
        assert str(e) == "Cannot divide by zero", f"test failed: expected ValueError with message 'Cannot divide by zero', got '{str(e)}'"
    
    print("All tests passed!")

@pytest.fixture
def zero_balance_account():
    print("creating empty bank account for testing...")
    return Bank_Account()

@pytest.fixture
def pre_funded_account():
    print("creating pre-funded bank account for testing...")
    return Bank_Account(100.0)


def test_bank_set_initial_balance(pre_funded_account):
    print("Testing bank account initialization...")
    bank_account = pre_funded_account
    assert bank_account.balance == 100.0, f"test failed: initial balance should be 100.0, got {bank_account.balance}"
    print("All tests passed!")


def test_bank_default_balance():
    print("Testing bank account initialization...")
    bank_account = Bank_Account()
    assert bank_account.balance == 0.0, f"test failed: default balance should be 0.0, got {bank_account.balance}"
    print("All tests passed!")

def test_bank_withdraw(pre_funded_account):
    print("Testing bank account initialization...")
    bank_account = pre_funded_account
    bank_account.withdraw(100.0)
    assert bank_account.balance == 0.0, f"test failed: after withdrawal, balance should be 0.0, got {bank_account.balance}"
    print("All tests passed!")

def test_collect_interest(pre_funded_account):
    print("Testing bank account initialization...")
    bank_account = pre_funded_account
    bank_account.collect_interest()
    assert bank_account.balance == 105.0, f"test failed: after collecting interest, balance should be 105.0, got {bank_account.balance}"
    print("All tests passed!")

def test_bank_deposit(zero_balance_account):
    print("Testing bank account deposit...")
    bank_account = zero_balance_account
    bank_account.deposit(50.0)
    assert bank_account.balance == 50.0, f"test failed: after deposit, balance should be 50.0, got {bank_account.balance}"
    print("All tests passed!")


@pytest.mark.parametrize("deposited_amount, withdrawn_amount, expected_balance", [
    (50, 10, 40),
    (100.00, 25.50, 74.50),
    (200.00, 150.00, 50.00)
])


def test_bank_transaction(zero_balance_account, deposited_amount, withdrawn_amount, expected_balance):
    print("Testing bank account transactions...")
    zero_balance_account.deposit(deposited_amount)
    zero_balance_account.withdraw(withdrawn_amount)
    assert zero_balance_account.balance == expected_balance, f"test failed: after transactions, balance should be {expected_balance}, got {zero_balance_account.balance}"
    print("All tests passed!")
    


def test_bank_withdraw_insufficient_funds(zero_balance_account):
    print("Testing bank account withdrawal with insufficient funds...")
    with pytest.raises(ValueError) as exc_info:
        zero_balance_account.withdraw(10.0)

    assert "Insufficient funds" in str(exc_info.value)
    print("All tests passed!")

