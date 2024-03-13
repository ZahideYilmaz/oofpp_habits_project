"""
This module provides some unit tests for the analysis functions defined in the analysis_functions module.
Some of the unit tests utilize freezegun.freeze_time to mock the current system time with a provided timestamp.
"""

from setup_test_tracking_data import (habit_weekly, habit_biweekly, habit_monthly, habit_daily, habit_daily2,
                                      example_habit_list)
from analysis_functions import *
from freezegun import freeze_time

dataframe_habit_weekly = DataFrame([{"habit_name": "climb_weekly", "period_unit": "weeks", "period_length": 1,
                                     "required_checkoffs": 1, "habit_description": "Go to climbing gym.",
                                     "create_datetime": datetime(year=2023, month=12, day=1)}])


def test_get_basic_habit_info_habit_weekly():
    assert dataframe_habit_weekly.compare(other=get_basic_habit_info(habit_weekly)).empty


def test_get_basic_info_table_for_habit_list_example_habit_list():
    result = get_basic_info_table_for_habit_list(example_habit_list)
    result_habit_weekly = result[result["habit_name"] == habit_weekly.habit_name]
    # resets index (to 0 for 1 expected row)
    result_habit_weekly = result_habit_weekly.reset_index(drop=True)
    assert len(result) == 5
    assert dataframe_habit_weekly.compare(result_habit_weekly).empty


def test_get_period():
    assert get_period(checkoff=datetime(2023, 12, 1, 0),
                      start_date=datetime(2023, 12, 1),
                      period_timedelta=timedelta(days=1)) == 0

    assert get_period(checkoff=datetime(2023, 12, 2, 13),
                      start_date=datetime(2023, 12, 1),
                      period_timedelta=timedelta(days=1)) == 1

    assert get_period(checkoff=datetime(2023, 12, 28, 18),
                      start_date=datetime(2023, 12, 1),
                      period_timedelta=timedelta(days=1)) == 27

    assert get_period(checkoff=datetime(2023, 12, 1, 18),
                      start_date=datetime(2023, 11, 15),
                      period_timedelta=timedelta(weeks=2)) == 1

    assert get_period(checkoff=datetime(2023, 11, 28, 23, 59),
                      start_date=datetime(2023, 11, 15),
                      period_timedelta=timedelta(weeks=2)) == 0

    assert get_period(checkoff=datetime(2023, 10, 9, 12),
                      start_date=datetime(2022, 8, 15),
                      period_timedelta=timedelta(days=30)) == 14


def test_get_period_timedelta():
    assert get_period_timedelta(habit_weekly.period_unit, habit_weekly.period_length) == timedelta(weeks=1)
    assert get_period_timedelta("days", 1) == timedelta(days=1)
    assert get_period_timedelta("days", 5) == timedelta(days=5)
    assert get_period_timedelta("months", 3) == timedelta(days=3 * 30)


def test_prepare_analysis_start_date():
    test_habit = Habit(habit_name="Dummy", create_datetime=datetime(2023, 12, 16, 18, 23))
    start_date_before_creation = datetime(2023, 11, 2)
    start_date_after_creation = datetime(2024, 1, 2)
    assert prepare_analysis_start_date(test_habit, start_date_after_creation) == start_date_after_creation
    assert prepare_analysis_start_date(test_habit, start_date_before_creation) == datetime(2023, 12, 16)


def test_get_period_checkoff_dict():

    assert get_period_checkoff_dict(habit_weekly) == {0: 1, 1: 1, 3: 1, 6: 2, 7: 1}
    assert (get_period_checkoff_dict(habit_weekly, start_date=datetime(2023, 11, 8))
            ==
            {0: 1, 1: 1, 3: 1, 6: 2, 7: 1})

    assert (get_period_checkoff_dict(habit_weekly, start_date=datetime(2023, 12, 7))
            ==
            {1: 1, 2: 1, 5: 1, 6: 2})


def test_calc_analysis_info():
    with (freeze_time("2024-01-30 19:00:00")):
        assert calc_analysis_info(habit_biweekly) == {"max_streak": 1,
                                                      "active_streak": 0,
                                                      "success_rate": round(2 / 5, 2)}

        assert calc_analysis_info(habit_weekly) == {"max_streak": 2,
                                                    "active_streak": 2,
                                                    "success_rate": round(5 / 9, 2)}

        assert (calc_analysis_info(habit_weekly, start_date=datetime(2023, 12, 7))
                == {"max_streak": 2,
                    "active_streak": 2,
                    "success_rate": round(4 / 8, 2)})

        assert calc_analysis_info(habit_monthly) == {"max_streak": 1,
                                                     "active_streak": 1,
                                                     "success_rate": round(2 / 3, 2)}

        assert calc_analysis_info(habit_daily) == {"max_streak": 6,
                                                   "active_streak": 3,
                                                   "success_rate": round(18 / 30, 2)}

        assert (calc_analysis_info(habit_daily, start_date=datetime(2024, 1, 16))
                == {"max_streak": 6,
                    "active_streak": 3,
                    "success_rate": round(13 / 15, 2)})

        assert calc_analysis_info(habit_daily2) == {"max_streak": 3,
                                                    "active_streak": 0,
                                                    "success_rate": round(11 / 41, 2)}


def test_get_analysis_info_table_for_habit():
    analysis_df_habit_daily2 = DataFrame([{"habit_name": "sleep_daily", "period_unit": "days", "period_length": 1,
                                           "required_checkoffs": 1, "habit_description": "",
                                           "create_datetime": datetime(year=2023, month=12, day=21, hour=15, minute=5),
                                           "max_streak": 3,
                                           "active_streak": 0,
                                           "success_rate": round(11 / 41, 2)}])
    with (freeze_time("2024-01-30 19:00:00")):
        result = get_analysis_info_table_for_habit(habit_daily2)
        assert analysis_df_habit_daily2.compare(result).empty


def test_get_analysis_info_table_for_habit_list():
    analysis_df_habit_weekly = DataFrame([{"habit_name": "climb_weekly", "period_unit": "weeks", "period_length": 1,
                                           "required_checkoffs": 1, "habit_description": "Go to climbing gym.",
                                           "create_datetime": datetime(year=2023, month=12, day=1), "max_streak": 2,
                                           "active_streak": 2, "success_rate": round(5 / 9, 2)}])
    with (freeze_time("2024-01-30 19:00:00")):
        result = get_analysis_info_table_for_habit_list(example_habit_list)
        print_df_prettily(result)
        result_habit_weekly = result[result["habit_name"] == habit_weekly.habit_name].reset_index(drop=True)
        assert analysis_df_habit_weekly.compare(result_habit_weekly).empty


def test_print_max_streak_info_for_habit_list():
    with (freeze_time("2024-01-30 19:00:00")):
        assert print_max_streak_info_for_habit_list(get_analysis_info_table_for_habit_list(example_habit_list)) == 6


def test_print_active_streak_info_for_habit_list():
    with (freeze_time("2024-01-30 19:00:00")):
        assert print_active_streak_info_for_habit_list(get_analysis_info_table_for_habit_list(example_habit_list)) == 3


def test_print_min_success_rate_info_for_habit_list():
    with (freeze_time("2024-01-30 19:00:00")):
        assert (print_min_success_rate_info_for_habit_list(get_analysis_info_table_for_habit_list(example_habit_list))
                ==
                round(11 / 41, 2))
        shorter_habit_list = [habit_biweekly, habit_monthly, habit_daily, habit_weekly]
        assert (print_min_success_rate_info_for_habit_list(get_analysis_info_table_for_habit_list(shorter_habit_list))
                ==
                round(2 / 5, 2))
