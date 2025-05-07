# Simple Bank System

#### A simple bank system implemented in Python with unit tests.

# **Features**

* ### **🔐 User Management**
* ### **🏦 Multi-Account Support**
* ### **💸 Core Banking Operations**
* ### **💱 Currency Exchange**
* ### **📊 Reports and Analysis**


## Project Structure

```
SimpleBankSystem/
├── data/
│   └── users.json
├── models/
│   ├── __init__.py
│   ├── account.py
│   ├── transaction.py
│   └── user.py
├── service/
│   ├── __init__.py
│   ├── account_service.py
│   ├── file_manager.py
│   └── user_service.py
├── Test/
│   ├── __init__.py
│   ├── test_account.py
│   ├── test_account_service.py
│   ├── test_filemanager.py
│   ├── test_transaction.py
│   ├── test_user.py
│   └── test_userservice.py
├── main.py
├── README.md
├── requirements.txt
└── .venv/
```

## Installation

1. Clone the repository
2. Install dependencies (if necessary): pip install -r requirements.txt

## 🧪Running Tests
Run all tests with: python -m unittest discover tests


## ⚙️ CLI Usage Examples

```python
from models.user import User
from models.account import Bankaccount
from service.account_service import AccountService

# ✅ Create a new user
user = User(user_id=1, username="Alice", surname="Smith")

# ✅ Add a new bank account
account = AccountService.create_bank_account(account_id=101, initial_balance=500.0, currency="USD")
user.add_account(account)

# ✅ Deposit money
AccountService.deposit_to_account(account, amount=200.0, currency="USD")

# ✅ Withdraw money
AccountService.withdraw_from_account(account, amount=100.0, currency="USD")

# ✅ Transfer money between accounts
second_account = AccountService.create_bank_account(account_id=102, initial_balance=0.0, currency="USD")
user.add_account(second_account)
AccountService.transfer_between_accounts(account, second_account, amount=150.0, currency="USD")

# ✅ View balances
print(user.get_total_balance())  # Output: 450.0

# ✅ Print summary report
user.print_summary()
