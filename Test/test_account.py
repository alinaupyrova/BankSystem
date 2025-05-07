import unittest
from datetime import datetime
from models.account import Bankaccount
from models.transaction import Transaction
import pytest

@pytest.mark.parametrize(
    "initial_balance, deposit_amount, currency, expected_balance",
    [
        (1000, 500, 'USD', 1500),
        (0, 100, 'EUR', 100),
        (50, 0, 'UAN', 50)
    ]
)
def test_deposit_success(initial_balance, deposit_amount, currency, expected_balance):
    """
    Test successful deposits:
    - Ensures the balance is updated correctly.
    - A 'deposit' transaction is created and recorded.
    """
    account = Bankaccount(account_id=1, balance=initial_balance, currency=currency)
    result = account.deposit(deposit_amount, currency)
    assert result == "Deposit successful"
    assert account.get_balance() == expected_balance
    assert len(account.get_transactions()) == 1
    assert account.get_transactions()[0].transaction_type == "deposit"


@pytest.mark.parametrize(
    "initial_balance, withdraw_amount, currency, expected_balance",
    [
        (1000, 300, 'USD', 700),
        (500, 500, 'EUR', 0),
    ]
)
def test_withdraw_success(initial_balance, withdraw_amount, currency, expected_balance):
    """
    Test successful withdrawals:
    - Verifies that the balance decreases correctly.
    - A 'withdraw' transaction is recorded.
    """
    account = Bankaccount(account_id=2, balance=initial_balance, currency=currency)
    result = account.withdraw(withdraw_amount, currency)
    assert result == "Withdrawal was successful"
    assert account.get_balance() == expected_balance
    assert len(account.get_transactions()) == 1
    assert account.get_transactions()[0].transaction_type == "withdraw"


@pytest.mark.parametrize(
    "amount, currency, expected_error",
    [
        (-100, 'USD', "Amount cannot be negative"),
        (200, 'EUR', "Currency cannot be changed"),
        (10000, 'USD', "Amount cannot be greater than balance"),
    ]
)
def test_withdraw_errors(amount, currency, expected_error):
    """
    Test various withdrawal error scenarios:
    - Negative withdrawal amount
    - Currency mismatch
    - Insufficient funds
    """
    account = Bankaccount(account_id=3, balance=500, currency='USD')
    result = account.withdraw(amount, currency)
    assert expected_error in result


class TestBankaccount(unittest.TestCase):
    """
       Unit tests for the Bankaccount class covering deposits, withdrawals, transfers, exchange rates,
       dictionary serialization/deserialization, and transaction integrity.
    """

    def setUp(self):
        """Initialize two bank accounts before each test."""
        self.account1 = Bankaccount(account_id=1, balance=500, currency="USD")
        self.account2 = Bankaccount(account_id=2, balance=300, currency="USD")

    def test_deposit(self):
        """Test depositing a valid amount increases balance and creates a transaction."""
        self.account1.deposit(100, "USD")
        self.assertEqual(self.account1.get_balance(), 600)
        self.assertEqual(len(self.account1.get_transactions()), 1)
        self.assertEqual(self.account1.get_transactions()[0].transaction_type, "deposit")

    def test_deposit_negative_amount(self):
        """Test that depositing a negative amount does not change the balance."""

        self.account1.deposit(-50, "USD")
        self.assertEqual(self.account1.get_balance(), 500)

    def test_deposit_none_amount(self):
        """Test that depositing None returns a type error message."""
        result = self.account1.deposit(None, "USD")
        self.assertIn("Amount must be of type int or float", result)

    def test_withdraw(self):
        """Test successful withdrawal decreases balance and returns success message."""
        result = self.account1.withdraw(200, "USD")
        self.assertEqual(result, "Withdrawal was successful")
        self.assertEqual(self.account1.get_balance(), 300)

    def test_withdraw_negative_amount(self):
        """Test that withdrawing a negative amount returns an appropriate error."""
        result = self.account1.withdraw(-100, "USD")
        self.assertIn("Amount cannot be negative", result)

    def test_withdraw_insufficient_funds(self):
        """Test that withdrawing with the wrong currency returns an error."""
        result = self.account1.withdraw(1000, "USD")
        self.assertIn("Amount cannot be greater than balance", result)

    def test_withdraw_invalid_currency(self):
        """Test that withdrawing with a non-numeric value returns an error."""
        result = self.account1.withdraw(100, "EUR")
        self.assertIn("Currency cannot be changed", result)

    def test_withdraw_invalid_amount_type(self):
        """Test that withdrawing None as amount returns a type error."""
        result = self.account1.withdraw("abc", "USD")
        self.assertIn("Value must be a number", result)

    def test_withdraw_none_amount(self):
        """Test that withdrawing None as amount returns a type error."""
        result = self.account1.withdraw(None, "USD")
        self.assertIn("Value must be a number", result)

    def test_transfer_success(self):
        """Test successful transfer between accounts of the same currency."""
        result = self.account1.transfer(self.account2, 100, "USD")
        self.assertEqual(result, "Transfer completed. 100 USD → 100 USD")
        self.assertEqual(self.account1.get_balance(), 400)
        self.assertEqual(self.account2.get_balance(), 400)

    def test_transfer_invalid_amount(self):
        """Test that transferring zero or negative amount returns an error."""
        result = self.account1.transfer(self.account2, 0, "USD")
        self.assertEqual(result, "Transfer error: The transfer amount must be greater than 0..")

    def test_transfer_insufficient_funds(self):
        """Test that transferring more than the balance returns an error."""
        result = self.account1.transfer(self.account2, 999, "USD")
        self.assertEqual(result, "Transfer error: Insufficient funds for transfer.")

    def test_transfer_rounding_conversion(self):
        """Test that exchange rates are correctly applied and amounts rounded."""
        eur_account = Bankaccount(account_id=3, balance=0, currency="EUR")
        result = self.account1.transfer(eur_account, 99, "USD")
        self.assertIn("USD →", result)
        converted = round(99 * 0.92, 2)
        self.assertEqual(eur_account.get_balance(), converted)

    def test_transfer_different_currency(self):
        """Test transfer with incorrect currency triggers a validation error."""
        result = self.account1.transfer(self.account2, 100, "EUR")
        self.assertEqual(result, "Transfer error: The amount must be in your account currency..")

    def test_transfer_transaction_types(self):
        """Test correct transaction types are recorded during transfer."""

        self.account1.transfer(self.account2, 50, "USD")
        tx1 = self.account1.get_transactions()[-1]
        tx2 = self.account2.get_transactions()[-1]
        self.assertTrue(tx1.transaction_type.startswith("transfer_to"))
        self.assertTrue(tx2.transaction_type.startswith("transfer_from"))

    def test_get_balance(self):
        """Test that get_balance returns the correct initial balance."""
        self.assertEqual(self.account1.get_balance(), 500)

    def test_get_transactions(self):
        """Test that deposits and withdrawals are correctly recorded."""
        self.account1.deposit(100, "USD")
        self.account1.withdraw(50, "USD")
        tx = self.account1.get_transactions()
        self.assertEqual(len(tx), 2)
        self.assertEqual(tx[0].transaction_type, "deposit")
        self.assertEqual(tx[1].transaction_type, "withdraw")

    def test_get_exchange_rate_valid(self):
        """Test that a known exchange rate returns a float."""
        rate = Bankaccount.get_exchange_rate('USD', 'UAN')
        self.assertEqual(rate, 39.5)

    def test_get_exchange_rate_same_currency(self):
        """Test that exchange rate for same currency returns 1.0."""
        rate = Bankaccount.get_exchange_rate('USD', 'USD')
        self.assertEqual(rate, 1.0)

    def test_get_exchange_rate_invalid(self):
        """Test that unknown currency pair returns None."""
        rate = Bankaccount.get_exchange_rate('USD', 'GBP')
        self.assertIsNone(rate)

    def test_to_and_from_dict(self):
        """Test that an account can be serialized and restored correctly."""
        self.account1.deposit(200, "USD")
        data = self.account1.to_dict()
        restored = Bankaccount.from_dict(data)
        self.assertEqual(restored.get_balance(), self.account1.get_balance())
        self.assertEqual(len(restored.get_transactions()), 1)

    def test_transaction_repr_format(self):
        """Test that __repr__ of transaction returns expected string format."""
        self.account1.deposit(150, "USD")
        tx = self.account1.get_transactions()[0]
        self.assertIsInstance(repr(tx), str)
        self.assertIn("Transaction(ID=", repr(tx))

    def test_multiple_transactions_history_order(self):
        """Test that multiple transactions are recorded in correct chronological order."""
        self.account1.deposit(100, "USD")
        self.account1.withdraw(30, "USD")
        self.account1.deposit(50, "USD")

        transactions = self.account1.get_transactions()
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0].transaction_type, "deposit")
        self.assertEqual(transactions[1].transaction_type, "withdraw")
        self.assertEqual(transactions[2].transaction_type, "deposit")


    def test_deposit_wrong_currency_simulation(self):
        """Test that depositing in wrong currency returns error and doesn't change balance."""
        result = self.account1.deposit(100, "EUR")
        self.assertIn("Deposit error: Currency mismatch", result)
        self.assertEqual(self.account1.get_balance(), 500)
        self.assertEqual(len(self.account1.get_transactions()), 0)


    def test_withdraw_none_currency(self):
        """Test withdrawing with None as currency returns an error."""
        result = self.account1.withdraw(100, None)
        self.assertIn("Currency cannot be changed", result)

    def test_transfer_no_exchange_rate(self):
        """Test transfer with unsupported currency pair returns error."""
        account_inr = Bankaccount(account_id=3, balance=0, currency="INR")
        result = self.account1.transfer(account_inr, 100, "USD")
        self.assertIn("no exchange rate available", result)


    def test_to_dict_contains_keys(self):
        """Test that to_dict output includes all necessary keys."""
        self.account1.deposit(123, "USD")
        data = self.account1.to_dict()
        self.assertIn("account_id", data)
        self.assertIn("balance", data)
        self.assertIn("currency", data)
        self.assertIn("transactions", data)

    def test_transfer_transaction_details(self):
        """Test transaction fields after transfer match expected data."""
        self.account1.transfer(self.account2, 50, "USD")
        tx1 = self.account1.get_transactions()[-1]
        tx2 = self.account2.get_transactions()[-1]

        self.assertEqual(tx1.amount, 50)
        self.assertEqual(tx2.amount, 50)
        self.assertIn("transfer_to_", tx1.transaction_type)
        self.assertIn("transfer_from_", tx2.transaction_type)
        self.assertEqual(tx1.currency, "USD")
        self.assertEqual(tx2.currency, "USD")

    def test_from_dict_missing_key(self):
        """Test from_dict with missing required fields returns None."""
        data = {
        "balance": 100,
        "currency": "USD"
        }
        account = Bankaccount.from_dict(data)
        self.assertIsNone(account)

    def test_get_exchange_rate_identical_currency(self):
        """Redundant: Test identical currency exchange returns 1.0."""
        rate = Bankaccount.get_exchange_rate("USD", "USD")
        self.assertEqual(rate, 1.0)

    def test_to_dict_structure(self):
        """Test that the structure of to_dict output matches the expected schema."""
        self.account1.deposit(20, "USD")
        d = self.account1.to_dict()
        self.assertEqual(d["account_id"], 1)
        self.assertEqual(d["balance"], self.account1.balance)
        self.assertIsInstance(d["transactions"], list)




if __name__ == "__main__":
    unittest.main()
