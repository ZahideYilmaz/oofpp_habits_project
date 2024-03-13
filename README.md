# Habit Tracker

## **Prerequisites**

For the best results, install python version 3.12.1.
You can check your python version by executing the following command in your command line interface:
`python --version `

## **Set up the Application**
Download the application by downloading the .zip-File.

Afterward, install the required packages with the following command:
`pip install -r requirements.txt`


To run the application, either open the project with a python-IDE and run the file main.py or enter the following command into your command line interface:

`python main.py`

## **Using the Application**
The application is easy to navigate, because it comes with a visual menu that provides you with all available options and prompts you for inputs when needed. To navigate you can use enter and arrow keys.

After choosing an action, the user is guided through the needed input for the action.

The program flow consists of the following menus:

###### 1. Start Menu
![start_menu](docs\menu_flow\0_start_menu.png)

This menu is the entry point of the application. The user can choose to register as a new user, login to an existing profile or to delete an existing user profile. The last option is to close the application.

In the following, you will see example screenshots for each available action.

<u>Register as a new user:</u>

![register_user](docs\menu_flow\register_user.png)

<u>Deletion of an existing user profile:</u>


![delete_user](docs\menu_flow\delete_user.png)

<u>Login of user: </u>

![login_user](docs\menu_flow\login_user.png)

<u>Exiting the habit tracker: </u>

![exit_from_main_menu](docs\menu_flow\exit_habit_tracker_in_main_menu.png)

###### 2. Main Menu

After a user has logged in, the main menu is entered, allowing for the user to choose between tracking new data or analysing existing one:

![main_menu](docs\menu_flow\1_main_menu.png)

###### 3. Tracking Menu

Entering the habit tracking menu, displays the following options:

![tracking_menu](docs\menu_flow\2a_habit_tracking_menu.png)

In the following, you will see example screenshots for each available action.

<u>Creating a new habit:</u>

![create_habit](docs\menu_flow\create_habit.png)

<u>Deletion of an existing habit:</u>

![delete_habit](docs\menu_flow\delete_habit.png)


<u>Deletion of checkoffs:</u>

![delete_checkoff](docs\menu_flow\delete_checkoff.png)

<u>Creation of new checkoffs:</u>

![create_checkoff](docs\menu_flow\create_checkoff.png)


###### 4. Tracking Menu


if in the main menu, (see 2. Main Menu) the action: "Analyse your habits!" was chosen, the following choces appear:

![analysis_menu_first](docs\menu_flow\2b_habit_analysis_menu.png)

###### 4.1 Single Habit Tracking Menu

For the option of analysing a specific habit, the following actions can be undertaken, as seen in the example screenshots.

<u>Printing out basic information for a single habit:</u>

![basic_info_single](docs\menu_flow\print_basic_habit_info_single.png)

<u>Printing out the analysis of a single habit:</u>

![basic_analysis_single](docs\menu_flow\print_analysis_info_single.png)

###### 4.2 Grouped Habit Tracking Menu

For the option of analysing grouped habits, the following actions can be undertaken, as seen in the example screenshots.

<u>Printing out basic information for a group of habits:</u>

![basic_info_group](docs\menu_flow\print_basic_habit_info_group.png)

<u>Printing out the analysis of a group of habits:</u>

![analysis_group](docs\menu_flow\print_analysis_info_habit_group.png)

<u>Printing out the maximal steak length for a group of habits:</u>

![analysis_group_max_streak](docs\menu_flow\print_max_max_streak.png)

<u>Printing out the lowest success rate for a group of habits:</u>

![analysis_group_lowest_success](docs\menu_flow\print_lowest_success_rates.png)

## **Testing the Application**
To test the application, run

`python -m pytest -v`

### Test Tracking Data
For testing purposes, both using the provided unit tests and testing the application via exploration, there is an example set of habits with example tracking data provided.

These examples are set up in the module setup_test_tracking_data.py, where we define a list parameter with the defined habit instances and also load this tracking data into the habit database for the test user test_user with password "password".

This means that after running setup_test_tracking_data.py you can log in using the credentials

* user_name = "test_user"
* password = "password"

and the test the different tracking and analysis functions that the application offers.

If you change the data in the user profile test_user and load this changed data into the database, you overwrite the provided testdata. Running the setup script a second time will reset the database data to the provided test tracking data again.

The same setup script is also imported by the unit test modules and the setup function is executed before the unit tests in test_tracking_classes.py.

#### Description and Visualization of the Test Tracking Data
Detailed description and visualization of the test tracking data is provided here to make the unit tests easier to understand.

###### 1. Example Habit "plan_monthly":
An example for a habit with monthly periodicity and the following Habit instance attributes:

![monthly_habit_basic_info](docs\test_objects\monthly_basic.png "monthly_habit_basic_info")

The pre-logged checkoffs are:

![checkoffs_monthly](docs\test_objects\checkoffs_monthly.png "checkoffs_monthly")

###### 2. Example Habit "restock_three_times_biweekly":
An example for a habit with biweekly periodicity and the following Habit instance attributes:

![biweekly_habit_basic_info](docs\test_objects\biweekly_basic.png "biweekly_habit_basic_info")

The pre-logged checkoffs are:

![checkoffs_biweekly](docs\test_objects\checkoffs_biweekly.png "checkoffs_weekly")

###### 3. Example Habit "skin_care_daily":
The first example for a habit with daily periodicity and the following Habit instance attributes:

![daily1_habit_basic_info](docs\test_objects\daily1_basic.png "daily1_habit_basic_info")

The pre-logged checkoffs are:

![checkoffs_daily1](docs\test_objects\checkoffs_daily1.png "checkoffs_daily")

When we filter the checkoffs using the start date '2024-01-16', we get the following checkoffs and corresponding period numbers:

![checkoffs_weekly](docs\test_objects\checkoffs_daily1_filtered.png "checkoffs_daily1")

###### 4. Example Habit "sleep_daily":
The second example for a habit with daily periodicity and the following Habit instance attributes:

![daily2_habit_basic_info](docs\test_objects\daily2_basic.png "daily2_habit_basic_info")

The pre-logged checkoffs are:

![checkoffs_daily2](docs\test_objects\checkoffs_daily2.png "checkoffs_daily2")

###### 5. Example Habit "climb_weekly":
An example for a habit with weekly periodicity and the following Habit instance attributes:

![weekly_habit_basic_info](docs\test_objects\weekly_basic.png "weekly_habit_basic_info")

The pre-logged checkoffs are:

![checkoffs_weekly](docs\test_objects\checkoffs_weekly.png "checkoffs_weekly")

When we filter the checkoffs using the start date '2023-12-07', we get the following checkoffs and corresponding period numbers:

![checkoffs_weekly](docs\test_objects\checkoffs_weekly_filtered.png "checkoffs_weekly")