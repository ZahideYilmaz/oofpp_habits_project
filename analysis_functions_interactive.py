"""
This module provides the interactive interface for analysis functionality provided by the analysis_functions module.
These functions query for user input required for the analysis functions by using the questionary library and execute
the corresponding analysis functions sometimes in combination with the helper function print_df_prettily.

Functions and corresponding analysis functionality:
- print_checkoff_info_table_for_habit_interactive:          print_df_prettily(get_checkoff_info_table_for_habit(...))
- print_basic_habit_info_interactive:                       print_df_prettily(get_basic_habit_info(...))
- print_analysis_info_table_for_habit_interactive:          print_df_prettily(get_analysis_info_table_for_habit((...))
- print_basic_info_table_for_habit_list_interactive:        print_df_prettily(get_basic_info_table_for_habit_list((...))
- get_analysis_info_table_for_habit_list_interactive:       get_analysis_info_table_for_habit_list(...)
- print_analysis_info_table_for_habit_list_interactive:     print_df_prettily(get_analysis_info_table_for_habit_list(...))
- print_active_streak_info_for_habit_list_interactive:      print_active_streak_info_for_habit_list(...)
- print_max_streak_info_for_habit_list_interactive:         print_max_streak_info_for_habit_list(...)
- print_min_success_rate_info_for_habit_list_interactive:   print_min_success_rate_info_for_habit_list(...)

"""

from analysis_functions import *
from helpers_interactive import *
from helpers import convert_to_datetime


def print_checkoff_info_table_for_habit_interactive() -> None:
    """
    Gets user input for and executes get_checkoff_info_table_for_habit, prints the resulting DataFrame.
    """
    # let user choose a habit using interactive helper function get_habit_interactive.
    habit = get_habit_interactive()

    # if user cancels the habit selection, exit function.
    if habit is None:
        return

    questions = [{"type": "text",
                  "name": "start_date",
                  "message": "A start date to only see the checkoffs since ('YYYY-MM-DD'))?",
                  "default": "1999-01-01",
                  "validate": questionary_validator_date_string,
                  "filter": convert_to_datetime},
                 {"type": "text",
                  "name": "end_date",
                  "message": "An end time to only see the checkoffs since ('YYYY-MM-DD')?",
                  "default": "2500-01-01",
                  "validate": questionary_validator_date_string,
                  "filter": convert_to_datetime}
                 ]

    answers = questionary.prompt(questions)

    # if user cancels any of the questions, exit function.
    if habit is None or len(answers) == 0:
        return

    # Else, execute get_checkoff_info_table_for_habit using the chosen habit and the rest of the user input.
    # Print the resulting DataFrame.
    print_df_prettily(get_checkoff_info_table_for_habit(habit, **answers))


def print_basic_habit_info_interactive() -> None:
    """
    Lets user choose a habit and executes get_basic_habit_info.
    Prints the resulting DataFrame containing the basic habit infos for the chosen habit.
    """
    habit = get_habit_interactive()

    # if user cancels the habit selection, exit function.
    if habit is None:
        return

    info = get_basic_habit_info(habit)
    print_df_prettily(info)


def print_analysis_info_table_for_habit_interactive() -> None:
    """
    Gets user input for and executes get_analysis_info_table_for_habit, prints the resulting DataFrame.
    Steps:
    - Lets user choose habit from a list of habit names using the interactive helper function get_habit_interactive.
    - Gets a start date for the analysis from user via interactive helper function get_optional_start_date_interactive.
    """
    habit = get_habit_interactive()

    # if user cancels the habit selection, exit function.
    if habit is None:
        return

    start_date = get_optional_start_date_interactive()

    # if user cancels the start_date question, exit function.
    if start_date is None:
        return

    df = get_analysis_info_table_for_habit(habit, start_date)
    print_df_prettily(df)


def print_basic_info_table_for_habit_list_interactive() -> None:
    """
    Gets user input for and executes get_basic_info_table_for_habit_list, prints the resulting DataFrame.
    Steps:
    - Using interactive helper filter_habit_list_interactive, calculates a potentially filtered list of users habits.
    - Calculates a DataFrame containing basic infos for this list of habits using analysis function
      get_basic_info_table_for_habit_list.
    - Prints the resulting DataFrame.
    """
    habit_list = filter_habit_list_interactive()

    # if user cancels any of the habit list filtering questions, exit function.
    if habit_list is None:
        return

    # if habit list is empty, inform user. Do nothing.
    if len(habit_list) == 0:
        print("No habits to get infos about!")
        return

    df = get_basic_info_table_for_habit_list(habit_list)
    return print_df_prettily(df)


def get_analysis_info_table_for_habit_list_interactive() -> DataFrame:
    """
    Gets user input for and executes get_analysis_info_table_for_habit_list, returns the resulting DataFrame.
    Function is reused in the following interactive functions.

    Returns:
    DataFrame: A DataFrame with basic and analysis infos for multiple habits. None, if user cancels any of the questions
    or the habit list is empty.
    """
    habit_list = filter_habit_list_interactive()

    # if user cancels any of the habit list filtering questions, exit function.
    if habit_list is None:
        return

    if len(habit_list) == 0:
        print("No habits to get infos about!")
        return

    start_date = get_optional_start_date_interactive()

    # if user cancels any of start date questions, exit function.
    if start_date is None:
        return
    df = get_analysis_info_table_for_habit_list(habit_list, start_date)
    return df


def print_analysis_info_table_for_habit_list_interactive() -> None:
    """
    Executes the interactive function get_analysis_info_table_for_habit_list_interactive and prints the resulting
    DataFrame containing basic and analysis habit infos for a list of habits.
    """
    df = get_analysis_info_table_for_habit_list_interactive()

    # if user cancels any of the analysis questions, exit function.
    if df is None:
        return

    print_df_prettily(df)


def print_active_streak_info_for_habit_list_interactive():
    """
    Executes the interactive function get_analysis_info_table_for_habit_list_interactive.
    Executes the function print_active_streak_info_for_habit_list for the resulting DataFrame.
    As a result, this function prints infos about active streaks in a list of habits.
    """
    df = get_analysis_info_table_for_habit_list_interactive()

    # if user cancels any of the analysis questions, exit function.
    if df is None:
        return

    print_active_streak_info_for_habit_list(df)


def print_max_streak_info_for_habit_list_interactive() -> None:
    """
    Executes the interactive function get_analysis_info_table_for_habit_list_interactive.
    Executes the function print_max_streak_info_for_habit_list for the resulting DataFrame.
    As a result, this function prints infos about habits with the maximum max streak length in a list of habits.
    """
    df = get_analysis_info_table_for_habit_list_interactive()

    # if user cancels any of the analysis questions, exit function.
    if df is None:
        return

    print_max_streak_info_for_habit_list(df)


def print_min_success_rate_info_for_habit_list_interactive() -> None:
    """
    Executes the interactive function get_analysis_info_table_for_habit_list_interactive.
    Executes the function print_min_success_rate_info_for_habit_list for the resulting DataFrame.
    As a result, this function prints infos about habits with the minimum success rate in a list of habits.
    """
    df = get_analysis_info_table_for_habit_list_interactive()

    # if user cancels any of the analysis questions, exit function.
    if df is None:
        return

    print_min_success_rate_info_for_habit_list(df)
