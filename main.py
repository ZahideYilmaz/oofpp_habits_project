"""
This module is the entry point for the habit tracking application. It provides the control flow of the interactive menus
that enable to user to use the tracking and analysis functionalities provided. The control flow is implemented using
while loops, questionary is used to enable the user to choose from the provided options for each menu.
"""

import os
from analysis_functions_interactive import *
from tracking_interactive import *


def clear_screen():
    """
    Helper function to clear the terminal between the execution of different menu functions for a cleaner output.
    """
    clear_command = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear_command)


DBConnector().setup_database()

# Menu choices for the start menu. Provided in dictionary form, readable by questionary.select.
# If user chooses, for example, "Delete an existing user profile!", the function delete_user_interactive is returned.
start_choices = [
    {"name": "Register as a new user!", "value": register_user_interactive},
    {"name": "Login into your existing user profile!", "value": login_user_interactive},
    {"name": "Delete an existing user profile!", "value": delete_user_interactive},
    {"name": "Exit the habit tracker :'( ", "value": "exit"}
]

# Start menu loop.
# Runs until user is logged in/registered or user chooses to exit the program.
while User.user_name == "":
    clear_screen()
    print("********* START MENU *************")

    # get users choice of start actions.
    start_option = questionary.select(message="Welcome! What do you want to do?", choices=start_choices).ask()

    if start_option is None:
        pass

    # exit the whole habit tracking program, if user chooses exit option.
    elif start_option == "exit":
        print("Farewell without login!")
        exit()

    # if user chooses one of the options corresponding to a function, execute the chosen function.
    else:
        start_option()
        # await user input
        questionary.press_any_key_to_continue().ask()

# Now a user is logged in! Move on to main menu.

# Menu choices fo the main menu. Provided in list form, readable by questionary.select
menu_choices = [
    "Track your habits!",
    "Analyse your habits!",
    "Exit the habit tracker!"]

# Main menu loop.
# Runs until user chooses to exit the habit tracker (=> breaks loop).
while True:
    clear_screen()
    print("*********MAIN MENU*************")
    print(f"username = {User.user_name}")

    # get users choice of main menu options
    menu_option = questionary.select(message="How do you want to start?", choices=menu_choices).ask()

    # if user cancels menu option selection ...
    if menu_option is None:
        pass   # ... restart tracking menu loop

    # if user chooses to exit the habit tracker, break the main menu loop.
    elif menu_option == "Exit the habit tracker!":
        break

    # if user chooses to enter the tracking menu ...
    elif menu_option == "Track your habits!":
        # Menu choices fo the tracking menu. Provided in dictionary form, readable by questionary.select
        tracking_choices = [
            {"name": "Create habits!", "value": add_habit_interactive},
            {"name": "Delete habits!", "value": delete_habit_interactive},
            {"name": "Edit a habit!", "value": edit_habit_interactive},
            {"name": "Delete checkoffs!", "value": delete_checkoff_interactive},
            {"name": "Create checkoffs!", "value": create_checkoff_interactive},
            {"name": "Exit habit tracking menu!", "value": "exit"}
        ]

        # Tracking menu loop.
        # Runs until user chooses to exit the tracking menu (=> breaks loop, back to main menu loop).
        while True:
            clear_screen()
            print("*********HABIT TRACKING MENU*************")

            tracking_option = questionary.select(message="What do you want to track?", choices=tracking_choices).ask()

            # if user cancels menu option selection
            if tracking_option is None:
                pass  # restart tracking menu loop

            elif tracking_option == "exit":
                break  # back to main menu loop

            else:
                tracking_option()
                questionary.press_any_key_to_continue().ask()

    # else, if user chooses to enter the analysis menu ...
    elif menu_option == "Analyse your habits!":
        # Sub menu choices in the analysis menu. Provided in dictionary form, readable by questionary.select
        sub_menu_choices = [
            "Analyse a specific habit!",
            "Analyse a group of habits!",
            "Exit analysis menu!"
        ]

        # Analysis menu loop.
        # Runs until user chooses to exit the analysis menu (=> breaks loop, back to main menu loop).
        while True:
            clear_screen()
            print("*********HABIT ANALYSIS MENU*************")

            sub_menu_option = questionary.select(message="What kind of analysis do you want to do?",
                                                 choices=sub_menu_choices).ask()

            # if user cancels menu option selection
            if sub_menu_option is None:
                pass  # restart analysis menu loop

            elif sub_menu_option == "Exit analysis menu!":
                break  # back to main menu loop

            # if user chooses to enter the single habit analysis submenu...
            elif sub_menu_option == "Analyse a specific habit!":
                # Menu choices for the single habit analysis submenu. Provided in dictionary form,
                # readable by questionary.select.
                analysis_choices = [
                    {"name": "Print out basic habit information for a chosen habit!",
                     "value": print_basic_habit_info_interactive},
                    {"name": "Print out checkoffs of a chosen habit!",
                     "value": print_checkoff_info_table_for_habit_interactive},
                    {"name": "Print out analysis for a chosen habit!",
                     "value": print_analysis_info_table_for_habit_interactive},
                    {"name": "Back to analysis menu!", "value": "exit"}
                ]

                # Single habit analysis menu loop.
                # Runs until user chooses to exit it (=> breaks loop, back to analysis menu loop).
                while True:
                    clear_screen()
                    print("*********SINGLE HABIT ANALYSIS MENU*************")

                    analysis_option = questionary.select(message="Which analysis do you want to do?",
                                                         choices=analysis_choices).ask()
                    if analysis_option is None:
                        pass  # restart single habit analysis menu loop

                    elif analysis_option == "exit":
                        break  # back to analysis menu

                    else:
                        analysis_option()
                        questionary.press_any_key_to_continue().ask()

            # else, if user chooses to enter the habit group analysis submenu...
            elif sub_menu_option == "Analyse a group of habits!":
                # Menu choices for the habit group analysis submenu. Provided in dictionary form,
                # readable by questionary.select.
                group_analysis_choices = [
                    {"name": "Print out basic information about a a group of habits!",
                     "value": print_basic_info_table_for_habit_list_interactive},
                    {"name": "Print out all the analysis info for a group of habits!",
                     "value": print_analysis_info_table_for_habit_list_interactive},
                    {"name": "Get the longest maximum streak length for a group of habits!",
                     "value": print_max_streak_info_for_habit_list_interactive},
                    {"name": "Get the habits in a group of habits with active streaks!",
                     "value": print_active_streak_info_for_habit_list_interactive},
                    {"name": "Get the lowest success rate for a group of habits!",
                     "value": print_min_success_rate_info_for_habit_list_interactive},
                    {"name": "Back to analysis menu!", "value": "exit"}
                ]

                # Habit group analysis menu loop.
                # Runs until user chooses to exit it (=> breaks loop, back to analysis menu loop).
                while True:
                    clear_screen()
                    print("*********HABIT GROUP ANALYSIS MENU*************")

                    group_analysis_option = questionary.select(message="Which analysis do you want to do?",
                                                               choices=group_analysis_choices).ask()

                    if group_analysis_option is None:
                        pass  # restart habit group analysis menu loop

                    elif group_analysis_option == "exit":
                        break  # back to analysis menu

                    else:
                        group_analysis_option()
                        questionary.press_any_key_to_continue().ask()

# Now the main menu loop has been broken.
# This means the user has chosen to leave the habit tracker.

# Ask user if the current tracking data should be loaded to the database.
# This would overwrite potential old data in the database for the current user.
load_data_confirmation = questionary.confirm(f"Save the session data and overwrite old data if it exists?").ask()

# If user confirms loading of tracking data ...
if load_data_confirmation:
    DBConnector().load_data()

print("Farewell!")
