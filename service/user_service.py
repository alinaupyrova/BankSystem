from models.user import  User
from service.file_manager import FileManager

class Userservice :
    """
      Userservice provides operations for user management such as registration, login, and retrieval.
      It interacts with the FileManager to persist user data.
    """

    @staticmethod
    def get_user(user_id: int)-> User:
        """
               Retrieves a User object by its user ID.

               :param user_id: The ID of the user to retrieve.
               :return: The User object with the given ID.
        """
        return User.get_user_id(user_id)

    @staticmethod
    def register(args):
        """
               Registers a new user with a unique ID.
               Loads existing users, generates a new ID, creates the user, and saves the updated list.

               :param args: An object with 'username' and 'surname' attributes.
        """
        users = FileManager.load_all_users()
        new_id = max([u.user_id for u in users], default=0) + 1
        user = User(user_id=new_id, username=args.username, surname=args.surname)
        users.append(user)
        FileManager.save_all_users(users)
        print(f"New user registered: {user.username} {user.surname}, ID: {new_id}")

    @staticmethod
    def login(args):
        """
               Logs in an existing user by verifying the provided user ID.
               Prints a welcome message if the user is found, otherwise displays an error.

               :param args: An object with a 'user_id' attribute.
        """
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if user:
            print(f"Hi, {user.username} {user.surname}!")
        else:
            print("User not found")
