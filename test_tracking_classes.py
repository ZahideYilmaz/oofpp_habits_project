"""
This module provides some unit tests for the tracking functionality provided by the tracking_classes module.
Some of the unit tests utilize freezegun.freeze_time to mock the current system time with a provided timestamp.
"""

from datetime import datetime, timedelta
import pytest
from tracking_classes import Habit, User, DBConnector
from freezegun import freeze_time
from setup_test_tracking_data import example_habit_list, habit_monthly, setup_test_data_db

setup_test_data_db()


# pytest fixture to set up User class to contain user named "test_user" with the 5 example habits
@pytest.fixture
def user_with_five_habits():
    User.user_name = "test_user"
    # copy habit list, so we don't change the constant habit_list
    User.habit_list = example_habit_list.copy()

    # Actions to do after the test method using this fixture is executed.
    # Clean up steps.
    yield
    User.user_name = ""
    User.habit_list = []


class TestHabit:

    # pytest fixture to set up an example habit freshly for all methods calling this fixture.
    @pytest.fixture
    def habit(self):
        with freeze_time("2024-01-01 12:00:00"):
            habit = Habit("Stretch", period_unit="days", period_length=1, required_checkoffs=5)
            return habit

    def test_habit_creation(self, habit):
        assert habit.habit_name == "Stretch"
        assert habit.period_unit == "days"
        assert habit.period_length == 1
        assert habit.required_checkoffs == 5
        assert habit.create_datetime == datetime(2024, 1, 1, 12)

    def test_habit_creation_w_create_time(self):
        create_datetime = datetime(2024, 1, 1, 13)

        habit = Habit("Stretch", period_unit="days", period_length=1,
                      required_checkoffs=5, create_datetime=create_datetime)

        assert habit.habit_name == "Stretch"
        assert habit.period_unit == "days"
        assert habit.period_length == 1
        assert habit.required_checkoffs == 5
        assert habit.create_datetime == create_datetime

    def test_create_checkoff(self, habit, capsys):
        with freeze_time("2024-01-01 12:00:00"):
            habit.create_checkoff()
            function_print = capsys.readouterr().out
            assert datetime.now() in habit.checkoff_list
            assert "successful" in function_print

    def test_create_checkoff_w_timestamp(self, habit, capsys):
        checkoff = datetime(2024, 1, 1, 13, 0)
        habit.create_checkoff(checkoff)
        function_print = capsys.readouterr().out
        assert checkoff in habit.checkoff_list
        assert "successful" in function_print

    def test_create_duplicate_checkoff(self, habit, capsys):
        checkoff_time = datetime(2024, 1, 1, 13, 0)
        habit.create_checkoff(checkoff_time)
        habit.create_checkoff(checkoff_time)
        function_print = capsys.readouterr().out
        assert "already exists" in function_print
        assert len(habit.checkoff_list) == 1

    def test_create_checkoff_in_future(self, habit, capsys):
        checkoff_time = datetime.now() + timedelta(days=1)
        habit.create_checkoff(checkoff_time)
        function_print = capsys.readouterr().out
        assert "future" in function_print
        assert len(habit.checkoff_list) == 0

    def test_create_checkoff_before_habit_creation(self, habit, capsys):
        checkoff_time = habit.create_datetime - timedelta(days=1)
        habit.create_checkoff(checkoff_time)
        function_print = capsys.readouterr().out
        assert "before you created the habit" in function_print
        assert len(habit.checkoff_list) == 0

    def test_checkoff_sorting(self, habit, capsys):
        checkoff_0 = datetime(2024, 1, 1, 13)
        checkoff_1 = datetime(2024, 1, 1, 18)
        checkoff_2 = datetime(2024, 1, 1, 19)

        habit.create_checkoff(checkoff_2)
        habit.create_checkoff(checkoff_0)
        habit.create_checkoff(checkoff_1)
        capsys.readouterr()

        assert habit.checkoff_list.index(checkoff_0) == 0
        assert habit.checkoff_list.index(checkoff_1) == 1
        assert habit.checkoff_list.index(checkoff_2) == 2

    def test_delete_checkoff(self, habit, capsys):
        checkoff = datetime(2024, 1, 1, 20)
        habit.create_checkoff(checkoff)
        habit.delete_checkoff(datetime(2024, 1, 1, 20))
        function_print = capsys.readouterr().out
        assert "successful" in function_print
        assert checkoff not in habit.checkoff_list

    def test_delete_checkoff_non_existent(self, habit, capsys):
        checkoff = datetime(2024, 1, 1, 20)
        habit.delete_checkoff(checkoff)
        function_print = capsys.readouterr().out
        assert "No checkoff" in function_print

    def test_list_checkoffs(self, habit, capsys):
        checkoff_0 = datetime(2024, 1, 1, 13)
        checkoff_1 = datetime(2024, 1, 1, 18)

        habit.create_checkoff(checkoff_1)
        habit.create_checkoff(checkoff_0)
        capsys.readouterr()
        assert habit.list_checkoffs() == [checkoff_0, checkoff_1]

    def test_list_checkoffs_filtered(self, habit, capsys):
        checkoff_0 = datetime(2024, 1, 1, 13)
        checkoff_1 = datetime(2024, 1, 1, 15)
        checkoff_2 = datetime(2024, 1, 1, 17)
        checkoff_3 = datetime(2024, 1, 1, 20)
        checkoff_4 = datetime(2024, 1, 1, 22)

        habit.create_checkoff(checkoff_1)
        habit.create_checkoff(checkoff_0)
        habit.create_checkoff(checkoff_2)
        habit.create_checkoff(checkoff_3)
        habit.create_checkoff(checkoff_4)

        capsys.readouterr()
        assert habit.list_checkoffs(start=checkoff_1, end=checkoff_3) == [checkoff_1, checkoff_2, checkoff_3]

    def test_list_checkoffs_empty(self, habit):
        assert habit.list_checkoffs() == []

    def test_edit_habit_periodicity(self, habit):
        habit_name = habit.habit_name
        habit_description = habit.habit_description
        habit.edit_habit("weeks", 2, 3)
        assert habit.habit_name == habit_name
        assert habit.habit_description == habit_description
        assert habit.period_unit == "weeks"
        assert habit.period_length == 2
        assert habit.required_checkoffs == 3

    def test_edit_habit_description(self, habit):
        habit_name = habit.habit_name
        habit_period_unit = habit.period_unit
        habit_period_length = habit.period_length
        habit_required_checkoffs = habit.required_checkoffs
        new_description = "new description"

        habit.edit_habit(habit_description=new_description)
        assert habit.habit_name == habit_name
        assert habit.habit_description == new_description
        assert habit.period_unit == habit_period_unit
        assert habit.period_length == habit_period_length
        assert habit.required_checkoffs == habit_required_checkoffs


class TestUser:

    def test_get_habit_name_list_empty(self):
        assert User.get_habit_name_list() == []

    def test_get_habit_name_list(self, user_with_five_habits):
        assert User.get_habit_name_list() == ["plan_monthly", "restock_three_times_biweekly", "skin_care_daily",
                                              "sleep_daily", "climb_weekly"]

    def test_habit_exists_true(self, user_with_five_habits):
        assert User.habit_exists("plan_monthly") is True

    def test_habit_exists_false(self, user_with_five_habits):
        assert User.habit_exists("not_test_habit") is False

    def test_habit_exists_false_when_empty(self):
        assert User.habit_exists("test_habit") is False

    def test_get_habit_empty(self):
        assert User.get_habit("test_habit") is None

    def test_get_habit_false(self, user_with_five_habits):
        assert User.get_habit("not_test_habit") is None

    def test_get_habit_true(self, user_with_five_habits):
        habit = User.get_habit("restock_three_times_biweekly")
        assert habit.habit_name == "restock_three_times_biweekly"
        assert habit.period_unit == "weeks"
        assert habit.period_length == 2
        assert habit.required_checkoffs == 3
        assert habit.habit_description == "restock 3 times in 2 weeks"
        assert isinstance(habit, Habit)

    def test_add_habit(self, user_with_five_habits, capsys):
        habit = Habit(habit_name="new_test_habit", period_unit="weeks", period_length=1, required_checkoffs=3,
                      habit_description="dummy")
        User.add_habit(habit)
        function_print = capsys.readouterr().out
        assert "successful" in function_print
        assert len(User.habit_list) == 6
        assert User.habit_list[-1].habit_name == habit.habit_name
        assert User.habit_list[-1].habit_description == habit.habit_description
        assert User.habit_list[-1].period_unit == habit.period_unit
        assert User.habit_list[-1].period_length == habit.period_length
        assert User.habit_list[-1].required_checkoffs == habit.required_checkoffs

    def test_add_duplicate_habit(self, user_with_five_habits, capsys):
        habit = User.habit_list[0]
        User.add_habit(habit)
        function_print = capsys.readouterr().out
        assert "already exists" in function_print

    def test_delete_habit(self, user_with_five_habits, capsys):
        User.delete_habit("skin_care_daily")
        function_print = capsys.readouterr().out
        assert "successful" in function_print
        assert not User.habit_exists("skin_care_daily")

    def test_delete_habit_fail(self, capsys):
        User.delete_habit("not_test_habit")
        function_print = capsys.readouterr().out
        assert "No habit" in function_print

    def test_filter_habit_list(self, user_with_five_habits):
        filtered_habit_list = User.filter_habit_list(period_unit="days", period_length=1, required_checkoffs=1)
        assert len(filtered_habit_list) == 2
        assert filtered_habit_list[0].habit_name == "skin_care_daily"
        assert filtered_habit_list[1].habit_name == "sleep_daily"
        assert isinstance(filtered_habit_list[0], Habit)
        assert isinstance(filtered_habit_list[1], Habit)


class TestDBConnector:

    def test_register_user_fail(self):
        db_connector = DBConnector()
        result = db_connector.register_user("test_user", "password")
        assert result is False

    def test_register_and_verify_user(self):
        db_connector = DBConnector()
        success = db_connector.register_user("empty_test_user", "password")
        assert success is True
        assert db_connector.verify_user("empty_test_user", "password") is True
        assert User.user_name == "empty_test_user"
        db_connector.delete_user_data("empty_test_user", "password")
        User.user_name = ""

    def test_verify_false(self):
        db_connector = DBConnector()
        success = db_connector.verify_user("nonexistent_user", "password")
        assert success is False

    def test_load_data(self, user_with_five_habits):
        import sqlite3

        db_connector = DBConnector()
        db_connector.load_data()

        connection = sqlite3.connect(db_connector.dbname)
        cursor = connection.cursor()
        db_habit_count = cursor.execute('SELECT Count(*) FROM Habit WHERE user_name = ?',
                                        (User.user_name,)).fetchone()[0]
        connection.close()

        assert db_habit_count == 5

    def test_login_user(self):
        db_connector = DBConnector()
        success = db_connector.login_user("test_user", "password")
        assert vars(User.get_habit(habit_monthly.habit_name)) == vars(habit_monthly)
        assert success is True
