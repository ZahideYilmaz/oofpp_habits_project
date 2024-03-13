"""
This module provide the interactive interface for functionality provided by the tracking_classes module.
These functions query for user input required for the methods of the classes defined in tracking classes by utilizing
the questionary library and execute the corresponding tracking methods. Some of them also use the interactive helper
functions defined in the module helper_functions_interactive to get the users input.

Functions and target method:
- add_habit_interactive:        User.add_habit
- delete_habit_interactive:     User.delete_habit
- edit_habit_interactive:       Habit.edit_habit
- create_checkoff_interactive:  Habit.create_checkoff
- delete_checkoff_interactive:  Habit.delete_checkoff
- login_user_interactive:       DBConnector.login_user
- register_user_interactive:    DBConnector.register_user
- delete_user_interactive:      DBConnector.delete_user

"""

from tracking_classes import Habit, DBConnector, User
from helpers_interactive import *
from helpers import convert_to_datetime


def add_habit_interactive():
    """
    Gets user input for and executes the constructor of class Habit to create new habit instance.
    Adds the resulting habit to the list of the users habit using the method add_habit of class User.
    """
    questions = [{"type": "text",
                  "name": "habit_name",
                  "message": "Which name should the new habit have? Choose a non empty string!",
                  "validate": questionary_validator_non_empty_string},
                 {"type": "select",
                  "name": "period_unit",
                  "message": "In what period unit should the period be measured?",
                  "choices": period_units,
                  "default": "days"},
                 {"type": "text",
                  "name": "period_length",
                  "message": "Which period length? Choose a positive integer!",
                  "validate": questionary_validator_positive_integer,
                  "filter": int,
                  "default": "1"},
                 {"type": "text",
                  "name": "required_checkoffs",
                  "message": "How many required checkoffs? Choose a positive integer!",
                  "validate": questionary_validator_positive_integer,
                  "filter": int,
                  "default": "1"},
                 {"type": "text",
                  "name": "habit_description",
                  "message": "Do you want to add a description to your habit? You can also leave it empty!",
                  "default": ""}
                 ]
    # questionary.prompt returns a dictionary of user inputs with the questions names as keys.
    answers = questionary.prompt(questions)

    # if user cancels any of the questions, exit function.
    if len(answers) == 0:
        return

    # Else (user provided input parameters for Habit constructor):
    habit = Habit(**answers)  # unpack answers dictionary
    User.add_habit(habit)


def delete_habit_interactive():
    """
    Lets user choose a habit and delete it.
    Utilizes the Habit method delete_habit.
    """
    habit = get_habit_interactive()

    # If user cancels during habit selection, exit function.
    if habit is None:
        return

    confirmation = questionary.confirm(f"Are you sure you want to delete the habit {habit.habit_name}?").ask()

    # If user cancels the confirmation question or answers no, exit the function.
    if not confirmation:
        return

    User.delete_habit(habit.habit_name)


def edit_habit_interactive():
    """
    Lets user edit an existing habit. The user can choose to edit a habits periodicity, or it's description.
    Utilizes Habit method edit_habit.
    """
    habit = get_habit_interactive()

    if habit is None:
        return

    edit_habit_mode = questionary.select("Which properties of the habit do you want to edit?",
                                         choices=["periodicity", "description"]).ask()
    if edit_habit_mode is None:
        return

    # Define appropriate set of questionary questions in dictionary form.
    # Depending on if the user wants to edit the habits periodicity or description.
    if edit_habit_mode == "description":
        questions = [{"type": "text",
                      "name": "habit_description",
                      "message": "Edit the description!",
                      "default": habit.habit_description}]
    else:
        questions = [{"type": "select",
                      "name": "period_unit",
                      "message": "Edit the period_unit!",
                      "choices": period_units,
                      "default": habit.period_unit},
                     {"type": "text",
                      "name": "period_length",
                      "message": "Edit the period length! Choose a positive integer!",
                      "validate": questionary_validator_positive_integer,
                      "filter": int,
                      "default": str(habit.period_length)},
                     {"type": "text",
                      "name": "required_checkoffs",
                      "message": "Edit the required checkoffs! Choose a positive integer!",
                      "validate": questionary_validator_positive_integer,
                      "filter": int,
                      "default": str(habit.required_checkoffs)}]

    answers = questionary.prompt(questions)

    # if user cancels any of the questions, exit function.
    if len(answers) == 0:
        return

    habit.edit_habit(**answers)


def create_checkoff_interactive():
    """
    Lets user create a checkoff for an existing habit. User can optionally provide a checkoff timestamp
    or alternatively create a checkoff for the current timestamp.  Utilizes Habit method create_checkoff.
    """
    habit = get_habit_interactive()

    if habit is None:
        return

    # Asks user if the checkoff is to be for a timestamp in the past.
    create_checkoff_for_past = questionary.confirm("Do you want to to check off a timestamp in the past?").ask()

    if create_checkoff_for_past is None:
        return

    # If checkoff is for the current time, create_checkoff is executed with no optional input.
    elif not create_checkoff_for_past:
        habit.create_checkoff()

    # If checkoff is intended for a time in the past ...
    else:
        # ... ask user  for a timestamp.
        checkoff = questionary.text(message="Enter a valid timestamp in format 'YYYY:MM:DD hh:mm'!"
                                            "Hours and Minutes optional.",
                                    validate=questionary_validator_datetime_string).ask()
        if checkoff is None:
            return
        # ... and execute create_checkoff for the converted datetime value of the user input.
        habit.create_checkoff(convert_to_datetime(checkoff))


def delete_checkoff_interactive():
    """
    Lets user delete an existing checkoff for a chosen habit. Utilizes Habit method delete_checkoff.
    """
    # Lets user pick a habit.
    habit = get_habit_interactive()

    # if user cancels the habit selection, exit function.
    if habit is None:
        return

    # if user cancels any of the questions, exit function.
    if len(habit.checkoff_list) == 0:
        print("No checkoffs to delete")
        return

    # calculates a list with the checkoff timestamps of chosen habit as strings.
    checkoffs_as_strings_list = [checkoff.strftime("%Y-%m-%d %H:%M") for checkoff in habit.checkoff_list]

    # Lets User pick from this list of checkoff timestamps.
    checkoff = questionary.select("Select the checkoff to delete.", choices=checkoffs_as_strings_list).ask()

    if checkoff is None:
        return

    # Asks user to confirm the deletion of the chosen checkoff.
    confirmation = questionary.confirm(f"Are you sure you want to delete this checkoff?").ask()

    if not confirmation:
        return

    habit.delete_checkoff(convert_to_datetime(checkoff))


def login_user_interactive():
    """
    Asks user for login credentials. Executes DBConnector method login_user.
    """
    questions = [
        {"type": "text",
         "name": "user_name",
         "message": "Type in your username!",
         "validate": questionary_validator_non_empty_string},
        {"name": "password",
         "type": "password",
         "message": "Type in your password!",
         "validate": questionary_validator_non_empty_string}
    ]
    answers = questionary.prompt(questions)

    # if user cancels any of the questions, exit function.
    if len(answers) == 0:
        return

    db_connector = DBConnector()
    db_connector.login_user(**answers)


def register_user_interactive():
    """
    Asks user for credentials to register as a new user. Executes DBConnector method register_user.
    """
    questions = [
        {"type": "text",
         "name": "user_name",
         "message": "Choose a username (non empty string)!",
         "validate": questionary_validator_non_empty_string},
        {"name": "password",
         "type": "password",
         "message": "Choose a password (non empty string)!",
         "validate": questionary_validator_non_empty_string}
    ]
    answers = questionary.prompt(questions)

    # if user cancels any of the questions, exit function.
    if len(answers) == 0:
        return

    db_connector = DBConnector()
    db_connector.register_user(**answers)


def delete_user_interactive():
    """
    Asks user for credentials to delete an existing user profile. Executes DBConnector method delete_user_data.
    """
    questions = [
        {"type": "text",
         "name": "user_name",
         "message": "Type in your username!",
         "validate": questionary_validator_non_empty_string},
        {"name": "password",
         "type": "password",
         "message": "Type in your password!",
         "validate": questionary_validator_non_empty_string}
    ]
    answers = questionary.prompt(questions)

    # if user cancels any of the questions, exit function.
    if len(answers) == 0:
        return

    confirmation = questionary.confirm(f"Are you sure you want to delete you user profile, {User.user_name}?").ask()

    # if user cancels the confirmation question or answers no, exit function.
    if not confirmation:
        return

    db_connector = DBConnector()
    db_connector.delete_user_data(**answers)
