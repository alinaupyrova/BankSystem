from models.account import Bankaccount
from service.file_manager import FileManager

class AccountService:
    """
       Service class that provides high-level operations for managing bank accounts.
       Includes helper methods for creating, depositing, withdrawing, and transferring funds.
       Interacts with file-based user storage via FileManager.
    """

    @staticmethod
    def create_bank_account(account_id: int, initial_balance: float = 0.0, currency: str = "USD") -> Bankaccount:
        """
               Creates a new bank account object with the given ID, initial balance, and currency.

               :param account_id: Unique ID for the account
               :param initial_balance: Starting balance (default is 0.0)
               :param currency: Currency code (e.g., "USD", "EUR")
               :return: Instance of Bankaccount
        """
        return Bankaccount(account_id, initial_balance, currency)

    @staticmethod
    def deposit_to_account(account: Bankaccount, amount: float, currency: str) -> None:
        """
                Deposits money into a specific bank account.

                :param account: Target Bankaccount instance
                :param amount: Amount to deposit
                :param currency: Currency in which deposit is made
        """
        return account.deposit(amount, currency)

    @staticmethod
    def withdraw_from_account(account: Bankaccount, amount: float, currency: str) -> bool:
        """
              Attempts to withdraw money from the specified bank account.

              :param account: Target Bankaccount instance
              :param amount: Amount to withdraw
              :param currency: Currency of withdrawal
              :return: Result message from the withdrawal method
        """
        return account.withdraw(amount, currency)

    @staticmethod
    def transfer_between_accounts(from_account: Bankaccount, to_account: Bankaccount, amount: float, currency: str) -> bool:
        """
               Transfers money between two accounts, with currency validation and conversion if needed.

               :param from_account: Source account
               :param to_account: Target account
               :param amount: Amount to transfer
               :param currency: Currency used for transfer
               :return: Result message from the transfer method
        """
        return from_account.transfer(to_account, amount, currency)

    @staticmethod
    def withdraw(args):
        """
                CLI wrapper for withdrawing money from a user's account based on provided arguments.

                :param args: Parsed arguments object with user_id, account_id, amount
        """
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if not user:
            print("User not found")
            return

        account = user.get_account_by_id(args.account_id)
        if account:
            result = account.withdraw(args.amount, account.currency)
            FileManager.save_all_users(users)
            print(f"{result}")
        else:
            print("Account not found")

    @staticmethod
    def create_account(args):
        """
                CLI wrapper for creating a new bank account for a user.

                :param args: Parsed arguments object with user_id, account_id, currency
        """
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if not user:
            print("User not found")
            return

        account = Bankaccount(account_id=args.account_id, balance=0.0, currency=args.currency)
        user.accounts.append(account)
        FileManager.save_all_users(users)
        print(f"Creating account ID {args.account_id} by user {user.username}")

    @staticmethod
    def deposit(args):
        """
                CLI wrapper for depositing funds into a user's account.

                :param args: Parsed arguments object with user_id, account_id, amount
        """
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if not user:
            print("User not found")
            return

        account = user.get_account_by_id(args.account_id)
        if account:
            account.deposit(args.amount, account.currency)
            FileManager.save_all_users(users)
            print(f"Account replenished {args.account_id} на {args.amount}")
        else:
            print("Account not found")

    @staticmethod
    def transfer(args):
        """
                CLI wrapper for transferring funds between two of a user's accounts.

                :param args: Parsed arguments object with user_id, from_id, to_id, amount
        """
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if not user:
            print("User not found")
            return

        from_acc = user.get_account_by_id(args.from_id)
        to_acc = user.get_account_by_id(args.to_id)
        if from_acc and to_acc:
            result = from_acc.transfer(to_acc, args.amount, from_acc.currency)
            FileManager.save_all_users(users)
            print(result)
        else:
            print("One of the accounts was not found.")
