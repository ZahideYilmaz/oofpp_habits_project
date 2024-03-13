"""
This module sets up example tracking data for 5 habits spanning at least 4 weeks.
These examples are used in the provided unit tests.

The module can also be run independently. In that case, it executes setup_test_data_db and the user can start
exploratory testing for the habit tracking application by logging into the test_user profile (password: "password") and
unloading the example tracking data into Habit and Checkoff objects.

Constants:
- habit_monthly: Example habit for monthly periodicity.
- habit_biweekly: Example habit for biweekly periodicity.
- habit_daily: Example habit for daily periodicity.
- habit_daily2: Second example habit for daily periodicity.
- habit_weekly: Example habit for weekly periodicity.
- example_habit_list: List of all example habits.

Function:
- setup_test_data_db: Cleans and sets up test_user profile with example habits and provided dummy tracking data in the
                      database.

"""
from tracking_classes import Habit, User, DBConnector
from datetime import datetime

habit_monthly = Habit(habit_name="plan_monthly", period_unit="months", period_length=1, required_checkoffs=1,
                      create_datetime=datetime(year=2023, month=12, day=1))

habit_monthly.checkoff_list = [datetime(year=2023, month=12, day=21),
                               datetime(year=2024, month=1, day=30)]

habit_biweekly = Habit(habit_name="restock_three_times_biweekly", period_unit="weeks", period_length=2,
                       required_checkoffs=3,
                       habit_description="restock 3 times in 2 weeks",
                       create_datetime=datetime(year=2023, month=12, day=1))

habit_biweekly.checkoff_list = [datetime(year=2023, month=12, day=5, hour=12),
                                datetime(year=2023, month=12, day=7, hour=10),
                                datetime(year=2023, month=12, day=13, hour=11),
                                datetime(year=2023, month=12, day=27, hour=16, minute=15),
                                datetime(year=2023, month=12, day=30, hour=13),
                                datetime(year=2024, month=1, day=5, hour=18, minute=15),
                                datetime(year=2024, month=1, day=6),
                                datetime(year=2024, month=1, day=20),
                                datetime(year=2024, month=1, day=25)]

habit_daily = Habit(habit_name="skin_care_daily", period_unit="days", period_length=1, required_checkoffs=1,
                    create_datetime=datetime(year=2024, month=1, day=1))

habit_daily.checkoff_list = [datetime(year=2024, month=1, day=6),
                             datetime(year=2024, month=1, day=9),
                             datetime(year=2024, month=1, day=11),
                             datetime(year=2024, month=1, day=13),
                             datetime(year=2024, month=1, day=14),
                             datetime(year=2024, month=1, day=16),
                             datetime(year=2024, month=1, day=17),
                             datetime(year=2024, month=1, day=18),
                             datetime(year=2024, month=1, day=19),
                             datetime(year=2024, month=1, day=20),
                             datetime(year=2024, month=1, day=21),
                             datetime(year=2024, month=1, day=23),
                             datetime(year=2024, month=1, day=24),
                             datetime(year=2024, month=1, day=25),
                             datetime(year=2024, month=1, day=26),
                             datetime(year=2024, month=1, day=28),
                             datetime(year=2024, month=1, day=29),
                             datetime(year=2024, month=1, day=30)]

habit_daily2 = Habit(habit_name="sleep_daily", period_unit="days", period_length=1, required_checkoffs=1,
                     create_datetime=datetime(year=2023, month=12, day=21, hour=15, minute=5))

habit_daily2.checkoff_list = [datetime(year=2024, month=1, day=1),
                              datetime(year=2024, month=1, day=4),
                              datetime(year=2024, month=1, day=7),
                              datetime(year=2024, month=1, day=12),
                              datetime(year=2024, month=1, day=13),
                              datetime(year=2024, month=1, day=14),
                              datetime(year=2024, month=1, day=19),
                              datetime(year=2024, month=1, day=20),
                              datetime(year=2024, month=1, day=22),
                              datetime(year=2024, month=1, day=26),
                              datetime(year=2024, month=1, day=27)]

habit_weekly = Habit(habit_name="climb_weekly", period_unit="weeks", period_length=1, required_checkoffs=1,
                     habit_description="Go to climbing gym.", create_datetime=datetime(year=2023, month=12, day=1))

habit_weekly.checkoff_list = [datetime(year=2023, month=12, day=6),
                              datetime(year=2023, month=12, day=14),
                              datetime(year=2023, month=12, day=22),
                              datetime(year=2024, month=1, day=14),
                              datetime(year=2024, month=1, day=18),
                              datetime(year=2024, month=1, day=24)]

example_habit_list = [habit_monthly, habit_biweekly, habit_daily, habit_daily2, habit_weekly]


def setup_test_data_db():
    db_connector = DBConnector()
    db_connector.setup_database()

    # if test_user profile already exists, delete db data.
    if db_connector.verify_user("test_user", "password"):
        db_connector.delete_user_data("test_user", "password")

    # register test_user
    db_connector.register_user("test_user", "password")

    # copies habit_list for assignment, so that the original habit_list is never modified.
    User.habit_list = example_habit_list.copy()

    # load example tracking data to db.
    db_connector.load_data()
    User.user_name = ""
    User.habit_list = []


if __name__ == "__main__":
    setup_test_data_db()
