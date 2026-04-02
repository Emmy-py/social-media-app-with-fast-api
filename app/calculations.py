def add(num1: int, num2: int) -> int:
    return num1 + num2

def subtract(num1: int, num2: int) -> int:
    return num1 - num2

def multiply(num1: int, num2: int) -> int:
    return num1 * num2

def divide(num1: int, num2: int) -> float:
    if num2 == 0:
        raise ValueError("Cannot divide by zero")
    return num1 / num2



class Bank_Account:
    def __init__(self, starting_balance: float = 0.0):
        self.balance = starting_balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")   

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        print(f"Withdrew {amount}. New balance: {self.balance}")

    def get_balance(self) -> str:
        return f"Current balance: {self.balance}"
    
    def collect_interest(self):
        interest_rate =0.05
        interest = self.balance * interest_rate
        self.balance += interest
        print(f"Collected interest: {interest}. New balance: {self.balance}")
