"""
This module contains the classes modeled for the Habit tracker. They are used to track habits and their checkoffs.

Classes:
- Habit:        Models a habit with attributes and provides functionality to track the checkoffs.
- User:         Models the User and provides class methods to track the Users habits.
- DBConnector:  Enables loading and unloading tracking data for users into the sqlite3 database 'habit_db'.
"""

from datetime import datetime
import sqlite3
import hashlib
from helpers import convert_to_datetime

class Habit:
    """
        A class that models a habit with its attributes including periodicity.
        This class provides functionality to track checkoffs for a habit.
    """

    def __init__(self, habit_name: str, period_unit: str = "days", period_length: int = 1, required_checkoffs: int = 1,
                 habit_description: str = "", create_datetime: datetime = None):
        """
        Initializes the habit with given attribute values or defaults.

        Parameters:
        - habit_name (str): Non-empty string.
        - period_unit (str): Optional. One of the values "days", "weeks", "months". Default "days"
        - period_length (int): Optional. Positive integer. Default 1.
        - required_checkoffs (int): Optional. Positive integer. Default 1.
        - habit_description (str): Optional. Default "".
        - create_datetime (datetime): Optional timestamp. If not given, it is set to current timestamp.
        """
        if create_datetime is None:  # new habits not loaded from db backup get the current time as create_datetime
            create_datetime = datetime.now().replace(second=0, microsecond=0)

        self.habit_name = habit_name
        self.period_unit = period_unit
        self.period_length = period_length
        self.required_checkoffs = required_checkoffs
        self.habit_description = habit_description
        self.create_datetime = create_datetime
        self.checkoff_list = []

    def create_checkoff(self, checkoff: datetime = None) -> None:
        """
        Creates a new checkoff for the habit by adding it to the attribute checkoff_list.

        Parameters:
        - checkoff (datetime): Optional timestamp for the checkoff, if it is logged for the past.

        Returns:
        None
        """
        if checkoff is None:  # if no checkoff is given, then take the current time
            checkoff = datetime.now().replace(second=0, microsecond=0)

        if checkoff in self.checkoff_list:  # if checkoff for the same timestamp already exists, print info, do nothing
            print(f"The checkoff {checkoff} already exists!")
            return

        if checkoff > datetime.now():  # if checkoff is in the future, print info, do nothing
            print("You can't log checkoffs for the future!")
            return

        if checkoff < self.create_datetime:  # if checkoff is before habit creation, print info, do nothing
            print(f"You can't log checkoff {checkoff} for before you created the habit"
                  f" at ({self.create_datetime})!")
            return

        self.checkoff_list.append(checkoff)
        self.checkoff_list.sort()  # sort checkoff_list (ascending) for future analysis
        print(f"Checkoff with timestamp {checkoff} successfully created!")

    def delete_checkoff(self, checkoff: datetime) -> None:
        """
        Deletes an existing checkoff for the habit by removing it from the attribute checkoff_list.

        Parameters:
        - checkoff (datetime): Timestamp of the checkoff to be deleted.

        Returns:
        None
        """
        if checkoff not in self.checkoff_list:  # if checkoff does not exist, inform user, do nothing
            print(f"No checkoff {checkoff} exists!")
            return

        self.checkoff_list.remove(checkoff)  # remove from checkoff_list
        print(f"Checkoff {checkoff} successfully deleted!")

    def list_checkoffs(self, start: datetime = None, end: datetime = None) -> list[datetime]:
        """
        Returns a list of the existing checkoffs, optionally only the ones between start and end.

        Parameters:
        - start (datetime): Optional. Timestamp for filtering of checkoff_list.
        - end (datetime): Optional. Timestamp for filtering of checkoff_list.

        Returns:
        list[datetime]: List of the checkoffs between start and end.
        """
        # set defaults for start and end if no value is provided.
        if start is None:
            start = datetime.min  # datetime(1,1,1,0,0)
        if end is None:
            end = datetime.max  # datetime(9999, 12, 31, 23, 59, 59, 999999)

        if len(self.checkoff_list) == 0:  # if no checkoffs exist, return an empty list
            return []

        return [checkoff for checkoff in self.checkoff_list if start <= checkoff <= end]  # return filtered list

    def edit_habit(self, period_unit: str = None, period_length: int = None, required_checkoffs: int = None,
                   habit_description: str = None) -> None:
        """
        Edit some habit attributes. The ones not given as input are not changed.

        Parameters:
        - period_unit (str): Optional. One of the values "days", "weeks", "months".
        - period_length (int): Optional. Positive integer.
        - required_checkoffs (int): Optional. Positive integer.
        - habit_description (str): Optional.

        Returns:
        None
        """
        if period_unit is not None:
            self.period_unit = period_unit
        if period_length is not None:
            self.period_length = period_length
        if required_checkoffs is not None:
            self.required_checkoffs = required_checkoffs
        if habit_description is not None:
            self.habit_description = habit_description


class User:
    """
        A class that models the User as a class with no instances and only class attributes and class methods.
        This class provides functionality to track habits (add, delete).

        Class Attributes:
        user_name (str): The chosen name for the user. Empty when not logged in yet.
        habit_list (list[Habit]): The list of the habits of the user. Initialized as empty list.
    """
    user_name: str = ""
    habit_list: list[Habit] = []

    @classmethod
    def get_habit_name_list(cls) -> list[str]:
        """
        Get a list of the names of the habits the user currently has.

        Returns:
        list[str]: List of the habit names for the user.
        """
        result = [habit.habit_name for habit in cls.habit_list]
        return result

    @classmethod
    def habit_exists(cls, habit_name: str) -> bool:
        """
        Check if a habit with the given name is included in users habits.

        Parameters:
        - habit_name (str): The name of the habit to search for.

        Returns:
        bool: True if habit exists in users habit_list, False if not.
        """
        return habit_name in cls.get_habit_name_list()

    @classmethod
    def get_habit(cls, habit_name: str) -> Habit:
        """
        Returns the habit with the given habit_name. Returns None if the habit is not part of users habits.

        Parameters:
        - habit_name (str): The name of the habit to return.

        Returns:
        Habit: The desired habit with the given habit_name.
        """
        for habit in cls.habit_list:  # loop through all habits of the user
            if habit.habit_name == habit_name:  # only if the habits name matches the given habit_name
                return habit  # return the habit
        # if no habit matches the given name, return value is None

    @classmethod
    def delete_habit(cls, habit_name: str):
        """
        Removes a habit of the user by removing it from the users habit_list.

        Parameters:
        - habit_name (str): The name of the habit to delete.

        Returns:
        None
        """
        if not cls.habit_exists(habit_name):  # if no habit with the given habit_name exists, print info, do nothing.
            print(f"No habit with the name {habit_name} exists!")
            return

        habit = cls.get_habit(habit_name)  # get habit to be deleted
        cls.habit_list.remove(habit)  # remove habit from habit_list
        print(f"Habit {habit_name} successfully deleted!")

    @classmethod
    def add_habit(cls, habit: Habit) -> None:
        """
        Adds a habit to the users habit_list.

        Parameters:
        - habit (Habit): The new habit as an instance of class Habit.

        Returns:
        None
        """
        if cls.habit_exists(habit.habit_name):  # if habit with the same name already exists, print info, do nothing ...
            print("This habit already exists!")
            return

        cls.habit_list.append(habit)  # ... else append habit to habit_list
        print(f"Habit {habit.habit_name} successfully added!")

    @classmethod
    def filter_habit_list(cls, period_unit: str, period_length: int, required_checkoffs: int) -> list[Habit]:
        """
        Returns a filtered list of the users habits.

        Parameters:
        - period_unit (str): Filter for habit attribute period_unit.
        - period_length (int): Filter for habit attribute period_length.
        - required_checkoffs (int): Filter for habit attribute required_checkoffs.

        Returns:
        - list[Habit]: List of user habits matching the filters for the periodicity attributes.
        """
        if len(User.habit_list) == 0:  # if user has no habits, return empty list
            return []

        # filter habit_list
        habit_list = [habit for habit in User.habit_list if habit.period_unit == period_unit
                      and habit.period_length == period_length and habit.required_checkoffs == required_checkoffs]

        return habit_list


class DBConnector:
    """
        A class to enable the loading and unloading of tracking data for users into the sqlite3 database 'habit_db'.
    """
    def __init__(self):
        """
        Initializes the DBConnector instance with the name of the sqlite3 database.
        """
        self.dbname = 'habit.db'

    def setup_database(self) -> None:
        """
        Sets up the required tables (User, Habit, Checkoff) in the sqlite3 database if they don't exist.
        """
        create_user_table = '''
        CREATE TABLE IF NOT EXISTS User (
            user_name TEXT, 
            password TEXT,
            Primary Key(user_name)
        )'''                                    # user_name should be unique.

        create_habit_table = '''
        CREATE TABLE IF NOT EXISTS Habit (
            user_name TEXT,
            habit_name TEXT,
            period_unit TEXT,
            period_length INTEGER,
            required_checkoffs INTEGER,
            habit_description TEXT,
            create_datetime DATETIME,
            Primary Key(user_name, habit_name) 
        )'''                                    # (user_name, habit_name) should be unique in habit table.

        create_checkoff_table = '''
        CREATE TABLE IF NOT EXISTS Checkoff (
            user_name TEXT,
            habit_name TEXT,
            checkoff DATETIME,
            Primary Key(user_name, habit_name, checkoff)
        )'''                                    # (user_name, habit_name, checkoff) should be unique in checkoff table.

        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()
        cursor.execute(create_user_table)
        cursor.execute(create_habit_table)
        cursor.execute(create_checkoff_table)
        connection.commit()
        connection.close()

    def register_user(self, user_name, password) -> bool:
        """
        Registers a new user in the database with the provided username and the hash of the provided password.

        Parameters:
        - user_name (str): The chosen name of the new user.
        - password (str): The chosen password for the new user.

        Returns:
        bool: True, if registration is successful. False, if a user with provided username already exists.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # hash provided password
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()
        try:
            # Insert user credentials into User table
            cursor.execute('INSERT INTO User VALUES (?, ?)', (user_name, hashed_password))
            connection.commit()
            User.user_name = user_name
        # If we try to insert non-unique username in User table, db raises exception
        except sqlite3.IntegrityError:
            print(f"Could not register User {user_name}! This User already exists.")
            connection.close()
            # If user can't be registered, because name is not unique, return False.
            return False

        connection.close()
        print("Registration successful!")
        return True

    def verify_user(self, user_name, password) -> bool:
        """
        Verifies if the provided user credentials match an existing user in the database.

        Parameters:
        - user_name (str): The username to verify.
        - password (str): The un-hashed password to verify.

        Returns:
        bool: True, if the user is verified. Else, False.
        """
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # hashed password

        # Execute select to check if user_name and hashed password exist in User table.
        cursor.execute('SELECT * FROM User WHERE user_name=? AND password=?', (user_name, hashed_password))

        # (bool) result: True if select returns row, else False.
        result = cursor.fetchone() is not None

        connection.close()
        return result

    def unload_data(self) -> None:
        """
        Unloads the tracking data (habits and checkoffs) for the current user from the database.
        Tracking data is loaded into class instances of Habit and into class User.
        """
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        # Select all rows in Habit table corresponding to current users name
        db_habits = cursor.execute('SELECT * FROM Habit WHERE user_name = ?',
                                   (User.user_name,)).fetchall()

        # If no rows could be selected, print info. Unload nothing.
        if len(db_habits) == 0:
            print(f"Oh, no habit backups found for user {User.user_name}. Starting on a blank canvas!")
            return

        # If rows from Habit table could be selected for current user, iterate through all rows.
        for row in db_habits:
            # row[0]: user_name,            row[1]: habit_name ,        row[2]: period_unit,    row[3]: period_length,
            # row[4]: required_checkoffs,   row[5]: habit_description,  row[6]: create_datetime.

            # Recreate Habit instance using row from db Habit table.
            habit = Habit(row[1], row[2], row[3], row[4], row[5], convert_to_datetime(row[6]))

            # Add the recreated habit to users habit_list.
            User.add_habit(habit)

        # Iterate over all habits, that are now in the users habit_list
        for habit in User.habit_list:
            # Select all checkoff rows belonging to the current user and current habit.
            db_checkoffs = cursor.execute('SELECT * FROM Checkoff where user_name = ? and habit_name = ?',
                                          (User.user_name, habit.habit_name)).fetchall()
            # Iterate over all selected checkoff rows.
            for row in db_checkoffs:
                # row[0]: user_name,    row[1]: habit_name,     row[2]: checkoff.

                # recreate checkoff
                habit.create_checkoff(convert_to_datetime(row[2]))
        connection.close()

    def login_user(self, user_name, password) -> bool:
        """
        Logs in a user. First verifies provided credentials. If successful, unloads data from the database.

        Parameters:
        - user_name (str): The provided username for the login.
        - password (str): The provided password for the login.

        Returns:
        bool: True if login is successful, False otherwise.
        """
        if self.verify_user(user_name, password):
            User.user_name = user_name
            self.unload_data()
            print("Login successful!")
            return True
        else:
            print("Login failed.")
            return False

    def load_data(self) -> None:
        """
        Loads the tracking data from the User class and the Habit instances into the sqlite3 database.
        """
        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        # Execute delete statements to remove all potential tracking data related to current user, so that the current
        # tracking data can be loaded.
        cursor.execute('DELETE FROM Habit WHERE user_name =?', (User.user_name,))
        cursor.execute('DELETE FROM Checkoff WHERE user_name =?', (User.user_name,))

        for habit in User.habit_list:
            # For each habit, execute insert statement to load data from the Habit instance into the db.
            # Use datetime.strftime to convert datetime into timestamp string before insertion.
            cursor.execute('INSERT INTO Habit values(?,?,?,?,?,?,?)',
                           (User.user_name, habit.habit_name, habit.period_unit,
                            habit.period_length, habit.required_checkoffs, habit.habit_description,
                            habit.create_datetime.strftime('%Y-%m-%d %H:%M')))

            for checkoff in habit.checkoff_list:
                # For each of the habits checkoff, execute insert statement to load the checkoff times into the db.
                # Use datetime.strftime to convert datetime into timestamp string before insertion.
                cursor.execute('INSERT INTO Checkoff values (?,?,?)',
                               (User.user_name, habit.habit_name, checkoff.strftime('%Y-%m-%d %H:%M')))

        connection.commit()
        connection.close()
        print("User data loaded successfully into the database!")

    def delete_user_data(self, user_name, password) -> bool:
        """
        Deletes user data (user credentials, habits, checkoffs) from the database
        if provided credentials can be verified.

        Parameters:
        - user_name (str): The username of the user to delete.
        - password (str): The password of the user to delete.

        Returns:
        None
        """
        # verify credentials
        verified = self.verify_user(user_name, password)
        if not verified:
            print("Verification failed. Cannot delete the user profile!")
            return False

        connection = sqlite3.connect(self.dbname)
        cursor = connection.cursor()

        # Execute delete statements to remove all rows from all tables relating to verified user.
        cursor.execute('DELETE FROM User WHERE user_name =?', (user_name,))
        cursor.execute('DELETE FROM Habit WHERE user_name =?', (user_name,))
        cursor.execute('DELETE FROM Checkoff WHERE user_name =?', (user_name,))

        connection.commit()
        connection.close()
        print("User data successfully deleted!")
        return True
