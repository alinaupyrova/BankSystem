import unittest
from datetime import datetime
import pytest
from models.transaction import Transaction



@pytest.mark.parametrize(
    "transaction_id, amount, transaction_type, currency",
    [
        (10, 99.99, "deposit", "USD"),
        (20, 123.45, "withdraw", "EUR"),
        (30, 1000, "transfer", "UAN"),
    ]
)
def test_transaction_creation_valid_data(transaction_id, amount, transaction_type, currency):
    """
    Test creating transactions with valid data using parameterization.
    """
    now = datetime.now()
    tx = Transaction(
        transaction_id=transaction_id,
        amount=amount,
        transaction_type=transaction_type,
        time_stamp=now,
        currency=currency
    )
    assert tx.transaction_id == transaction_id
    assert tx.amount == amount
    assert tx.transaction_type == transaction_type
    assert tx.currency == currency
    assert isinstance(tx.time_stamp, datetime)


@pytest.mark.parametrize("invalid_value, expected_exception",
    [
        ("not-int", TypeError),
        (None, TypeError),
    ]
)
def test_transaction_invalid_id(invalid_value, expected_exception):
    """
    Test that invalid transaction_id raises the correct exception.
    """
    with pytest.raises(expected_exception):
        Transaction(
            transaction_id=invalid_value,
            amount=100.0,
            transaction_type="deposit",
            time_stamp=datetime.now(),
            currency="USD"
        )


@pytest.mark.parametrize("amount", ["invalid", None, [], {}])
def test_transaction_invalid_amount_types(amount):
    """
    Test that invalid amount types raise TypeError.
    """
    with pytest.raises(TypeError):
        Transaction(
            transaction_id=1,
            amount=amount,
            transaction_type="deposit",
            time_stamp=datetime.now(),
            currency="USD"
        )

@pytest.mark.parametrize("t_type", ["", "   ", "\n"])
def test_transaction_empty_type_string(t_type):
    """
    Test that empty or whitespace-only transaction_type raises ValueError.
    """
    with pytest.raises(ValueError):
        Transaction(
            transaction_id=1,
            amount=100.0,
            transaction_type=t_type,
            time_stamp=datetime.now(),
            currency="USD"
        )


@pytest.mark.parametrize(
    "timestamp", ["not-a-date", 123456, None]
)
def test_transaction_from_dict_invalid_timestamp(timestamp):
    """
    Test that from_dict raises ValueError or TypeError on invalid timestamp.
    """
    data = {
        "transaction_id": 1,
        "amount": 100.0,
        "transaction_type": "deposit",
        "currency": "USD",
        "time_stamp": timestamp
    }

    with pytest.raises((TypeError, ValueError)):
        if isinstance(timestamp, str):
            Transaction.from_dict(data)
        else:
            # Manually construct if timestamp isn't even a string
            Transaction(
                transaction_id=1,
                amount=100.0,
                transaction_type="deposit",
                time_stamp=timestamp,
                currency="USD"
            )
class TestTransaction(unittest.TestCase):
    """Unit tests for the Transaction class."""

    def setUp(self):
        """Set up a sample transaction for testing."""
        self.transaction = Transaction(
            transaction_id=1,
            amount=100.0,
            transaction_type="deposit",
            time_stamp=datetime(2023, 5, 17, 10, 30, 0),
            currency="USD"
        )

    def test_get_transaction_id(self):
        """Test that transaction ID is returned correctly."""
        self.assertEqual(self.transaction.get_transaction_id(), 1)

    def test_get_transaction_type(self):
        """Test that transaction type is returned correctly."""
        self.assertEqual(self.transaction.get_transaction_type(), "deposit")

    def test_get_transaction_detail(self):
        """Test that the transaction detail string is formatted correctly."""
        expected_detail = (
            "Amount: 100.0 Currency USD, Transaction type: deposit, Time= 2023-05-17 10:30:00"
        )
        self.assertEqual(self.transaction.get_transaction_detail(), expected_detail)

    def test_to_dict(self):
        """Test serialization of transaction to dictionary."""
        expected_dict = {
            "transaction_id": 1,
            "amount": 100.0,
            "transaction_type": "deposit",
            "currency": "USD",
            "time_stamp": "2023-05-17T10:30:00"
        }
        self.assertEqual(self.transaction.to_dict(), expected_dict)

    def test_from_dict(self):
        """Test deserialization from dictionary to Transaction object."""
        data = {
            "transaction_id": 1,
            "amount": 100.0,
            "transaction_type": "deposit",
            "currency": "USD",
            "time_stamp": "2023-05-17T10:30:00"
        }
        new_transaction = Transaction.from_dict(data)
        self.assertEqual(new_transaction.get_transaction_id(), 1)
        self.assertEqual(new_transaction.amount, 100.0)
        self.assertEqual(new_transaction.transaction_type, "deposit")
        self.assertEqual(new_transaction.currency, "USD")
        self.assertEqual(new_transaction.time_stamp, datetime(2023, 5, 17, 10, 30, 0))

    def test_round_trip_dict_conversion(self):
        """Test that to_dict followed by from_dict retains original data."""
        data = self.transaction.to_dict()
        new_obj = Transaction.from_dict(data)
        self.assertEqual(self.transaction.get_transaction_detail(), new_obj.get_transaction_detail())

    def test_repr(self):
        """Test the __repr__ output format."""
        expected_repr = "Transaction(ID=1, Type=deposit, Amount=100.0, Time=2023-05-17 10:30:00)"
        self.assertEqual(repr(self.transaction), expected_repr)

    def test_str_output(self):
        """Test that __str__ returns a valid string."""
        string_output = str(self.transaction)
        self.assertIsInstance(string_output, str)
        self.assertIn("Transaction", string_output)

    def test_different_transaction_types(self):
        """Test that different transaction types are accepted."""
        for t_type in ["deposit", "withdraw", "transfer"]:
            with self.subTest(t_type=t_type):
                tx = Transaction(
                    transaction_id=2,
                    amount=50.0,
                    transaction_type=t_type,
                    time_stamp=datetime.now(),
                    currency="EUR"
                )
                self.assertEqual(tx.get_transaction_type(), t_type)

    def test_invalid_transaction_id_type(self):
        """Test that invalid transaction_id type raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction("one", 100.0, "deposit", datetime.now(), "USD")

    def test_missing_timestamp_raises(self):
        """Test that passing None as timestamp raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction(1, 100.0, "deposit", None, "USD")

    def test_from_dict_with_invalid_timestamp(self):
        """Test that invalid timestamp string raises ValueError."""
        data = {
            "transaction_id": 1,
            "amount": 100.0,
            "transaction_type": "deposit",
            "currency": "USD",
            "time_stamp": "not-a-valid-timestamp"
        }
        with self.assertRaises(ValueError):
            Transaction.from_dict(data)

    def test_transaction_detail_contains_fields(self):
        """Test that detail string contains key fields."""
        detail = self.transaction.get_transaction_detail()
        self.assertIn("Amount", detail)
        self.assertIn("Currency", detail)
        self.assertIn("Time", detail)

    def test_invalid_amount_type(self):
        """Test that non-float amount raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction(1, "one hundred", "deposit", datetime.now(), "USD")

    def test_invalid_currency_type(self):
        """Test that non-string currency raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction(1, 100.0, "deposit", datetime.now(), 100)

    def test_invalid_transaction_type_type(self):
        """Test that non-string transaction_type raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction(1, 100.0, 123, datetime.now(), "USD")

    def test_from_dict_missing_timestamp(self):
        """Test that missing timestamp key in dict raises KeyError."""
        data = {
            "transaction_id": 1,
            "amount": 100.0,
            "transaction_type": "deposit",
            "currency": "USD"
        }
        with self.assertRaises(KeyError):
            Transaction.from_dict(data)

    def test_from_dict_exact_timestamp_parsing(self):
        """Test correct parsing of ISO timestamp from dict."""
        data = {
            "transaction_id": 2,
            "amount": 123.45,
            "transaction_type": "withdraw",
            "currency": "EUR",
            "time_stamp": "2023-08-01T14:45:00"
        }
        tx = Transaction.from_dict(data)
        self.assertEqual(tx.time_stamp, datetime(2023, 8, 1, 14, 45))

    def test_transaction_fields_types(self):
        """Test that all fields have correct types."""
        self.assertIsInstance(self.transaction.transaction_id, int)
        self.assertIsInstance(self.transaction.amount, float)
        self.assertIsInstance(self.transaction.transaction_type, str)
        self.assertIsInstance(self.transaction.currency, str)
        self.assertIsInstance(self.transaction.time_stamp, datetime)

    def test_batch_dict_conversion(self):
        """Test batch conversion to and from dict works for many transactions."""
        tx_list = [self.transaction for _ in range(100)]
        dicts = [tx.to_dict() for tx in tx_list]
        restored = [Transaction.from_dict(d) for d in dicts]
        self.assertEqual(len(restored), 100)
        for r in restored:
            self.assertEqual(r.get_transaction_type(), "deposit")

    def test_empty_transaction_type(self):
        """Test that empty string for transaction_type raises ValueError."""
        with self.assertRaises(ValueError):
            Transaction(1, 100.0, "", datetime.now(), "USD")


if __name__ == "__main__":
    unittest.main()
