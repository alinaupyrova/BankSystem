import os
import json
from models.user import User

class FileManager:
    """
        FileManager handles saving and loading all user data to/from a JSON file.
        This allows persistent storage of user accounts and their associated bank accounts and transactions.
    """

    USERS_FILE = "data/users.json"

    @staticmethod
    def save_all_users(users: list[User]) -> None:
        """
               Saves the list of User objects to a JSON file.
               If the directory does not exist, it creates it.

               :param users: A list of User objects to be saved.
        """
        os.makedirs('data', exist_ok=True)
        data = [user.to_dict() for user in users]
        with open(FileManager.USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all_users() -> list[User]:
        """
               Loads all users from the JSON file and returns them as a list of User objects.
               If the file does not exist, an empty list is returned.

               :return: A list of User objects.
               """
        if not os.path.exists(FileManager.USERS_FILE):
            return []
        with open(FileManager.USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [User.from_dict(user_data) for user_data in data]
