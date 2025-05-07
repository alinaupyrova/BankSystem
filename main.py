import argparse
from models.user import User
from models.account import Bankaccount
from service.file_manager import FileManager
from service.account_service import AccountService
from service.user_service import  Userservice


def console_vision(user_id: int):
    users = FileManager.load_all_users()
    user = next((u for u in users if u.user_id == user_id), None)
    if not user:
        print("User not found")
        return
    user.print_summary()


def main():
    parser = argparse.ArgumentParser(description="BankApp CLI")
    subparsers = parser.add_subparsers(dest="command")

    acc = subparsers.add_parser("create-account", help="Create a bank account")
    acc.add_argument("--user-id", type=int, required=True)
    acc.add_argument("--account-id", type=int, required=True)
    acc.add_argument("--currency", type=str, required=True)
    acc.set_defaults(func=AccountService.create_account)

    reg = subparsers.add_parser("register", help="Create a bank account")
    reg.add_argument("--username", required=True)
    reg.add_argument("--surname", required=True)
    reg.set_defaults(func=Userservice.register)

    log = subparsers.add_parser("login", help="Login to the system")
    log.add_argument("--user-id", type=int, required=True)
    log.set_defaults(func=Userservice.login)

    withd = subparsers.add_parser("withdraw", help="Withdraw funds from the account")
    withd.add_argument("--user-id", type=int, required=True)
    withd.add_argument("--account-id", type=int, required=True)
    withd.add_argument("--amount", type=float, required=True)
    withd.set_defaults(func=AccountService.withdraw)


    dep = subparsers.add_parser("deposit", help="Account replenishment")
    dep.add_argument("--user-id", type=int, required=True)
    dep.add_argument("--account-id", type=int, required=True)
    dep.add_argument("--amount", type=float, required=True)
    dep.set_defaults(func=AccountService.deposit)

    trans = subparsers.add_parser("transfer", help="Transfer between accounts")
    trans.add_argument("--user-id", type=int, required=True)
    trans.add_argument("--from-id", type=int, required=True)
    trans.add_argument("--to-id", type=int, required=True)
    trans.add_argument("--amount", type=float, required=True)
    trans.set_defaults(func=AccountService.transfer)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
    console_vision(2)

