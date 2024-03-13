"""
This module contains a few helper functions.

functions:
- print_df_prettily: Prints DataFrames in a readable way using PrettyTable.
- convert_to_datetime: Converts given timestamp string into a datetime.
"""
from prettytable import PrettyTable
from datetime import datetime
from pandas import DataFrame


def print_df_prettily(df: DataFrame):
    """
    Printer function to print DataFrames in a more readable way. Utilizes PrettyTable.

    Parameters:
    - df: (DataFrame): Provided DataFrame for printing.
    """
    # Define pt as empty PrettyTable instance.
    pt = PrettyTable()

    # Create column with header "nr." for row numbering in pt.
    # For each column in the DataFrame df, add corresponding column in pt
    pt.field_names = ["nr."] + df.columns.tolist()

    # iterate over all rows in the provided DataFrame
    for row in df.itertuples():
        # add the rows to pt
        pt.add_row(row)

    # Print resulting PrettyTable
    print(pt)


def convert_to_datetime(timestamp: str) -> datetime:
    """
    Converts given timestamp string into a datetime.
    Accepts timestamps in one of the formats '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H', '%Y-%m-%d'.

    Parameters:
    - timestamp: (str): Provided timestamp string.
    """
    formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H', '%Y-%m-%d']

    for format_str in formats:
        # for each format, check if the timestamp matches it
        try:
            result = datetime.strptime(timestamp, format_str)
            return result
        except ValueError:
            pass  # Try the next format if the current one fails

    # If there is no match, raise exception ValueError.
    raise ValueError(f"{timestamp} is not a valid timestamp in any of the formats {", ".join(formats)}")
