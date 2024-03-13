"""
This module contains functions that can be used to get basic information
and derived analysis information about habits in a structured way.

Functions:
- get_basic_habit_info: Gets the basic attributes of a habit in DataFrame format.

- get_checkoff_info_table_for_habit: Gets the checkoff info for a habit in DataFrame format.

- get_basic_info_table_for_habit_list: Gets the basic attributes for a list of habits in DataFrame format.

- get_period_timedelta: Calculates a timedelta representation of the timespan of a habits period defined by the
                        attributes period_length and period_unit.

- get_period: Returns the index of the period that contains a given checkoff. The index is calculated relative to the
              analysis start date.

- prepare_analysis_start_date:  Adjusts the given start date for analysis if necessary
                                (i.e. if start date is before the habits creation).

- get_period_checkoff_dict: Returns dictionary with key value pairs of period indices and the period checkoff counts.

- calc_analysis_info: Calculates max_streak, active_streak and success_rate for a habit.

- get_analysis_info_table_for_habit: Returns a DataFrame containing basic habit infos and the analysis infos.

- get_analysis_info_table_for_habit_list: Multiple habit version of get_analysis_info_table_for_habit.

- print_max_streak_info_for_habit_list: Answers which habits have the maximum max_streak length in a group of habits.

- print_active_streak_info_for_habit_list: Answers which habits have active streaks in a group of habits.

- print_min_success_rate_info_for_habit_list: Answers which habits are the least successful in a group of habits.
"""

from tracking_classes import Habit
from datetime import datetime, timedelta, time
from helpers import print_df_prettily
from pandas import concat as df_concat, DataFrame


def get_basic_habit_info(habit: Habit) -> DataFrame:
    """
    Get the basic information about a habit.

    Parameters:
    - habit (Habit): A habit instance.

    Returns:
    DataFrame: A DataFrame containing basic information (instance attributes with values) of the provided habit.
    """
    attributes_df = DataFrame([vars(habit)])  # vars yields a dictionary with (instance_attribute:value) pairs.
    attributes_df = attributes_df.drop(columns='checkoff_list')  # drop attribute checkoff_list, readability
    return attributes_df


def prepare_analysis_start_date(habit: Habit, start_date: datetime = datetime(1999, 1, 1)) -> datetime:
    """
    Adjusts the start_date for the analysis core functions if necessary.

    Parameters:
    - habit (Habit): The habit instance.
    - start_date (datetime): The provided start_date as a datetime with no time values.

    Returns:
    datetime: The adjusted start_date.
    """
    # If the start_date is before the timestamp of the habit creation, adjust it to the date the habit was created.
    # This avoids artificially created unsuccessful periods in the timespan before habit creation.
    start_date = max(start_date, habit.create_datetime)
    start_date = datetime.combine(start_date, time.min)
    return start_date


def get_checkoff_info_table_for_habit(habit: Habit, start_date: datetime, end_date: datetime) -> DataFrame:
    """
    For a given habit, returns a DataFrame with the checkoff timestamps and the period indexes within a specified
    date range. The period indexes are calculated using get_period and are relative to the adjusted start_date.
    Adjustment to start_date made by function prepare_analysis_start_date.

    Parameters:
    - habit: The habit instance.
    - start_date (datetime): Start date for filtering checkoffs.
    - end_date (datetime): End date for filtering checkoffs.

    Returns:
    DataFrame: The DataFrame containing the numbered checkoff timestamps of the provided habit.
    """
    start_date = prepare_analysis_start_date(habit, start_date)
    df = DataFrame()
    df["checkoff"] = habit.list_checkoffs(start_date, end_date)
    df["period"] = get_period(df["checkoff"], start_date, get_period_timedelta(habit.period_unit, habit.period_length))
    return df


def get_basic_info_table_for_habit_list(habit_list: list[Habit]) -> DataFrame:
    """
    Returns a DataFrame with basic information for a list of habits.

    Parameters:
    - habit_list (list[Habit]): The provided list of habit instances.

    Returns:
    DataFrame: Contains basic information for the given habit list.
    """
    habit_info_df_list = [get_basic_habit_info(habit) for habit in habit_list]
    # df_concat creates a new Dataframe containing all rows from all DataFrames in the given list of DataFrames.
    # "ignore_index" ensures correct numbering.
    df = df_concat(habit_info_df_list, ignore_index=True)
    return df


def get_period_timedelta(period_unit: str, period_length: int) -> timedelta:
    """
    Calculate timedelta for a given period unit and length to represent the timespan of a habits period.
    A timedelta is a representation of the difference between two datetimes or in other words a timespan.

    Parameters:
    - period_unit (str): 'days', 'weeks' or 'months'.
    - period_length (int): Length of the period in the given period_unit.

    Returns:
    timedelta: The calculated timedelta representing the timespan of a habit's period.
    """
    if period_unit == 'weeks':
        period_timedelta = timedelta(weeks=period_length)
    elif period_unit == 'months':
        period_timedelta = timedelta(days=30 * period_length)
    else:
        period_timedelta = timedelta(days=period_length)
    return period_timedelta


def get_period(checkoff: datetime, start_date: datetime, period_timedelta: timedelta) -> int:
    """
    Returns the period index containing a given a checkoff relative to analysis start date.
    Indexing starts at 0.

    Parameters:
    - checkoff (datetime): The checkoff timestamp.
    - start_date (datetime): The start date for the analysis.
    - period_timedelta (timedelta): The timedelta for the habits period.

    Returns:
    int: A positive integer representing the period index for a checkoff (starting from 0).

    """
    # How often does the period timedelta fit into the distance between start_date and checkoff?
    return (checkoff - start_date) // period_timedelta


def get_period_checkoff_dict(habit: Habit, start_date=datetime(1999, 1, 1)) -> dict:
    """
    Returns a dictionary with period indices as keys and the corresponding checkoff count as the values.

    Parameters:
    - habit (Habit): The given habit instance.
    - start_date (datetime): The start date for the analysis.

    Returns:
    dict: A dictionary containing period indices and the corresponding checkoff counts.
    """
    period_checkoff_dict = {}  # initialize empty dictionary for result
    start_date = prepare_analysis_start_date(habit, start_date)  # adjust start_date if necessary
    period_timedelta = get_period_timedelta(habit.period_unit, habit.period_length)

    # filter checkoff_list, we are only concerned with checkoffs after the given start_date.
    checkoff_list_filtered = habit.list_checkoffs(start_date)

    # Return the empty dictionary if no checkoffs are found after the start_date.
    if len(checkoff_list_filtered) == 0:
        return period_checkoff_dict

    # Iterate over all relevant checkoffs.
    for checkoff in checkoff_list_filtered:
        # calculate the index of the period containing the checkoff
        period_index = get_period(checkoff, start_date, period_timedelta)
        # For each checkoff in a period, add 1 to corresponding checkoff count.
        # (period_checkoff_dict.get(period_index, 0) returns 0 if period_index was not already a key of the dictionary.)
        period_checkoff_dict[period_index] = period_checkoff_dict.get(period_index, 0) + 1
    return period_checkoff_dict


def calc_analysis_info(habit: Habit, start_date=datetime(1999, 1, 1)) -> dict:
    """
    Calculates the derived analysis information (max_streak, active_streak,success_rate) for a habit.
    Returns them in a dictionary. Core function of the analysis_functions module.

    Parameters:
    - habit (Habit): The habit instance.
    - start_date (datetime): The start date for analysis.

    Returns:
    dict: A dictionary containing analysis information.
    """
    start_date = prepare_analysis_start_date(habit, start_date)

    # Get the dictionary mapping period indices to the count of checkoffs within the period.
    period_checkoff_dict = get_period_checkoff_dict(habit, start_date)

    # Prepare result dictionary.
    analysis_info_dict = {"max_streak": 0, "active_streak": 0, "success_rate": 0}

    if len(period_checkoff_dict) == 0:
        return analysis_info_dict

    period_timedelta = get_period_timedelta(habit.period_unit, habit.period_length)
    # The last period, i.e. the running period that has not ended yet, is the one that includes the current timestamp.
    last_period = get_period(datetime.now(), start_date, period_timedelta)
    nr_of_periods = last_period + 1

    # temporary variables for loop calculation
    max_streak = 0
    active_streak = 0
    current_streak = 0
    nr_of_success_periods = 0

    # Iterate through period indices in sorted order
    for period_index in sorted(period_checkoff_dict.keys()):
        # A period is successful, if the checkoff count is equal to or greater than habit.required_checkoffs
        success = (period_checkoff_dict.get(period_index) >= habit.required_checkoffs)
        # Same calculation for next period (consider case if it is not included in the period_checkoff_dict)
        next_period_success = period_checkoff_dict.get(period_index + 1, 0) >= habit.required_checkoffs
        if success:
            # In case of success ...
            # 1) current streak gets higher by 1
            # 2) total number of successes gets higher by 1.
            current_streak += 1
            nr_of_success_periods += 1
        if not next_period_success and current_streak > 0:
            # If the next period is not successful, but we have a current streak...
            # 1) ... we can update max streak to current streak, if the current streak is longer.
            max_streak = max(max_streak, current_streak)
            # 2) ... check, if the current streak is active
            # (i.e. if it's last successful period is the running period(last_period) or the period right before it)
            streak_active = (last_period - period_index <= 1)
            if streak_active:
                # If it is active, we have found the active streak length.
                active_streak = current_streak
            # 3) ... reset the current streak to 0, because the streak is broken.
            current_streak = 0

    # Calculate the success_rate (the ratio of successful periods to all periods).
    success_rate = nr_of_success_periods / nr_of_periods
    success_rate = round(success_rate, 2)

    # Populate the result dictionary with calculated values.
    analysis_info_dict["success_rate"] = success_rate
    analysis_info_dict["max_streak"] = max_streak
    analysis_info_dict["active_streak"] = active_streak

    return analysis_info_dict


def get_analysis_info_table_for_habit(habit: Habit,
                                      start_date: datetime = datetime(1999, 1, 1)) -> DataFrame:
    """
    For a provided habit, the function returns a DataFrame with the basic information and the analysis information
    calculated using calc_analysis_info (max_streak, active_streak,success_rate).

    Parameters:
    - habit (Habit): The habit instance.
    - start_date (datetime): The start date for analysis.

    Returns:
    DataFrame: A Dataframe containing basic and analysis information for the provided habit.
    """
    analysis_info_dict = calc_analysis_info(habit, start_date)

    df = get_basic_habit_info(habit)
    df["max_streak"] = analysis_info_dict["max_streak"]
    df["active_streak"] = analysis_info_dict["active_streak"]
    df["success_rate"] = analysis_info_dict["success_rate"]
    return df


def get_analysis_info_table_for_habit_list(habit_list: list[Habit],
                                           start_date: datetime = datetime(1999, 1, 1)) -> DataFrame:
    """
    For a provided list of habits, the function returns a DataFrame with the basic information and the analysis
    information calculated using calc_analysis_info (max_streak, active_streak,success_rate) for each habit.

    Parameters:
    - habit_list (list[Habit]): A list of habit instances.
    - start_date (datetime): The start date for analysis.

    Returns:
    DataFrame: A Dataframe containing basic and analysis information for the provided habit list.
    """
    # Calculate the analysis info DataFrames for all habits in habit_list and write them in a list of DataFrames.
    analysis_info_table_list = [get_analysis_info_table_for_habit(habit, start_date) for habit in habit_list]
    # df_concat creates a new Dataframe containing all rows from all DataFrames in the given list of DataFrames.
    # "ignore_index" ensures correct numbering.
    return df_concat(analysis_info_table_list, ignore_index=True)


def print_max_streak_info_for_habit_list(df: DataFrame) -> int:
    """
    Given a DataFrame with the basic information and the analysis information (calculated using
    get_analysis_info_table_for_habit_list) for a list of habits, this function prints
    information about habits with the longest max streak included in this DataFrame. For test purposes,
    it also returns the longest max streak.

    Parameters:
    - df: A Dataframe containing basic and analysis information for each habit in a list of habits.

    Returns:
    int: The number of habits with the longest max streaks included in the provided DataFrame.
    """
    # calculate the maximum of the values in the column "max_streak" in the provided DataFrame containing analysis info.
    max_group_streak = df["max_streak"].max()

    # "Filter" the DataFrame, keep only rows, where max_streak has the calculated maximum value.
    df = df[df["max_streak"] == max_group_streak]

    # print and return info
    print_df_prettily(df)
    print(f"These are the habits with the longest max streak length in this group, which is {max_group_streak}.")
    return max_group_streak


def print_active_streak_info_for_habit_list(df: DataFrame) -> int:
    """
    Given a DataFrame with the basic information and the analysis information
    (calculated using get_analysis_info_table_for_habit_list) for a list of habits, this function prints
    information about habits with active streaks that are included in this DataFrame. For test purposes,
    it also returns the number of such habits.

    Parameters:
    - df: A Dataframe containing basic and analysis information for each habit in a list of habits.

    Returns:
    int: The number of habits with active streaks included in the provided DataFrame.
    """
    # "Filter" the given DataFrame, only keep rows where column "active_streak" is greater than 0.
    df = df[df["active_streak"] > 0]

    # print and return info
    print_df_prettily(df)
    print(f"These are the habits with active streaks in this group.")
    return len(df)


def print_min_success_rate_info_for_habit_list(df: DataFrame) -> int:
    """
    Given a DataFrame with the basic information and the analysis information
    (calculated using get_analysis_info_table_for_habit_list) for a list of habits, this function prints
    information about habits with the lowest success rate included in this DataFrame. For test purposes,
    it also returns the lowest success rate found.

    Parameters:
    - df: A Dataframe containing basic and analysis information for each habit in a list of habits.

    Returns:
    int: The lowest success rate for habits included in the provided DataFrame.
    """
    # calculate the minimum of the values in column success_rate
    min_group_success_rate = df["success_rate"].min()

    # "Filter" the DataFrame, keep only rows, where success_rate has the calculated minimum value.
    df = df[df["success_rate"] == min_group_success_rate]

    # print and return info
    print_df_prettily(df)
    print(f"These are the habits you struggled most with in this group (success rate of {min_group_success_rate})")
    return min_group_success_rate
