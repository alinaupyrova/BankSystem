import random
from models.account import Bankaccount
from typing import List
from models.transaction import Transaction


class User:
    """
       Represents a user of the banking system with multiple accounts.
       Provides access to user's personal data, bank accounts, and summary reports.
    """
    user_id: int
    username: str
    surname: str
    accounts: List[Bankaccount]

    def __init__(self, username: str, surname: str, user_id: int) -> None:
        """
               Initializes a new User with the given name, surname, and unique user ID.
               :param username: First name of the user
               :param surname: Last name of the user
               :param user_id: Unique identifier for the user
        """
        self.username = username
        self.surname = surname
        self.accounts: List[Bankaccount] = []
        self.user_id = user_id

    def get_user_id(self):
        """
                Returns the user's unique identifier.
                :return: User ID as integer
        """
        return self.user_id

    def __repr__(self):
        """
              Returns a developer-friendly string representation of the user.
              :return: String showing username, surname, and user ID
        """
        return f"UserName: {self.username}, Surname: {self.surname}, UserId: {self.user_id}"

    def add_account(self, account) -> None:
        """
               Adds a new bank account to the user's list of accounts.
               :param account: A Bankaccount object
        """
        self.accounts.append(account)

    def get_total_balance(self) -> float:
        """
               Calculates the total balance across all the user's accounts.
               :return: Sum of all account balances
        """
        return sum(account.get_balance() for account in self.accounts)

    def get_account(self) -> List[Bankaccount]:
        """
              Returns the list of bank accounts associated with the user.
              :return: List of Bankaccount objects
        """
        return self.accounts

    def get_account_by_id(self, account_id):
        """
                Searches for an account by ID among the user's accounts.
                :param account_id: Account ID to search for
                :return: Bankaccount object if found, else None
        """
        for account in self.accounts:
            print(f"Account verification: {account}")
            if isinstance(account, Bankaccount) and account.get_account_id() == account_id:
                return account
        return None


    def get_balances_by_currency(self) -> dict:
        """
                Groups and returns the balances of the user's accounts by currency.
                :return: Dictionary with currency as key and total balance as value
        """
        balances = {}
        for account in self.accounts:
            currency = account.currency
            if currency in balances:
                balances[currency] += account.get_balance()
            else:
                balances[currency] = account.get_balance()
        return balances

    def print_summary(self):
        """
               Prints a formatted summary report of the user including:
               - Name and ID
               - Total balance
               - Balances by currency
               - Detailed information about each account and its transactions
        """
        print(f"=== User report ===")
        print(f"Name: {self.username} {self.surname}")
        print(f"User ID: {self.get_user_id()}")
        print(f"General balance: {self.get_total_balance()}")
        print("Balance by currencies:")

        for currency, balance in self.get_balances_by_currency().items():
            print(f"  {currency}: {balance}")
        print("\n--- Accounts ---")
        for account in self.accounts:
            print(f"account ID: {account.get_account_id()}, balance: {account.get_balance()} {account.currency}")
            print("Transactions:")
            if not account.get_transactions():
                print("(No transactions)")
            else:
                for t in account.get_transactions():
                    print("   ",t.get_transaction_detail())
            print("-" * 30)

    @staticmethod
    def from_dict(data):
        """
                Creates a User object from a dictionary (typically from JSON).
                :param data: Dictionary with user fields and account data
                :return: Initialized User object
        """
        user = User(username=data["username"],surname=data["surname"],user_id=data["user_id"])

        for acc_data in data.get("accounts",[]):
            account = Bankaccount(account_id=acc_data["account_id"],
                                  balance=acc_data["balance"],
                                  currency=acc_data["currency"])
            for tr_data in acc_data.get("transactions",[]):
                transaction = Transaction.from_dict(tr_data)
                account.transactions.append(transaction)
            user.add_account(account)
        return user

    def to_dict(self):
        """
               Converts the User object into a dictionary suitable for JSON serialization.
               :return: Dictionary containing user data and list of account dictionaries
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "surname": self.surname,
            "accounts": [a.to_dict() for a in self.accounts]
        }
