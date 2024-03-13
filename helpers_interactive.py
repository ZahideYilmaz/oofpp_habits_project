"""
This module contains interactive helper functions, i.e. helper functions that contain interactive queries for user
input implemented using the questionary library. These helper functions are mainly used in the modules
- tracking_interactive
- analysis_functions_interactive

Constant:
- period_units

Functions:
- questionary_validator_non_empty_string: Checks if user input is non-empty string.
- questionary_validator_positive_integer: Checks if user input can be converted to a positive integer.
- questionary_validator_datetime_string: Checks if user input can be converted to a datetime.
- questionary_validator_date_string: Checks if user input can be converted to a date.
- get_habit_interactive: Lets the user choose one of his/her habits by name.
- filter_habit_list_interactive: Lets the user filter his/her habits by periodicity attributes.
- get_optional_start_date_interactive: Gives the user the opportunity to input a start date (for analysis functions).
"""

import questionary
from tracking_classes import User
from helpers import convert_to_datetime
from datetime import datetime
period_units = ["days", "weeks", "months"]


def questionary_validator_non_empty_string(value: str) -> bool:
    """
    Validator function used for questionary questions, that require non-empty string inputs from user.

    Parameters:
    - value: (str): Any user input.

    Returns:
    bool: True if value is a non-empty string, else False.
    """
    result = isinstance(value, str)
    if result:
        result = result and len(value) > 0
    return result


def questionary_validator_positive_integer(value):
    """
    Validator function used for questionary questions, that require a positive integer as user input.

    Parameters:
    - value: (str): Any user input.

    Returns:
    bool: True if value is a positive integer, else False.
    """
    try:
        int(value)
    except ValueError:
        return False
    return int(value) >= 0


def questionary_validator_datetime_string(value):
    """
    Validator function used for questionary questions, that require a datetime string as user input.
    Datetime strings in the formats "%Y-%m-%d %H:%M" and "%Y-%m-%d %H" are accepted.

    Parameters:
    - value: (str): Any user input.

    Returns:
    bool: True if value is a datetime string, else False.
    """
    formats = ["%Y-%m-%d %H:%M", "%Y-%m-%d %H"]
    for format_str in formats:
        try:
            datetime.strptime(value, format_str)
            return True
        except ValueError:
            pass  # Try the next format if the current one fails
    # If none of the formats match
    return False


def questionary_validator_date_string(value):
    """
    Validator function used for questionary questions, that require a date string as user input.
    Date strings have to have the format "%Y-%m-%d".

    Parameters:
    - value: (str): Any user input.

    Returns:
    bool: True if value is a date string, else False.
    """
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_habit_interactive():
    """
    Gets user input for and executes the get_habit method of class User, returns the resulting instance of habit.
    Steps:
    - Presents the user with a list of the names of his/her habits.
    - Executes the get_habit method of class User for the chosen habit name.
    - Returns the resulting instance of habit.

    Returns:
    Habit: The habit instance selected by the user from a list of habit names.
    """
    habit_name_list = User.get_habit_name_list()

    if len(habit_name_list) == 0:
        print("No habits to choose!")
        return

    habit_name = questionary.select("Pick a habit!", habit_name_list).ask()

    # if user cancels the habit selection, exit function.
    if habit_name is None:
        return
    return User.get_habit(habit_name)


def filter_habit_list_interactive():
    """
    Gets user input for and executes the filter_habit_list method of class User, returns the resulting list of habits.
    Thereby lets the user filter his/her habits by periodicity attributes
    Returns:
    list[Habit]: Potentially filtered list of habits.
    """
    questions = [
        {"type": "select",
         "name": "period_unit",
         "message": "Select a period unit value to filter by.",
         "choices": period_units},
        {"type": "text",
         "name": "period_length",
         "message": "Type a period length to filter by.",
         "validate": questionary_validator_positive_integer,
         "default": "1",
         "filter": int},
        {"type": "text",
         "name": "required_checkoffs",
         "message": "Type a required checkoff value to filter by.",
         "validate": questionary_validator_positive_integer,
         "default": "1",
         "filter": int}]

    # Asks the user, if the list of habits should be filtered.
    filter_habits = questionary.confirm("Do you want to filter your habits by periodicity?").ask()

    #  If the user cancels the question, exit function.
    if filter_habits is None:
        return

    # If the user does not want to filter the habit list, return the entire list of the users habits.
    if not filter_habits:
        return User.habit_list

    # Else (user wants to filter), ask the questions to get the filter criteria. Resulting answers is a dictionary.
    answers = questionary.prompt(questions)

    # If the answers dictionary is empty, the user has cancelled the questions. Exit function.
    if len(answers) == 0:
        return

    # Else (user provided filter criteria): Execute filter_habit_list method of class User with provided user input.
    filtered_habit_list = User.filter_habit_list(**answers)

    # Return resulting filtered list of habits.
    return filtered_habit_list


def get_optional_start_date_interactive():
    """
    Gets a start date string from user input.
    Returns the input converted to datetime.

    Returns:
    datetime: user input for start date (for analysis functions) converted to datetime.
    """
    message = "Choose an explicit analysis start? Enter a valid date string('YYYY:MM:DD')! If not, take the default!"

    start_date = questionary.text(message, default="1999-01-01", validate=questionary_validator_date_string).ask()

    # if user cancels question, exit the function
    if start_date is None:
        return

    return convert_to_datetime(start_date)
