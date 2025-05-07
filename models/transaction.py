from datetime import datetime


class Transaction:
    """
       Represents a single banking transaction including deposit, withdrawal, or transfer.
       Contains transaction ID, amount, type, timestamp, and currency.
    """

    transaction_id: int
    amount: float
    transaction_type: str
    time_stamp: datetime
    currency: str

    def __init__(self, transaction_id: int, amount: float, transaction_type: str, time_stamp: datetime,currency)-> None:
        """
               Initializes a new Transaction object with validation.

               :param transaction_id: Unique ID of the transaction
               :param amount: The amount of money involved in the transaction
               :param transaction_type: Type of transaction (e.g., 'deposit', 'withdraw', 'transfer')
               :param time_stamp: The date and time of the transaction
               :param currency: The currency used (e.g., 'USD', 'EUR')
               :raises TypeError: If any argument is of an incorrect type
               :raises ValueError: If transaction_type is empty
               """
        if not isinstance(transaction_id, int):
            raise TypeError("Transaction id must be an integer")
        if not isinstance(amount, (int,float)):
            raise TypeError("Amount must be a num")
        if not isinstance(transaction_type, str):
            raise TypeError("Transaction type must be an string")
        if not transaction_type.strip():
            raise ValueError("Transaction type must not be empty")
        if not isinstance(time_stamp, datetime):
            raise TypeError("Time_stamp must be an datetime")
        if not isinstance(currency, str):
            raise TypeError("Currency must be an string")

        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.time_stamp = time_stamp
        self.currency = currency


    def get_transaction_id(self) -> int:
        """
            Returns the transaction ID.
            :return: Transaction ID as integer
        """
        return self.transaction_id

    def get_transaction_type(self) -> str:
        """
            Returns the type of the transaction as a string.
            :return: Transaction type (e.g., 'deposit', 'withdraw')
        """
        return f'{self.transaction_type}'

    def get_transaction_detail(self)-> str:
        """
               Returns a detailed string description of the transaction.
               :return: Formatted transaction detail string
        """
        return f'Amount: {self.amount} Currency {self.currency}, Transaction type: {self.transaction_type}, Time= {self.time_stamp}'

    def __repr__(self):
        """
            Returns a developer-friendly string representation of the transaction.
            :return: String in the format: Transaction(ID=..., Type=..., ...)
        """
        return f"Transaction(ID={self.transaction_id}, Type={self.transaction_type}, Amount={self.amount}, Time={self.time_stamp})"

    def to_dict(self):
        """
            Converts the transaction into a dictionary for JSON serialization.
            :return: Dictionary with transaction fields
        """
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "currency": self.currency,
            "time_stamp": self.time_stamp.isoformat()
        }



    @staticmethod
    def from_dict(data):
        """
               Creates a Transaction object from a dictionary (typically from JSON).
               :param data: Dictionary containing transaction fields
               :return: Transaction object
        """
        return Transaction(
            transaction_id=data["transaction_id"],
            amount=data["amount"],
            transaction_type=data["transaction_type"],
            currency=data["currency"],
            time_stamp=datetime.fromisoformat(data["time_stamp"])
        )